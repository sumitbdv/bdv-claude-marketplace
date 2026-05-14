# BDV Claude Marketplace

Private Claude Code marketplace for the By Dr. Vali team. Contains the `bdv-podcast` plugin: five skills that take a podcast episode from "what should we film" → "filmed-ready script" without spending hours hunting transcripts.

## What's inside

| Skill | Trigger phrases | What it does |
|---|---|---|
| **bdv-podcast-topic-mapper** | "what should I film for [lab]", "give me topic options for [lab]" | Reads `taxonomy.xlsx` and returns a ranked filming shortlist |
| **bdv-podcast-reference-puller** | "pull references for [topic]", "what did the competitors say about [topic]" | Pulls verbatim quotes from YouTube (yt-dlp), Apple/Spotify (Whisper), IG/TikTok (Apify) — scoped to taxonomy creators |
| **bdv-podcast-virality-monitor** | "what is trending in [lab] this week" + weekly Monday 7am auto-run | Surfaces top trending topics per lab with velocity signals and BDV angles |
| **bdv-podcast-scriptwriter** | "write the script for [topic]" | Drafts an 8–12 min, 7-section, Dr-Vali-voiced script |
| **bdv-podcast-reviewer** | "review the script for [topic]", "compliance check this" | Audits a draft against structure, length, voice, MHRA compliance |

## Install (for Nina or any teammate)

### One-time setup

1. **Install Claude Code** (https://claude.com/claude-code). Sign in.

2. **Install yt-dlp** (used by the reference puller + virality monitor):
   ```bash
   brew install yt-dlp        # macOS
   # or: pipx install yt-dlp
   ```

3. **Optional Python packages** (only needed if you want Whisper / Google Trends):
   ```bash
   pip3 install openpyxl pytrends openai
   ```
   `openpyxl` is required for the topic mapper. The others are optional.

4. **Environment variables** (optional):
   - `OPENAI_API_KEY` — enables Whisper transcription of Apple/Spotify podcasts.
   - `APIFY_TOKEN` — enables IG/TikTok scraping.
   - `SLACK_WEBHOOK_URL` — virality monitor posts the Monday brief to Slack.

5. **Add this marketplace and install the plugin.** In Claude Code:
   ```
   /plugin marketplace add <git-url-of-this-repo>
   /plugin install bdv-podcast@bdv-claude-marketplace
   ```

   (If running locally without a remote, point at the local path: `/plugin marketplace add /Users/sumit/Documents/Projects/bdv-claude-marketplace`.)

6. **Verify** — restart Claude Code, then in any session type:
   ```
   what should I film for skin
   ```
   You should see Claude invoke `bdv-podcast-topic-mapper`.

### Weekly auto-run (Monday 7am UK)

In Claude Code, once per machine:
```
/bdv-podcast:setup-weekly-schedule
```
This registers a remote scheduled agent that runs the virality monitor for all five labs every Monday morning and saves briefs to `outputs/`. List with `/schedule list`, cancel with `/schedule delete bdv-virality-monday`.

If `/schedule` isn't on your plan, use `/loop 7d /bdv-podcast-virality-monitor` instead — fires only while Claude Code is running.

## Daily workflow

Nina's typical Monday:

```
what is trending in skin this week
   → outputs/virality-skin-YYYYMMDD.md

what should I film for skin
   → outputs/topic-shortlist-skin-YYYYMMDD.md

pull references for "Pigmentation and Hyperpigmentation"
   → outputs/references-pigmentation-YYYYMMDD.md
   → outputs/transcripts/*.txt (verbatim)

write the script for Pigmentation and Hyperpigmentation
   → outputs/script-pigmentation-YYYYMMDD.md

review the script for Pigmentation and Hyperpigmentation
   → outputs/script-pigmentation-YYYYMMDD.reviewed.md
   → outputs/audit-pigmentation-YYYYMMDD.md
```

The reviewer's verdict is the gate to filming.

## Updating the taxonomy

The taxonomy is bundled at `plugins/bdv-podcast/data/taxonomy.xlsx`. When Nina updates the v3 sheet, drop the new version in that path and commit. Teammates `git pull` to get the update — no plugin reinstall needed.

Strategy doc lives at `plugins/bdv-podcast/data/strategy.docx` for the same reason.

## Layout

```
bdv-claude-marketplace/
├── .claude-plugin/marketplace.json
├── README.md
└── plugins/
    └── bdv-podcast/
        ├── .claude-plugin/plugin.json
        ├── skills/
        │   ├── bdv-podcast-topic-mapper/SKILL.md
        │   ├── bdv-podcast-reference-puller/SKILL.md
        │   ├── bdv-podcast-virality-monitor/SKILL.md
        │   ├── bdv-podcast-scriptwriter/SKILL.md
        │   └── bdv-podcast-reviewer/SKILL.md
        ├── commands/
        │   └── setup-weekly-schedule.md
        ├── scripts/
        │   ├── read_taxonomy.py
        │   ├── fetch_transcript.py
        │   └── scan_virality.py
        └── data/
            ├── taxonomy.xlsx
            └── strategy.docx
```

## Owner

Sumit · sumit@bydrvali.com
