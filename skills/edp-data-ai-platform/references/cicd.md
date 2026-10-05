# CI/CD: pipeline, branches, compliance, overrides

## One pipeline, one bundle

`gtd-gedp-<opteam>-ai-CICD` is the only pipeline available for the AI repository. It
deploys exactly one bundle per run.

Parameters:

| Parameter | Meaning |
|---|---|
| `bundleDirectory` | the bundle to deploy |
| `runApp` | run the app after deployment — check only if the bundle contains an app |
| `runJob` | run the job after deployment — check only if the bundle contains a job |

`trigger: none` — the pipeline is started manually, but the **branch it runs on
decides the environment**. There is no environment parameter.

The pipeline extends the platform template and passes `opteam`, `region4`,
`opteamHomeDir`, `productProjectName`, `bundlePath`, and optionally the evaluation
parameters. You can validate and approve your own pipeline run.

## Branch → environment

The pipeline reads the branch name. Permanent branches are `main` and `develop`;
short-lived ones are `feat/<name>`, `release(s)/<version>`, `fix/<name>` or
`hotfix/<name>`.

| Branch | Validation | DEV | UAT | PROD |
|---|---|---|---|---|
| `develop` | yes | yes | no | no |
| `feat/*` | yes | yes | no | no |
| `fix/*`, `hotfix/*` | yes | no | yes | no |
| `release(s)/*` | yes | no | yes | no |
| `main` | yes | no | **yes** | **yes** |
| pull request | yes | no | no | no |

This is **not** a linear DEV → UAT → PROD flow for every branch. The branch picks the
entry point: development branches enter at DEV, release and fix branches enter at
UAT, `main` enters at UAT and may continue to PROD.

**PROD is reachable only from `main`, and only after UAT succeeds.** A frequent
misconception is that `main` goes straight to prod — it does not, it goes through UAT
first. See uncertainty (B) in `SKILL.md`: if UAT is not provisioned for the entity,
`main` cannot reach PROD at all.

Each environment deployment requires approval from the corresponding Azure DevOps
environment (`<opteam>-dev`, `<opteam>-uat`, `<opteam>-prod`).

Branch rules enforced by policy: pull requests are required before merging into
`develop`, a release branch or `main`; at least one reviewer from the leaders team
must approve; pipeline checks must pass; direct commits to `main` and `develop` are
not permitted; force push is blocked; branch policies cannot be bypassed.

Non-standard branch names silently bypass pipeline routing conditions — the run
validates and then deploys nowhere.

## Stages

1. **Compliance checks** — resource types, naming, `run_as`, Python lint. For utils
   repositories this stage is `buildAndTest` instead.
2. **Deploy to DEV** — applies overrides, `databricks bundle validate`, then deploy.
3. **Deploy to UAT** — same.
4. **Deploy to PROD** — same.

For AI bundles, the documentation adds: if the bundle directory ends with `_agent`,
the pipeline also resolves AI agent config and runs evaluation jobs in the target
environment. **See uncertainty (A) in `SKILL.md`** — directories ending in
`_ai_agent_app` do not match that suffix.

## Stage 1 — the four blocking compliance rules

### Rule 1: allowed resource types

`jobs`, `pipelines`, `apps`, `dashboards`, `alerts`, `experiments`,
`model_serving_endpoints`, `serving_endpoints`. Anything else fails immediately, with
no deployment.

### Rule 2: resource naming

`^<opteam>_[a-z0-9_]+_<type>$`. Full abbreviation table in `bundles.md`.
Sub-resources are not checked.

### Rule 3: service principal execution

`run_as.user_name` is forbidden. Allowed: `service_principal_name` with any value
(it will be overridden), or omitting `run_as` entirely (it may be added
automatically for compatible resource types).

### Rule 4: Python code quality (ruff) — read this carefully

Two passes, and only one of them blocks.

**Pass 1 — non-blocking.** `ruff format --check` plus a full `ruff check` report.
Whitespace, import ordering, unused imports, missing trailing newline. Logged, never
fatal.

**Pass 2 — blocking.** A targeted lint selecting only real runtime errors:

| Rule group | Catches |
|---|---|
| `E9` | syntax errors and runtime exceptions |
| `F63` | invalid comparisons, assert misuse |
| `F7` | misplaced statements (e.g. `return` outside a function) |
| `F82` | undefined names (e.g. calling something never imported) |

Notebooks (`.ipynb`) and `agent.py` files are exempt from `F821` (undefined name),
since they commonly reference names injected at runtime.

> The platform team's shorthand — "the linter is not blocking" — refers to pass 1
> only. Pass 2 fails the pipeline. Do not ship an undefined name expecting it to pass.

Reproduce locally before pushing:

```bash
uv run ruff format .        # fix formatting
uv run ruff check --fix .   # fix what is auto-fixable
```

VS Code users: install the Ruff extension and add to `.vscode/settings.json`:

```json
{
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.fixAll.ruff": "explicit",
      "source.organizeImports.ruff": "explicit"
    }
  }
}
```

### SonarQube — not blocking, for now

A SonarQube project is created automatically per repository on
`https://codequality.edenred.io/`. It runs both in the compliance stage and during
pull request validation, posting annotations directly in the PR.

