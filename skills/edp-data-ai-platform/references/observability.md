# Observability: tracing, logs, dashboards, cost

## What you get, what you owe

| Signal | Who instruments | Where it lands |
|---|---|---|
| Application logs | you, by writing to stdout/stderr | Unity Catalog table, via `telemetry_export_destinations` |
| LLM traces, tokens, cost, latency | you, via MLflow tracing in your code | MLflow experiment, persisted to Unity Catalog |
| Serverless infrastructure cost | platform | central dashboard, filtered by entity |
| Databricks DBU / FinOps dashboards | platform, provisioned by Terraform | the entity's `Monitoring` workspace folder |

The short version: **logs are nearly free, tracing is your job.**

## Logs — three lines and a dashboard

By default Databricks App logs are reachable only through the Apps UI Logs tab or the
`/logz` endpoint, both of which require `CAN_MANAGE` on the app. You do not want to
grant that to contributors in UAT and PROD.

Declaring `telemetry_export_destinations` in the app resource exports logs to a Unity
Catalog table instead. Contributors then need only `SELECT` on the monitoring schema.

```yaml
telemetry_export_destinations:
  - unity_catalog:
      logs_table: ${var.catalog_name}.monitoring.apps_monitoring_logs
      metrics_table: ${var.catalog_name}.monitoring.apps_monitoring_metrics
      traces_table: ${var.catalog_name}.monitoring.apps_monitoring_spans
```

Two things to know:

- **All three fields are required**, even though only `logs_table` is used. The
  metrics and traces tables are created and can be ignored — MLflow tracing handles
  agent traces separately.
- **All agents in an entity can share the same logs table.** Each entry carries a
  `service_name` column identifying the producing app, so per-agent filtering is
  trivial. Do not create one table per agent.

The agent DAB template already includes this block, so for a template-derived bundle
there is no extra work.

### The Apps Monitoring Logs dashboard

Deployed automatically per entity during entity onboarding. Reverse-chronological,
with four global filters:

| Filter | Use |
|---|---|
| Service Name | pick one app |
| Date Range | time window |
| Severity | INFO, ERROR, WARN |
| Log Source | lifecycle phase: BUILD, APP, SYSTEM |

Contributors already hold `SELECT` on the monitoring schema, so they can open it
directly.

**Practical consequence for code:** structured, filterable stdout is worth more than
clever log plumbing. Emit a consistent severity and enough context to be findable by
`service_name` + time range, because that is the only query surface users have.

## MLflow tracing — what you instrument

Each agent app is linked to an MLflow experiment declared as a bundle resource:

```yaml
resources:
  experiments:
    <opteam>_<name>_exp:
      name: /Workspace/${workspace.root_path}/<name>_experiment
```

and referenced from the app with `CAN_MANAGE`:

```yaml
resources:
  - name: "experiment"
    description: "MLflow experiment for agent tracing"
    experiment:
      experiment_id: ${resources.experiments.<opteam>_<name>_exp.id}
      permission: "CAN_MANAGE"
```

Environment, declared in the DAB resource (not in `app.yml`):

```yaml
env:
  - name: MLFLOW_TRACKING_URI
    value: "databricks"
  - name: MLFLOW_REGISTRY_URI
    value: "databricks-uc"
  - name: MLFLOW_EXPERIMENT_NAME
    value: /Workspace/${workspace.root_path}/<name>_experiment
```

Captured per trace:

| Dimension | Detail |
|---|---|
| Token usage | `input_tokens`, `output_tokens`, `total_tokens` per call |
| Cost (USD) | `input_cost`, `output_cost`, `total_cost` — computed automatically |
| Latency | end-to-end duration |
| Session | session id, for grouping multi-turn conversations |
| Execution flow | full span tree (handler → LangGraph → model → ChatDatabricks) |

Tag the session from `request.context.conversation_id` so multi-turn conversations
are groupable — without it, traces are a flat undifferentiated stream.

Traces persist to Unity Catalog under the entity's agent catalog `monitoring` schema,
which makes them queryable in SQL for trend dashboards and alerting on token or cost
spikes. Dashboards are available inside the experiment itself.

> Note: the cost-monitoring page claims this works "without any manual
> instrumentation — tracing is built into the serving layer". The platform team's
> position is the opposite: instrumentation is yours to write. Reconcile by reading
> the template: what is built in is the *plumbing* (experiment, tracking URI,
> autolog hook). The spans your own code produces, and the session tagging, are
> yours. Treat tracing as work to be done.

