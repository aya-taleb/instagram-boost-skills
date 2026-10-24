#!/usr/bin/env python3
"""Count Instagram profile fields the way the app counts them, and flag common problems.

Limits (checked 2026-10-23, see references/instagram-limits.md):
  bio 150 characters, name field 30, username 30, links up to 5.

Usage:
  python3 bio.py --bio "text" [--name "Name | phrase"] [--username handle] [--links 3]
  python3 bio.py --file bio.txt           # one bio option per block, blank line between
  python3 bio.py --json --bio "..."

Counts by Unicode code points, which matches the app closely for plain text and most emoji.
Some combined emoji (flags, skin tones, families) count as 2 or more. Leave a few spare
characters when you use them.

Standard library only.
"""
import argparse
import json
import re
import sys

BIO_MAX = 150
NAME_MAX = 30
USERNAME_MAX = 30
LINKS_MAX = 5
HYPE = ["world-class", "best in", "#1", "number one", "guaranteed", "life-changing", "award-winning"]
URL = re.compile(r"(https?://|www\.)\S+", re.I)
USERNAME_OK = re.compile(r"^[A-Za-z0-9._]+$")


def count(text):
    return len(text or "")


def check(bio="", name="", username="", links=None):
    """Return a dict with counts, problems and warnings."""
    problems, warnings = [], []
    b, n, u = count(bio), count(name), count(username.lstrip("@"))
    if b > BIO_MAX:
        problems.append("bio is %d characters, %d over the %d limit" % (b, b - BIO_MAX, BIO_MAX))
    elif b > BIO_MAX - 5:
        warnings.append("bio is %d of %d. Little room for emoji that count double." % (b, BIO_MAX))
    if name and n > NAME_MAX:
        problems.append("name field is %d characters, limit %d" % (n, NAME_MAX))
    if username:
        handle = username.lstrip("@")
        if u > USERNAME_MAX:
            problems.append("username is %d characters, limit %d" % (u, USERNAME_MAX))
        if not USERNAME_OK.match(handle):
            problems.append("username can only use letters, numbers, periods and underscores")
    if links is not None and links > LINKS_MAX:
        problems.append("%d links. Instagram allows %d." % (links, LINKS_MAX))
    if URL.search(bio or ""):
        warnings.append("URL in the bio text is not clickable. Use the links field.")
    if "—" in (bio or "") + (name or ""):
        problems.append("em dash found. Use a comma or a period.")
    low = (bio or "").lower()
    for h in HYPE:
        if h in low:
            warnings.append("'%s' is a claim. Keep it only if you can prove it." % h)
    tags = re.findall(r"#\w+", bio or "")
    if len(tags) > 2:
        warnings.append("%d hashtags in the bio. They are clickable and lead people away." % len(tags))
    if bio and "\n" not in bio and b > 90:
        warnings.append("one long line. Line breaks make a bio easier to scan.")
    return {"bio_chars": b, "bio_left": BIO_MAX - b, "name_chars": n, "username_chars": u,
            "problems": problems, "warnings": warnings, "ok": not problems}


def split_options(text):
    return [blk.strip("\n") for blk in re.split(r"\n\s*\n", text) if blk.strip()]


def main(argv=None):
    p = argparse.ArgumentParser(description="Count and check Instagram profile fields.")
    p.add_argument("--bio", default=None)
    p.add_argument("--file")
    p.add_argument("--name", default="")
    p.add_argument("--username", default="")
    p.add_argument("--links", type=int)
    p.add_argument("--json", action="store_true")
    a = p.parse_args(argv)
    if a.file:
        with open(a.file, encoding="utf-8") as fh:
            options = split_options(fh.read())
    elif a.bio is not None:
        options = [a.bio.replace("\\n", "\n")]
    else:
        p.error("give --bio or --file")
    results = [check(o, a.name, a.username, a.links) for o in options]
    if a.json:
        print(json.dumps(results, indent=2))
        return 0 if all(r["ok"] for r in results) else 1
    for i, (o, r) in enumerate(zip(options, results), 1):
        print("OPTION %d  %d/%d characters (%d left)" % (i, r["bio_chars"], BIO_MAX, r["bio_left"]))
        for line in o.splitlines():
            print("  | " + line)
        if a.name:
            print("  name field: %d/%d" % (r["name_chars"], NAME_MAX))
        for x in r["problems"]:
            print("  FAIL  " + x)
        for x in r["warnings"]:
            print("  WARN  " + x)
    return 0 if all(r["ok"] for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
