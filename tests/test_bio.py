import io
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _load import load  # noqa: E402

bio = load("instagram-profile", "bio.py")


class BioTests(unittest.TestCase):
    def test_counts_and_ok(self):
        r = bio.check("Lunch from 4 SLU food trucks.\nPickup at Denny Park.", "Curbside | SLU lunch", "curbsidelunchclub", 2)
        self.assertTrue(r["ok"])
        self.assertEqual(r["bio_chars"], len("Lunch from 4 SLU food trucks.\nPickup at Denny Park."))

    def test_bio_over_limit(self):
        r = bio.check("x" * 151)
        self.assertFalse(r["ok"])
        self.assertIn("1 over", r["problems"][0])

    def test_near_limit_warns(self):
        r = bio.check("x" * 148)
        self.assertTrue(r["ok"])
        self.assertTrue(any("Little room" in w for w in r["warnings"]))

    def test_name_and_username(self):
        r = bio.check("hi", "N" * 31, "bad handle!", 6)
        self.assertEqual(len(r["problems"]), 3)

    def test_url_hype_tags_em_dash(self):
        r = bio.check("World-class bread — www.x.com #a #b #c")
        self.assertFalse(r["ok"])
        joined = " ".join(r["warnings"])
        self.assertIn("not clickable", joined)
        self.assertIn("world-class", joined)
        self.assertIn("3 hashtags", joined)

    def test_split_options(self):
        self.assertEqual(len(bio.split_options("a\nb\n\nc\n\n\nd")), 3)

    def test_cli(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "b.txt")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write("Option one\nline two\n\n" + "y" * 160)
            buf = io.StringIO()
            with redirect_stdout(buf):
                code = bio.main(["--file", path, "--name", "Corner Loaf | Ballard bakery"])
            self.assertEqual(code, 1)
            self.assertIn("OPTION 2", buf.getvalue())
            buf = io.StringIO()
            with redirect_stdout(buf):
                self.assertEqual(bio.main(["--bio", "line one\\nline two"]), 0)
            self.assertIn("| line two", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
