# Bundles: structure, naming, packaging

## Repository layout

Entity onboarding provisions up to three repositories, named from the product
instance name `<entityCode>-<appName>-<opteam>`:

- `<productInstanceName>-data` — data bundles
- `<productInstanceName>-ai` — AI bundles (only for EDP core platform, and only when
  the entity type is not "companion")
- `<productInstanceName>-utils` — shared libraries

Example: `gtd-gedp-aifa-ai`. One CI/CD pipeline per repository:
`gtd-gedp-aifa-ai-CICD`, living in the build folder `\gtd-gedp-aifa-ai`.

`azure-pipeline.yml` sits at the repository root and is shared by every bundle. It
extends `databricks/stages/ai-template.yml@edp-data-pipeline-templates` and takes
`bundleDirectory` as its main parameter: **one pipeline run deploys exactly one
bundle**.

## Bundle families

The directory name suffix is the contract. It selects the template, the structure and
whether APIM publication applies.

### `<code>_ai_agent_app` — one agent

```
<code>_ai_agent_app/
├── agent_server/          # the agent runtime (start_server.py, agent.py, utils.py)
├── prompts/               # the domain prompts
├── resources/
│   └── agent-app.yml      # DEPLOYMENT SOURCE OF TRUTH
├── variables/
│   ├── variables.yml
│   ├── variables-dev.yml
│   ├── variables-uat.yml
│   └── variables-prod.yml
├── apim/
│   └── apim-config.yml
├── tests/
├── app.yml                # start command ONLY
└── requirements.txt       # + requirements-dev.txt, or pyproject.toml + uv.lock
```

A bundle agent contains **the prompt, the output model and the tools. Nothing else.**
The consequence that matters: it carries no credentials and no keys, only the serving
endpoint reference. That is what makes agents safe to deploy in bulk.

### `<code>_ai_chat` — UI, backend, orchestration

Same structure **without `apim/`**. This is where the interface lives, where agents
are orchestrated, and where any database access happens. It is also where secrets
live — see `runtime.md`.

### `<code>_ai_rag` and `<code>_ai_mcp`

Same shape, same `variables/` per-environment pattern, same pipeline hooks. The MCP
family declares `resources/mcp-app.yml` instead of `resources/agent-app.yml` and
ships a `mcp_server/` package.

## Name derivation — mechanical, and it hits the 30-character wall

```
directory        spsahirg_ai_agent_app
var.app_name     aifa-spsahirg-ai-agent-app          = "aifa-" + directory in hyphens
deployed app     aifa-spsahirg-ai-agent-app-app      = ${var.app_name} + "-app"  → 30 chars
```

**30 characters is Databricks' hard limit**, verified empirically. The convention
lands exactly on it with zero margin. That is why the project code is constrained to
8 characters. Any longer code produces a name that fails at deploy time.

MCP apps derive differently — `mcp-<opteam>-<app_name>`, **no `-app` suffix** — and
the `mcp-` prefix is mandatory for Databricks to recognise the app as an MCP server.
The 30-character limit still applies, so the prefix eats 4 characters of budget.

## Logical key ≠ directory name

Never let the directory name carry the execution contract. Platform directory naming
is a convention that has already been renamed once; if URL resolution depends on it,
a rename breaks production with no test failing.

Use a stable logical key in code, and derive environment variable names from that key:

```
logical key "hiring"  →  SPSA_HIRING_AGT_APP_BASE_URL
```

## URL resolution

The deployed app URL is deterministic:

```
https://<deployed-app-name>-<workspace_app_domain>
```

So a backend or chat bundle declares, per called app, its **name** in
`variables.yml` (`<agent>_agt_app_name`) plus a single `workspace_app_domain` per
environment in `variables-<env>.yml`. This replaces hand-entering a full URL per
agent after each deployment.

**To verify (B):** `workspace_app_domain` is typically populated for dev only. Read
it off a deployed app in UAT and PROD before deploying a backend or chat bundle
there. And confirm UAT exists at all — see `SKILL.md`.

## Deployment order

Backend and chat bundles declare a `CAN_USE` grant on the apps they call. Those apps
must already exist. So:

1. verify packaging coherence (see "drift" below)
2. deploy every called agent
3. deploy the chat bundle
4. deploy the backend bundle

## The three places literal values drift

Nothing synchronises these, and drift has already happened in production:

