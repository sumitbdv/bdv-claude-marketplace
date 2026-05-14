---
description: One-time setup to run the BDV virality monitor as a scheduled remote agent every Monday 07:00 UK
---

# Setup weekly virality schedule

This command registers a remote scheduled agent (Claude Code routine) that runs the BDV virality monitor for all five labs every Monday at 07:00 UK and saves the briefs to `outputs/` (and posts to Slack if `SLACK_WEBHOOK_URL` is configured).

## What you need first

- Claude Code logged in with an Anthropic account that has `/schedule` enabled.
- `yt-dlp` installed (`brew install yt-dlp` on macOS).
- Optional but recommended: `pip3 install pytrends openai` for Google Trends and Whisper fallback.
- Optional: `SLACK_WEBHOOK_URL` in env if you want the briefs posted to a channel.

## What I will do for you

1. Use the `/schedule` skill to register a routine named `bdv-virality-monday`.
2. Cron: `0 7 * * 1` (Monday 07:00 UK — adjust if the runtime is UTC; the routine accepts a `timezone: Europe/London` field).
3. Prompt the routine runs each Monday: "Run the bdv-podcast-virality-monitor for each of the five labs (Skin, Face, Hair, Body, Wellness). Save each brief to outputs/. If SLACK_WEBHOOK_URL is set, post each brief's headline + top 3 topics to Slack."

After this command, the routine is live. List it with `/schedule list`. Cancel with `/schedule delete bdv-virality-monday`.

## On-demand fallback

If `/schedule` is unavailable on your plan, you can run the monitor locally on a cron via the `/loop` skill: `/loop 7d /bdv-podcast-virality-monitor all-labs`. This only fires while Claude Code is open, so the remote schedule is preferred.
