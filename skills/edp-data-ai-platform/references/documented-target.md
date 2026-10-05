# The documented target — designed, not available

Everything in this file is **published platform documentation describing capabilities
that are not implemented** in the pipeline or the bundle templates as of
September 2026.

Two uses, and only two:

1. **Do not build against any of it.** If a task assumes one of these capabilities,
   the task is based on a stale document. Say so and ask.
2. **Cite it accurately in architecture discussions.** These documents carry weight
   in review boards. Knowing the gap between the written target and the running
   platform is the difference between arguing from evidence and arguing from
   impression.

Every entry states what is documented, then what is actually true.

---

## Mosaic AI Gateway — mandatory for all LLM calls

**Documented.** "100% of all LLM API calls (including embedding and generation) must
be routed through the dedicated Mosaic AI Gateway provisioned for the agent instance.
Direct access to LLM endpoints is strictly prohibited and should be enforced via
network policies." With mandatory guardrails: PII detection and masking on prompt and
response, prompt-injection risk scoring with blocking, toxicity scoring, request rate
limits (e.g. 50 RPM staging / 500 RPM production), token consumption caps, and a
central audit log at `lakehouse.observability.gateway_audit_log` carrying
`original_prompt`, `final_prompt`, `pii_detected_flag`, `token_count`, `latency_ms`.

**Actually.** Agents call a Databricks Model Serving endpoint directly via
`ChatDatabricks`, with a `CAN_QUERY` grant. No gateway in the path, no PII masking on
LLM traffic, no guardrails, no gateway audit log.

The one place PII masking genuinely happens is the **outbound APIM policy** for
external API calls, by regex on emails and French phone numbers — a different
mechanism, a different traffic direction, and far narrower. See `runtime.md`.

---

## The four-gateway architecture

**Documented.** Nine traffic patterns across three axes (north-south inbound,
east-west internal, outbound) served by four logical gateway roles: an N-S Gateway
(Azure APIM), a Tool Gateway governing agent-to-tool MCP traffic, an Agent Gateway
governing agent-to-agent A2A traffic, and an LLM Gateway governing agent-to-model
traffic. With a 7-level action classification (AC-01 → AC-07), a 5-level kill switch
(tool, agent, action class, lane, global) propagating in under a second, HITL
orchestration for AC-04+, OBO identity propagation, mTLS between services,
a permission matrix of role × action class × lane, delegation depth limits, tool
definition hashing against rug-pull, and a vendor-neutral
`POST /v1/chat/completions` API with a fallback chain.

**Actually.** Azure APIM exists and does real work — inbound publication with OAuth
exchange, outbound JWT validation, rate limiting, quota, key injection. The other
three gateway roles do not exist as products. There is no action classification, no
kill switch, no permission matrix, no mTLS between agents, no vendor-neutral LLM API.

HITL exists, but as an application-level pattern implemented per use case: a Chainlit
frontend, a LangGraph interrupt, Lakebase persistence, and an APIM check on an
`X-HITL-User` header. See `runtime.md`. It is something you build, not something you
enable.

---

## Service Catalog — mandatory self-service provisioning

**Documented.** A central control plane pulls the Agent Blueprint from Git, captures
user preferences (framework choice, LLM choice, state persistence), applies
customisation, then autonomously provisions the agent: creates a dedicated Git
repository, injects the customised blueprint, and sets up a tailored CI/CD pipeline.
"All new agent creations must flow through the Service Catalog; direct manual
creation of agent infrastructure or CI/CD pipelines is strictly prohibited to
maintain governance."

**Actually.** You create a bundle directory by hand in the entity's existing AI
repository, and deploy it with the single shared pipeline. There is no service
catalog, no per-agent repository, no per-agent pipeline.

The `databricks bundle init` templates (`edp-product-ai-agent-app`, `-ai-chat`,
`-ai-rag`, `-ai-mcp`) are the real, usable part of this design. The orchestration
layer around them is not built.

---

## Model Serving with provisioned GPU compute

**Documented.** "The agent is deployed exclusively on Databricks Model Serving",
configured with provisioned GPU compute rather than scale-to-zero, to guarantee low
P95 latency, with mandatory Blue/Green updates for zero downtime and safe rollback.
Models registered in MLflow as `lakehouse.models.<agent_name>_agent_model` with
mandatory metadata (git commit hash, pipeline id, owner, staging evaluation result).

