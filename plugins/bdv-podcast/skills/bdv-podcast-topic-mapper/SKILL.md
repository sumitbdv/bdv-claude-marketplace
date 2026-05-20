---
name: bdv-podcast-topic-mapper
description: Recommend the next podcast topics to film for a given BDV lab (Skin, Face, Hair, Body, Wellness). Use when the user says "what should I film for [lab]", "give me topic options for [lab]", "what's next in [lab]", "topic shortlist for [lab]", or "what's open in [lab]". Reads the live v3 taxonomy Google Sheet via the Drive MCP and ranks topics by status, strategic priority, and creator-evidence depth.
allowed-tools: mcp__claude_ai_Google_Drive__read_file_content, Read, Write
---

# BDV Podcast Topic Mapper

You help Nina decide what to film next. The source of truth is the live Google Sheet "BDV_Podcast_Taxonomy_v3".

**Sheet ID:** `1xeS5sYkRsyivUfaeTwxj4dr0e1ep3_B5EuvXSv1FQSg`

## When to invoke

Trigger phrases:
- "what should I film for [lab]"
- "give me topic options for [lab]"
- "what's next in [lab]"
- "topic shortlist for [lab]"
- "what's open in [lab]"

`[lab]` is one of: Skin, Face, Hair, Body, Wellness. If ambiguous, ask once.

## What to do

### Step 1 — Fetch the live Sheet

Call `mcp__claude_ai_Google_Drive__read_file_content` with the Sheet ID above. The response will be a markdown rendering of the entire spreadsheet (≈85 KB; Claude Code will auto-save it to a file and report the path if it's large — `Read` that path).

If the tool reports an auth error, tell the user to run `/mcp` and authenticate `claude.ai Google Drive`.

### Step 2 — Find the lab's section

The markdown export uses sub-section banner rows like:
```
| LLAS \| SKIN LAB \| TREATMENT MODALITIES | ... |
| PLAL \| WELLNESS LAB \| SYMPTOMS | ... |
```

The chosen lab's data is split across multiple sub-sections (TREATMENT MODALITIES, SYMPTOMS, VIRAL TOPICS, FOUNDATION, SPECIFIC INGREDIENTS, etc.). Collect rows from all sub-sections belonging to that lab — they are all candidate topics.

### Step 3 — Extract each topic row

Every data row contains these fields (column position may vary slightly between sub-sections and labs because the Sheet allows authors to add columns — **match by content, not by hardcoded position**):

- **Sub-Section** — the leftmost short label like MODALITY / SYMPTOM / VIRAL / blank (Foundation rows). Skip banner rows.
- **Topic / Modality** — the topic name. Skip rows with empty topic.
- **Clinical Mechanism** — long descriptive text about biology/chemistry.
- **Sub-Topics** — comma-separated sub-points.
- **Opening Hook** — a punchy quoted-style sentence Nina wrote (often the most emotional cell).
- **Dr Vali Notes** — editorial direction, case-study hints, strategic notes.
- **Creator references** — 1–3 episode titles from competitor creators.
- **Transcript Link** — pointer to a docx/master spreadsheet ref.
- **Status** — e.g., "Not Started", "Research", "Script Drafted", "SCRIPTED", "Approved".
- **Approved** — Y/N flag (last column).

Detection hints if positions look misaligned:
- The cell containing `MODALITY` / `SYMPTOM` / `VIRAL` is the Sub-Section.
- The cell immediately to its right is Topic.
- The Opening Hook is usually a short emotional sentence with a contrarian or specific claim.
- Status is usually a one or two-word value from a small enum.
- If a sub-section table has different number of cells than the lab's other sub-sections, that's normal — Google Sheets merges cells and the markdown export reflects that. Realign per row by finding Sub-Section keyword and walking right.

### Step 4 — Rank topics

- **Tier 1 — Ready to film:** `status` is "Script Drafted" / "Scripted" / "Approved" AND `approved` column is not Y. These are the fastest path to a filmed episode.
- **Tier 2 — High strategic priority, not started:** `dr_vali_notes` contains language like "case study", "bridge", "LLAS-PLAL bridge", "signature", "foundational", "BDV differentiator", or `opening_hook` has a specific number / contrarian claim / named patient archetype.
- **Tier 3 — Backfill:** everything else, in taxonomy order.

Never recommend a topic whose `approved` column is Y — those are locked / already filmed.

### Step 5 — Output

Write a markdown shortlist to `./outputs/topic-shortlist-<lab>-<YYYYMMDD>.md` with this structure:

```
# Filming shortlist — <Lab> Lab
_Generated <date> from live taxonomy Sheet_

## Tier 1 — Ready to film (script exists)
1. **<Topic>** — <one-line why it's ready>
   - Opening hook: "<verbatim>"
   - Status: <status>
   - Creator references: <Creator 1>, <Creator 2>, <Creator 3>

## Tier 2 — High priority, script needed
…

## Tier 3 — Backfill
…

---
Want me to pull references for any of these? Just say `pull references for <topic>`.
```

Confirm the saved file path back to the user. Quote opening hooks verbatim — Nina wrote those.

## Rules

- **Never invent topics that aren't in the Sheet.** If a lab is empty or the Sheet structure has changed in a way you can't parse, say so plainly and offer to show the user the raw lab section.
- **Always fetch live.** Don't cache. The Sheet changes weekly; stale data is worse than no data.
- If `dr_vali_notes` flags a case study (e.g., "Melasma bride case study"), surface it — it's the emotional core of the episode.
