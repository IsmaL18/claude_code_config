---
name: architecture-audit
description: Audit a repository architecture without changing code. Use when assessing boundaries, coupling, dependency direction, modularity, testability, maintainability, or risks before a refactor or takeover.
---

# Architecture audit

Inspect only. Do not modify code unless explicitly requested.

1. Read the root `CLAUDE.md`, `ARCHITECTURE.md`, relevant ADRs, and repository structure when available.
2. Identify:
   - entry points;
   - functional modules;
   - dependency directions;
   - shared state and cross-cutting dependencies;
   - infrastructure boundaries;
   - external integrations;
   - test boundaries;
   - areas requiring many unrelated files to change together.
3. Evaluate:
   - cohesion;
   - coupling;
   - separation of concerns;
   - functional modularity;
   - testability;
   - architectural drift;
   - likely regression hotspots.
4. Distinguish evidence from inference.
5. Prioritize concrete risks by impact and confidence.
6. Prefer incremental recommendations over rewrites.

Return:
- current architecture summary;
- strengths;
- findings with affected areas and impact;
- recommended improvements ordered by priority;
- suggested first safe extraction or refactor when relevant.
