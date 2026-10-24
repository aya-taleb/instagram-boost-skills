---
name: instagram-repurpose
description: >-
  Turns something the user already made (a blog post, newsletter, LinkedIn post,
  podcast, talk, their own video, or an old Instagram post) into 2 to 5 Instagram pieces
  for the active business: picks the ideas worth posting, chooses Reel, carousel, stories
  or a single image for each, and writes a ready brief for the skill that makes it. Works
  from text or files the user owns; for audio or video it uses the transcribe skill. Use it
  when the user says "turn this into Instagram posts", "repurpose my blog for IG", "make
  reels from my podcast", "reuse my LinkedIn post on Instagram", "I wrote a newsletter, what
  can I post from it", or "recycle my best old posts".
---

# instagram-repurpose

Most founders already have more material than they post. A newsletter, a talk, a long
LinkedIn post. The work is picking the ideas inside it and reshaping each for how people
use Instagram: fast, visual, on a phone.

This skill picks and shapes. It does not post. And it only works on material the user owns
or made.

## 1. Get the source

Ask for the source as text, a file, or a link to a page the user owns. Then:

- **Text or document**: read it.
- **Audio or video the user owns**: run `/transcribe` (multimedia-skills) on the file to get
  a transcript with timestamps. If it is not installed, ask the user for a transcript.
- **A link to YouTube, Instagram, TikTok or similar**: do not download it, even if it is
  theirs. Ask them for the original file or a transcript. Downloading from those platforms
  breaks their terms.
- **Someone else's content**: do not repurpose it as the user's. Offer to write the user's
  own take on the idea, with credit.

Read the active business file (`references/business-files.md`) for tone, proof and
off-limits topics. A newsletter might mention a client the business file says not to name.

## 2. Find what is worth posting

Read the whole source and list its strongest parts. Look for:

- **The one idea** someone would repeat to a friend.
- **Steps or a list**: carousel material.
- **A moment with a turn**: something went wrong, a decision, a surprise. Reel material.
- **A line worth quoting**: word for word from the source, with the timestamp or paragraph.
- **A number or result**: only if it is in the source.
- **A question it raises**: story poll or question box material.

Drop the rest. Most of a long piece is connective tissue that does not survive on its own.

Score each candidate quickly: does it stand alone for someone who never saw the source? Is it
on one of the business's topics? Is it new for this account (check `log.md`)?

Then map every strong moment to its best format before you choose, one line each:
`<moment, with timestamp or paragraph> -> <format> -> <why>`. Use the table in section 3.
A process counts as steps even when the speaker says it in one sentence: how an offer
works, how to sign up, what happens when. Its steps can come from the source plus the
business file, so an offer with a price, a deadline and a pickup point is carousel material.
Keep the best 2 to 5 from the map, mixing formats where the source allows. Every moment you
drop goes in `skipped` with its reason, so the user sees what was left on the table.

## 3. Pick a format per idea

| the idea is | format | made by |
| --- | --- | --- |
| a moment, a face, something seen happening | Reel | `/ig-reel` (Jake's, linked) |
| steps, a framework, a list, a before and after | carousel | `/instagram-carousel` |
| a quick question, a poll, a daily bit | stories | `/instagram-story` |
| a strong quote with a talking-head clip | Reel with cards | `/talking-head-cards` (multimedia) |
| one striking line or image | single image post | `/ig-caption` for the caption |

Do not turn everything into the same format. A week of five carousels from one blog post
reads like a blog post cut up.

## 4. Write the briefs

For each piece, a brief the next skill can run with:

```
PIECE 2  ·  carousel  ·  theme: <topic>
idea:      <one sentence>
from:      <paragraph 4 / 12:40 to 14:05 in the transcript>
hook:      <a first line or cover in 6 words or fewer>
beats:     <the 3 to 7 points, in order>
quote:     "<exact words>" (source, timestamp)
proof:     <only from the source or the business file, else {{your number}}>
ask:       <one>
hand to:   /instagram-carousel
```

Rules for the briefs:

- **Quotes are exact.** Copy the words. If you shorten, use "...". Never polish a quote
  into something the speaker did not say.
- **Credit other people** quoted in the source, by name, and only if the user can use it.
- **Each piece stands alone.** No "as I said in my newsletter" unless the ask is to read it.
- **No new facts.** If the piece needs a number the source does not have, it gets a
  placeholder. A goal in the business file is not a fact to post: "fill 50 seats" is a
  goal, not "50 seats left".
- **A keyword ask says what it sends.** "Comment STUCK and I'll DM you the card method",
  then hand the replies to `/instagram-dm`. A keyword with nothing behind it wastes the
  comment.

## 5. Old Instagram posts

To reuse the user's own old post: keep what worked (the user can share the numbers from
Insights), change the hook and the format, and leave at least a few months between them.
Say what changed and why. Never repost someone else's post.

## 6. Output

```
REPURPOSE  ·  <business>  ·  source: <title, type, length>
worth posting: <n> ideas, kept <k>

PIECE 1 ...
PIECE 2 ...

skipped: <ideas left out and why, one line each>
suggested slots: <which days, from plan.md if there is one>
```

Run hooks and lines through `references/before-you-show.md`.

Save to `~/.founder/social/instagram/<slug>/repurpose/<YYYY-MM-DD>-<short-name>.md`, with the
source path and the transcript path if there was one.

Reads: the source, business file, `log.md`, `plan.md`. Writes: `repurpose/`. Next: the skill
named in each brief, and `/instagram-plan` to place the pieces in the week.
