#!/usr/bin/env python3
"""Print the dates of a planning week and what was posted recently.

Models get weekdays wrong. This tool gives the real dates for the week, the ISO week id
for the file name, and the themes from log.md in the days before the week starts, so the
plan does not repeat them.

Usage:
  python3 week.py                          # next Monday's week
  python3 week.py --start 2026-10-26       # the week that holds this date
  python3 week.py --log ~/.founder/social/instagram/my-cafe/log.md --days 28
  python3 week.py --json

log.md lines look like this (the plan skill appends them when the user says "posted"):
  - 2026-10-20 | reel | proof | theme: lunch rush | the 11:52 line out the door

Standard library only.
"""
import argparse
import datetime as dt
import json
import os
import re
import sys

LOG_LINE = re.compile(r"^\s*[-*]\s*(\d{4}-\d{2}-\d{2})\s*\|(.*)$")



def resolve(path):
    """Expand ~ and, when FOUNDER_HOME is set, map a leading ~/.founder onto it.

    User data lives in ~/.founder (Claude Code protects ~/.claude). Tests set FOUNDER_HOME.
    """
    env = os.environ.get("FOUNDER_HOME")
    norm = path.replace("\\", "/")
    if env and (norm == "~/.founder" or norm.startswith("~/.founder/")):
        path = os.path.join(os.path.expanduser(env), norm[len("~/.founder/"):])
    return os.path.expanduser(path)


def week_of(day):
    """Return the Monday to Sunday dates of the ISO week that holds `day`."""
    monday = day - dt.timedelta(days=day.weekday())
    return [monday + dt.timedelta(days=i) for i in range(7)]


def next_monday(today):
    days = (7 - today.weekday()) % 7 or 7
    return today + dt.timedelta(days=days)


def parse_log(text):
    """Yield dicts with date, format, type, theme, angle from log lines."""
    entries = []
    for line in text.splitlines():
        m = LOG_LINE.match(line)
        if not m:
            continue
        try:
            date = dt.date.fromisoformat(m.group(1))
        except ValueError:
            continue
        parts = [p.strip() for p in m.group(2).split("|")]
        entry = {"date": date, "format": "", "type": "", "theme": "", "angle": ""}
        loose = []
        for p in parts:
            if p.lower().startswith("theme:"):
                entry["theme"] = p.split(":", 1)[1].strip()
            elif p:
                loose.append(p)
        keys = ["format", "type", "angle"]
        for key, val in zip(keys, loose):
            entry[key] = val
        entries.append(entry)
    return entries


def recent(entries, start, days):
    since = start - dt.timedelta(days=days)
    return [e for e in entries if since <= e["date"] < start]


def build(start, log_text=None, days=28):
    dates = week_of(start)
    iso = dates[0].isocalendar()
    out = {
        "week_id": "%d-W%02d" % (iso[0], iso[1]),
        "days": [{"date": d.isoformat(), "weekday": d.strftime("%a").upper()} for d in dates],
        "recent": [],
        "repeat_themes": [],
    }
    if log_text:
        rec = recent(parse_log(log_text), dates[0], days)
        out["recent"] = [
            {"date": e["date"].isoformat(), "format": e["format"], "type": e["type"],
             "theme": e["theme"], "angle": e["angle"]}
            for e in rec
        ]
        counts = {}
        for e in rec:
            key = e["theme"].lower()
            if key:
                counts[key] = counts.get(key, 0) + 1
        out["repeat_themes"] = sorted(counts)
    return out


def main(argv=None):
    parser = argparse.ArgumentParser(description="Dates for a planning week.")
    parser.add_argument("--start", help="any date in the week to plan (YYYY-MM-DD)")
    parser.add_argument("--today", help=argparse.SUPPRESS)
    parser.add_argument("--log", help="path to log.md")
    parser.add_argument("--days", type=int, default=28, help="look back this many days (default 28)")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    try:
        if args.start:
            start = dt.date.fromisoformat(args.start)
        else:
            today = dt.date.fromisoformat(args.today) if args.today else dt.date.today()
            start = next_monday(today)
    except ValueError:
        print("Dates must look like 2026-10-26.", file=sys.stderr)
        return 2

    log_text = None
    if args.log:
        path = resolve(args.log)
        if os.path.exists(path):
            with open(path, encoding="utf-8") as fh:
                log_text = fh.read()
        else:
            print("No log at %s yet. That is fine for a first plan." % path, file=sys.stderr)

    data = build(start, log_text, args.days)
    if args.json:
        print(json.dumps(data, indent=2))
        return 0
    print("WEEK %s" % data["week_id"])
    for d in data["days"]:
        print("  %s  %s" % (d["weekday"], d["date"]))
    if log_text is not None:
        print("\nPOSTED IN THE %d DAYS BEFORE" % args.days)
        if not data["recent"]:
            print("  nothing logged")
        for e in data["recent"]:
            print("  %s  %-9s %-8s theme: %s" % (e["date"], e["format"], e["type"], e["theme"] or "-"))
        if data["repeat_themes"]:
            print("\nAVOID REPEATING: " + ", ".join(data["repeat_themes"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
