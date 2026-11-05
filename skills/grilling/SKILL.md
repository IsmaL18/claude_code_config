---
name: grilling
description: Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases.
---

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask the whole frontier in one round, then wait for the user's answers before the next round.

**Ask through the `AskUserQuestion` tool, never as chat text.** The user answers by picking an option in Claude Code's question interface, not by typing a reply to a wall of text. If the tool's schema is not loaded, load it first with `ToolSearch("select:AskUserQuestion")`.

For each question of the round:

- `question`: the full question, ending with a question mark. Put the context the user needs to decide in it, not in a separate chat message.
- `header`: a short label (max 12 characters) naming the decision.
- `options`: 2 to 4 distinct, mutually exclusive choices, each with a `label` (1-5 words) and a `description` stating what it implies and its trade-off. Put **your recommended answer first** and end its label with `(Recommended)`. Do not add an "Other" option: the interface provides one for free-text answers.
- `multiSelect`: `true` only when the choices are genuinely not exclusive.
- Use the `preview` field when options are best compared as concrete artifacts (code, config, schema, layout).

The tool takes at most 4 questions per call. If the frontier holds more, send them in successive calls of up to 4, without recomputing the tree in between (they are all on the same frontier). A question that needs an open-ended answer still goes through the tool: offer the likely answers as options and let the user use "Other".

Do not restate the questions in chat before or after the call; at most one line of framing. Treat an answer given through "Other", or any note attached to an option, as a real input that may reshape the tree.

Each round the user answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, etc.), dispatch a sub-agent to find it; don't ask the user for anything you could look up yourself. Don't block on it: a running exploration is an unsettled prerequisite, so only the questions downstream of it wait for the sub-agent to report; ask the rest of the frontier now. The _decisions_ are the user's: put each to them through `AskUserQuestion` and wait.

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Do not act on it until the user confirms you have reached a shared understanding.