**Actually.** Agents deploy as **Databricks Apps** — FastAPI/uv on serverless
compute, behind a Databricks-managed URL. No GPU provisioning, no Blue/Green, no
model registration step in the deployment path.

The authoritative document for what is actually deployed is
`edp-product-ai-agent-app — Product Usage & APIM Registration`, not the
Agent-as-a-Service LLD.

---

## Prompt versioning in the Unity Catalog prompt registry

**Documented.** A complete four-stage design decoupling prompt lifecycle from code
lifecycle: register prompts with `mlflow.genai.register_prompt` into a per-environment
catalog, promote by setting a `dev_candidate` tag which triggers CI via a Databricks
webhook plus an Azure Logic App, move aliases `@dev` → `@staging` → `@prod` from the
pipeline, and have the endpoint reload the prompt automatically by tracking the alias
(`entity_version: "aliases/${var.env_tag}"`). With SQL-grant-based permissions —
data scientists write to the dev registry and read staging and prod — and manual
approval gates between stages.

**Actually.** The MLflow server provided by the platform is too old to support prompt
versioning. An upgrade has not been requested yet.

**What to do instead:** keep prompts as files in the bundle's `prompts/` directory,
versioned in Git, deployed with the bundle. This matches architecture principle AP-08
(knowledge assets stored in Git alongside agent code) and keeps a clean migration
path: when MLflow is upgraded, the file content becomes the registered template.

Note the consequence that is easy to miss: **prompt changes require a bundle
redeploy.** There is no hot-swap. The documented design exists precisely to avoid
that, which is why people expect it to work.

---

## Automated agent evaluation as a CI/CD quality gate

**Documented, extensively.** Mosaic AI Agent Evaluation via `mlflow.genai.evaluate()`
as a blocking pipeline stage. Five evaluation dimensions (answer quality, retrieval
quality, safety, tool use accuracy, performance) with named MLflow 3 scorers.
Lane-calibrated thresholds:

| Metric | Lane A blocks below | Lane B blocks below |
|---|---|---|
| RetrievalGroundedness | 0.80 | 0.90 |
| Faithfulness (RAGAS) | 0.78 | 0.88 |
| RelevanceToQuery | 0.78 | 0.88 |
| Correctness | 0.75 | 0.85 |
| Safety — PII / Harm | any detection blocks | any detection blocks |
| Tool Selection Accuracy | 0.80 | 0.90 |
| Latency p95 | > 10 s warns | > 6 s blocks |

Plus golden dataset governance: four generation strategies, a dataset quality gate
(minimum 50 rows Lane A / 150 Lane B, ≥95% human-reviewed, ≥10% adversarial rows
Lane A / 20% Lane B, zero unmasked PII), a lifecycle with `candidate` →
`under_review` → `golden` → `deprecated` status tags, explicit version pinning in an
evaluation manifest, and a rule that the judge model must differ from the evaluated
model.

**Actually.** A simplified version is implemented, gated on parameters in
`azure-pipeline.yml`:

```yaml
endpointName: 'onai_<agent_name>_query'
evalTableFqn: '<catalog>.<schema>.eval_<agent_name>'
experimentPath: '/gtd-gedp-onai-d/<agent_name>/evaluation'
qualityThreshold: '0.8'
warehouseId: '<warehouse-id>'
```

It runs **two** scorers, not the documented matrix: `Correctness` and
`RelevanceToQuery`, each scoring 0 or 1 per row. The mean of both must be ≥ a
**single global** `qualityThreshold` — per-metric thresholds and a configurable
metric list are named as future work. The golden dataset is a table with just
`request` and `target` columns, and 10–20 representative examples are described as
sufficient. The stage runs after Deploy DEV; a failure blocks promotion past DEV.

**And it may not run at all for your bundles** — see uncertainty (A) in `SKILL.md`.
The trigger is documented as a bundle directory ending in `_agent`, which
`_ai_agent_app` does not match. A pipeline carrying `qualityThreshold` but none of
the other four parameters is further evidence the stage is inert. Verify before
claiming either way.

---

## The Lanes operating model — Lane 0 / A / B

**Documented, and detailed.** Three lanes balancing innovation speed against
governance:

- **Lane 0 (Sandbox)** — anyone builds, builders self-test, no approval, immediate
  self-service. Network-isolated from Edenred infrastructure, prototype-and-discard,
  nothing formally released.
