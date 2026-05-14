#!/usr/bin/env python3
"""Fetch a transcript for a search query.

Strategy:
  1. youtube  — yt-dlp search + auto-captions (vtt -> plain text)
  2. podcast  — yt-dlp on the episode URL (audio) + Whisper transcription
  3. ig_tiktok — Apify actor (requires APIFY_TOKEN)

Usage:
    python3 fetch_transcript.py --query "acne hormonal Dr Idriss" --source youtube
    python3 fetch_transcript.py --url <youtube-url> --source youtube
    python3 fetch_transcript.py --url <spotify-or-apple-url> --source podcast
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def slug(s: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s.lower()).strip("-")
    return s[:60] or "transcript"


def have(cmd: str) -> bool:
    return shutil.which(cmd) is not None


def vtt_to_text(vtt: str) -> str:
    lines = []
    for line in vtt.splitlines():
        if "-->" in line or line.startswith("WEBVTT") or line.strip().isdigit() or not line.strip():
            continue
        line = re.sub(r"<[^>]+>", "", line)
        if lines and lines[-1].strip() == line.strip():
            continue
        lines.append(line)
    return "\n".join(lines)


def fetch_youtube(query: str | None, url: str | None, out_dir: Path) -> dict:
    if not have("yt-dlp"):
        return {"ok": False, "error": "yt-dlp not installed. Run: brew install yt-dlp (macOS) or pipx install yt-dlp"}
    target = url or f"ytsearch1:{query}"
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        cmd = [
            "yt-dlp",
            "--skip-download",
            "--write-auto-subs",
            "--write-subs",
            "--sub-langs", "en.*",
            "--sub-format", "vtt",
            "--print", "%(id)s\t%(title)s\t%(uploader)s\t%(webpage_url)s\t%(upload_date)s",
            "-o", str(td / "%(id)s.%(ext)s"),
            target,
        ]
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        except subprocess.TimeoutExpired:
            return {"ok": False, "error": "yt-dlp timed out"}
        if r.returncode != 0:
            return {"ok": False, "error": r.stderr.strip()[:500]}
        meta_line = (r.stdout.strip().splitlines() or [""])[0]
        parts = meta_line.split("\t")
        if len(parts) < 4:
            return {"ok": False, "error": "no result"}
        vid, title, uploader, webpage_url = parts[0], parts[1], parts[2], parts[3]
        upload_date = parts[4] if len(parts) > 4 else ""
        vtts = sorted(td.glob(f"{vid}*.vtt"))
        if not vtts:
            return {"ok": False, "error": "no captions available for this video", "url": webpage_url, "title": title}
        text = vtt_to_text(vtts[0].read_text(errors="ignore"))
        out_path = out_dir / f"{slug(title)}.txt"
        out_path.write_text(text)
        return {
            "ok": True,
            "source": "youtube",
            "title": title,
            "uploader": uploader,
            "url": webpage_url,
            "upload_date": upload_date,
            "transcript_path": str(out_path),
            "transcript_chars": len(text),
        }


def fetch_podcast_via_whisper(url: str, out_dir: Path) -> dict:
    if not have("yt-dlp"):
        return {"ok": False, "error": "yt-dlp required for podcast audio download"}
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return {"ok": False, "error": "OPENAI_API_KEY missing — needed for Whisper transcription"}
    try:
        import openai  # noqa: F401
    except Exception:
        return {"ok": False, "error": "openai package missing. Run: pip3 install openai"}
    from openai import OpenAI

    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        cmd = ["yt-dlp", "-x", "--audio-format", "mp3",
               "--print", "%(id)s\t%(title)s\t%(uploader)s\t%(webpage_url)s",
               "-o", str(td / "%(id)s.%(ext)s"), url]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if r.returncode != 0:
            return {"ok": False, "error": r.stderr.strip()[:500]}
        meta = (r.stdout.strip().splitlines() or [""])[0].split("\t")
        if len(meta) < 4:
            return {"ok": False, "error": "no audio extracted"}
        vid, title, uploader, webpage_url = meta
        mp3s = sorted(td.glob(f"{vid}*.mp3"))
        if not mp3s:
            return {"ok": False, "error": "audio file missing"}
        client = OpenAI(api_key=api_key)
        with open(mp3s[0], "rb") as f:
            tr = client.audio.transcriptions.create(model="whisper-1", file=f, response_format="text")
        out_path = out_dir / f"{slug(title)}.txt"
        out_path.write_text(tr)
        return {"ok": True, "source": "podcast", "title": title, "uploader": uploader,
                "url": webpage_url, "transcript_path": str(out_path), "transcript_chars": len(tr)}


def fetch_ig_tiktok(query: str, out_dir: Path) -> dict:
    token = os.environ.get("APIFY_TOKEN")
    if not token:
        return {"ok": False, "error": "APIFY_TOKEN missing — needed for IG/TikTok scraping"}
    return {"ok": False, "error": "IG/TikTok fetch not implemented in v0.1 — wire to Apify actor 'apify/tiktok-scraper' or 'apify/instagram-scraper' and parse captions field"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--query")
    ap.add_argument("--url")
    ap.add_argument("--source", choices=["youtube", "podcast", "ig_tiktok"], default="youtube")
    ap.add_argument("--out-dir", default="./outputs/transcripts")
    args = ap.parse_args()
    if not args.query and not args.url:
        sys.stderr.write("--query or --url required\n")
        sys.exit(2)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.source == "youtube":
        result = fetch_youtube(args.query, args.url, out_dir)
    elif args.source == "podcast":
        if not args.url:
            sys.stderr.write("--url required for --source podcast\n")
            sys.exit(2)
        result = fetch_podcast_via_whisper(args.url, out_dir)
    else:
        result = fetch_ig_tiktok(args.query or "", out_dir)

    json.dump(result, sys.stdout, indent=2)


if __name__ == "__main__":
    main()
