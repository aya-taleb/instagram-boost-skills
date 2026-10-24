import csv
import datetime as dt
import io
import os
import sys
import tempfile
import unittest
from unittest import mock
from contextlib import redirect_stdout

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _load import load  # noqa: E402

leads = load("instagram-dm", "leads.py")

HEADER = "business_slug,name,company,role,email,linkedin_url,instagram_handle,website,city,source,source_url,fit_score,fit_reason,status,last_contact,notes"
CSV_TEXT = HEADER + """
curbside-lunch-club,Sam Lee,Westlake Tech,Office manager,,,@samcoffee,,Seattle,instagram,https://example.com/a,82,runs office catering,new,,commented LUNCH on our reel
curbside-lunch-club,Ana Ruiz,,Food blogger,,,https://www.instagram.com/ana.eats/?hl=en,,Seattle,instagram,https://example.com/b,91,food blogger in SLU,new,,
curbside-lunch-club,Old Lead,,,,,@old,,,manual,,95,,do-not-contact,,
curbside-lunch-club,No Handle,,,,,,,,manual,,70,,new,,
rankwise,Other Biz,,,,,@other,,,manual,,99,,new,,
curbside-lunch-club,Low Fit,,,,,@low,,,manual,,30,,new,,
curbside-lunch-club,Replied,,,,,@rep,,,manual,,88,,replied,2026-10-01,
"""


def rows():
    reader = csv.DictReader(io.StringIO(CSV_TEXT))
    return list(reader), reader.fieldnames


class LeadsTests(unittest.TestCase):
    def test_header_matches_shared_layout(self):
        _, header = rows()
        self.assertEqual(header, leads.COLUMNS)
        self.assertEqual(leads.missing_columns(header), [])
        self.assertEqual(leads.missing_columns(["name", "email"]), ["business_slug", "instagram_handle", "status"])

    def test_clean_handle(self):
        self.assertEqual(leads.clean_handle("https://www.instagram.com/ana.eats/?hl=en"), "@ana.eats")
        self.assertEqual(leads.clean_handle("sam"), "@sam")
        self.assertEqual(leads.clean_handle("  "), "")

    def test_pick_filters_business_status_and_fit(self):
        r, _ = rows()
        chosen, skipped = leads.pick(r, "curbside-lunch-club", top=5, min_fit=50)
        self.assertEqual([c["handle"] for c in chosen], ["@ana.eats", "@samcoffee"])
        self.assertEqual(chosen[1]["trigger"], "commented LUNCH on our reel")
        reasons = dict(skipped)
        self.assertIn("do-not-contact", reasons["Old Lead"])
        self.assertIn("replied", reasons["Replied"])
        self.assertEqual(reasons["No Handle"], "no instagram_handle")
        self.assertEqual(reasons["Other Biz"], "for another business")
        self.assertIn("below", reasons["Low Fit"])

    def test_pick_other_business_and_top(self):
        r, _ = rows()
        chosen, _ = leads.pick(r, "rankwise", top=1)
        self.assertEqual([c["handle"] for c in chosen], ["@other"])

    def test_mark_sent_finds_row(self):
        r, _ = rows()
        row = leads.mark_sent(r, "curbside-lunch-club", "samcoffee", "2026-10-23")
        self.assertEqual(row["name"], "Sam Lee")
        self.assertIsNone(leads.mark_sent(r, "rankwise", "@samcoffee", "2026-10-23"))

    def test_due_follow_ups(self):
        log = [
            {"handle": "@a", "sent": "2026-10-10", "follow_up_1": "", "follow_up_2": "", "replied": ""},
            {"handle": "@b", "sent": "2026-10-10", "follow_up_1": "2026-10-14", "follow_up_2": "", "replied": ""},
            {"handle": "@c", "sent": "2026-10-10", "follow_up_1": "", "follow_up_2": "", "replied": "yes"},
            {"handle": "@d", "sent": "2026-10-22", "follow_up_1": "", "follow_up_2": "", "replied": ""},
            {"handle": "@e", "sent": "bad", "follow_up_1": "", "follow_up_2": "", "replied": ""},
        ]
        items = leads.due(log, dt.date(2026, 10, 23))
        self.assertIn(("@a", "follow-up 1: add something new", "2026-10-14"), items)
        self.assertIn(("@b", "follow-up 2: close the loop", "2026-10-20"), items)
        self.assertEqual(len(items), 2)

    def test_cli_pick_sent_and_bad_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "leads.csv")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(CSV_TEXT)
            buf = io.StringIO()
            with redirect_stdout(buf):
                self.assertEqual(leads.main(["pick", path, "--business", "curbside-lunch-club"]), 0)
                self.assertEqual(leads.main(["sent", path, "--business", "curbside-lunch-club", "--handle", "@samcoffee", "--date", "2026-10-23"]), 0)
                self.assertEqual(leads.main(["pick", os.path.join(tmp, "nope.csv"), "--business", "x"]), 2)
                bad = os.path.join(tmp, "bad.csv")
                with open(bad, "w", encoding="utf-8") as fh:
                    fh.write("name,email\nA,a@x.com\n")
                self.assertEqual(leads.main(["pick", bad, "--business", "x"]), 2)
            out = buf.getvalue()
            self.assertIn("status new -> contacted, last_contact (empty) -> 2026-10-23", out)
            self.assertIn("is missing: business_slug, instagram_handle, status", out)

    def test_cli_log_then_due(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "sub", "dm-log.csv")
            buf = io.StringIO()
            with redirect_stdout(buf):
                self.assertEqual(leads.main(["log", path, "--handle", "sam", "--kind", "warm", "--sent", "2026-10-01"]), 0)
                self.assertEqual(leads.main(["due", path, "--today", "2026-10-23"]), 0)
            self.assertIn("@sam  follow-up 1", buf.getvalue())

    def test_founder_path_goes_to_founder_home(self):
        with tempfile.TemporaryDirectory() as tmp, mock.patch.dict(os.environ, {"FOUNDER_HOME": tmp}):
            with redirect_stdout(io.StringIO()):
                self.assertEqual(leads.main(["log", "~/.founder/social/instagram/cafe/dm-log.csv",
                                             "--handle", "sam", "--kind", "warm", "--sent", "2026-10-01"]), 0)
            self.assertTrue(os.path.isfile(os.path.join(tmp, "social", "instagram", "cafe", "dm-log.csv")))


if __name__ == "__main__":
    unittest.main()
