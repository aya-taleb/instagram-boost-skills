---
name: instagram-story
description: >-
  Plans Instagram stories for the active business, frame by frame: what to shoot, the
  short text on screen, the sticker that gets replies, the one ask, and what to save to a
  Highlight. Built for a few minutes a day, and for local businesses whose stories carry
  the daily news (today's menu, sold out, where the truck is, last day of an offer). Use
  it when the user says "what should I put on my story", "plan my stories", "story ideas
  for today", "stories for the launch", "a poll for my story", "countdown story", or the
  week's plan has a story slot. Not for Reels or feed posts.
---

# instagram-story

Stories are where followers decide if they still care. Feed posts and Reels find new
people. Stories keep the people you have, and replies to a story land in DMs, which is
where sales start. So a good story day is short, real, and asks for one small reply.

This skill writes the frames. The user shoots and posts them. Never post, schedule or log
in for them.

## 1. Read first

Follow `references/business-files.md`: the active business, its tone and proof, and
`account.md` (for a local business, the `## Local` block). Read this week's `plan.md` for
the story slot and the day's feed post. Ask one question if you need it: "What is actually
happening today?" Real material beats ideas. If nothing is happening, use the business's
topics and say the frames are evergreen.

## 2. Shape of a story day

3 to 7 frames. Past 7, people tap through without reading.

Each day has one job. Pick it first:

| job | when | ends with |
| --- | --- | --- |
| news | something changed today (menu, stock, hours, location) | where and when |
| push the post | a new Reel or carousel went up | share the post, then a reply sticker |
| behind the scenes | a normal day | a question or poll |
| offer | an offer with a real end date | countdown or link, once |
| ask the audience | you need to learn something | poll or question box |

Then build the frames in this order:

1. **Open with motion or a face.** The first frame decides if they stay. A hand doing the
   work, the street, the founder talking. Not a text card.
2. **Middle frames carry one thing each.** One fact, one shot, one line of text.
3. **One frame invites a reply**: poll, question box, quiz, emoji slider. Replies open a DM
   thread, and they tell you what people want. Pick the sticker that fits the question,
   and write its exact text.
4. **One ask per day.** A link, a keyword to DM, "come by". Not three.

## 3. Text on screen

- Up to about 10 words per frame. People read stories at a glance.
- Keep text and stickers inside the safe zone. Stay clear of the top and bottom 250 px of
  the 1080x1920 frame, where Instagram puts its own buttons. (Checked Oct 2026, see
  `references/instagram-limits.md`.)
- Turn on captions for any talking frame. Many people watch with the sound off.
- A link sticker only with a link the user gave. Otherwise write `{{link}}`.

## 4. Local business mode

For a shop, cafe, truck, studio or lunch subscription:

- **Post at the decision time**, from the busy times in `account.md`. A lunch business posts
  its story before people leave their desks, not after.
- **Daily news first**: today's menu, what sold out, the weather, the line, where we are.
  These are the stories people check for.
- **Add the location sticker** with the geotag from `account.md`, so people nearby find it.
- **Tag partners** (a truck, the shop next door) only with their OK. They can reshare it.
- **Show the place and the people.** Faces of staff or regulars only with their consent.

## 5. Offers and launches

A countdown sticker works for a real deadline. People can tap to get a reminder. Use it once
a day at most, and never for a fake deadline. Say the real end date in words too.

For a launch week, plan one frame a day that moves the countdown, and one that shows proof
from the file. No proof in the file means no proof frame. Use a question box instead.

## 6. Highlights

Say which frames to save, and to which Highlight. Highlights stay on the profile after 24
hours, so they act as the "start here" for new visitors. Good ones for most businesses:
how it works, menu or product, reviews (real ones only, with permission), find us, FAQ.
`/instagram-profile` sets their names and order.

## 7. Output

```
STORIES  ·  <business>  ·  <weekday, date>  ·  job: <news / push / bts / offer / ask>
post at: <time and why>

1  SHOOT  hands folding tacos at the Taco Ruta window, 3 seconds
   TEXT   "Wednesday at Denny Park"
2  SHOOT  ...
   TEXT   ...
3  STICKER poll: "Where do you eat lunch most?"  options: "At my desk" / "Outside"
4  ASK    "DM SEAT for a founding seat"   (the day's one ask)

location sticker: <geotag>      tag: <partner, if they agreed>
save to Highlight: frames 1, 4 -> "How it works"
open: <any {{placeholder}}>
```

Run the text through `references/before-you-show.md`.

Save to `~/.founder/social/instagram/<slug>/stories/<YYYY-MM-DD>.md`.

Reads: business file, `account.md`, `plan.md`. Writes: `stories/`. Next: `/instagram-dm` for
the replies that come in, `/instagram-reply` for comments, `/instagram-profile` for Highlights.
