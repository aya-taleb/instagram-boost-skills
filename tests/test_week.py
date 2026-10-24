import datetime as dt
import io
import os
import sys
import unittest
from contextlib import redirect_stdout

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _load import load  # noqa: E402

week = load("instagram-plan", "week.py")

LOG = """# log
- 2026-10-12 | reel | proof | theme: lunch rush | line out the door
- 2026-10-20 | carousel | teach | theme: Menu | how to order
- 2026-10-21 | reel | offer | theme: menu | founding seats
- not a log line
- 2026-13-40 | reel | bad date
- 2026-10-27 | reel | proof | theme: future | inside the week, not before it
"""


class WeekTests(unittest.TestCase):
    def test_week_of_returns_monday_to_sunday(self):
        days = week.week_of(dt.date(2026, 10, 29))
        self.assertEqual(days[0], dt.date(2026, 10, 26))
        self.assertEqual(days[-1], dt.date(2026, 11, 1))
        self.assertEqual(days[0].weekday(), 0)

    def test_next_monday_from_a_monday_is_a_week_later(self):
        self.assertEqual(week.next_monday(dt.date(2026, 10, 26)), dt.date(2026, 11, 2))
        self.assertEqual(week.next_monday(dt.date(2026, 10, 23)), dt.date(2026, 10, 26))

    def test_parse_log_skips_bad_lines(self):
        entries = week.parse_log(LOG)
        self.assertEqual(len(entries), 4)
        self.assertEqual(entries[0]["theme"], "lunch rush")
        self.assertEqual(entries[0]["format"], "reel")
        self.assertEqual(entries[0]["angle"], "line out the door")

    def test_build_lists_recent_and_repeat_themes(self):
        data = week.build(dt.date(2026, 10, 26), LOG, 14)
        self.assertEqual(data["week_id"], "2026-W44")
        dates = [e["date"] for e in data["recent"]]
        self.assertIn("2026-10-12", dates)
        self.assertNotIn("2026-10-27", dates)
        self.assertEqual(data["repeat_themes"], ["lunch rush", "menu"])

    def test_lookback_window(self):
        data = week.build(dt.date(2026, 10, 26), LOG, 7)
        self.assertEqual([e["date"] for e in data["recent"]], ["2026-10-20", "2026-10-21"])

    def test_cli_prints_week(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = week.main(["--start", "2026-10-28"])
        self.assertEqual(code, 0)
        self.assertIn("2026-W44", buf.getvalue())
        self.assertIn("MON  2026-10-26", buf.getvalue())

    def test_cli_rejects_bad_date(self):
        err = io.StringIO()
        from contextlib import redirect_stderr
        with redirect_stderr(err):
            self.assertEqual(week.main(["--start", "26/10/2026"]), 2)


if __name__ == "__main__":
    unittest.main()
