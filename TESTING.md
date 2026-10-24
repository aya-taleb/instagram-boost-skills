# Testing

**Read this first.** Every score here comes from my own grading of runs I did myself. No
subagent tool was available in the build session, so I could not hand runs to a fresh
assistant that saw only the skill and the prompt. For each case I followed the SKILL.md by
hand, saved the output, and then graded it in a separate pass, one statement at a time. The
baseline runs were me following Jake's file the same way. I wrote our skills and the graders,
so expect some bias in our favor. Aya can rerun every case with `claude plugin eval` to check.

Run outputs and grade notes: `/home/claude/build/_work/instagram-boost-skills/<skill>/`
(round-0-baseline, round-0-ours, round-1, ... and grades.md).

Rubric: TEST-PROTOCOL.md section 2 (graders 40, own rules 15, nothing made up 15, tone 10,
handoff 10, trigger fit 10). Trigger fit is my read of the 12 prompts in each
`evals/triggers.json` against the description, not a live trigger test. So I never gave it
10/10 in a final score.

| skill | status | baseline | final | rounds | beats baseline? |
| --- | --- | --- | --- | --- | --- |
| instagram-plan | reworked | 55 (Jake ig-plan) | 98 | 3 | yes |
| instagram-carousel | reworked | 61 (Jake ig-carousel) | 98 | 1 | yes |
| instagram-dm | reworked | 72 (Jake ig-dm) | 99 | 3 | yes |
| instagram-story | rewritten | 62 (Jake ig-story) | 98 | 1 | yes |
| instagram-profile | rewritten | 76 (Jake ig-profile) | 98 | 1 | yes |
| instagram-comment | rewritten | 72 (Jake ig-comment) | 99 | 2 | yes |
| instagram-reply | rewritten | 68 (Jake ig-reply) | 99 | 1 | yes |
| instagram-repurpose | rewritten | 74 (Jake ig-repurpose) | 99 | 1 | yes |
| instagram-audit | rewritten | 69 (Jake ig-audit) | 98 | 1 | yes |

Linked skills (ig-reel, ig-caption): read-through check only, see the end.

## Where the gap to Jake really comes from

Be careful reading the table. Much of the gap comes from things our test cases ask for that
his pack was never built to do: a business file, several businesses, a local mode, a leads
CSV, the saved file paths. His skills are strong on craft. On craft alone (hooks, slide
rules, comment quality, the story shape) his versions and ours score close. Our clear wins
on the same footing are: nothing invented (his runs made up details in 7 of 9 skills), tools
that count and compute instead of guessing, and refusals for fake proof and copying.

## Per skill

