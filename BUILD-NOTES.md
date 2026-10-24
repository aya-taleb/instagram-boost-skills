# Build notes

Built 2026-10-23, unattended. Nothing was pushed to GitHub.

## Status

- 9 skills built with evals (3 cases each plus triggers.json): 3 reworked, 6 rewritten.
- 2 linked skills listed in skills.json (ig-reel, ig-caption), installed with
  `python3 scripts/get_linked.py`. Jake's ig-viral is not linked (see below).
- 5 synced skills listed in skills.json, not copied yet: generate-images, transcribe,
  talking-head-cards (multimedia-skills), humanize, founder-context (entrepreneur-skills).
  Their folders appear after the sync step.
- `python3 scripts/validate.py`: clean.
- `python3 -I -m unittest discover -s tests`: 42 tests pass.
- Tools (standard library, no network): week.py (plan), slides.py (carousel), leads.py (dm),
  bio.py (profile), insights.py (audit).

## Unfinished

- Scores are self-run and self-graded. No subagent was available. Rerun the evals with
  `claude plugin eval` before launch to get independent numbers.
- Trigger fit was judged by reading, not tested live.
- The generate-images hand-off is untested end to end. It assumes generate-images gives a
  live price per image and accepts a list of prompts. Check that against the real skill once
  multimedia-skills is built.
- humanize and founder-context did not exist yet. Skills fall back to a hand check
  (`references/before-you-show.md`) and a one-message interview. Recheck the hand-off
  wording once those skills exist.
- The three shared reference files (business-files.md, before-you-show.md,
  instagram-limits.md) are copied into every skill folder, so each skill works when installed
  alone. If one changes, copy it to all 9. A small sync script would help.

## Aya to decide

1. **ig-viral.** Removed from the linked skills, because it reads Instagram through the user's
   logged-in browser and downloads with yt-dlp (against CONVENTIONS section 8). The README
   names it as optional. Keep it unlinked (current state), or link it with the warning?

## Decided (orchestrator, 2026-10-23)

- instagram-plan writes Jake's `~/.claude/instagram/voice.md` from the active business, after
  showing the draft and getting a yes. The old file is saved under the old business's folder.
- Keep "plan for 5 hashtags".
- Keep the three-question profile test (no numeric score).
- instagram-dm reads the shared sales/leads.csv layout from CONVENTIONS section 5. It uses
  `notes` for the trigger, since the layout has no trigger column.

## Calls to review

- Curbside Lunch Club in the evals is modeled on Curbside Lunch Club (SLU, trucks, founding
  seats) but uses only made-up details.
- Stories and plans default to "post 30 to 90 minutes before the busy window" for local
  businesses. That is a judgment call, not a sourced number. The skill says to check
  Insights.
- I left Jake's "reply to a comment with a Reel" idea out of instagram-reply, to keep the
  rewrite clean of his structure. It is a good idea. Adding it in our own words is fine.

## Fix round after review

- User data moved out of `~/.claude` (protected by Claude Code) to `~/.founder`: business files, social folders and the media ledger. Tools honor `FOUNDER_HOME`; tests use a temp one.
- `leads.py` and `week.py` map a `~/.founder/...` path onto `FOUNDER_HOME` when set (test added).
- Jake's linked files (`~/.claude/instagram/voice.md`, `log.md`, `swipe.md`) stay where his skills read them.
