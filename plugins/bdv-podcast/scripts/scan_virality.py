#!/usr/bin/env python3
"""Scan virality signals for a BDV lab.

Sources:
  - YouTube: yt-dlp search for recent uploads from tagged creators
  - Google Trends: pytrends (optional)
  - Reddit: public JSON endpoints (no auth needed for /hot.json)
  - TikTok/IG: Apify (skipped without APIFY_TOKEN)
  - Apple Podcasts charts: itunes RSS (Medicine + Health UK)

Output: JSON to stdout. Per-source 'skipped' field if unavailable.
"""
import argparse
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

LAB_REDDIT = {
    "skin": ["SkincareAddiction", "30PlusSkinCare", "AsianBeauty"],
    "face": ["PlasticSurgery", "30PlusSkinCare"],
    "hair": ["tressless", "FemaleHairLoss"],
    "body": ["loseit", "PlasticSurgery", "Biohackers"],
    "wellness": ["Biohackers", "Menopause", "Longevity", "Peptides"],
}

LAB_SEEDS = {
    "skin": ["acne", "melasma", "rosacea", "skin barrier", "tretinoin", "exosomes skin", "polynucleotides"],
    "face": ["facelift", "filler dissolved", "biostimulator", "PLLA", "deep plane", "exosomes face"],
    "hair": ["minoxidil oral", "hair peptide", "alopecia", "PRP hair", "exosomes hair"],
    "body": ["GLP-1", "tirzepatide", "body recomposition", "BBL", "lipo regen"],
    "wellness": ["perimenopause", "testosterone women", "NAD", "peptides longevity", "GLP-1 microdose", "libido"],
}


def reddit_hot(subs, limit=10):
    results = []
    for sub in subs:
        try:
            req = urllib.request.Request(
                f"https://www.reddit.com/r/{sub}/hot.json?limit={limit}",
                headers={"User-Agent": "bdv-virality-monitor/0.1"},
            )
            with urllib.request.urlopen(req, timeout=10) as r:
                data = json.load(r)
            for post in data["data"]["children"]:
                p = post["data"]
                age_hr = max(1, (dt.datetime.utcnow().timestamp() - p["created_utc"]) / 3600)
                results.append({
                    "subreddit": sub,
                    "title": p["title"],
                    "score": p["score"],
                    "comments": p["num_comments"],
                    "velocity": round(p["score"] / age_hr, 2),
                    "age_hours": round(age_hr, 1),
                    "url": "https://reddit.com" + p["permalink"],
                })
        except Exception as e:
            results.append({"subreddit": sub, "error": str(e)[:200]})
    results.sort(key=lambda r: r.get("velocity", 0), reverse=True)
    return results[:15]


def youtube_recent(seeds, days=7):
    if not shutil.which("yt-dlp"):
        return {"skipped": "yt-dlp not installed"}
    out = []
    after = (dt.date.today() - dt.timedelta(days=days)).strftime("%Y%m%d")
    for seed in seeds[:5]:
        try:
            cmd = ["yt-dlp", "--flat-playlist", "--dateafter", after,
                   "--match-filter", f"upload_date >= {after}",
                   "--print", "%(title)s\t%(uploader)s\t%(view_count)s\t%(upload_date)s\t%(webpage_url)s",
                   f"ytsearch5:{seed}"]
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            for line in r.stdout.strip().splitlines():
                parts = line.split("\t")
                if len(parts) < 5: continue
                title, uploader, views, date, url = parts
                try:
                    age_hr = max(1, (dt.datetime.utcnow() - dt.datetime.strptime(date, "%Y%m%d")).total_seconds() / 3600)
                    velocity = int(views or 0) / age_hr
                except Exception:
                    velocity = 0
                out.append({"seed": seed, "title": title, "uploader": uploader,
                            "views": int(views or 0), "age_hours": round(age_hr, 1),
                            "velocity_vph": round(velocity, 1), "url": url})
        except Exception as e:
            out.append({"seed": seed, "error": str(e)[:200]})
    out.sort(key=lambda r: r.get("velocity_vph", 0), reverse=True)
    return out[:15]


def google_trends(seeds):
    try:
        from pytrends.request import TrendReq
    except ImportError:
        return {"skipped": "pytrends not installed (pip3 install pytrends)"}
    try:
        pt = TrendReq(hl="en-GB", tz=0)
        pt.build_payload(seeds[:5], timeframe="now 7-d", geo="GB")
        df = pt.interest_over_time()
        if df.empty:
            return []
        latest = df.iloc[-1].to_dict()
        latest.pop("isPartial", None)
        ranked = sorted(latest.items(), key=lambda kv: kv[1], reverse=True)
        return [{"term": k, "score_0_100": int(v)} for k, v in ranked]
    except Exception as e:
        return {"skipped": f"pytrends error: {str(e)[:200]}"}


def apple_charts():
    out = {}
    for cat_id, label in (("1512", "Medicine"), ("1512", "Health & Fitness")):
        try:
            url = f"https://itunes.apple.com/gb/rss/topaudiopodcasts/limit=25/genre={cat_id}/json"
            with urllib.request.urlopen(url, timeout=10) as r:
                data = json.load(r)
            entries = data.get("feed", {}).get("entry", [])
            out[label] = [{"rank": i + 1, "title": e["im:name"]["label"], "artist": e["im:artist"]["label"]}
                          for i, e in enumerate(entries)]
        except Exception as e:
            out[label] = {"skipped": str(e)[:200]}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lab", required=True)
    args = ap.parse_args()
    lab = args.lab.strip().lower()
    if lab not in LAB_SEEDS:
        sys.stderr.write(f"Unknown lab '{args.lab}'\n")
        sys.exit(2)

    result = {
        "lab": lab,
        "generated_at": dt.datetime.utcnow().isoformat() + "Z",
        "reddit_hot": reddit_hot(LAB_REDDIT[lab]),
        "youtube_rising": youtube_recent(LAB_SEEDS[lab]),
        "google_trends_rising": google_trends(LAB_SEEDS[lab]),
        "apple_chart": apple_charts(),
        "ig_tiktok": {"skipped": "APIFY_TOKEN not set"} if not os.environ.get("APIFY_TOKEN") else {"todo": "wire apify actor"},
    }
    json.dump(result, sys.stdout, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
