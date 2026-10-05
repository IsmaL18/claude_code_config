# Runtime: Databricks Apps, call paths, LLM, external APIs, secrets, state

## Everything is a Databricks App

Whatever the family, the deployed artifact is a **Databricks App**: a Python process
started by a declared command, running on Databricks serverless compute, reachable at
a Databricks-managed URL, protected by Databricks OAuth.

Not a Model Serving endpoint. The Agent-as-a-Service design document describes
Model Serving with provisioned GPU compute and Blue/Green updates — that is not what
is deployed. See `documented-target.md`.

Language: **Python**. Package manager: **uv**. No agent framework is imposed;
LangGraph is suggested without strong conviction.

`requirements.txt` is the documented dependency file; `pyproject.toml` and
`uv.lock` are shipped by the templates alongside it and are expected to work. The
`start-server` / `start-mcp-server` entrypoint is declared in `pyproject.toml`.

## The start command

Declared in `app.yml` and mirrored in `resources/<name>-app.yml`. The DAB resource
is authoritative. `app.yml` carries **the command only, no `env:` block** —
duplicating environment declarations has already produced silent drift where a
called app's URL kept pointing at a renamed app.

Typical commands:

```yaml
# agent app
command: ["uv", "run", "start-server"]

# MCP server
command: ["uv", "run", "start-mcp-server"]

# Chainlit chat UI
command: [chainlit, run, src/app.py, --host, 0.0.0.0, --port, 8000, --headless]
```

## Routes exposed by an agent app

The MLflow GenAI `AgentServer` (type `ResponsesAgent`) behind FastAPI/uvicorn:

| Method | Route | Purpose |
|---|---|---|
| `POST` | `/invocations` | main MLflow serving endpoint; streaming when the body sets `stream: true` |
| `POST` | `/responses` | OpenAI Responses-compatible alias, same handlers |
| `GET` | `/agent/info` | name, agent API kind, MLflow version |
| `GET` | `/health` | MLflow standard health check |
| `GET` | `/` | custom health check (`service` + `status`) |

Two handlers are registered: `invoke_handler` decorated with `@invoke()` for
request/response, and `stream_handler` decorated with `@stream()` for SSE. The
chat-proxy is disabled — only the API surface is published.

An MCP server app instead exposes `/mcp` (MCP Streamable HTTP transport) plus `/` and
`/health`.

## Two inbound call paths

### In-workspace — prefer this

A notebook, a Databricks Job, another Databricks App or a serving endpoint in the
same workspace calls the app **directly**. APIM is unnecessary: the caller already
holds a Databricks identity the app can trust.

- grant the caller `CAN_USE` on the deployed app (UI: Compute → Apps → Permissions,
  or the apps permissions API)
- for app-to-app, grant `CAN_USE` to the **caller app's service principal**, visible
  on the caller app's details as `service_principal_client_id`
- resolve the URL at runtime via the SDK (`apps.get(name=...).url`) rather than
  hardcoding it
- credentials are injected by the runtime: a PAT in notebooks, OAuth in jobs, the
  app's own SP for app-to-app — the Databricks SDK resolves them automatically

**The functional advantage over APIM: on-behalf-of.** When called from inside the
workspace with a user token, Databricks Apps forwards it as
`x-forwarded-access-token`. A helper such as `utils.get_user_workspace_client()`
re-uses it to call Databricks resources **as the end user**, so Unity Catalog
row-level security and grants apply to that user. Document this in the calling
notebook or app: end users must then hold the required grants themselves.

### Via APIM — external clients

The pipeline publishes the deployed app on the shared Edenred APIM instance and
attaches a policy performing a **Databricks OAuth client-credentials exchange**, so
the request reaching the app carries a valid Bearer token. The OAuth credentials
(Databricks SP `client_id` / `client_secret`) are APIM Named Values backed by Azure
Key Vault — not part of any bundle.

Databricks-side prerequisite you own: grant the **APIM service principal** `CAN_USE`
on the deployed app. If the agent touches other resources, grant the matching scopes
(`CAN_QUERY`, `USE_CATALOG`, …).

Four caveats that bite:

- **End-user identity is lost.** Every call arrives as the APIM service principal.
  `x-forwarded-access-token` will not carry an end-user token. To trace the original
  user, propagate a custom header (e.g. `X-End-User`) and read it explicitly.
- **Streaming.** SSE over long-lived connections requires APIM Standard or Premium;
  the Consumption tier cuts at 240 s.
- **Subscription required.** External clients must present
  `Ocp-Apim-Subscription-Key`. APIM strips it before forwarding.
