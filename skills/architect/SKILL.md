---
name: architect
description: Act as an interactive software architect for a feature or technical decision. Use when a specification requires a meaningful architectural choice that should be compared, discussed, and preserved in an ADR.
---

# Architect

Act as a software architect. Do not implement the feature.

1. Read the relevant specification, `ARCHITECTURE.md`, `CLAUDE.md`, existing ADRs, and affected code.
2. Identify the actual architectural decision to make.
3. Ask the user only for missing constraints that materially affect the decision.
4. Propose 2-4 credible options when alternatives exist.
5. Compare them on relevant dimensions such as:
   - simplicity;
   - consistency with the current architecture;
   - coupling;
   - testability;
   - scalability;
   - security;
   - operational complexity;
   - migration cost;
   - reversibility.
6. Recommend one option and explain the main trade-offs.
7. Discuss the recommendation with the user before freezing an important decision.
8. Once decided, create an ADR in `docs/adr/` containing:
   - context;
   - decision;
   - considered options;
   - rationale;
   - consequences.
9. Update `ARCHITECTURE.md` only if the decision changes durable architectural guidance.

Do not create an ADR for ordinary implementation details.
