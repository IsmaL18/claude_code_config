---
name: edp-data-ai-platform
description: "Use this skill when building, packaging, deploying or debugging any AI workload on the Edenred Data & AI Platform (EDP) — Databricks Asset Bundles in a gtd-gedp-<opteam>-ai repository, Databricks Apps hosting agents, chat UIs, RAG pipelines or MCP servers, the Azure DevOps gtd-gedp-<opteam>-ai-CICD pipeline, Unity Catalog asset naming, MLflow tracing, APIM publication. It states what the platform imposes and what it silently overrides. Triggers: databricks asset bundle, DAB, bundleDirectory, agent-app.yml, apim-config.yml, variables-dev.yml, databricks apps, opteam, gedp, edp, ai-template.yml, telemetry_export_destinations, serving_endpoint."
metadata:
  author: "Ismaël Debbagh"
  date: "2026-09-22"
  sources: "Confluence space EDP (sections '1 - Data platform' and '3 - AI'), platform team interview, gtd-gedp-aifa-ai reference implementation"
---

# Edenred Data & AI Platform — integration rules

This skill is about **compliance with the platform**, not about how to design a good
agent. It answers "what does EDP impose, and what will it change behind my back?"

It deliberately does not cover agent architecture, prompt design, orchestration
patterns or testing strategy. Those are engineering choices and belong elsewhere.

## Non-negotiable behaviour of this skill

**On any contradiction or any fact not covered here: stop and ask the user.**
Do not pick a side, do not infer, do not "reasonably assume". The EDP documentation
contains four mutually incompatible Unity Catalog naming conventions, cites an ADR
that does not exist, and describes at least five capabilities as mandatory that are
not implemented. A confident guess in this environment produces code that deploys
and then fails silently.

Escalate rather than decide whenever the question touches:

- Unity Catalog catalog or schema naming
- which environments actually exist for the entity
- secrets handling
- whether a quality gate runs
- anything the reference `documented-target.md` marks as unavailable

## The mental model in eight facts

1. **One repository per entity, one bundle per deployable unit.** The AI repository is
   `gtd-gedp-<opteam>-ai`. Each top-level directory inside it is one Databricks Asset
   Bundle, deployed independently. Nothing is deployed repository-wide.

2. **The directory suffix declares the bundle family**, and the family decides the
   structure, the resource file and whether APIM applies. Four families exist,
   mirroring four platform templates:

   | Suffix | Template | Contains | `apim/` |
   |---|---|---|---|
   | `_ai_agent_app` | `edp-product-ai-agent-app` | one agent: prompt, output model, tools | yes |
   | `_ai_chat` | `edp-product-ai-chat` | UI, backend, agent orchestration, DB access | no |
   | `_ai_rag` | `edp-product-ai-rag` | ingestion, parsing, vector index | no |
   | `_ai_mcp` | `edp-product-ai-mcp` | MCP server exposing tools | no |

3. **Everything deploys as a Databricks App**, not as a Model Serving endpoint. A
   FastAPI/uv process behind a Databricks-managed URL, protected by Databricks OAuth.
   Read `references/runtime.md` before writing any entrypoint or call path.

4. **The deployed app URL is deterministic**, so never hardcode it:
   `https://<deployed-app-name>-<workspace_app_domain>`. Callers declare the *name*
   of the app they call plus one `workspace_app_domain` per environment.

5. **The branch name decides the environment.** There is no environment parameter.
   `develop` and `feat/*` reach DEV; `release(s)/*`, `fix/*`, `hotfix/*` and `main`
   reach UAT; only `main` reaches PROD, and only after UAT succeeds. A pull request
   deploys nowhere.

6. **The pipeline rewrites your bundle before deploying it.** It overrides `run_as`,
   replaces all `permissions`, merges FinOps tags, and **replaces your entire
   `targets:` block** with the platform default. Writing those is wasted effort at
   best and misleading at worst. See `references/cicd.md`.

7. **Observability is your job, with one exception.** You instrument MLflow tracing
   yourself. Logs are free: write to stdout/stderr and declare
   `telemetry_export_destinations` — the platform ships the dashboard. See
   `references/observability.md`.

8. **A bundle agent carries no credentials.** Only the serving endpoint reference.
   Chat and backend bundles *do* carry secrets, and this asymmetry is load-bearing —
   keeping agents credential-free is what makes them safely deployable in bulk.

## Hard limits — violating these fails, silently or loudly

- **30 characters** is the absolute maximum for a deployed Databricks app name.
  Verified empirically, no margin in the standard convention.
- **App names accept lowercase letters, digits and hyphens only.** An underscore is
  invalid. Published examples contain this mistake — do not copy them.