- **Only `POST /responses` is exposed** as the default operation. To reach
  `/invocations` or the health/info routes from outside, additional operations must
  be requested.

## LLM access

Through a **Databricks Model Serving endpoint**, declared as a bundle resource with
`CAN_QUERY`, and called with `ChatDatabricks`:

```yaml
resources:
  - name: "serving-endpoint"
    description: "The LLM serving endpoint used by the agent"
    serving_endpoint:
      name: ${var.serving_endpoint}
      permission: "CAN_QUERY"
```

The endpoint name lives in `variables/variables-<env>.yml` so it can differ per
environment (observed: `databricks-gpt-oss-120b`).

There is **no Mosaic AI Gateway in the call path**, despite the design documents
declaring it mandatory for 100% of LLM calls. See `documented-target.md`.

The approved model list, quotas and rate limits per endpoint are not documented
anywhere in the space. Ask the platform team rather than assuming.

## Outbound calls to external APIs — APIM again, in the other direction

This is the real, implemented pattern for reaching a third-party service (the
documented example is an external search MCP server). The agent never holds the
provider key.

```
Databricks Agent
    │  Bearer <OAuth2 Entra ID token>
    ▼
Azure APIM  (gtd-apim-<region4>-apim-n.azure-api.net/<path>)
    │  1. validate-jwt              (inherited from the product policy via <base/>)
    │  2. quota monitoring          (APIM cache counter)
    │  3. rate-limit-by-key         (10 calls/second per subscription → 429)
    │  4. quota-by-key              (400 calls/day per subscription → 403)
    │  5. Teams alert at 80%        (fires once, at call 320)
    │  6. PII masking               (regex: emails → [EMAIL], FR phones → [PHONE])
    │  7. provider key injection    (replaces Authorization)
    ▼
External service
```

Agent side:

- two Entra ID App Registrations. **App A** defines the token audience
  (`api://<App-A-id>`), has no secret, and is referenced in APIM's `validate-jwt`.
  **App B** is the agent's client identity, with `client_id` and `client_secret`.
- the agent authenticates **as** App B and requests a token **for** App A:
  `ClientSecretCredential(tenant, client_id, client_secret).get_token("api://<App-A-id>/.default")`
- **fetch the token at each tool invocation** via a credential captured in a closure,
  not statically at startup. `get_token()` keeps an MSAL cache and only hits the
  network when the token is expired or near expiry, so there is no performance cost —
  and the ~1 h Entra ID TTL cannot break a long-running app.

Two operational traps:

- **WAF (F5 Volterra) must allow calls from the Databricks cluster to APIM.** Easy to
  miss, and the failure looks like a network timeout.
- **MCP rejects optional parameters passed explicitly as `null`.** Filter unset
  parameters on the agent side so only valued ones are sent.

APIM policy ordering matters: `<base />` must come **first**, before the
`set-header Authorization` that swaps the OAuth token for the provider key —
otherwise JWT validation runs against the provider key and always fails.

## Secrets

The claim "an agent carries no credentials" holds for `_ai_agent_app` bundles: they
reference only the serving endpoint. A test per bundle should fail if a
backend-reserved module reappears there.

**Chat and backend bundles do carry secrets.** Observed set for a HITL-enabled chat:

| Variable | Purpose |
|---|---|
| `POSTGRES_CONN_STRING` | Lakebase connection string |
| `LAKEBASE_ENDPOINT` | Lakebase endpoint path |
| `DATABRICKS_HUMAN_PAT` | **human PAT**, used to generate the Lakebase OAuth token |
| `APIM_TENANT_ID` | Azure tenant for the APIM SP token |
| `APIM_CLIENT_ID` / `APIM_CLIENT_SECRET` | SP credentials for APIM |
| `OAUTH_AZURE_AD_CLIENT_ID` / `_SECRET` | Azure AD login for the UI |
| `OAUTH_AZURE_AD_SCOPES` | fixed: `https://graph.microsoft.com/User.Read` |
| `CHAINLIT_AUTH_SECRET` | session signing |

Two things to know:

- **`dbutils.secrets.get()` does not work in a Databricks App.** The design document
  prescribes it; it applies to notebooks and jobs, not to Apps. Secrets reach an app
  through the DAB resource's environment declaration referencing a secret scope.
- **A human PAT stored as a secret is a real dependency**, not an oversight — it is
  how the Lakebase OAuth token is generated. It is also a single point of failure
  tied to one person's account. Flag it if you touch this area.

Never hardcode a secret, never put it in `app.yml`, and remember the DAB resource is
the single place environment is declared.

## Conversation state — Databricks serverless has no request affinity

This is a structural constraint, not an implementation detail.

