---
name: instagram-plan
description: >-
  Plans the week on Instagram for one business at a time: what to post each day,
  which format, the real angle, when, which stories, and who to engage with. Reads the
  active business from founder-context, so a founder with a cafe and an app gets a
  separate plan for each. Has a local mode for shops, cafes, food trucks and lunch
  subscriptions: busy times, offers, geotags, local hashtags and nearby collabs. Use it
  when the user says "plan my Instagram week", "what should I post", "content calendar
  for my shop", "I have nothing to post", "Instagram schedule for next week", "plan
  posts for my cafe", or before writing any reel, carousel or story without a plan.
  It plans a whole week; for one post, use the post's own skill.
---

# instagram-plan

> Based on ig-plan by Jake Schincariol (MIT). Changed by Aya Taleb: one plan per business from founder-context, a local business mode, real dates and a posting log.

This skill decides what gets made. The other skills in this pack write it. Run it once a
week, on the same day, so the week starts with a plan instead of a blank screen.

It never posts or schedules anything. It writes a plan, and the user runs it.

## Safety first

- Never log in to Instagram, post, schedule or message for the user. It breaks Instagram's
  terms and can get the account restricted. Offer the plan, and point to Instagram's own
  scheduler (or Meta Business Suite) if they want to schedule it themselves.
- If the user shares a password, do not repeat it, store it, or use it. Tell them to change
  it, since it is now in a chat log.

## 1. Find the business and its files

Read `references/business-files.md` and follow it. In short:

- Use the active business from founder-context. If the user names another business, use
  that one and say so in the first line.
- Read from `~/.founder/social/instagram/<slug>/`: `account.md`, `log.md`, the last plan.
- Read `~/.claude/instagram/swipe.md` if it exists. That is the user's own evidence about
  which hooks work in their niche (from Jake's optional ig-viral). It beats the defaults here.

One plan covers one business. If the user asks for "all my businesses", make one plan per
business, each in its own folder. Never mix two brands in one week. Their audiences differ
and a mixed feed confuses both.

### Keep Jake's voice file on the right business

Jake's linked `/ig-reel` and `/ig-caption` read one file, `~/.claude/instagram/voice.md`. It
holds one voice for one account. If it describes another business, every Reel script from
this plan comes out in the wrong voice.

So check its first line, `<!-- business: <slug> -->`. If the file is missing, or the slug is
not the active business:

1. Draft a new `voice.md` from the business file. Use the headings of Jake's template (Who I
   am, What I sound like, My positions, Off limits, Proof I can use, The ask). Fill only
   what the business file says. Leave the rest as `{{fill in}}`, never guessed.
2. Show the user the draft. If a file is already there, say which business it was for and
   that it will be replaced.
3. Write it only after a clear yes. Before overwriting, copy the old file to
   `~/.founder/social/instagram/<old slug>/voice.md`, so switching back is one copy.

If the user says no, go on with the plan and note in the output that voice.md is for
another business.

## 2. Get what happened this week

Posts come from real events, not topics. Ask in one message, and only for what the files
do not already say:

1. What happened this week? A customer moment, a number, a mistake, something new, a
   question people keep asking.
2. Anything to sell or announce? An offer, a launch, a deadline, an event.
3. For a first plan only: the audience's time zone and 5 to 10 accounts worth being seen by.

If the user has nothing, use the business's topics and proof. Never invent an event. A
slot with no real material gets `{{what happened}}` and a question, not a made-up story.

## 3. Get the dates right

Run the date tool. Models get weekdays wrong, and a plan with "Tue Oct 27" on a Monday
looks careless.

```bash
python3 scripts/week.py --start <any date in the week> --log ~/.founder/social/instagram/<slug>/log.md
```

It prints the seven dates, the week id for the file name, and the themes posted in the
last 28 days. Read the whole log too, not only the tool's window.

Do not reuse a recent theme with the same angle. Sometimes a theme has to come back, like
an offer in its deadline week. Then give it a new angle and say why in one line of the plan.
For example: "founding seats again: deadline week, new angle is the last-day countdown".

## 4. Choose the posts

Aim for 3 to 5 feed posts a week. Fewer good posts beat more weak ones, and a solo
founder has to keep this up for months. If the user says they have two hours a week,
plan two posts and say why.

Reels reach people who do not follow the account yet. Carousels go deep with people who
already do, and they get saved and sent. Stories keep followers warm daily. So the default
is at least two Reels, one carousel, and stories most days.

Mix the post types across the week. Never two of the same type back to back.

| type | how often | job |
| --- | --- | --- |
| Proof | 1 a week | something that happened, with a real number. Reel. |
| Teach | 1 to 2 a week | one thing the viewer can do today. Reel or carousel. |
| Opinion | 1 a week | a view some of the audience will disagree with. Reel. |
| Story | 1 a fortnight | a scene with a cost or a turn. Reel. |
| Offer | 1 a fortnight, more in launch weeks | what you sell, said plainly. Carousel or stories. |