## Cost attribution — and why it stops at the entity

Serverless resources (apps, endpoints, jobs) **cannot be tagged directly**. Tags can
only reach them through budget policies. The deployment pipeline can derive a budget
policy *name* for an entity but not its *id*, which is what assignment requires — so
policies cannot be assigned at deploy time.

The workaround in place: each entity's deploying service principal is granted the
"Serverless usage policy: User" role on the entity's budget policy. When a service
principal has access to exactly one policy, that policy is applied automatically to
every serverless resource it creates.

**Consequence: the deploying service principal operates at entity level, so entity
level is the finest achievable granularity for infrastructure billing attribution.**
Combined with `apps` being `tags_compatible: false` (see `cicd.md`), this means you
cannot attribute app cost per use case out of the box.

### Infra Cost Monitoring dashboard

Sourced from `gds_prd.gds_edp360.billing_usage`, filterable by entity owner
(`edp360_owner`, derived from budget policy tags) and date range.

| Page | Content |
|---|---|
| Overview | total cost (USD), total DBUs, daily cost by product, cost by SKU, usage table |
| Apps | active app count, cost per app, split by AI chat apps and AI agent apps |
| Model Serving | active endpoint count, cost per endpoint |
| Vector Search | active endpoint count, cost per endpoint |

### Per-use-case cost, if you need it

The architecture convention is *one schema = one use case*. Two options:

**Option 1 — a budget policy per use case (recommended by the platform).** Create a
dedicated serverless usage policy per use case, with custom tags carrying both entity
and use case, and assign it to every resource of that use case. Tags propagate
automatically into `system.billing.usage` under `custom_tags`, so the existing
dashboard pattern works with one added filter. Cost: policy proliferation, and manual
assignment per resource.

**Option 2 — manual mapping.** Maintain a `resource_name → use_case` reference table
and join against the billing table on `endpoint_name` or `app_name`. Flexible and
retroactively reclassifiable, but drift-prone and not natively integrated.

**Neither is needed for token cost.** Each agent's MLflow experiment already records
`input_cost`, `output_cost` and `total_cost` per trace, persisted in Unity Catalog,
aggregatable directly in SQL.

## Platform-provided dashboards and alerts

Provisioned by Terraform into each team's `Monitoring` workspace folder, in Lakeview
format, attached to a SQL Warehouse.

Workspace paths:

```
/Workspace/gtd-gedp-<region>-data-platform-<env>/Monitoring   # companion team
/Workspace/gtd-gedp-<bubl_name>-<env>/Monitoring              # onboarded team
```

FinOps dashboards: `finops - account usage`, `finops - account usage v2`
(the preferred one for day-to-day), `finops - budget usage`,
`finops - warehouse serverless cost`, `finops - model serving cost`.
Observability: `observability - workflow analysis` (job success/failure rates,
duration trends, most frequently failing jobs).

Pre-configured alerts, scoped per team via the `gedp_owner` tag:

| Alert | Schedule | Trigger |
|---|---|---|
| Daily Cost Increase | daily 08:00 Europe/Paris | 24 h cost > 200% of the 8-day baseline scaled to 24 h |
| Monthly Budget | daily 08:00 Europe/Paris | cumulative month-to-date spend ≥ configured budget (default 1000 USD) |
| Data Quality | daily 09:00 Europe/Paris | any `dq_rules` failure today |
| Schema Validation | daily 09:00 Europe/Paris | any `schema` failure today |

The two data alerts only apply to teams using the EDP ingestion pipeline with data
quality agreements. Alerts are provisioned only if a matching notification
destination already exists in the workspace — on sandbox environments provisioning is
skipped silently.

**Direct access to Databricks system tables is not authorised.** Curated views in
the shared catalog `gds_prd.gds_slv_dbxsysteminsights` are the only path:
`billing_usage` (filtered by `custom_tags['gedp_owner']`), `billing_list_prices`
(unfiltered reference data), `access_workspaces_latest`.

## Where observability is *not* provided

- **Datadog** is the documented single pane of glass for SRE-layer metrics, and the
  architecture principles make SRE + model-layer telemetry mandatory for Lane A/B.
  Nothing in the bundle templates emits to Datadog. If someone requires it, that is
  an integration to build, not a switch to flip.
- **Per-agent operational alerting** (latency, error rate, groundedness, budget) is
  described in the design documents as templated and auto-provisioned. It is not.
  You have the trace tables and a SQL warehouse; the alerts are yours to write.