```
Worker A  →  question received  →  interrupt()  →  state written to Lakebase
Worker B  →  "yes" received      →  reads state from Lakebase  →  resumes thread
```

Turn N+1 of a conversation can land on a different worker than turn N. Without
externalised state, the thread is lost between turns — with no error.

**Lakebase** (Databricks-managed PostgreSQL) is the answer used on the platform, as a
LangGraph checkpointer. It creates three tables at startup: `checkpoints` (full
thread state), `checkpoint_writes` (in-progress writes), `checkpoint_blobs`
(serialised heavy objects).

Authentication chain:

```
DATABRICKS_HUMAN_PAT (secret)
  → WorkspaceClient(token=PAT)
  → w.postgres.generate_database_credential(endpoint=LAKEBASE_ENDPOINT)
  → OAuth token (~1 h)  →  psycopg.connect(user=email, password=token)
```

The token is renewed automatically 5 minutes before expiry by rebuilding the
connection. From an MCP server the same is done with
`generate_database_credential` — short-lived Databricks-issued OAuth credentials,
never a static password. Requires a provisioned Lakebase instance, the
`psycopg[binary]` dependency, and the instance name passed via an environment
variable declared in **both** `app.yml` and the DAB resource.

Any design that assumes in-process conversation memory is wrong on this platform.

## Human-in-the-loop

The implemented pattern gates sensitive tool calls behind explicit human approval,
across three components:

| Component | Role |
|---|---|
| Chainlit frontend | authenticates via Azure AD OAuth 2.0 (authorization code), reads `userPrincipalName` from Microsoft Graph, routes `yes`/`no` to the agent |
| LangGraph agent | interrupts before a sensitive tool, persists pending state in Lakebase, resumes after approval |
| Azure APIM | rejects any sensitive tool call lacking a valid `X-HITL-User` header |

The agent calls APIM with its **own** service principal token and passes the user's
UPN as `X-HITL-User` — the header is the proof of human approval, the token is the
machine identity. The UPN is used for nothing else.

## MCP servers

Three primitives, with different governance weight:

| Primitive | Direction | Risk |
|---|---|---|
| **Tool** | agent → system, action | the only one with side effects; highest governance |
| **Resource** | system → agent, read-only URI-addressed data | exfiltration and PII leakage |
| **Prompt** | system → agent, reusable template | prompt injection |

The template layers every tool in three thin, testable pieces:

1. `schemas.py` — Pydantic request/response models; the validated input contract
2. `handlers.py` — pure business logic, no MCP or FastAPI concern; this is what you
   unit test with no server running
3. `tools.py` — thin `@mcp_server.tool()` wrapper: validate via the model, call the
   handler, return `result.model_dump()`

**The tool docstring is the contract for the LLM.** Write it deliberately.

A `capture_headers` middleware stores incoming request headers in a `contextvars`
store; that is what makes on-behalf-of authentication possible inside a tool.

Two authentication helpers:

- `get_workspace_client()` — the app's own service principal; for calls that should
  always run with the app's identity
- `get_user_authenticated_workspace_client()` — on behalf of the calling user via
  `x-forwarded-access-token`; falls back to the service principal when running
  locally. Use it when a tool must respect the caller's own Unity Catalog
  permissions rather than the app's blanket access.

Discovery: once deployed with the `mcp-` prefix, the server appears automatically in
the AI Playground and the Agent Bricks MCP catalog. No registration step. Grant the
calling identity `CAN_USE` either way.

## Local development

```bash
uv sync
uv run start-server        # or start-mcp-server; serves on http://localhost:8000
uv run pytest tests/
```

Provide a local `.env` with `DATABRICKS_HOST` and a personal access token. The same
HTTP routes are exposed locally as in production, so `/agent/info` and
`/invocations` make usable smoke tests.

**Tests must run with no network and no Databricks credentials.** The templates mock
every Databricks, MLflow and LangChain call. Keep it that way — it is what lets
`pytest` run in the pipeline.

For interactive MCP exploration: `npx @modelcontextprotocol/inspector`, transport
Streamable HTTP, URL `http://localhost:8000/mcp/`, connection via proxy.

To smoke-test a deployed instance, `databricks auth login --host <workspace-url>`
once, then a script built on `databricks_mcp.DatabricksMCPClient` plus a
`WorkspaceClient` so authentication reuses the local CLI profile. If you hit
`ConnectError: [SSL: CERTIFICATE_VERIFY_FAILED]` while a browser reaches the same URL
fine, that is a local trust-store gap (Python's bundled `certifi` not trusting the
corporate root CA), not a server bug — add the CA or install `pip-system-certs`.
