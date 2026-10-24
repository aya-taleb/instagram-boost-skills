#!/usr/bin/env python3
"""Check carousel copy, build slide HTML, and do the image cost math.

Slides file format (slides.md), one block per slide:

  ## 1 COVER
  Lunch in 6 minutes flat
  Your desk deserves better than a sad salad.

  ## 2
  ...

The first line under the heading is the headline. The rest is the body.

Usage:
  python3 slides.py check slides.md
  python3 slides.py html slides.md --out carousel.html --handle @mycafe --accent "#d9480f"
  python3 slides.py cost --images 7 --price 0.04 --spent 1.10 --cap 5

Limits (checked 2026-10-23, see references/instagram-limits.md): up to 20 items per
carousel, 1080x1350 (4:5) is the safe size, 1080x1440 (3:4) also works.

Standard library only. No network.
"""
import argparse
import html
import re
import sys

MAX_ITEMS = 20
COVER_WORDS = 6
HEADLINE_WORDS = 7
BODY_WORDS = 25
SIZES = {"4:5": (1080, 1350), "3:4": (1080, 1440), "1:1": (1080, 1080)}
HEAD = re.compile(r"^##\s*(\d+)\s*(.*)$")


def parse(text):
    slides = []
    cur = None
    for raw in text.splitlines():
        line = raw.rstrip()
        m = HEAD.match(line)
        if m:
            cur = {"n": int(m.group(1)), "label": m.group(2).strip().upper(), "lines": []}
            slides.append(cur)
            continue
        if cur is not None and line.strip():
            cur["lines"].append(line.strip())
    for s in slides:
        s["headline"] = s["lines"][0] if s["lines"] else ""
        s["body"] = " ".join(s["lines"][1:])
    return slides


def words(text):
    return len([w for w in re.split(r"\s+", text.strip()) if w])


def check(slides):
    """Return (problems, warnings) as lists of strings."""
    problems, warnings = [], []
    if not slides:
        return ["no slides found. Use '## 1 COVER' style headings."], []
    if len(slides) > MAX_ITEMS:
        problems.append("%d slides. Instagram allows %d items." % (len(slides), MAX_ITEMS))
    if len(slides) < 3:
        warnings.append("only %d slides. Under 3 rarely earns a swipe." % len(slides))
    if len(slides) > 12:
        warnings.append("%d slides. Past 12, most people stop swiping." % len(slides))
    nums = [s["n"] for s in slides]
    if nums != list(range(1, len(slides) + 1)):
        warnings.append("slide numbers are not 1..%d in order: %s" % (len(slides), nums))
    cover = slides[0]
    cw = words(cover["headline"])
    if cw == 0:
        problems.append("slide 1 has no headline")
    elif cw > COVER_WORDS:
        problems.append("cover headline is %d words. Keep it to %d or fewer." % (cw, COVER_WORDS))
    for s in slides[1:]:
        hw = words(s["headline"])
        bw = words(s["body"])
        if hw == 0:
            problems.append("slide %d has no headline" % s["n"])
        elif hw > HEADLINE_WORDS + 3:
            problems.append("slide %d headline is %d words. Aim for %d or fewer." % (s["n"], hw, HEADLINE_WORDS))
        elif hw > HEADLINE_WORDS:
            warnings.append("slide %d headline is %d words." % (s["n"], hw))
        if bw > BODY_WORDS:
            problems.append("slide %d body is %d words. Split it, the cap is %d." % (s["n"], bw, BODY_WORDS))
    if "—" in "".join(" ".join(s["lines"]) for s in slides):
        problems.append("em dash found. Use a comma or a period.")
    ph = [s["n"] for s in slides if "{{" in " ".join(s["lines"])]
    if ph:
        warnings.append("placeholders to fill on slides %s" % ph)
    return problems, warnings