### instagram-plan  (reworked)
baseline: 55 (Jake's ig-plan, same 3 cases)
round 0 ours: 86
final: 98 after 3 rounds. Stopped because the score was 95+ and the last round gained under 5.
rounds:
- r1: 97, safety section (passwords, no login), geotag on every feed post, no broad hashtags,
  log window 14 to 28 days in week.py, returning themes need a reason and a new angle.
- r2: 98, description says it plans a whole week, and a single post goes to its own skill.
- r3: 98, orchestrator follow-up: keeps Jake's `~/.claude/instagram/voice.md` matched to the
  active business (draft shown, written only with a yes, old file saved). New grader passes.
open issues: none.

### instagram-carousel  (reworked)
baseline: 61 (Jake's ig-carousel)
round 0 ours: 94
final: 98 after 1 round. Stopped because the score was 95+ and the last round gained under 5.
rounds:
- r1: 98, limits quoted to the user with their checked date; description names what it is
  not for (LinkedIn carousels, single images).
open issues: the AI image route was tested only up to the cost check and the yes. I did not
run generate-images, since it is a paid call and not installed here.

### instagram-dm  (reworked)
baseline: 72 (Jake's ig-dm)
round 0 ours: 94
final: 99 after 3 rounds. Stopped because the score was 95+ and the last round gained under 5.
rounds:
- r1: 99, dates, prices and quantities the user did not give become placeholders in pitches.
- r2: 99, description says private messages only (comment replies and captions go elsewhere).
- r3: 99, orchestrator follow-up: leads.py reads the shared leads.csv layout (CONVENTIONS
  section 5) and suggests the status and last_contact update after sending. New grader passes.
open issues: none.

### instagram-story  (rewritten)
baseline: 62 (Jake's ig-story)
round 0 ours: 95
final: 98 after 1 round. Stopped because the score was 95+ and the last round gained under 5.
rounds:
- r1: 98, shared reference: refusals give a plain reason and no legal cites from memory.
open issues: none.

### instagram-profile  (rewritten)
baseline: 76 (Jake's ig-profile with his rubric)
round 0 ours: 92
final: 98 after 1 round. Stopped early, see "Calls I made".
rounds:
- r1: 98, run bio.py on every option shown, even in a refusal; no new facts worked out
  from the file ("3 years" stays "3 years").
open issues: Jake's 12-part score out of 100 is something users may like. Ours gives a
3 question test instead, on purpose. Aya may want a numeric score too.

### instagram-comment  (rewritten)
baseline: 72 (Jake's ig-comment)
round 0 ours: 90
final: 99 after 2 rounds. Stopped because the score was 95+ and the last round gained under 5.
rounds:
- r1: 98, first-person stories need a source in the file or from the user; keep the
  business's timeline true (no "serving now" before launch).
- r2: 99, show the final comment only, not drafts.
open issues: none.

### instagram-reply  (rewritten)
baseline: 68 (Jake's ig-reply)
round 0 ours: 89
final: 99 after 1 round. Stopped early, see "Calls I made".
rounds:
- r1: 99, guesses stay out of reply text even when flagged in a note.
open issues: Jake's "reply to a question with a Reel" move is good. Ours sends repeat
questions to instagram-plan instead. Worth a second look.

### instagram-repurpose  (rewritten)
baseline: 74 (Jake's ig-repurpose)
round 0 ours: 98
final: 99 after 1 round. Stopped because the score was 95+ and the last round gained under 5.
rounds:
- r1: 99, a keyword ask must say what it sends and hand off to instagram-dm.
open issues: the test sources are short (330 words, 2:40 of talk). A 40 minute transcript
would test the "pick ideas, not paragraphs" part harder. Add one.

### instagram-audit  (rewritten)
baseline: 69 (Jake's ig-audit)
round 0 ours: 95
final: 98 after 1 round. Stopped because the score was 95+ and the last round gained under 5.
rounds:
- r1: 98, insights.py prints the median rate per post; every keep and stop carries its
  number, or it moves to try. While testing I also found and fixed a bug where top and
  bottom lists overlapped on small samples (unit test added).
open issues: Jake's audit asks for hold at 3 seconds and non-follower share. Ours uses them
only if the export has them. A user with screenshots of retention gets less from ours.

## Linked skills, read-through check

- **ig-reel**: reads `~/.claude/instagram/voice.md` and `swipe.md`, logs to
  `~/.claude/instagram/log.md`. One account only. Fine to use per business if the user
  points voice.md at the active business. No safety concerns found.
- **ig-caption**: caption linter enforces 5 hashtags and the 125 character cut. Matches our
  dated limits. Good.
- **ig-viral**: no longer linked. It drives the user's own logged-in browser to read reels and
  uses yt-dlp, which breaks our no-scraping and no-download rules. The README names it as
  optional. See BUILD-NOTES.md.

## Calls I made

- No subagent tool was available, so all runs and grades are mine. Said at the top.
- Round numbering: "round 0" holds both the baseline and our first version. Rounds 1 and up
  are changes.
- instagram-profile and instagram-reply: round 1 gained more than 5 points (to 98 and 99).
  The rule allowed another round. I looked for a change worth making, found none, and
  stopped. For reply, only 1 point was left to gain at all.
- Where a change only touched the description, I did not rewrite outputs that stayed the
  same. The round folders say so.
- Fictional test businesses (Plotline, Curbside Lunch Club, Corner Loaf) stand in for an
  app, a lunch subscription and a shop.
- Hashtag cap: I wrote "5, rolling out since Dec 2025; some accounts still allow 30; plan
  for 5". Sources disagree in 2026, so I did not state 5 as a hard rule for everyone.
- humanize was not built yet, so every run used the hand check in `before-you-show.md`.

## Independent review (blind)

Run by an independent reviewer on 2026-10-23, following `REVIEW-PROTOCOL.md`. Each case was
run twice in fresh `claude -p` sessions with their own HOME: once with our skill plus the
synced founder-context and humanize, once with Jake's SKILL.md (text only, no scripts) plus
his ig-human SKILL.md. Jake's runs got a `~/.claude/instagram/voice.md` built from the same
fictional business file the case uses. Both sides got a one-line note naming the skill to
use. A separate `claude -p` judge saw the prompt, the input files, the expected outcome and
both outputs as A and B in random order, with skill names masked. Scores are out of 50
(five criteria, 0 to 10 each). Runs, packets, keys and verdicts:
`/home/claude/build/_work/review/instagram/`.

| skill | case | winner | ours score | baseline score | fix rounds | one-line reason |
| --- | --- | --- | --- | --- | --- | --- |
| instagram-plan | app-week-plotline | ours | 41 | 35 | 0 | Saved plan, right dates and time zones, sized to 3 hours, clear hand-offs; Jake's script invented Dana's story. |
| instagram-plan | local-week-curbside | ours | 41 | 31 | 0 | Geotag, local hashtags, Monday slow lunch used, Nov 15 is a Sunday caught; Jake had no geotag or tags and no real collab. |
| instagram-carousel | app-carousel-plotline | ours | 43 | 32 | 0 | Full 10-slide deck with alt text, caption and built files; Jake stopped at draft copy with cover alt text only. |
| instagram-carousel | local-ai-images-curbside | ours | 36 | 31 | 0 | Ours showed the cost and cap and waited for a yes and suggested real photos; Jake never raised cost. Both added unsupported lines. |
| instagram-dm | app-leads-plotline | ours | 43 | 39 | 3 (rerun after fixes) | Same lead picks; ours used placeholders, Jake invented the resource's how-to line. Ours offered the leads.csv update. |
| instagram-dm | local-collab-cornerloaf | ours | 41 | 36 | 3 | Lost r0 to r2 (35/41, 41/40, 39/40); won r3 after the pitch got a named format, a concrete "what they get" and one specific ask. |
| instagram-story | app-launch-story-plotline | ours | 44 | 32 | 0 | Face open, one reply sticker, one ask with {{link}}, Highlight and save path; Jake invented a method and had no placeholder. |
| instagram-story | local-daily-curbside | ours | 43 | 35 | 0 | Timed before lunch, Denny Park sticker, Seoul Bowl tagged only with OK, one ask; Jake had two asks and no timing. |
| instagram-profile | app-bio-plotline | ours | 43 | 33 | 0 | Real 3 second test, three counted bios, link plan, reach caveat; Jake gave one bio and a long rubric score. |
| instagram-profile | local-profile-cornerloaf | ours | 43 | 39 | 0 | Three bios naming who it serves, Order button, hours in contact fields, address placeholder. |
| instagram-comment | app-round-plotline | ours | 43 | 37 | 0 | Skipped the grieving author and the competitor with reasons; Jake drafted a comment for the grief post. |
| instagram-comment | local-neighbors-curbside | ours | 41 | 35 | 0 | Neighborly and honest about pre-launch; Jake opened by criticizing the post and stated an unsupported fact. |
| instagram-reply | app-replies-plotline | ours | 42 | 36 | 0 | Stuck to the file ($8/month, no trial claim), grouped and routed to DM; Jake invented a trial and "60k words". Both missed the Mac and iPad line. |
| instagram-reply | edge-injection-and-argue | ours | 41 | 38 | 0 | Both ignored the injection; ours gave one calm reply, Jake's options leaned toward the savage tone asked for. |
| instagram-repurpose | app-newsletter-plotline | ours | 45 | 33 | 0 | Four briefs with source part, exact quote, next skill, skipped list and save path; Jake invented details and had no quotes. |
| instagram-repurpose | local-talk-transcript-curbside | ours | 42 | 33 | 0 | Briefs with timestamps, exact quotes and the exact offer; Jake stopped at an outline. Ours skipped the founding-seats carousel. |
| instagram-audit | app-audit-plotline | ours | 42 | 37 | 0 | Per-100-reach numbers match the CSV, trend reel called out, missing signups asked for, scorecard from data only. |
| instagram-audit | local-small-sample-cornerloaf | ours | 43 | 36 | 0 | Flagged the small sample, tied tries to the 12:30 slow window and Nov 1 preorders, asked whether posts led to visits. |

Result: 18 of 18 cases won after fixes (17 at round 0, 1 after 3 fix rounds on instagram-dm).

What changed (instagram-dm, `SKILL.md` sections 7 and 8 only):
- r1: keep the first ask small, never commit the user to money, discounts, stock or staff
  time; write both follow-ups out in full with dates. Still lost narrowly (41 to 40).
- r2: "what they get" must be specific to them (who they reach plus one small thing the user
  can give, flagged to confirm). Still lost narrowly (39 to 40).
- r3: name the format of the idea and end with one specific ask, not a menu. Won 41 to 36.
  Both dm cases were rerun after each change; app-leads-plotline won every time.
- validate.py and the 42 unit tests passed after each change.

Read these numbers with care:
- One judge per case. Jake's unchanged collab output scored 41, 40, 40 and 36 across four
  judges, so a gap of 1 or 2 points is noise. Most wins here are 4 to 12 points.
- The expected outcomes were written for our skills (tool names, save paths). The judge was
  told to credit substance over exact tools, but some lean toward ours is likely.
- Jake's runs could not run his ig-human scripts (we never run upstream code), so his drafts
  got a hand check only. Ours ran humanize.
- Some runs could not save files because `mkdir` through Bash needed an approval the
  harness could not give. This hit both sides and is a harness limit, not a skill bug.
- Weak spots still open: the carousel AI-image case scored low on both sides (ours 36) and
  ours added copy lines the file does not support. The reply skill left the iPad question as
  a placeholder though the file says users are on Mac and iPad. The repurpose transcript run
  skipped the founding-seats carousel the case expected.
