---
name: bdv-podcast-virality-monitor
description: Surface what's trending this week in a BDV lab (Skin, Face, Hair, Body, Wellness) — used to feed the Viral Topic episode slot and to time evergreen episodes against rising waves. Use when the user says "what is trending in [lab] this week", "viral topics in [lab]", "what's hot in [lab]", or asks for a weekly trend brief. Also runs automatically every Monday 07:00 UK as a scheduled remote agent (see commands/setup-weekly-schedule.md).
allowed-tools: mcp__claude_ai_Google_Drive__read_file_content, Read, Bash, Write, WebFetch, WebSearch
---

# BDV Podcast Virality Monitor

**Live taxonomy Sheet ID:** `1xeS5sYkRsyivUfaeTwxj4dr0e1ep3_B5EuvXSv1FQSg`

You produce a weekly trend brief, scoped to one BDV lab. Output is a ranked list of topics with velocity signals, creator citations, and a "BDV angle" recommendation per topic.

## When to invoke

**On demand**, when the user says:
- "what is trending in [lab] this week"
- "viral topics in [lab]"
- "what's hot in [lab] right now"
- "weekly trend brief for [lab]"

**Automatically**, every Monday 07:00 UK, via a remote scheduled agent. See `commands/setup-weekly-schedule.md` in this plugin for the one-time setup.

## Signal sources

In rough priority order:
1. **YouTube** — search the lab's tagged Knowledge & Lifestyle creators for uploads in the last 7 days. Look at view velocity (views / age in hours) and comment volume.
2. **Google Trends** — rising queries for the lab's symptom/modality vocabulary (use the unofficial `pytrends` Python package via the helper).
3. **Reddit** — r/SkincareAddiction, r/30PlusSkinCare, r/Biohackers, r/Menopause, r/Tressless. Hot posts in the last 7 days, filtered by lab keywords.
4. **TikTok/IG** — only if `APIFY_TOKEN` is set. Hashtag velocity for `#The360DrVali` competitor space.
5. **Apple Podcasts charts** — Medicine + Health & Fitness UK top 50, week-over-week movement.

Don't fail the whole brief if one source is unavailable — note it and continue.

## Procedure

1. **Confirm the lab.** If the trigger phrase doesn't name one, ask.

2. **Pull the lab's vocabulary** from the live taxonomy Sheet. Call `mcp__claude_ai_Google_Drive__read_file_content` with the Sheet ID above, find the chosen lab's section, and collect every topic name and sub-topic keyword. Use those as your seed search vocabulary plus general lab keywords (acne, melasma, alopecia, perimenopause, libido, GLP-1, exosomes, peptides, etc.).

   If the tool reports the response was auto-saved to a file, `Read` that path. If it returns an auth error, tell the user to run `/mcp` and authenticate `claude.ai Google Drive`.

3. **Pull signals** via:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/scan_virality.py" --lab "<lab>"
   ```
   This prints JSON with `youtube_rising`, `google_trends_rising`, `reddit_hot`, `apple_chart_moves`. Skipped sources are marked with `"skipped": "<reason>"`.

4. **Rank topics**. Score each candidate topic on:
   - Velocity (views/hr or upvotes/hr, normalised to source)
   - Multi-source corroboration (a topic trending on YouTube AND Reddit AND Trends scores higher than one source)
   - BDV fit (does the taxonomy already have an entry for it? Then it's a quick-turn Viral Topic episode)

5. **For each top-5 topic, write a one-block recommendation:**
   - Topic
   - Velocity signal (with numbers)
   - Top 2 creator citations
   - Existing BDV taxonomy match (if any) — link to the topic row
   - **BDV angle** — 1–2 sentences on how Dr. Vali should enter the conversation (extend / rebut / clarify), anchored on her clinical authority and a named patient archetype from the strategy doc

## Output

Save to `./outputs/virality-<lab>-<YYYYMMDD>.md`:

```markdown
# Weekly virality brief — <Lab> Lab
_Week of <date>. Generated <date> from YouTube, Google Trends, Reddit<, TikTok>, Apple charts._

## Top 5 trending topics this week

### 1. <Topic>
**Velocity:** <metric>
**Why it's hot:** <one sentence>
**Citations:**
- <Creator> · <Episode/Post title> · <date> · <URL>
- <Creator> · <Episode/Post title> · <date> · <URL>
**BDV taxonomy match:** <topic row from sheet, or "none — net-new Viral Topic candidate">
**BDV angle:** <1–2 sentences>

…repeat for 2–5…

## Skipped sources
- <source>: <reason>

## Recommended actions this week
1. <Quick-turn Viral Topic candidate>
2. <Evergreen topic to time against this wave>
3. <Topic to NOT film this week — saturated>
```

## Rules

- **Never claim a topic is viral without a number.** "Trending" alone is not evidence. Always include a velocity metric.
- **Never quote private creator videos** (members-only, paywalled). Public uploads only.
- **Compliance:** If a trending topic involves an unregulated peptide, GLP-1 off-label use, or a substance not approved in the UK, flag it in the BDV angle as a compliance risk — do not just recommend filming.
- **Keep the brief under 1,500 words.** Nina reads this in 5 minutes Monday morning.
- **When auto-run**, send the brief by writing to `./outputs/virality-<lab>-<date>.md` and (if configured) posting to the Slack webhook in `SLACK_WEBHOOK_URL`.
