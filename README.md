# BDV Claude Marketplace

Claude Code marketplace for the By Dr. Vali team. Contains the `bdv-podcast` plugin: five skills that take a podcast episode from "what should we film" → "filmed-ready script", plus two scheduled agents that email a Monday trend briefing.

The plugin reads everything live from Google Workspace — the taxonomy spreadsheet and the brand style guide are Google files the team already edits. **There is no data bundled in this repo**, so the code can be public while the proprietary content stays gated behind Google Drive permissions.

## What's inside

| Skill | Trigger phrases | What it does |
|---|---|---|
| **bdv-podcast-topic-mapper** | "what should I film for [lab]", "topic options for [lab]" | Reads the live taxonomy Sheet and returns a ranked filming shortlist |
| **bdv-podcast-reference-puller** | "pull references for [topic]", "what did [creator] say about [topic]" | Pulls verbatim quotes from YouTube (yt-dlp), Apple/Spotify (Whisper), IG/TikTok (Apify) — scoped to the creators tagged in the Sheet |
| **bdv-podcast-virality-monitor** | "what is trending in [lab] this week" | Surfaces top trending topics per lab with velocity signals and BDV angles |
| **bdv-podcast-scriptwriter** | "write the script for [topic]" | Drafts an 8–12 min, 7-section, Dr-Vali-voiced script using the live Style Guide |
| **bdv-podcast-reviewer** | "review the script for [topic]", "compliance check this" | Audits a draft against structure, length, voice (per Style Guide), and MHRA compliance |

### Scheduled agents (run remotely in Anthropic's cloud)

Two routines fire every Monday at **06:00 UTC** (≈07:00 BST London) and email `sumit@bydrvali.com`:

- **`bdv-virality-monday`** — runs the virality monitor across all five labs.
- **`bdv-longevity-monday`** — broader longevity / biohacking trend scan (NAD+, peptides, GLP-1, hormones, sleep, hormesis, etc.).

Set them up once with `/bdv-podcast:setup-weekly-schedule`, or manage at https://claude.ai/code/routines.

## The data lives in Google Drive

| Source | What it is | Who edits it |
|---|---|---|
| [BDV_Podcast_Taxonomy_v3](https://docs.google.com/spreadsheets/d/1xeS5sYkRsyivUfaeTwxj4dr0e1ep3_B5EuvXSv1FQSg/edit) (Sheet) | Per-lab topic taxonomy: mechanisms, hooks, Dr Vali notes, creator refs, status | Nina |
| By Dr. Vali (BDV) Style Guide (Doc, id `1mvk6zxCFWZTaX2OhYTLQOpjRL7Zn1xb50vGo07RMR4Y`) | Authoritative brand voice: signature phrases, patterns, trademark rules, vocab banks | Dr Vali |

Skills fetch these live on every run via the **claude.ai Google Drive connector**. Edit the file → the next skill run sees the change. No plugin update, no version bump, no stale data. You can add columns, rows, or whole new tabs and the skills adapt (they match by header label, not fixed positions).

## Install (for Nina or any teammate)

A non-technical teammate needs three things: Claude Code, the Google Drive connector, and the plugin. No git, Xcode, or Homebrew.

1. **Install Claude Code** (https://claude.com/claude-code) and sign in.

2. **Connect Google Drive.** In Claude Code, run `/mcp`, select **claude.ai Google Drive**, and authenticate in the browser with your `@bydrvali.com` account. (You must already have view access to the taxonomy Sheet — ask Sumit or Nina.)

3. **Add the marketplace and install the plugin:**
   ```
   /plugin marketplace add https://github.com/sumitbdv/bdv-claude-marketplace.git
   /plugin install bdv-podcast@bdv-claude-marketplace
   /reload-plugins
   ```

4. **Verify** — in any session type `what should I film for skin`. You should get a ranked shortlist pulled live from the Sheet.

> Full step-by-step onboarding for non-technical teammates lives in `team-docs/NINA_ONBOARDING.md` (kept in Sumit's local project, not this repo).

### Optional extras (only for the reference puller)

The reference puller can transcribe sources locally. These are optional — without them it falls back to what's available:
- `yt-dlp` on PATH — YouTube captions (`brew install yt-dlp`, or download the binary).
- `OPENAI_API_KEY` — Whisper transcription of Apple/Spotify podcasts.
- `APIFY_TOKEN` — IG/TikTok scraping.

## Keeping things updated

- **When the skills change** (Sumit pushes an update): run `/plugin marketplace update bdv-claude-marketplace` then `/reload-plugins`.
- **When the taxonomy or style guide changes**: just edit the Google file. Nothing else to do.

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
        └── scripts/
            ├── fetch_transcript.py
            └── scan_virality.py
```

Data files (taxonomy, style guide) are intentionally **not** in this repo — they live in Google Drive (see above).

## Owner

Sumit · sumit@bydrvali.com