1. **`apim/apim-config.yml`** — read by the Azure pipeline, **not** by DAB.
   `${var.*}` is not interpolated; values stay literal. An app renamed elsewhere
   leaves this file pointing at the old name.
2. **App names referenced by the backend and the chat** in their `variables.yml`.
   A renamed agent breaks URL resolution at runtime, with no error at deploy time.
3. **The `values:` list of the pipeline parameter**, if the pipeline enumerates
   deployable bundles.

A drift check belongs in the repository (the Sparky Sales precedent calls it
`scripts/check_bundles.py`). It should verify, in both directions:

- length and charset of every deployed app name
- coherence of directory ↔ `app_name` ↔ APIM `path` and `display_name`
- byte-identity of resource files within a bundle family
- existence of every app referenced by a caller
- the pipeline's bundle list against the directories on disk

This is a repository concern, not a platform-provided tool. The platform does not
check any of it.

## Bundle family identity

Bundles that share a role should have a **byte-identical** `resources/*-app.yml`.
Divergence inside a family is the signal that someone hardcoded a value that should
have been a variable. In the Sparky Sales precedent the families are: the web-tool
agents (carrying an external search key), the no-tool agents, and then chat and
backend, each alone in its family because of its `CAN_USE` fan-out.

*This grouping is a Sparky Sales convention, not a platform constraint.* The platform
constraint is only that literal bundle-specific values do not belong in the resource
file.

## Documented bundle structure vs Apps reality

The platform documents an allowed bundle structure — `resources/`, `notebooks/`,
`variables/`, `config/`, `fixtures/`, `dist/`, `databricks.yml`,
`requirements.txt`, `requirements-dev.txt` — and states:

> Files outside these directories are NOT validated, nor deployed except for synced
> directories.

Taken literally this would mean `agent_server/`, `prompts/`, `core/` and `tests/` are
never deployed. **That is not what happens for Databricks Apps**, because the app
resource declares `source_code_path: "../"`, which synchronises the whole bundle
directory.

Consequence for compliance scanning: only `resources/` and `notebooks/` are scanned
for the naming and resource-type rules. Your Python packages are deployed but not
validated by stage 1 — ruff, however, does reach them.

## `#{environment}#` is a pipeline token, not DAB

Values such as:

```yaml
catalog_name:
  default: "gedp_#{environment}#_eq_aifa_agt"
```

use `#{...}#`, the **pipeline's** substitution syntax (the same one used by the
templates' `databricks_template_config.json`). DAB uses `${var.*}` and
`${workspace.*}`. Mixing them up produces a literal `#{environment}#` in a catalog
name at runtime. Never assume DAB resolves `#{...}#`.

## APIM configuration — what you own

Only the `apim:` section of `apim/apim-config.yml`, and only before deployment. The
`deployment:` section is written by the pipeline afterwards; never edit it.

Fields you fill: `display_name`, `description`, `path`, `protocols`, `api_type`,
`product_id` (empty to skip product association).

Fields you must **not** set — the pipeline derives them from the naming convention,
only the Azure region varies:

| Resource | Non-prod | Prod |
|---|---|---|
| APIM service | `gtd-apim-<region4>-apim-n` | `gtd-apim-<region4>-apim-p` |
| Resource group | `gtd-apim-<region4>-rg-n` | `gtd-apim-<region4>-rg-p` |
| API id | the deployed app name `<opteam>-<app-name>-app` | idem |
| APIM path | `<opteam>/<app-name>` | idem |
| Backend id | `backend-<api-id>` | idem |

Resulting external URL:
`https://gtd-apim-<region4>-apim-{n|p}.azure-api.net/<opteam>/<app-name>/<route>`

## Resource naming rules

Pattern: `^<opteam>_[a-z0-9_]+_<type>$`, lowercase and underscores only.

| Resource type | Abbreviation |
|---|---|
| `jobs` | `job` |
| `pipelines` | `pipe` |
| `apps` | `app` |
| `dashboards` | `dash` |
| `alerts` | `alert` |
| `experiments` | `exp` |
| `model_serving_endpoints` / `serving_endpoints` | `mse` |

Sub-resources are exempt from the naming check.

Note the two distinct namespaces, easily confused:

- the **DAB resource key** follows this underscore pattern:
  `aifa_sparky_sales_ai_agent_app_app`
- the **deployed app name** allows hyphens only:
  `aifa-sparky-sales-ai-agent-app-app`