- **An MCP server app name must start with `mcp-`.** Without the prefix the app runs
  identically but is not recognised as an MCP server: invisible in AI Playground and
  in the Agent Bricks MCP catalog. No error is raised.
- **Resource keys must match `^<opteam>_[a-z0-9_]+_<type>$`** with `type` in
  `job`, `pipe`, `app`, `dash`, `alert`, `exp`, `mse`. Sub-resources are exempt.
  A violation fails the pipeline at stage 1.
- **Only these resource types are allowed**: `jobs`, `pipelines`, `apps`,
  `dashboards`, `alerts`, `experiments`, `model_serving_endpoints`,
  `serving_endpoints`. Anything else fails immediately.
- **`run_as.user_name` is forbidden.** Use `service_principal_name` with any
  placeholder value, or omit `run_as` entirely.
- **ruff `E9`, `F63`, `F7`, `F82` are blocking.** Formatting and the rest of the lint
  report are not. Do not conclude from "the linter is not blocking" that undefined
  names or syntax errors will pass — they will not.
- **All three `telemetry_export_destinations` tables are required**, even though only
  the logs table is used.

## Which file wins

Duplication between packaging files has already caused silent production drift.
The precedence is fixed:

| File | Authority |
|---|---|
| `resources/<name>-app.yml` | **Deployment source of truth.** Command, environment, secrets, `CAN_USE` grants. No literal bundle-specific value — everything through variables. |
| `variables/variables.yml` | What distinguishes this bundle from its siblings: `app_name`, experiment name, description, names of called apps. |
| `variables/variables-<env>.yml` | What varies per environment: `serving_endpoint`, `workspace_app_domain`. |
| `apim/apim-config.yml` | APIM publication. **Read by the Azure pipeline, not by DAB** — `${var.*}` is not interpolated here, values stay literal. |
| `app.yml` | **Start command only.** No `env:` block — the DAB resource is authoritative, and declaring environment twice has already produced drift. |
| `databricks.yml` | Optional. Its `targets:` are replaced at deploy time regardless. |

## Three facts to verify — do not treat as settled

Raise these with the platform team before relying on them. Each is marked in the reference files where it matters.

**A. Does the evaluation quality gate ever run?** The AI template documentation says
the evaluation stage fires when the bundle directory ends with `_agent`. Directories
ending in `_ai_agent_app` do not match that suffix. A pipeline carrying
`qualityThreshold` but none of `endpointName`, `evalTableFqn`, `experimentPath`,
`warehouseId` is further evidence the stage never executes.
*Question to ask:* "On what exact suffix does the evaluation stage trigger, and does
`<dir>_ai_agent_app` match it?"
*If it does run:* the threshold, the golden dataset table and the warehouse id all
become mandatory configuration, and documented lane thresholds start at 0.75.

**B. Is UAT provisioned for the entity?** The GitFlow model routes four branch types
to UAT, but the infrastructure state repository shows environments `dev`, `qa`,
`snbx` and only the platform itself under `uat`. The platform product parameters
accept `dev`/`qa`/`prod` — `uat` is absent. And `workspace_app_domain` is populated
for dev only.
*Question to ask:* "Is there a UAT workspace for our entity, and what is its
`workspace_app_domain`? Is `qa` the same thing as `uat`?"
*If UAT does not exist:* `main` cannot reach PROD, since PROD requires UAT success.

**C. What is the catalog actually called?** Four incompatible conventions are
published. See `references/unity-catalog.md` for all four and the question to ask.

## Reading order

Read `SKILL.md` alone for orientation. Then load only what the task needs.

| Task | Read |
|---|---|
| creating or renaming a bundle, packaging, naming | `references/bundles.md` |
| pipeline behaviour, branches, compliance failures, lint | `references/cicd.md` |
| entrypoints, call paths, LLM access, external APIs, secrets, state | `references/runtime.md` |
| tracing, logs, dashboards, cost attribution | `references/observability.md` |
| catalogs, schemas, tables, vector indexes, RBAC | `references/unity-catalog.md` |
| someone cites a capability you cannot find | `references/documented-target.md` |

## Source hierarchy, when you must weigh evidence

Higher wins. But per the rule at the top of this file, a conflict between the top
three levels is an escalation, not a decision.

1. Observed behaviour of the running pipeline and of a deployed bundle
2. The `edp-product-ai-*` bundle templates
3. A working bundle already deployed in the entity repository
4. Confluence operational pages (bundle CI/CD, GitFlow, logs, cost, MCP, APIM)
5. Confluence Low-Level Design documents — **frequently stale**; the Agent-as-a-Service
   and Chat-UI-as-a-Service LLDs describe a runtime that was never built
