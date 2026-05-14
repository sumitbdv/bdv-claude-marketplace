---
name: bdv-podcast-topic-mapper
description: Recommend the next podcast topics to film for a given BDV lab (Skin, Face, Hair, Body, Wellness). Use when the user says "what should I film for [lab]", "give me topic options for [lab]", "what's next in [lab]", or asks for a filming shortlist drawn from the taxonomy. Reads the v3 taxonomy spreadsheet and ranks by status (not started > drafted > approved), strategic priority, and creator-evidence depth.
allowed-tools: Read, Bash, Write
---

# BDV Podcast Topic Mapper

You help Nina decide what to film next. The source of truth is the v3 taxonomy at `${CLAUDE_PLUGIN_ROOT}/data/taxonomy.xlsx`.

## When to invoke

Trigger phrases:
- "what should I film for [lab]"
- "give me topic options for [lab]"
- "what's next in [lab]"
- "topic shortlist for [lab]"
- "what's open in [lab]"

`[lab]` ∈ { Skin, Face, Hair, Body, Wellness }. If the lab is ambiguous, ask once.

## What to do

1. **Load the taxonomy** by running the helper:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/read_taxonomy.py" --lab "<lab>"
   ```
   It prints JSON with one row per topic: `sub_section`, `topic`, `mechanism`, `sub_topics`, `opening_hook`, `dr_vali_notes`, `creators` (list of 3), `transcript_link`, `status`, `approved`.

2. **Rank** the topics:
   - **Tier 1 — Ready to film:** status == "Script Drafted" AND approved is empty/false → these are the fastest path to a filmed episode. List first.
   - **Tier 2 — High strategic priority, not started:** topics where `dr_vali_notes` contains language like "case study", "bridge", "signature", "LLAS-PLAL bridge", or where `opening_hook` is exceptionally strong (specific number, contrarian claim, named patient archetype).
   - **Tier 3 — Backfill:** everything else, in taxonomy order.

3. **Output** as a markdown shortlist with this exact structure:
   ```
   # Filming shortlist — <Lab> Lab
   _Generated <date> from taxonomy v3_

   ## Tier 1 — Ready to film (script exists)
   1. **<Topic>** — <one-line why it's ready>
      - Opening hook: "<verbatim from sheet>"
      - Status: <status>
      - Creator references: <Creator 1>, <Creator 2>, <Creator 3>

   ## Tier 2 — High priority, script needed
   …

   ## Tier 3 — Backfill
   …
   ```

4. **Always offer a follow-up**: end with "Want me to pull references for any of these? Just say `pull references for <topic>`."

## Rules

- Do not invent topics that aren't in the spreadsheet. If a lab is empty, say so.
- Quote the opening hook verbatim — Nina wrote those.
- Never recommend a topic whose `approved` column is true (those are already locked / filmed).
- If `dr_vali_notes` flags a case study, surface that — it's the emotional core of the episode.

## Output artifact

Save the shortlist to `./outputs/topic-shortlist-<lab>-<YYYYMMDD>.md` so it can be shared with Dr. Vali via Slack/email. Confirm the path back to the user.