def render_html(slides, handle="", accent="#222222", ratio="4:5"):
    w, h = SIZES[ratio]
    total = len(slides)
    out = [
        "<!doctype html><html><head><meta charset='utf-8'><title>carousel</title><style>",
        "@page{size:%dpx %dpx;margin:0}" % (w, h),
        "body{margin:0;background:#ddd;font-family:Helvetica,Arial,sans-serif}",
        "section{width:%dpx;height:%dpx;box-sizing:border-box;padding:140px 120px;" % (w, h),
        "background:#fff;color:#111;position:relative;page-break-after:always;display:flex;",
        "flex-direction:column;justify-content:center;margin:0 auto 24px}",
        "h1{font-size:96px;line-height:1.05;margin:0 0 32px;color:%s}" % html.escape(accent),
        "h2{font-size:72px;line-height:1.1;margin:0 0 28px}",
        "p{font-size:40px;line-height:1.35;margin:0}",
        ".foot{position:absolute;bottom:60px;left:120px;right:120px;font-size:30px;",
        "display:flex;justify-content:space-between;color:#666}",
        "</style></head><body>",
    ]
    for i, s in enumerate(slides):
        tag = "h1" if i == 0 else "h2"
        out.append("<section>")
        out.append("<%s>%s</%s>" % (tag, html.escape(s["headline"]), tag))
        if s["body"]:
            out.append("<p>%s</p>" % html.escape(s["body"]))
        out.append("<div class='foot'><span>%s</span><span>%d/%d</span></div>" % (html.escape(handle), i + 1, total))
        out.append("</section>")
    out.append("</body></html>")
    return "\n".join(out)


def cost(images, price, spent=0.0, cap=5.0):
    """Return a dict with the estimate and whether it fits under the cap."""
    estimate = round(images * price, 4)
    after = round(spent + estimate, 4)
    return {
        "images": images,
        "price_each": price,
        "estimate": estimate,
        "spent_so_far": spent,
        "cap": cap,
        "total_after": after,
        "fits": after <= cap + 1e-9,
        "room_left": round(cap - spent, 4),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description="Carousel copy checks, HTML and cost math.")
    sub = parser.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check")
    c.add_argument("file")
    hp = sub.add_parser("html")
    hp.add_argument("file")
    hp.add_argument("--out", required=True)
    hp.add_argument("--handle", default="")
    hp.add_argument("--accent", default="#222222")
    hp.add_argument("--ratio", choices=sorted(SIZES), default="4:5")
    cp = sub.add_parser("cost")
    cp.add_argument("--images", type=int, required=True)
    cp.add_argument("--price", type=float, required=True, help="dollars per image, from the live model page")
    cp.add_argument("--spent", type=float, default=0.0)
    cp.add_argument("--cap", type=float, default=5.0)
    args = parser.parse_args(argv)

    if args.cmd == "cost":
        r = cost(args.images, args.price, args.spent, args.cap)
        print("%d images x $%.4f = $%.2f estimated" % (r["images"], r["price_each"], r["estimate"]))
        print("spent this session: $%.2f, cap: $%.2f, after this run: $%.2f" % (r["spent_so_far"], r["cap"], r["total_after"]))
        if r["fits"]:
            print("FITS under the cap. Ask the user for a yes before running.")
            return 0
        print("OVER the cap. Room left: $%.2f. Cut images or ask the user to raise the cap." % r["room_left"])
        return 1

    with open(args.file, encoding="utf-8") as fh:
        slides = parse(fh.read())
    if args.cmd == "check":
        problems, warnings = check(slides)
        print("%d slides" % len(slides))
        for p in problems:
            print("  FAIL  " + p)
        for wmsg in warnings:
            print("  WARN  " + wmsg)
        print("READY" if not problems else "FIX THE FAILS")
        return 1 if problems else 0
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(render_html(slides, args.handle, args.accent, args.ratio))
    w, h = SIZES[args.ratio]
    print("wrote %s (%d slides at %dx%d)" % (args.out, len(slides), w, h))
    return 0


if __name__ == "__main__":
    sys.exit(main())
