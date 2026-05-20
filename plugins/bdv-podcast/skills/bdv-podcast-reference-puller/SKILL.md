---
name: bdv-podcast-reference-puller
description: Pull verbatim quotes, transcripts and citations from competitor creators on a given topic, scoped to the BDV taxonomy's Knowledge and Lifestyle tier creators. Use when the user says "pull references for [topic]", "what did the competitors say about [topic]", "what did [creator] say about [topic]", or asks for citation packs / transcript snippets before scripting. Pulls from YouTube (yt-dlp captions), Apple/Spotify (Whisper), and Instagram/TikTok (Apify).
allowed-tools: mcp__claude_ai_Google_Drive__read_file_content, Read, Bash, Write, WebFetch, WebSearch
---

# BDV Podcast Reference Puller

**Live taxonomy Sheet ID:** `1xeS5sYkRsyivUfaeTwxj4dr0e1ep3_B5EuvXSv1FQSg`

You assemble a citation pack for a podcast topic so Nina can write the script without spending 2 hours hunting transcripts. Output is a structured markdown brief with verbatim quotes, source links, and creator metadata.

## When to invoke

Trigger phrases:
- "pull references for [topic]"
- "what did the competitors say about [topic]"
- "what did [creator] say about [topic]"
- "citations for [topic]"
- "reference pack for [topic]"

## Sources, in priority order

1. **Taxonomy creators first.** Call `mcp__claude_ai_Google_Drive__read_file_content` with the Sheet ID above. Read the auto-saved file if reported. Find the topic's lab section and the topic row; collect the Creator 1/2/3 Episode references attached to it. Start with their channels.
   - Knowledge tier: Dr. Idriss, Dr. Anthony Youn, Beauty Brains, Inside Aesthetics, Grant Stevens, William Gaunitz, Gary Brecka, Darshan Shah, Mark Hyman, Gabrielle Lyon, etc.
   - Lifestyle tier: Susan Yara, Arielle Lorre, Jason Martin, Saluja/Novo, Dr. Louise Newson, Mel Robbins, Iman Gadzhi, TSK, Kayla Barnes, Tamsen Fadal, etc.
   - If the Drive MCP returns an auth error, tell the user to run `/mcp` and authenticate `claude.ai Google Drive`.
2. **Then YouTube broadly** via `yt-dlp` for captions. Search query: `<topic> <creator>`.
3. **Then podcasts** (Apple/Spotify) via Whisper transcription if no YouTube version exists.
4. **Then short-form** (IG/TikTok) via Apify if user explicitly asks for "viral takes".

## Procedure

1. **Disambiguate the lab.** Map the topic to a lab using the taxonomy. Skin/Face/Hair/Body/Wellness. If ambiguous, ask once.

2. **Pull the creator list** from the live Sheet (see step 1 source). For each topic row in the lab's section, the Creator 1 / Creator 2 / Creator 3 Episode cells contain the relevant references.

3. **For each tagged creator, fetch transcripts.** Use the helper:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/fetch_transcript.py" --query "<topic> <creator>" --source youtube
   ```
   The helper requires `yt-dlp` on PATH. If missing, tell the user: `brew install yt-dlp` (macOS) or `pipx install yt-dlp`.

4. **For Apple/Spotify**, the helper falls back to Whisper. Needs `OPENAI_API_KEY` in env. If missing, skip and note in the output.

5. **For IG/TikTok**, the helper uses Apify. Needs `APIFY_TOKEN`. If missing, skip and note.

6. **Extract**, per source, the 3–5 most quotable lines on the topic. Prefer:
   - Direct claims (with named numbers)
   - Mechanism explanations Nina can paraphrase
   - Contrarian takes Dr. Vali can rebut or amplify
   Avoid filler and ad-reads.

## Output

Write a citation pack to `./outputs/references-<topic-slug>-<YYYYMMDD>.md`:

```markdown
# Reference pack — <Topic>
_Generated <date>. Topic mapped to <Lab> Lab._

## Taxonomy context
- Clinical mechanism: <from sheet>
- BDV opening hook: "<verbatim>"
- Dr Vali notes: <from sheet>

## Knowledge tier — verbatim quotes

### <Creator> — <Episode title> (<platform>, <date>)
URL: <link>
Transcript saved to: ./outputs/transcripts/<slug>.txt

> "<verbatim quote 1>" — <timestamp>
> "<verbatim quote 2>" — <timestamp>

**Take for BDV:** <one sentence on how Dr. Vali should position relative to this — agree, extend, or rebut>

…repeat for each creator…

## Lifestyle tier — verbatim quotes
…

## What's missing
List any tagged creator whose transcript could not be fetched, with reason (no captions, paywalled, etc.) and the suggested fallback.

## Suggested angle for the BDV episode
2–3 sentences. What Dr. Vali can say that none of these creators are saying, anchored on her clinical authority + Selfridges patient base.
```

## Rules

- **Quote verbatim.** Never paraphrase a competitor and present it as their words. Mis-quoting a competitor is a legal risk.
- **Always include the URL and timestamp** so a reviewer can verify.
- **Never include peptide compound brand names in captions** — BDV-specific rule from the strategy doc. If a competitor's transcript names a peptide, surface it in the body, not in any caption-format excerpt.
- **Cap output at ~3,000 words** per pack. Nina reads these end-to-end.
- If the user only names a creator (not a topic), ask once for the topic.

## Output artifact

Confirm the path back to the user. Offer: "Want me to feed this into the scriptwriter? Just say `write the script for <topic>`."
