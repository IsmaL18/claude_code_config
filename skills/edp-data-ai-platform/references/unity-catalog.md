# Unity Catalog: naming, assets, RBAC

## Read this first: the naming convention is not settled

Four incompatible catalog naming conventions are published in the same Confluence
space, and the ADR cited as the authority for the most detailed one **does not
exist** — the `ADR/` folder is empty, `Les referentiels` is empty, yet the agent
evaluation page references "ADR CA15" around a dozen times as its source of truth.

| Source | Catalog | Schema |
|---|---|---|
| Agentic AI / Unity Catalog page | `gedp_{env}_bu_{bu_code}_agt` | `uc_{use_case}` |
| Central team variant, same page | `gedp_{env}_eq_pdt_agt` | `uc_{use_case}` |
| "The environments" page | `gedp_dev_bu_aifa_agt`, and also `gedp_dev_bu_aifa_agent` and `gedp_dev_bu_aifa_ing` | — |
| RAG-as-a-Service LLD | `edp_<bu>_ai_knowledge` | `raw_ingest`, `core_kb`, `served_vectors` |
| Observed in a working bundle | `gedp_#{environment}#_eq_aifa_agt` | `sparky_sales` (no `uc_` prefix) |

Note the working bundle uses `eq` (not `bu`) and an unprefixed schema — it agrees
with none of the documented conventions exactly.

**This is uncertainty (C) in `SKILL.md`. Do not pick one.** Ask:

> "What is the exact catalog name for our entity in dev, uat and prod? Is the entity
> type `bu` or `eq`? Must use-case schemas be prefixed `uc_`? And is `agt` vs `agent`
> vs `ing` a live distinction or legacy?"

Until answered: **read the catalog and schema names from `variables/variables.yml` of
a bundle that currently deploys successfully.** That file is the only trustworthy
source. Never hardcode a catalog name in Python.

And remember `#{environment}#` is a pipeline substitution token, not DAB
interpolation — see `bundles.md`.

## The structure that is agreed on

Whatever the catalog spelling, the shape is consistent and worth following:

```
<agent catalog>/                         # one per entity per environment
  ├── <use-case schema>/                 # one schema = one use case, BU-owned
  │     ├── <agent_name>                 (registered model)
  │     ├── <tool_name>                  (UC function used as an agent tool)
  │     ├── <entity>_features            (Delta table with a primary key)
  │     ├── <kb>_knowledge_document_chunks        (Delta table: chunks + embeddings)
  │     ├── <kb>_knowledge_document_metadata      (Delta table: source, version, parse status)
  │     ├── <kb>_knowledge_document_chunks_index  (Vector Search index on the chunks table)
  │     ├── <kb>_knowledge_landing/               (Volume: raw source documents)
  │     ├── eval_<name>                  (Delta table: golden evaluation dataset)
  │     └── eval_runs_<agent_name>       (Delta table: one row per CI/CD gate decision)
  └── monitoring/                        # entity-level observability
        ├── apps_monitoring_logs         (telemetry_export_destinations target)
        ├── apps_monitoring_metrics
        ├── apps_monitoring_spans
        ├── inference_<agent_name>       (auto-captured)
        └── vw_inference, vw_agents      (aggregation views)
```

Two load-bearing principles:

- **One use case = one schema.** This is what makes per-use-case cost tracking and
  per-use-case RBAC possible at all.
- **Evaluation records are co-located with the use case**, not centralised. The BU
  pipeline writes to its own catalog where it already holds privileges, so no
  cross-catalog grant is needed and a failure in one BU cannot affect another. A
  central aggregation view reads across them.

## Asset naming

| Element | Convention | Example |
|---|---|---|
| Use-case schema | `uc_{use_case}` *(disputed — see above)* | `uc_fraud_detection` |
| Monitoring schema | `monitoring` | — |
| Functions (tools) | `{verb}_{entity}` | `search_knowledge_base`, `get_customer_profile` |
| Registered models | `{descriptive_name}` | `fraud_classifier`, `hr_faq_agent` |
| Model aliases | `@Champion`, `@Challenger`, `@Archived` | `fraud_classifier@Champion` |
| Feature tables | `{entity}_features` | `transaction_features` |
| Vector indexes | `{source}_index` | `hr_policy_index` |
| Evaluation tables | `eval_{name}` | `eval_golden_set` |
| Inference tables | `inference_{agent_name}` | `inference_hr_faq_agent` |
| Aggregation views | `vw_inference_{agent_name}` | — |

Hard rules:

- lowercase with underscores exclusively, no special characters
- **provide a rich `tool_description` and a `COMMENT` on every function.** Agents
  decide when to invoke a tool from that text — it is the contract, not
  documentation. An empty description makes the tool unusable in practice.
- use Google docstring syntax for Python UC functions; the toolkit parses it

