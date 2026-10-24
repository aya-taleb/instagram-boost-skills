import csv
import io
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _load import load  # noqa: E402

ins = load("instagram-audit", "insights.py")

EXPORT = """Publish time,Post type,Reach,Likes,Comments,Shares,Saves,Follows,Profile visits,Description
2026-09-02 10:30,IG reel,2000,80,10,30,20,5,40,truck reel
2026-09-05 10:30,IG carousel,1000,50,5,10,40,2,20,menu carousel
2026-09-09 10:30,IG reel,4000,100,12,20,20,8,60,another reel
2026-09-12 10:30,IG image,500,20,1,0,1,0,5,photo
2026-09-15 10:30,IG reel,,,,,,,,no reach row
"""
LOG = """- 2026-09-02 | reel | story | theme: meet the trucks | x
- 2026-09-05 | carousel | teach | theme: menu | y
"""


def parsed():
    reader = csv.DictReader(io.StringIO(EXPORT))
    return list(reader), reader.fieldnames


class InsightsTests(unittest.TestCase):
    def test_resolve(self):
        _, header = parsed()
        cols = ins.resolve(header)
        self.assertEqual(cols["date"], "Publish time")
        self.assertEqual(cols["format"], "Post type")
        self.assertEqual(cols["visits"], "Profile visits")
        self.assertNotIn("link_taps", cols)

    def test_load_rates_and_skips_empty(self):
        rows, header = parsed()
        posts, _ = ins.load(rows, header, ins.themes_from_log(LOG))
        self.assertEqual(len(posts), 4)
        first = posts[0]
        self.assertEqual(first["share_save_rate"], 2.5)
        self.assertEqual(first["theme"], "meet the trucks")
        self.assertEqual(posts[1]["share_save_rate"], 5.0)
        self.assertEqual(posts[2]["theme"], "")

    def test_summary(self):
        rows, header = parsed()
        posts, _ = ins.load(rows, header)
        s = ins.summary(posts)
        self.assertTrue(s["small_sample"])
        self.assertEqual(s["top"][0]["format"], "ig carousel")
        self.assertEqual(s["total_follows"], 15)
        self.assertEqual(s["median_share_save_rate"], 1.75)  # rates 2.5, 5.0, 1.0, 0.2
        fmts = {g["format"]: g for g in s["by_format"]}
        self.assertEqual(fmts["ig reel"]["posts"], 2)
        self.assertEqual(fmts["ig reel"]["median_reach"], 3000)

    def test_top_and_bottom_do_not_overlap(self):
        rows, header = parsed()
        posts, _ = ins.load(rows, header)
        s = ins.summary(posts)
        top = {p["date"] for p in s["top"]}
        bottom = {p["date"] for p in s["bottom"]}
        self.assertEqual(len(s["top"]), 3)
        self.assertEqual(len(s["bottom"]), 1)
        self.assertFalse(top & bottom)

    def test_no_reach_column(self):
        reader = csv.DictReader(io.StringIO("date,likes\n2026-01-01,4\n"))
        with self.assertRaises(ValueError):
            ins.load(list(reader), reader.fieldnames)

    def test_views_fallback_and_commas(self):
        reader = csv.DictReader(io.StringIO('date,views,saves\n2026-01-01,"1,000",10\n'))
        posts, _ = ins.load(list(reader), reader.fieldnames)
        self.assertEqual(posts[0]["base"], 1000)
        self.assertEqual(posts[0]["share_save_rate"], 1.0)

    def test_cli(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "e.csv")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(EXPORT)
            buf = io.StringIO()
            with redirect_stdout(buf):
                self.assertEqual(ins.main([path]), 0)
            out = buf.getvalue()
            self.assertIn("SMALL SAMPLE", out)
            self.assertIn("not in this export: link_taps", out)
            bad = os.path.join(tmp, "b.csv")
            with open(bad, "w", encoding="utf-8") as fh:
                fh.write("a,b\n1,2\n")
            with redirect_stdout(io.StringIO()):
                self.assertEqual(ins.main([bad]), 2)


if __name__ == "__main__":
    unittest.main()
