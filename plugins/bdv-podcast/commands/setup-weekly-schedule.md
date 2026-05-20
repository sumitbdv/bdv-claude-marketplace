---
description: One-time setup to register the two Monday-morning BDV scheduled agents (lab virality + longevity/biohacking)
---

# Setup weekly schedules

This command registers two remote scheduled agents that fire every Monday at **06:00 UTC** (≈07:00 BST London / 06:00 GMT in winter — cron is UTC and has no DST awareness):

1. **`bdv-virality-monday`** — runs the `bdv-podcast-virality-monitor` skill across all five BDV labs (Skin, Face, Hair, Body, Wellness), pulling live from the taxonomy Google Sheet. Emails the briefs to `sumit@bydrvali.com` via the Gmail MCP.
2. **`bdv-longevity-monday`** — broader trend scan in longevity, biohacking, NAD/peptides, supplements, hormesis, gut health, sleep optimization, cold/heat therapy. No Sheet dependency. Emails a digest to `sumit@bydrvali.com` via the Gmail MCP.

## What you need first

- A claude.ai account with `/schedule` enabled.
- These connectors connected on claude.ai (Settings → Connectors): **Google Drive** (for the Sheet), **Gmail** (for delivery). Both should already be connected.

That's it. No local installs needed — the routines run remotely in Anthropic's cloud.

## What this command does

When invoked, this command calls `/schedule` to create both routines with:
- `cron_expression: "0 6 * * 1"`
- `model: claude-sonnet-4-6`
- `mcp_connections`: Google Drive + Gmail attached to routine #1; Gmail attached to routine #2

After creation, list with `/schedule list`. Delete via https://claude.ai/code/routines.

## To skip auto-create

If you'd rather schedule manually, just say `/schedule` in Claude Code and follow the prompts using the cron + prompts above.