## Securable object types that matter here

| Object | UC category | Note |
|---|---|---|
| Registered models | FUNCTION (subtype) | MLflow agents/models; governed via `GRANT ON FUNCTION` |
| Functions (UDFs) | FUNCTION | Python or SQL agent tools |
| Tables | TABLE | evaluation datasets, inference tables, feedback |
| Volumes | VOLUME | unstructured source data for RAG |
| Vector Search indexes | INDEX | named `catalog.schema.index_name` |
| Model serving endpoints | ENDPOINT | managed separately, linked to UC models |
| Connections | CONNECTION | external systems, MCP servers |

`system.ai` is a built-in catalog of pre-installed foundation models, available to all
account users by default unless restricted by admins.

## Tags

Governed tags drive ABAC policies. Two tag vocabularies are published and they do not
overlap cleanly — a third symptom of the missing ADR.

Agentic AI page:

| Key | Values |
|---|---|
| `domain` | `sales`, `finance`, `hr`, `engineering` |
| `sensitivity` | `public`, `internal`, `confidential`, `restricted` |
| `agent_type` | `supervisor`, `specialist`, `retriever`, `tool` |
| `maturity` | `experimental`, `beta`, `production`, `deprecated` |
| `owner_team` | e.g. `ml-platform`, `data-eng` |
| `use_case` | e.g. `customer_support` |

RAG-as-a-Service page: `data_product_type` (`knowledge_base`), `ai_domain`,
`classification` (drives PII masking logic).

The Databricks tagging strategy page is an unfinished draft with incomplete tables —
do not treat it as normative.

**Distinguish these from FinOps tags** (`gedp_application`, `gedp_environment`,
`gedp_location`, `gedp_owner`, `gedp_companion`, `gedp_entitytype`), which the
pipeline applies to compute resources and which you never write yourself. See
`cicd.md`.

## RBAC by environment

Set up at BU/BL provisioning. Note PROD: only DevOps has any access at all.

| Object | DEVOPS | ANALYSTS / ENGINEERS / SCIENTISTS (DEV & QA) | same roles in PROD |
|---|---|---|---|
| Unity Catalog | `ALL_PRIVILEGES` | `USE_CATALOG, USE_SCHEMA, SELECT` | none |
| Clusters | `CAN_MANAGE` | `CAN_ATTACH_TO` | none |
| Jobs | `CAN_MANAGE` | `CAN_VIEW` | none |
| SQL Warehouses | `CAN_MANAGE` | `CAN_USE` | none |
| Notebooks | `CAN_MANAGE` | `CAN_RUN` | none |
| ML Models / Experiments | `CAN_MANAGE` | `CAN_READ` | none |
| Dashboards / Queries | `CAN_MANAGE` | `CAN_RUN` | none |
| Alerts | `CAN_MANAGE` | `CAN_USE` | none |

Consequence: **a developer cannot inspect anything in PROD directly.** This is
precisely why `telemetry_export_destinations` matters — the exported logs table plus
`SELECT` on the monitoring schema is the only production visibility contributors get.

The environment axis here is labelled DEV / QA / PROD, while the pipeline deploys to
DEV / UAT / PROD. That mismatch is uncertainty (B) in `SKILL.md`.

## Where agent-facing grants actually live

Do not confuse UC grants with the app resource grants. Inside
`resources/<name>-app.yml` you declare what the app's service principal may reach:

```yaml
resources:
  - name: "serving-endpoint"
    serving_endpoint:
      name: ${var.serving_endpoint}
      permission: "CAN_QUERY"
  - name: "experiment"
    experiment:
      experiment_id: ${resources.experiments.<...>.id}
      permission: "CAN_MANAGE"
  - name: "agent-app"
    app:
      name: ${var.agent_app_name}
      permission: "CAN_USE"        # lets this app call another app
```

These survive deployment. Resource-level `permissions:` blocks do not — the pipeline
replaces them with group-based permissions. See `cicd.md`.

## RAG-specific constraints

If the use case involves a knowledge base, three rules are stated as
non-negotiable even when using low-code orchestration tools:

1. **No local vector stores.** Creating local files (ChromaDB and similar) is
   prohibited.
2. **Retrieval must go through a Databricks Vector Search endpoint.**
3. **Authentication must use a service principal, never a personal access token.**

Also: direct RAG against an external API is prohibited for a core knowledge model —
structured source data must be materialised in Delta tables first, for auditability.

The vector index must support metadata filtering (e.g. on an access policy column) so
agents can respect security boundaries at retrieval time.

*Caveat on this page: the RAG LLD states GitHub Actions is the mandated CI/CD
platform. That is wrong — Azure DevOps is mandated everywhere else, including in the
Agent-as-a-Service LLD and every operational page. Treat the rest of the RAG page
with matching suspicion.*
