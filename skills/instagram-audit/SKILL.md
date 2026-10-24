---
name: instagram-audit
description: >-
  Monthly check of what is working on Instagram for the active business, from the user's
  own Insights export: rates by format and theme (not raw totals), top and bottom posts and
  why, whether the account reaches new people and moves them to act, then keep 3, stop 3,
  try 3 tied to the business's goals, and a scorecard to beat next month. Says plainly when
  there is too little data. Use it when the user says "audit my Instagram", "is Instagram
  working for us", "what's working on my IG", "monthly Instagram review", "why is my reach
  down", "here's my Insights export", or before planning next month.
---

# instagram-audit

Most founders look at follower count and likes and guess. Both mislead. A post can get many
likes from people who already follow and never buy. This audit asks two questions instead:
are we reaching new people, and are those people doing something (saving, sending,
visiting the profile, messaging, buying)?

It reads numbers the user exports. It never scrapes, logs in, or guesses numbers.

## 1. Get the numbers

Ask for one of these, in this order of preference:

1. **The Insights export** from Meta Business Suite (Insights, then Content, then Export) as
   CSV, for the last 30 to 90 days. Works for business and creator accounts.
2. **A pasted table**: date, format, reach, likes, comments, shares, saves, follows, profile
   visits. Whatever the user has.
3. **Screenshots** of Insights: read the numbers out, and say which ones you could not read.

Also read `log.md` and old `plan.md` files for the theme of each post, and the business
file for goals (`references/business-files.md`). An audit without goals can only say what
is popular, not what is working.

If the user has no numbers at all, do not invent any. Offer a review you can do now: the
profile (`/instagram-profile`) and the last few captions they paste. Then explain how to
export Insights for next month.

## 2. Run the numbers

```bash
python3 scripts/insights.py export.csv --log ~/.founder/social/instagram/<slug>/log.md
```

For each post it works out shares plus saves per 100 people reached. It groups posts by format
and theme, lists the top and bottom posts, and flags a small sample (under 8 posts). It also
says which columns the export did not have.

Why shares and saves per reach? People send and save a post when it is worth something to
them. Dividing by reach makes a small post and a big post comparable.

## 3. Read it, honestly

Report only what the numbers support:

- **Reaching new people?** Reach compared with follower count, and which formats reach
  furthest. If the export shows followers vs non-followers, use it.
- **Worth something?** Shares plus saves per 100 reached, by format and theme. Which themes
  people keep.
- **Moving people?** Profile visits, follows, link taps, DMs. And, from the user, what
  matters most: seats sold, trial signups, preorders. Ask for those if not given.
- **Top 3 and bottom 3 posts**, with a plain guess at why. Label it a guess: "likely the
  hook", not "because of the hook".

Rules:

- **Small samples are hunches.** With under 8 posts, or one post far ahead of the rest, say
  so and keep the advice light.
- **No made-up benchmarks.** Do not say "a good save rate is 2 percent". Compare the account
  with itself: this month vs last, this format vs that one. If the user wants an industry
  number, it needs a source with a link and a date.
- **Raw totals are context, not findings.** A 10x reach month with no new follows is a
  finding. A 10x reach month alone is not.
- **Reach drops have dull causes first**: fewer posts, fewer Reels, a quiet season, a
  weaker hook. Check those before blaming the algorithm.

## 4. Keep, stop, try

Three of each, tied to the goal in the business file:

- **Keep**: what is working, with the number that says so.
- **Stop**: what costs time and returns little, with its number.
- **Try**: one test per line, with what you will measure next month.

A keep or stop with no number behind it is a hunch. Move it to try. Fewer than three is
fine when the data is thin. Say so instead of filling the slot.

Every number in the scorecard comes from the tool's output or the user. If you work one out
yourself, show the sum.

For a local business, also ask three things. Are posts reaching people nearby (location data
in Insights, if shown)? Did the offer posts lead to visits or orders (ask the user)? Which
collabs helped?

## 5. Scorecard

End with a small table to beat next month, using only numbers from this audit:

```
SCORECARD  ·  <month>
posts            <n>       next month aim: <n>
median reach     <n>
shares+saves/100 <n>
follows          <n>
profile visits   <n>
goal metric      <n or {{from you}}>   (e.g. founding seats sold)
```

## 6. Output and files

```
INSTAGRAM AUDIT  ·  <business>  ·  <date range>  ·  <n> posts
data: <file>, columns missing: <list>
sample: <ok / small, read as hunches>

REACH ...
WORTH ...
MOVING ...
TOP 3 / BOTTOM 3 ...
KEEP / STOP / TRY ...
SCORECARD ...
```

Keep the wording plain; run it through `references/before-you-show.md`.

Save to `~/.founder/social/instagram/<slug>/audits/<YYYY-MM-DD>.md`. Next month, read the last
audit first and compare.

This is a read of the user's own data, not financial advice. If the user is deciding on ad
spend or hiring based on it, say to sanity check the numbers with whoever does their books.

Reads: the export, `log.md`, `plan.md` history, business file, the last audit. Writes:
`audits/`. Next: `/instagram-plan` for next month, `/instagram-profile` if visits do not
become follows.