For each slot give the theme, the angle from this week's real material, and the format.
An angle is specific. "Lunch" is a topic. "The office that ordered 14 bowls on Tuesday and
what they picked" is a post.

## 5. Local business mode

Turn this on when the business is a place or serves an area: a shop, cafe, salon, studio,
food truck, or a street food lunch subscription. Read the `## Local` block in
`account.md`. If it is missing, ask for it in one message and write it there.

What changes:

- **Time posts to the walk-past hours.** Post 30 to 90 minutes before the busy window, so
  the post is fresh when people decide. A lunch business posts around 10:30, not 19:00.
- **Use slow times on purpose.** Put the offer on the day that needs customers, and say so
  in the plan.
- **Every feed post gets the geotag** from `account.md`, Reels and carousels alike. Local
  search and the map surface tagged posts, so an untagged post is invisible to the people
  closest to you.
- **Up to 5 hashtags, mostly local** (area name, area plus category, city plus category).
  Skip broad tags like #foodtrucks or #food, they describe millions of posts and help no
  one find you. Never more than 5. Check `references/instagram-limits.md`.
- **One collab a week with a nearby business**, office or venue. Name the partner only if
  it is in the file or the user said it. Otherwise write `{{partner}}` and suggest the
  kind of place to ask. A Collab post shows on both accounts' grids.
- **Show the place and the people.** The line, the hands, the street, the regulars (with
  their OK). Faces and real places beat stock-looking flat lays.
- **Stories carry the daily stuff**: today's menu, sold out, the weather, where the truck
  is. Plan a daily story slot at the busy time.

## 6. When to post

Use the audience's time zone, not the user's. For a local business, use the busy times in
the file. For others, use early morning for a work audience and early evening for a
consumer audience, unless Instagram Insights says otherwise.

Say this plainly when it comes up: the hour matters far less than the first two seconds
of the post. If the hooks are weak, moving the time will not fix it.

## 7. The engagement round

Plan 15 to 20 minutes a day, before posting. Build a list of up to 10 accounts:

- **reach**: bigger accounts the audience follows, where an early comment gets seen.
- **peers**: same size and field. They reply and comment back.
- **buyers or partners**: people who could buy, or a nearby business to collab with.
  Comment for a while before any DM, and never pitch in a comment.

Use only accounts the user gave or that are in the files. If there are none, write
`{{account}}` slots and ask for them. Hand the list to `/instagram-comment`.

## 8. Output

Show the plan in this shape, then save it.

```
INSTAGRAM PLAN  ·  <business name>  ·  week <id> (<Mon date> to <Sun date>)
based on: <business file path>, log.md (last 28 days), swipe.md (yes/no)
voice.md: matches <slug> / updated with your yes / still set to <other slug>

MON <date>  engage only (15 min)
TUE <date>  10:30  REEL      PROOF   theme: lunch rush   angle: 14 bowls for one office
            geotag: <place>   tags: #<area>lunch ...   hand to: /ig-reel
WED <date>  stories only + engage
...

STORIES   daily at <time>: <what each day carries>. Plan with /instagram-story.
COLLAB    <partner or {{partner}}>: <the idea in one line>
ENGAGE    reach: ... / peers: ... / buyers or partners: ...
OPEN      <every {{placeholder}} the user must fill, in one list>

Next: say "write Tuesday" and I will hand it to the right skill.
```

Run the plan's wording through the check in `references/before-you-show.md`.

Write it to `~/.founder/social/instagram/<slug>/plan.md`. If an older plan is there, move
it to `plans/<week id>.md` first.

## 9. After the week

When the user says a post went out, append one line to `log.md`:

```
- 2026-10-27 | reel | proof | theme: lunch rush | 14 bowls for one office
```

That line is what stops next week's plan repeating itself.

## Hand-offs

| slot | skill |
| --- | --- |
| Reel | `/ig-reel` (Jake's, linked), then `/ig-caption` |
| Carousel | `/instagram-carousel` |
| Stories | `/instagram-story` |
| Engagement list | `/instagram-comment` |
| Keyword or offer DMs | `/instagram-dm` |
| Old post to reuse | `/instagram-repurpose` |
| Is it working? Monthly | `/instagram-audit` |

Reads: founder-context business file, `account.md`, `log.md`, last `plan.md`,
`~/.claude/instagram/swipe.md`, `~/.claude/instagram/voice.md`. Writes: `plan.md`, `plans/`,
`log.md`, `account.md` (local block), and `~/.claude/instagram/voice.md` with the user's yes. Next: the skill for the first slot.
