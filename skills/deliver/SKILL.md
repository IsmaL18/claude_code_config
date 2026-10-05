---
name: deliver
description: Prepare and perform a clean code delivery with the user. Use when implementation and reviews are complete and the change must be checked, summarized, committed, pushed, or prepared as a pull request.
---

# Deliver

Act as the delivery owner.

1. Confirm the intended delivery scope and inspect the final Git diff.
2. Run or apply `pre-delivery-check` before delivery.
3. Stop if blocking verification fails unless the user explicitly accepts the risk.
4. Summarize:
   - what changed;
   - why;
   - important implementation decisions;
   - tests and checks performed;
   - known limitations or follow-ups.
5. Identify the repository's commit and PR conventions.
6. Propose a concise commit message and PR title/body when relevant.
7. Ask the user before consequential Git or remote actions when their intent is not already explicit.
8. If requested, create clean commits containing only intended changes.
9. If requested and permitted, push and create or prepare the pull request.
10. Report exactly what was delivered and what remains local or pending.

Do not hide failed checks, unresolved review findings, or unrelated changes.
Do not include files outside the intended delivery scope without user approval.

## Next step

End with the **Next step** block defined in `AGENTS.md` (role, skill, session, ready-to-send prompt).

Routing:

* delivered and nothing remains → say the workflow is complete; record the memory hand-off.
* a follow-up was identified (next slice, deferred finding, new feature) → the matching skill (`tdd-implementation`, `start-feature`, `bug-investigation`, `refactor-module`), new session; the prompt gives the delivered PR/commit, the follow-up and its source.
* PR awaiting review comments → `tdd-implementation` or `bug-investigation`, new session, with the PR link and the comments to address.
