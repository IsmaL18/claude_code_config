# Setup and preflight

Run once per project at the start of CREATE, REDESIGN, multi-screen IMPLEMENT or large EXTEND, and whenever STATE has no Tooling section. Skip it for MODIFY and small EXTEND unless a capture is needed and fails.

## 1. Check what is available

- Run `node <skill>/scripts/preflight.mjs` from the app root: Node version, Playwright, launchable browsers, `@axe-core/playwright`. It installs nothing.
- Read your own tool list for skills (`frontend-design`, a web interface guidelines skill, UI/UX Pro Max) and MCP servers (Playwright MCP, 21st.dev Magic, a design-tool connector).
- Note the environment: local agent with a terminal, CI or headless, or a chat interface where nothing can be installed.

## 2. Recommend only what this mode needs

| Tool | Status | Recommend when | Without it |
|---|---|---|---|
| Playwright + browsers of the matrix | required for web projects | always | visual core checks `not verified`, so `incomplete` |
| `@axe-core/playwright` | recommended | CREATE, REDESIGN, EXTEND, IMPLEMENT, unless the project has equivalent a11y tooling | project tooling or manual pass only; C3 weaker |
| Playwright MCP | recommended | task walkthroughs and interactive state checks | scripts plus manual steps; C2 slower |
| `frontend-design` | optional | CREATE, REDESIGN (candidate refinement, Golden polish) | `craft.md` alone |
| Web interface guidelines (Vercel) | optional | Golden set and final release, as a complement | `quality-gates.md` C3 alone |
| UI/UX Pro Max | optional, rarely | a narrow category checklist is clearly useful | nothing lost by default |
| 21st.dev Magic | optional, deferred | only when a behavior-heavy pattern is missing (React stacks) | existing headless libraries |
| Design-tool connector (Figma MCP...) | optional | IMPLEMENT from a design file | measurement from captures, marked approximate |

Propose 21st.dev only at the moment it would be used, never in the initial preflight.

## 3. Ask once, then respect the answer

Present a short table in one message: what is available, what is missing, what each missing item would bring for this work, and the exact commands. Then ask which ones to install.

Rules:
- Never install, configure an MCP server, add a skill or change global configuration without explicit approval of that item.
- Prefer project scope for dependencies, skills and MCP servers the team should share (versioned). Use user scope for anything holding a secret: an API key never goes into a committed file.
- Third-party skills and MCP servers run code on the user's machine; name the source repository so the user can judge it.
- If the user declines, continue with the fallbacks above and set the evidence statuses accordingly. Do not ask again for the same item in this project unless the user raises it.
- Where nothing can be installed (chat interface, locked CI), say so once, give the commands for the user's own machine, and continue in degraded mode.
- Record the result in STATE §Tooling: available, installed with approval, declined, unavailable.

## 4. Install commands (Claude Code)

Commands for third-party tools change; if one fails, check the tool's repository README before retrying.

```bash
# Playwright, browsers and accessibility scan (in the project)
npm i -D @playwright/test @axe-core/playwright
npx playwright install chromium            # plus firefox webkit if in the matrix; Linux/CI: --with-deps

# Playwright MCP (shared with the team through .mcp.json)
claude mcp add playwright --scope project -- npx @playwright/mcp@latest

# 21st.dev Magic (user scope: holds an API key from 21st.dev)
claude mcp add magic --scope user --env API_KEY="<key>" -- npx -y @21st-dev/magic@latest
```

```text
# frontend-design (Anthropic), inside a Claude Code session
/plugin marketplace add anthropics/claude-code
/plugin install frontend-design@claude-code-plugins
# fallback: copy skills/frontend-design from github.com/anthropics/skills into .claude/skills/

# Web interface guidelines (Vercel): skill web-design-guidelines in vercel-labs/agent-skills
npx skills add vercel-labs/agent-skills
# fallback: copy that skill folder into .claude/skills/

# UI/UX Pro Max (community: nextlevelbuilder/ui-ux-pro-max-skill; needs Python 3)
/plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill
/plugin install ui-ux-pro-max@ui-ux-pro-max-skill
```

Other agents: install the npm packages the same way, and add skills and MCP servers through that agent's own mechanism.

After installing UI/UX Pro Max, do not use its persistent design-system option: it writes its own `MASTER.md` and would compete with this skill's source of truth.

After any installation, rerun `preflight.mjs` and check that new skills and MCP tools appear in the tool list (a new session may be needed).
