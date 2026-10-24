---
name: instagram-profile
description: >-
  Fixes the Instagram profile for the active business so a visitor knows in 3 seconds
  what it is, if it is for them, and what to do next: the name field, bio options counted
  to the 150 character limit, links, Highlights, which posts to pin, and for local
  businesses the address, hours, category and action button. Counts with a small tool,
  never by eye. Use it when the user says "fix my Instagram bio", "rewrite my IG bio",
  "what should my profile say", "my profile gets visits but no follows", "set up the
  Instagram for my new business", "which posts should I pin", or "what Highlights do I
  need". It writes; the user makes the changes in the app.
---

# instagram-profile

Every post that works sends people to the profile. There they decide in a few seconds
whether to follow, tap the link, or leave. So the profile is the page that turns attention
into followers and customers, and it is the cheapest thing on Instagram to fix.

This skill writes the profile. The user edits it in the app. Never log in or change it for
them.

## 1. Read first

Follow `references/business-files.md`. Use the active business file for what it sells, to
whom, tone, proof and off-limits topics. Ask the user to paste the current profile: name
field, username, bio, links, Highlight names, pinned posts. A screenshot works too.

If the user has several businesses, each one gets its own account and profile. Do not mix
them in one bio. Say so if they ask.

## 2. The 3 second test

A visitor should be able to answer three questions from the top of the profile:

1. **What is this?** In plain words, not a slogan.
2. **Is it for me?** Name the who: "for indie authors", "SLU office lunch".
3. **What do I do now?** One next step, which the first link or button delivers.

Score the current profile on these three before rewriting. Quote the line that answers each
one, or say that nothing does.

## 3. The fields

**Name field (30 characters).** It is searchable, the bio is not as much. Put the name plus
the phrase people would search: "Corner Loaf | Ballard Bakery". Use the words people type,
not a tagline.

**Bio (150 characters).** Two to four short lines:

- line 1: what it is and who it is for
- line 2: proof or the reason to believe, only from the business file
- line 3: the next step, pointing at the link or button
- optional: location and hours for a local business, if not in the contact fields

Write 2 or 3 options, each with a different angle (plain, proof-led, offer-led). Count each
with the tool, because models miscount characters:

```bash
python3 scripts/bio.py --file bio-options.txt --name "Corner Loaf | Ballard Bakery" --username cornerloafballard --links 2
```

It fails anything over the limits and warns about URLs in the bio text (they are not
clickable), unprovable claims, and long single lines. Fix every FAIL before showing.

Run it on every option you show, even a quick one in a refusal, and copy its counts into
the output. Never type a count yourself. A 151 character bio gets cut off in the app. And a count
that is off by two makes the user stop trusting the rest.

**Links (up to 5).** The first one shows in full, the rest hide behind "and 2 more". So the
first link is the one next step from the bio. Name each link title in plain words.

**Highlights.** 3 to 6, in the order a new visitor needs them. Short names that fit under
the circle (about 10 to 12 characters show). Common set: Start here or How it works, Menu or
Product, Reviews (real ones, shared with permission), Find us, FAQ. Say which existing stories
should go in each, or hand to `/instagram-story` to make them.

**Pinned posts (up to 3).** Pin what a new visitor should see first: the clearest
explanation of the offer, the best proof, and the post that best shows the people. Pick from
posts the user names, or say which kind of post to make next.

## 4. Local business mode

For a business with a place or a service area (the `## Local` block in `account.md`):

- Use a **professional account** (business or creator) so the contact, address and action
  buttons show. Pick the closest category.
- **Address or service area, hours, and the action button** (order, reserve, book, call,
  directions) that matches how people buy. The button beats a link for a local business.
- Put the neighborhood in the name field or line 1. People search "bakery Ballard".
- Hours belong in the contact fields if there, so the bio has room for something else.

## 5. Never

- Never work out a new fact from the file and present it as given. "Open 3 years" stays
  "3 years", not "since 2023". If the user wants the year, ask.
- Never invent awards, press, follower counts, ratings or customer numbers. A missing proof
  line becomes `{{your proof}}` or is dropped.
- Never promise the bio will grow the account. It turns visits into follows. Reach comes
  from posts.
- Never suggest buying followers, follow-unfollow tactics, or engagement pods. They break
  Instagram's terms and make the numbers useless.

## 6. Output

```
PROFILE  ·  <business>  ·  @username

3 SECOND TEST (now)
  what is it:   <quote or "nothing says it">
  is it for me: ...
  what next:    ...

NAME FIELD    Corner Loaf | Ballard Bakery   (28/30)

BIO OPTION 1  (plain)        112/150
  ...
BIO OPTION 2  (proof-led)    ...
BIO OPTION 3  (offer-led)    ...
bio.py: all READY

LINKS         1. <title> -> {{url}}   2. ...
HIGHLIGHTS    Start here | Menu | Pies | Find us
PIN           1. ... 2. ... 3. ...
LOCAL         category, address, hours, button: <which and why>
```

Run the words through `references/before-you-show.md`. When the user picks an option, save
it to `account.md` under `## Profile` with the date.

Reads: business file, `account.md`, the pasted profile. Writes: `account.md`. Next:
`/instagram-story` for Highlights, `/instagram-plan` for the posts to pin, `/instagram-audit`
next month to see if profile visits turn into follows.