- **Lane A (Pilot/Internal)** — serves Edenred employees, governed data, actions only
  with human confirmation, 1–2 weeks to start, 95% SLA and business-hours support.
  Agents may stay in Lane A permanently if only internal.
- **Lane B (Production/External)** — serves merchants, cardholders, partners,
  4–8 weeks, 99.9% SLA, 24/7, full governance.

With a "start-low" principle, Gate 1 (ARB majority) for Lane A, Gate 2 (ARB unanimous
plus explicit Security approval) for Lane B, and an EU AI Act compliance track
(Annex III questionnaire before Gate 1, 5-year log retention, mandatory HITL for
AC-03+ on high-risk systems, Article 50 disclosure headers for external-facing
agents).

Lane × environment: Lane 0 lives only in SANDBOX; Lane A and Lane B share DEV, UAT
and PROD, differentiated by governance rather than infrastructure.

**The part that would change engineering, and is not enforced:**

| Data source | SANDBOX | DEV | UAT | PROD |
|---|---|---|---|---|
| Public web | yes | **no** | **no** | **no** |
| Document upload | yes | no | no | no |
| Edenred data via MCP | no access | **synthetic mocks only** | anonymised sample | real, governed |

With the corresponding tool-owner obligation: every internal tool owner must ship a
**mock MCP endpoint returning synthetically generated data for DEV**, an anonymised
pre-loaded dataset for UAT, and the production endpoint for PROD. No cross-environment
index access. From DEV onward, all external calls must go through tools registered in
a platform tool registry.

**Actually.** None of this environment cloisonnement is implemented. There is no
platform tool registry, no mock MCP variant obligation, and agents reach external
APIs through APIM identically in every environment. Agents in DEV can and do call the
real internet.

So: **an agent may call the web from DEV today.** But if anyone asks you to design
around "DEV has no internet access", they are reading this document, and the right
answer is that it describes an unimplemented target.

---

## Additional undelivered items, briefly

- **Datadog as the SRE pane of glass.** Named in the application architecture matrix
  for every component and required by principle AP-11 for Lane A/B. Nothing in the
  bundle templates emits to Datadog.
- **Templated per-agent dashboards and alerts** (`monitoring/dashboard.json`,
  `monitoring/alerts.yml`) auto-provisioned per agent instance with P95 latency,
  cost, groundedness and error-rate alerts. Not provisioned. You get the entity-level
  Apps Monitoring Logs dashboard and the FinOps set; per-agent alerting is yours.
- **AI Marketplace** with quality scores surfaced per agent listing, asset tiers,
  and principle AP-09 requiring teams to check it before building anything. Not
  available.
- **CrewAI as a mandated second framework** alongside LangGraph. The platform imposes
  no framework and suggests LangGraph without strong conviction.
- **Streamlit as the chat UI framework.** The Chat-UI-as-a-Service LLD specifies
  Streamlit with `session_state`; deployed chat apps use **Chainlit**.
- **The "CA15" ADR**, cited repeatedly as the authority for Unity Catalog structure
  and the MLflow-vs-Delta responsibility split. Not published. See
  `unity-catalog.md`.
- **A 2-3 pipeline model with a separate PR-validation pipeline, staging deployment
  on PR, and RAG evaluation results posted as PR comments.** One pipeline exists;
  routing is by branch; a PR deploys nowhere.

---

## The architecture principles — these are real, and citable

Unlike the above, the principle catalog (AP-01 → AP-11) is a live governance document
and the right thing to cite. The four that constrain engineering work:

| Principle | What it demands of you |
|---|---|
| **AP-02 Automated Policy Enforcement** | governance rules must be machine-enforceable, not prose; policy changes follow the code review process |
| **AP-08 Managed Knowledge Lifecycle** | prompts and knowledge assets are architectural artifacts: stored in Git alongside agent code, versioned, tested, formally promoted; ingestion declarative and reproducible; changes trigger regression tests against reference queries |
| **AP-11 Operational Observability** | every component and agent emits structured telemetry; end-to-end traceability mandatory for Lane A/B; owning teams accountable for maintaining coverage |
| **AP-01 Cost Transparency** | every workload attributable to an accountable business unit |

AP-08 is the one that justifies keeping prompts in Git rather than waiting for the
prompt registry — useful to have at hand when someone objects.
