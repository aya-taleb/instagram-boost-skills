#!/usr/bin/env python3
"""Pick Instagram leads from sales/leads.csv and track DM follow-ups.

The lead-gen skill (biz-boost-skills) writes sales/leads.csv in the shared layout from
CONVENTIONS section 5:

  business_slug,name,company,role,email,linkedin_url,instagram_handle,website,city,
  source,source_url,fit_score,fit_reason,status,last_contact,notes

This tool reads exactly those columns. It filters by business_slug, uses instagram_handle,
skips do-not-contact (and won, lost, contacted, replied, meeting), and sorts by fit_score.
The notes column is the place for a trigger ("commented LUNCH on the Nov 9 reel").

It never contacts anyone. It prints who to write to and, after the user sends, prints the
status and last_contact values to put back in leads.csv.

Usage:
  python3 leads.py pick sales/leads.csv --business my-cafe [--top 5] [--min-fit 60]
  python3 leads.py sent sales/leads.csv --business my-cafe --handle @sam --date 2026-10-23
  python3 leads.py due ~/.founder/social/instagram/my-cafe/dm-log.csv [--today 2026-10-23]
  python3 leads.py log ~/.founder/social/instagram/my-cafe/dm-log.csv --handle @sam --kind warm --sent 2026-10-23

Standard library only. No network.
"""
import argparse
import csv
import datetime as dt
import os
import sys

COLUMNS = ["business_slug", "name", "company", "role", "email", "linkedin_url",
           "instagram_handle", "website", "city", "source", "source_url", "fit_score",
           "fit_reason", "status", "last_contact", "notes"]
REQUIRED = ["business_slug", "instagram_handle", "status"]
SKIP_STATUS = {"do-not-contact", "contacted", "replied", "meeting", "won", "lost"}
FOLLOW_UPS = [(4, "follow-up 1: add something new"), (10, "follow-up 2: close the loop")]
LOG_FIELDS = ["handle", "kind", "sent", "follow_up_1", "follow_up_2", "replied", "notes"]



def resolve(path):
    """Expand ~ and, when FOUNDER_HOME is set, map a leading ~/.founder onto it.

    User data lives in ~/.founder (Claude Code protects ~/.claude). Tests set FOUNDER_HOME.
    """
    env = os.environ.get("FOUNDER_HOME")
    norm = path.replace("\\", "/")
    if env and (norm == "~/.founder" or norm.startswith("~/.founder/")):
        path = os.path.join(os.path.expanduser(env), norm[len("~/.founder/"):])
    return os.path.expanduser(path)


def norm(s):
    return (s or "").strip().lower()


def missing_columns(header):
    have = {norm(h) for h in header or []}
    return [c for c in REQUIRED if c not in have]


def to_float(v):
    try:
        return float(str(v).strip().rstrip("%"))
    except (TypeError, ValueError):
        return None


def clean_handle(h):
    h = (h or "").strip()
    if not h:
        return ""
    if "instagram.com/" in h:
        h = h.split("instagram.com/", 1)[1].split("/")[0].split("?")[0]
    h = h.lstrip("@")
    return "@" + h if h else ""


def pick(rows, business, top=5, min_fit=None):
    """Return (chosen, skipped) for one business. skipped holds (label, reason)."""
    chosen, skipped = [], []
    for row in rows:
        get = lambda k: (row.get(k) or "").strip()
        label = get("name") or get("company") or get("instagram_handle") or "(no name)"
        if norm(get("business_slug")) != norm(business):
            skipped.append((label, "for another business"))
            continue
        status = norm(get("status"))
        if status in SKIP_STATUS:
            skipped.append((label, "status is '%s'" % status))
            continue
        handle = clean_handle(get("instagram_handle"))
        if not handle:
            skipped.append((label, "no instagram_handle"))
            continue
        fit = to_float(get("fit_score"))
        if min_fit is not None and (fit is None or fit < min_fit):
            skipped.append((label, "fit_score below %g" % min_fit))
            continue
        chosen.append({
            "name": get("name"), "company": get("company"), "handle": handle, "fit": fit,
            "reason": get("fit_reason"), "trigger": get("notes"), "city": get("city"),
            "source_url": get("source_url"),
        })
    chosen.sort(key=lambda r: (r["fit"] is None, -(r["fit"] or 0)))
    return chosen[:top], skipped


