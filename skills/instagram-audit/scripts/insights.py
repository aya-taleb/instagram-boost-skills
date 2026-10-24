#!/usr/bin/env python3
"""Turn an Instagram Insights export into rates by post, format and theme.

Takes the CSV the user exports from Meta Business Suite (Insights > Content > Export) or a
CSV they type up. Column names vary by export and language, so it looks for common names,
case-insensitive. Only `reach` (or `views`) is required; the rest are used when present.

  date         publish time, date, posted
  format       post type, type, format, media type
  reach        reach, accounts reached
  views        views, impressions, plays
  likes        likes, reactions
  comments     comments
  shares       shares
  saves        saves
  follows      follows, new followers
  visits       profile visits, profile activity
  link_taps    link clicks, external link taps, website taps
  theme        theme, topic, pillar (add this yourself, or join from log.md)
  caption      description, caption, title

Usage:
  python3 insights.py export.csv
  python3 insights.py export.csv --log ~/.founder/social/instagram/<slug>/log.md   # theme from log by date
  python3 insights.py export.csv --json

Standard library only. Reads files you exported. Never calls Instagram.
"""
import argparse
import csv
import json
import re
import statistics
import sys

ALIASES = {
    "date": ["publish_time", "date", "posted", "publish_date", "post_date"],
    "format": ["post_type", "type", "format", "media_type"],
    "reach": ["reach", "accounts_reached"],
    "views": ["views", "impressions", "plays"],
    "likes": ["likes", "reactions"],
    "comments": ["comments"],
    "shares": ["shares"],
    "saves": ["saves"],
    "follows": ["follows", "new_followers"],
    "visits": ["profile_visits", "profile_activity"],
    "link_taps": ["link_clicks", "external_link_taps", "website_taps", "link_taps"],
    "theme": ["theme", "topic", "pillar"],
    "caption": ["description", "caption", "title"],
}
NUMERIC = ["reach", "views", "likes", "comments", "shares", "saves", "follows", "visits", "link_taps"]
SMALL_SAMPLE = 8
LOG_LINE = re.compile(r"^\s*[-*]\s*(\d{4}-\d{2}-\d{2})\s*\|(.*)$")


def norm(s):
    return re.sub(r"[^a-z0-9]+", "_", (s or "").strip().lower()).strip("_")


def resolve(header):
    cols = {norm(h): h for h in header}
    out = {}
    for key, names in ALIASES.items():
        for n in names:
            if n in cols:
                out[key] = cols[n]
                break
    return out


def num(v):
    s = str(v or "").replace(",", "").strip()
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def themes_from_log(text):
    out = {}
    for line in text.splitlines():
        m = LOG_LINE.match(line)
        if not m:
            continue
        for part in m.group(2).split("|"):
            if part.strip().lower().startswith("theme:"):
                out[m.group(1)] = part.split(":", 1)[1].strip()
    return out


def load(rows, header, log_themes=None):
    cols = resolve(header)
    if "reach" not in cols and "views" not in cols:
        raise ValueError("no reach or views column found")
    posts = []
    for r in rows:
        p = {k: (r.get(cols[k], "") if k in cols else "") for k in ALIASES}
        for k in NUMERIC:
            p[k] = num(p[k])
        base = p["reach"] if p["reach"] else p["views"]
        if not base:
            continue
        p["base"] = base
        p["date"] = (p["date"] or "")[:10]
        p["format"] = (p["format"] or "unknown").strip().lower() or "unknown"
        if not p["theme"] and log_themes and p["date"] in log_themes:
            p["theme"] = log_themes[p["date"]]
        p["theme"] = (p["theme"] or "").strip().lower()
        for k in ("shares", "saves", "comments", "follows", "likes"):
            p[k + "_rate"] = None if p[k] is None else round(100.0 * p[k] / base, 2)
        sends_saves = (p["shares"] or 0) + (p["saves"] or 0)
        p["share_save_rate"] = round(100.0 * sends_saves / base, 2) if (p["shares"] is not None or p["saves"] is not None) else None
        posts.append(p)
    return posts, cols


