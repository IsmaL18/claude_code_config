---
name: linkup-search
description: "Use this skill whenever the agent has access to Linkup search or fetch tools. It explains how to choose the right Linkup endpoint, search depth, output type, query style, and iteration strategy for web search, source-backed answers, structured extraction, page fetching, company research, news retrieval, data enrichment, or real-time information gathering."
metadata: 
  author : "Ismaël Debbagh"
  date : "2026-06-15"
  version: "1.0.0"
---

# Linkup Search Skill

This skill teaches you how to use Linkup's search and fetch tools effectively. Linkup is a semantic web search API — it interprets natural language instructions and executes retrieval steps to return accurate, real-time web data. Read this skill before making any Linkup call.

## Choose the right Linkup call

Use `/fetch` when the exact URL is known and the goal is to extract that page's content.  
Use `/search` when the URL is unknown, when several sources may contain the right data, or when Linkup must discover relevant pages.

Before calling Linkup, identify the inputs, where data likely lives, and whether the task requires sequential steps.

Use `fast` when the answer is one focused fact likely available in snippets.  
Use `standard` when the task can be solved through snippets, parallel searches, or scraping one provided URL.  
Use `deep` only for genuinely complex cases that multiple `standard` calls cannot handle: autonomous URL discovery + scraping or multi-step retrieval where intermediate results cannot be anticipated. It is significantly more expensive (10x) than `standard`.

**Default strategy: multiple focused `standard` calls** (parallel or sequential) rather than one `deep` call. Run independent angles in parallel; run dependent steps sequentially, waiting for each result before forming the next query. Both approaches can match `deep` quality at a fraction of the cost. Reserve `deep` only when this strategy is insufficient.

## Set parameters

`search_depth="fast"`: simple factual lookups, low latency, no scraping, no chaining.  
`search_depth="standard"`: default. Most searches, parallel searches, one known URL scrape.  
`search_depth="deep"`: reserved for complex cases only — autonomous URL discovery + scraping, multi-step retrieval. Much more expensive.

`output_type="searchResults"`: when you want to get the content of the retrieved pages.  
`output_type="sourcedAnswer"`: when you need a source-backed summary. Returns an AI-generated answer grounded in retrieved sources.  
`output_type="structured"`: **only use with `search_depth="deep"`** — without it, structured extraction is unreliable. You will rarely need to use this parameter. Only use when a specific output format has been given by the user.

**Good default parameters:** `output_type="sourcedAnswer"`, `search_depth="standard"`, `max_results=10`.

**Date and domain filters — use only when explicitly or implicitly required:**
- `fromDate` / `toDate`: restrict results to a time window (e.g., Anthropic product launches: `fromDate: "2025-01-01"`, `toDate: "2025-03-31"`).
- `includeDomains`: focus on specific trusted sources (e.g., `["tesla.com", "sec.gov"]` for earnings data).
- `excludeDomains`: remove noisy or irrelevant sources.

For `/fetch`, default to JavaScript rendering unless latency takes priority over extraction reliability.

## Write effective queries

**Simple lookups** (`fast` + `searchResults` or `standard` + `searchResults`): use short, specific keyword queries. Include entity, date, location, version, domain, or metric when relevant.  
_Example: "Mistral AI funding round 2024", "Bitcoin price today", "NVIDIA Q4 2024 revenue"

**All other cases:** use the structured query pattern below, written in the language most relevant to the target sources.

**Structured query pattern (3–6 sentences):**
1. **Expert persona**: "You are an expert in [domain]."
2. **Objective**: "Your objective is to find [X] about [entity Y]."
3. **Qualified entity**: provide enough context to identify the subject unambiguously — name + type or domain + location/context when relevant. **Normalize legal or administrative names to their natural form before writing the query** (e.g., `OCTO-TECHNOLOGY` → `Octo Technology`, `LVMH MOET HENNESSY` → `LVMH`). Semantic search performs significantly better with natural names than with raw legal identifiers.
4. **1-3 numbered sub-questions** with concrete examples in parentheses.
5. **Expected format and preferred source types.**

Add a temporal constraint inline when needed: year, "recent", "last 12 months", or an explicit date range.

**Rules:** one intention per call. For dependent steps, run sequential calls and wait for the first result before formulating the next.

**When using `deep`, outline the key retrieval steps** so Linkup can follow a clear path rather than discovering structure on its own.  
_Example — LinkedIn extraction:_
> "First, find LinkedIn posts about context engineering. Then, for each URL, extract the post content and comments. Return the LinkedIn profile URL of each commenter."

## Validate and iterate

After receiving results, check source relevance, freshness, authority, and consistency.

If results are weak: reformulate with a clearer entity, narrower time window, source preferences, or a more precise objective.  
If results are too broad: split the task into focused sub-queries.  
If results miss page-level details: switch from `fast` to `standard`, provide the URL, or use `/fetch`. If multi-page scraping is needed, prefer multiple `standard` calls before resorting to `deep`.  
If structured output is incomplete: retry with `search_depth="deep"` and a tighter schema-oriented query.

When using `sourcedAnswer`, verify the answer is supported by the returned sources before presenting it.

## Quick reference

| Situation                                  | Endpoint              | `search_depth` | `output_type`                      |
| ------------------------------------------ | --------------------- | -------------- | ---------------------------------- |
| Known URL extraction                       | `/fetch`              | —              | —                                  |
| One focused fact, low latency              | `/search`             | `fast`         | `searchResults`                    |
| Standard search                            | `/search`             | `standard`     | `sourcedAnswer` or `searchResults` |
| Independent parallel angles                | `/search` × N         | `standard`     | `sourcedAnswer`                    |
| Dependent sequential steps                 | `/search` → `/search` | `standard`     | `sourcedAnswer`                    |
| Autonomous discovery + scraping (complex)  | `/search`             | `deep`         | `sourcedAnswer`                    |
| Structured JSON or other format extraction | `/search`             | `deep`         | `structured`                       |