def mark_sent(rows, business, handle, date):
    """Return the row to update (or None). Does not write the file."""
    want = clean_handle(handle).lower()
    for row in rows:
        if norm(row.get("business_slug")) == norm(business) and clean_handle(row.get("instagram_handle")).lower() == want:
            return row
    return None


def due(log_rows, today):
    """Return follow-ups due on or before today, as (handle, label, date)."""
    out = []
    for r in log_rows:
        if (r.get("replied") or "").strip().lower() in ("yes", "y", "true"):
            continue
        try:
            sent = dt.date.fromisoformat((r.get("sent") or "").strip())
        except ValueError:
            continue
        for i, (days, label) in enumerate(FOLLOW_UPS, 1):
            if (r.get("follow_up_%d" % i) or "").strip():
                continue
            when = sent + dt.timedelta(days=days)
            if when <= today:
                out.append((r.get("handle", ""), label, when.isoformat()))
            break
    return out


def read_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        return list(reader), reader.fieldnames or []


def main(argv=None):
    parser = argparse.ArgumentParser(description="Instagram leads and DM follow-ups.")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("pick")
    p.add_argument("csv")
    p.add_argument("--business", required=True, help="the active business_slug")
    p.add_argument("--top", type=int, default=5)
    p.add_argument("--min-fit", type=float)
    st = sub.add_parser("sent")
    st.add_argument("csv")
    st.add_argument("--business", required=True)
    st.add_argument("--handle", required=True)
    st.add_argument("--date", required=True)
    d = sub.add_parser("due")
    d.add_argument("log")
    d.add_argument("--today")
    lg = sub.add_parser("log")
    lg.add_argument("log")
    lg.add_argument("--handle", required=True)
    lg.add_argument("--kind", required=True, choices=["keyword", "warm", "collab", "lead", "reply"])
    lg.add_argument("--sent", required=True)
    lg.add_argument("--notes", default="")
    args = parser.parse_args(argv)

    if args.cmd in ("pick", "sent"):
        if not os.path.exists(args.csv):
            print("No leads file at %s. Run lead-gen (biz-boost-skills) or paste handles." % args.csv)
            return 2
        rows, header = read_csv(args.csv)
        missing = missing_columns(header)
        if missing:
            print("leads.csv is missing: %s. Expected the shared layout:" % ", ".join(missing))
            print("  " + ",".join(COLUMNS))
            return 2

    if args.cmd == "pick":
        chosen, skipped = pick(rows, args.business, args.top, args.min_fit)
        print("%d rows, %d picked for %s, %d skipped" % (len(rows), len(chosen), args.business, len(skipped)))
        for r in chosen:
            fit = "-" if r["fit"] is None else "%g" % r["fit"]
            who = r["name"] or r["company"]
            print("  %-22s fit %-5s %s | trigger: %s" % (r["handle"], fit, who, r["trigger"] or "NONE, comment first"))
            if r["reason"]:
                print("  %-22s why: %s" % ("", r["reason"]))
        for label, why in skipped:
            print("  skip  %s (%s)" % (label, why))
        return 0

    if args.cmd == "sent":
        dt.date.fromisoformat(args.date)
        row = mark_sent(rows, args.business, args.handle, args.date)
        if row is None:
            print("No row for %s in %s." % (clean_handle(args.handle), args.business))
            return 1
        print("Update this row in sales/leads.csv (ask the user first):")
        print("  %s: status %s -> contacted, last_contact %s -> %s" % (
            clean_handle(args.handle), row.get("status") or "(empty)", row.get("last_contact") or "(empty)", args.date))
        return 0

    if args.cmd == "due":
        if not os.path.exists(resolve(args.log)):
            print("No DM log yet.")
            return 0
        rows, _ = read_csv(resolve(args.log))
        today = dt.date.fromisoformat(args.today) if args.today else dt.date.today()
        items = due(rows, today)
        if not items:
            print("Nothing due.")
        for handle, label, when in items:
            print("  %s  %s (due %s)" % (handle, label, when))
        return 0

    path = resolve(args.log)
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    new = not os.path.exists(path)
    dt.date.fromisoformat(args.sent)
    with open(path, "a", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=LOG_FIELDS)
        if new:
            w.writeheader()
        w.writerow({"handle": clean_handle(args.handle), "kind": args.kind, "sent": args.sent,
                    "follow_up_1": "", "follow_up_2": "", "replied": "", "notes": args.notes})
    print("logged %s (%s, sent %s)" % (clean_handle(args.handle), args.kind, args.sent))
    return 0


if __name__ == "__main__":
    sys.exit(main())