def group(posts, key):
    groups = {}
    for p in posts:
        groups.setdefault(p[key] or "(none)", []).append(p)
    out = []
    for name, items in groups.items():
        rates = [x["share_save_rate"] for x in items if x["share_save_rate"] is not None]
        out.append({
            key: name, "posts": len(items),
            "median_reach": statistics.median([x["base"] for x in items]),
            "median_share_save_rate": statistics.median(rates) if rates else None,
            "follows": sum(x["follows"] or 0 for x in items),
        })
    out.sort(key=lambda g: -(g["median_share_save_rate"] or 0))
    return out


def brief(p):
    label = p["theme"] or (p.get("caption") or "").strip()[:28]
    return {"date": p["date"], "format": p["format"], "theme": p["theme"], "label": label,
            "rate": p["share_save_rate"], "reach": p["base"], "follows": p["follows"]}


def summary(posts):
    ranked = sorted([p for p in posts if p["share_save_rate"] is not None], key=lambda p: -p["share_save_rate"])
    return {
        "posts": len(posts),
        "small_sample": len(posts) < SMALL_SAMPLE,
        "median_reach": statistics.median([p["base"] for p in posts]) if posts else 0,
        "median_share_save_rate": round(statistics.median([p["share_save_rate"] for p in posts if p["share_save_rate"] is not None]), 2) if any(p["share_save_rate"] is not None for p in posts) else None,
        "total_follows": sum(p["follows"] or 0 for p in posts),
        "total_visits": sum(p["visits"] or 0 for p in posts),
        "total_link_taps": sum(p["link_taps"] or 0 for p in posts),
        "top": [brief(p) for p in ranked[:3]],
        "bottom": [brief(p) for p in ranked[max(3, len(ranked) - 3):][::-1]],
        "by_format": group(posts, "format"),
        "by_theme": group(posts, "theme"),
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description="Rates from an Instagram Insights export.")
    ap.add_argument("csv")
    ap.add_argument("--log")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    with open(a.csv, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        rows, header = list(reader), reader.fieldnames or []
    log_themes = None
    if a.log:
        try:
            with open(a.log, encoding="utf-8") as fh:
                log_themes = themes_from_log(fh.read())
        except OSError:
            print("no log at %s, themes come from the CSV only" % a.log, file=sys.stderr)
    try:
        posts, cols = load(rows, header, log_themes)
    except ValueError as exc:
        print("Cannot read this export: %s. Columns seen: %s" % (exc, ", ".join(header)))
        return 2
    s = summary(posts)
    if a.json:
        print(json.dumps(s, indent=2))
        return 0
    print("%d posts with reach or views. median reach %g" % (s["posts"], s["median_reach"]))
    if s["small_sample"]:
        print("SMALL SAMPLE: under %d posts. Treat patterns as hunches, not findings." % SMALL_SAMPLE)
    missing = [k for k in ("shares", "saves", "follows", "visits", "link_taps") if k not in cols]
    if missing:
        print("not in this export: " + ", ".join(missing))
    print("follows %d, profile visits %d, link taps %d" % (s["total_follows"], s["total_visits"], s["total_link_taps"]))
    if s["median_share_save_rate"] is not None:
        print("median shares+saves per 100 reached, per post: %.2f" % s["median_share_save_rate"])
    print("\nSHARES + SAVES PER 100 REACHED")
    for label, items in (("top", s["top"]), ("bottom", s["bottom"])):
        for p in items:
            print("  %-6s %s  %-11s %-28s %5.2f  (reach %g, follows %s)" % (
                label, p["date"], p["format"], p["label"] or "-", p["rate"], p["reach"],
                "-" if p["follows"] is None else "%g" % p["follows"]))
    for key in ("format", "theme"):
        print("\nBY %s" % key.upper())
        for g in s["by_" + key]:
            r = g["median_share_save_rate"]
            print("  %-18s %2d posts  median reach %-8g shares+saves/100 %s  follows %d" % (
                g[key], g["posts"], g["median_reach"], "-" if r is None else "%.2f" % r, g["follows"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