**Quality gate failures are informational only and do not block the pipeline** — but
the documentation states the gate *can* block when configured to. Treat "not
blocking" as a current configuration, not a guarantee.

Access requires a Jira "Onboarding & Offboarding" request through the SonarQube
service desk portal, submitted by a Central or Regional team, to be added to
`ZHQ-SonarQube-egt-data-developers` or the appropriate group.

## Stages 2–4 — the four automatic overrides

These are applied at deploy time and do **not** modify your source in Git. They mean
several things you might write are wasted effort.

### Override 1: `run_as` → managed identity

For top-level resource types flagged run_as-compatible: an existing
`service_principal_name` is overwritten with the managed identity client id; a
missing `run_as` is added. For incompatible types, no `run_as` is added. Sub-resources
are never touched. If any top-level resource type is incompatible, bundle-level
`run_as` is removed from `databricks.yml`.

### Override 2: permissions → group-based

**All** `permissions` on your resources are added or replaced with two Azure AD
groups: `<opteam>-contributors` at `CAN_MANAGE`, `<opteam>-readers` at `CAN_VIEW`.
Your original permissions are discarded entirely. Writing per-user permissions is
pointless.

Note this is distinct from resource-level grants inside the app definition
(`serving_endpoint: CAN_QUERY`, `app: CAN_USE`, `experiment: CAN_MANAGE`), which are
a different mechanism and are preserved.

### Override 3: FinOps tags → merged

Tags from the `GLOBAL_FINOPS_TAGS` environment variable are merged onto top-level
tags-compatible resources: `gedp_application`, `gedp_environment`, `gedp_location`,
`gedp_owner`, `gedp_companion`, `gedp_entitytype`. Keys present in the global set are
added or updated; other keys are left untouched. Only top-level resources.

**`apps`, `dashboards` and `alerts` are `tags_compatible: false`** — they receive no
tags at all. For apps this has a direct consequence on cost attribution; see
`observability.md`.

### Override 4: `targets` → replaced wholesale

The pipeline **replaces all `targets` in your `databricks.yml`** with the default
targets from the template's own `databricks.yml`. This happens after compliance
checks, before `validate` and `deploy`, for every stage, and whether or not your
bundle declares targets.

You therefore **cannot** configure: custom targets such as `sandbox` or `test`,
target workspace hosts, target modes, or any environment-specific target setting.

You **can** configure: resources, jobs, pipelines, apps, notebooks, variables, and
anything outside the `targets:` section not covered by another override.

A bundle-level `databricks.yml` is optional — the default is used when absent.

## Reading a failure

Compliance failure: the message names the file and the violated rule. Fix the YAML,
commit, push, re-run. Nothing was deployed.

Failure after compliance: check the Databricks workspace, review validation errors in
the pipeline log, confirm that every notebook and code file referenced by the bundle
exists, and verify cluster policies allow your compute specification.

The override summary at the end of a successful deploy looks like:

```
Successfully applied 5 run_as + 5 permission + 3 tags + 1 targets override(s) across 3 file(s)
```

## Versioning

GitVersion computes a semantic version from branch type, tags, commit count and
commit-message hints.

| Branch | Label | Shape | Example |
|---|---|---|---|
| `develop` | alpha | `M.m.p-alpha.n` | `2.5.0-alpha.14` |
| `main` | beta | `M.m.p-beta.n`, or stable when tagged | `2.6.0-beta.3` |
| `release(s)/*` | rc | `M.m.p-rc.n` | `2.6.1-rc.2` |
| `feat/*` | branch name | `M.m.p-<branch-label>.n` | `2.6.0-payment-retry.5` |
| pull request | PullRequest | `M.m.p-PullRequest.<id>.n` | `2.6.0-PullRequest.842.3` |
| `fix/*`, `hotfix/*` | hotfix | `M.m.p-hotfix.n` | `2.6.1-hotfix.1` |

Commit-message hints: `+semver: breaking|major`, `+semver: feature|minor`,
`+semver: fix|patch`, `+semver: none|skip`.

Exposed variables include `SemVer`, `FullSemVer`, `AssemblySemVer`,
`AssemblySemFileVer`, `InformationalVersion`.

## Governance data contracts

If the repository carries data contracts, a `governanceValidation` stage runs first
and DEV/UAT/PROD only run after it succeeds. It resolves contract references against
the central `gtd-gedp-governance` repository, validates them, and publishes a
`resolved-governance` artifact. Enforcement modes: `dry-run` (validate and report),
`apply` (enforce and execute), `disabled` (skip).

Contract content is domain-owned in the BU repository; rules and engine are
platform-owned and centralised.

## What you cannot do, by design

Service connections are authorised at pipeline level. Only the Terraform-created
pipelines may use them.

- you **can** create and edit pipelines, and queue builds
- you **cannot** use a service connection from a pipeline you created
- you **cannot** deploy to Azure outside the authorised pipelines
- you **cannot** delete repositories or pipelines, modify permissions or security
  policies, bypass branch policies, or force push

So: do not propose a custom pipeline as a workaround. It cannot authenticate.
