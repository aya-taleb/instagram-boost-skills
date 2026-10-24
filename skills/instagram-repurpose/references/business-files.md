# Business files: where to read and where to write

Every skill in this pack works for one business at a time, the active one. This page says
how to find it and where its Instagram files live.

## 1. Find the active business

Read in this order. The first one that exists wins.

1. `founder/context.md` in the current project.
2. `~/.founder/active` holds a slug, for example `curbside-lunch-club`. Read
   `~/.founder/businesses/<slug>.md`.
3. Nothing found: run `/founder-context` if it is installed. If not, ask the user for
   these in one message: business name, what it sells and to whom, three themes, tone in
   three words, words to avoid, proof they can use, topics that are off limits.

The business file holds: name, one-line pitch, who it serves, stage, goals, topics, tone
(3 words plus words to avoid), proof, off-limits topics. Use it as written. Never fill a
gap with a guess. A missing number becomes `{{your number}}`.

If the user names a business that is not the active one ("plan for my cafe, not the app"),
use that business's file and say which one you used in the first line of the output.

## 2. The Instagram folder for that business

`~/.founder/social/instagram/<business-slug>/`

| file | written by | what it holds |
| --- | --- | --- |
| `account.md` | instagram-profile, or instagram-plan on first run | handle, audience, time zone, best times, and the local block below |
| `plan.md` | instagram-plan | this week's plan. Older weeks move to `plans/YYYY-Www.md` |
| `log.md` | any skill, when the user says "posted" | one line per post: `- YYYY-MM-DD \| format \| type \| theme: x \| angle` |
| `carousels/<date>-<slug>/` | instagram-carousel | slides.md, caption.md, prompts.md, images/ |
| `stories/<date>.md` | instagram-story | the frame list for that day |
| `dm-log.csv` | instagram-dm | who was messaged, when, follow-ups |
| `replies.md` | instagram-reply | saved reply patterns the user approved |
| `audits/YYYY-MM-DD.md` | instagram-audit | the audit and its scorecard |
| `repurpose/<date>-<slug>.md` | instagram-repurpose | the source and what came out of it |

Create the folder when you first write to it. Never write into another business's folder.

## 3. The local block in account.md

Fill this only for a business people visit or that delivers nearby: a shop, cafe, food
truck, studio, or a street food lunch subscription. Ask for each line. Do not guess.

```
## Local
area: neighborhood and city
address or pickup point:
geotag: the exact place name to tag on Instagram
hours:
busy times: when people walk past or order (e.g. 11:30 to 13:00 weekdays)
slow times: when you want more people
offers running: what, until when
nearby partners: businesses, offices or venues you could collab with
local hashtags: up to 5 that people near you search (area name, area plus food, etc.)
```

## 4. Jake's linked skills

ig-reel and ig-caption (linked) read `~/.claude/instagram/voice.md` and log to
`~/.claude/instagram/log.md`. They know one account only, so instagram-plan keeps
`voice.md` matched to the active business (with the user's yes). Its first line says which
business it is for. If the voice file is for another business, say so before handing off.
Read `~/.claude/instagram/swipe.md` as evidence when it exists.
