import os
import sys
import tempfile
import unittest
import io
from contextlib import redirect_stdout

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _load import load  # noqa: E402

slides = load("instagram-carousel", "slides.py")

GOOD = """## 1 COVER
Lunch in six minutes flat
Your desk deserves better.

## 2
Why it matters
You get 30 minutes. The line eats 20 of them.

## 3 RECAP
Order, walk, eat
That is the whole system.
"""


class SlidesTests(unittest.TestCase):
    def test_parse(self):
        s = slides.parse(GOOD)
        self.assertEqual(len(s), 3)
        self.assertEqual(s[0]["label"], "COVER")
        self.assertEqual(s[0]["headline"], "Lunch in six minutes flat")
        self.assertEqual(s[1]["body"], "You get 30 minutes. The line eats 20 of them.")

    def test_good_copy_passes(self):
        problems, warnings = slides.check(slides.parse(GOOD))
        self.assertEqual(problems, [])

    def test_long_cover_fails(self):
        text = GOOD.replace("Lunch in six minutes flat", "This is a very long cover line that nobody reads")
        problems, _ = slides.check(slides.parse(text))
        self.assertTrue(any("cover headline" in p for p in problems))

    def test_long_body_fails(self):
        body = " ".join(["word"] * 30)
        text = GOOD.replace("That is the whole system.", body)
        problems, _ = slides.check(slides.parse(text))
        self.assertTrue(any("slide 3 body" in p for p in problems))

    def test_over_twenty_fails(self):
        text = "\n".join("## %d\nHead %d\nbody" % (i, i) for i in range(1, 23))
        problems, _ = slides.check(slides.parse(text))
        self.assertTrue(any("allows 20" in p for p in problems))

    def test_em_dash_fails(self):
        text = GOOD.replace("Your desk deserves better.", "Your desk — better.")
        problems, _ = slides.check(slides.parse(text))
        self.assertTrue(any("em dash" in p for p in problems))

    def test_placeholder_warns(self):
        text = GOOD.replace("20 of them", "{{your number}} of them")
        _, warnings = slides.check(slides.parse(text))
        self.assertTrue(any("placeholders" in w for w in warnings))

    def test_empty(self):
        problems, _ = slides.check([])
        self.assertTrue(problems)

    def test_html_has_sizes_numbers_and_escapes(self):
        s = slides.parse(GOOD.replace("Why it matters", "Why <it> matters"))
        out = slides.render_html(s, handle="@cafe", ratio="3:4")
        self.assertIn("1080px", out)
        self.assertIn("1440px", out)
        self.assertIn("3/3", out)
        self.assertIn("@cafe", out)
        self.assertIn("&lt;it&gt;", out)
        self.assertEqual(out.count("<section>"), 3)

    def test_cost_fits(self):
        r = slides.cost(7, 0.04, spent=1.0, cap=5.0)
        self.assertAlmostEqual(r["estimate"], 0.28)
        self.assertTrue(r["fits"])

    def test_cost_over_cap(self):
        r = slides.cost(10, 0.5, spent=1.0, cap=5.0)
        self.assertFalse(r["fits"])
        self.assertAlmostEqual(r["room_left"], 4.0)

    def test_cost_exactly_at_cap_fits(self):
        self.assertTrue(slides.cost(5, 1.0, spent=0.0, cap=5.0)["fits"])

    def test_cli_check_and_cost_exit_codes(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "s.md")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(GOOD)
            buf = io.StringIO()
            with redirect_stdout(buf):
                self.assertEqual(slides.main(["check", path]), 0)
                self.assertEqual(slides.main(["cost", "--images", "200", "--price", "0.05"]), 1)
                out = os.path.join(tmp, "c.html")
                self.assertEqual(slides.main(["html", path, "--out", out]), 0)
            self.assertTrue(os.path.exists(out))


if __name__ == "__main__":
    unittest.main()
