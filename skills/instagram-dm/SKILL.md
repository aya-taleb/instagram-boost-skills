---
name: instagram-dm
description: >-
  Writes Instagram DMs for the active business that get replies: the keyword reply
  (someone commented a word and expects the thing), the first message to someone warm,
  the collab pitch to a nearby business or creator, and two follow-ups. Reads real leads
  from sales/leads.csv when it is there, and tracks who is due a follow-up. The user sends
  every message by hand. Use it when the user says "DM this person", "what do I send
  them", "reply to people who commented LUNCH", "message my leads on Instagram", "pitch
  a collab to the coffee shop next door", "how do I follow up on Instagram", or has a
  lead list and wants Instagram messages for it. Private messages only: public comment
  replies go to instagram-reply, captions to ig-caption.
---

# instagram-dm

> Based on ig-dm by Jake Schincariol (MIT). Changed by Aya Taleb: follows the active business from founder-context, reads leads from sales/leads.csv with a small tool, adds local collab pitches and a follow-up tracker; the user sends every message.

DMs are where money changes hands on Instagram. They are also where accounts burn the
goodwill their posts earned. The difference is who moved first.

This skill writes messages. The user sends each one by hand. Never send, schedule or
automate DMs, never log in, and never ask for a password. Unsolicited bulk DMs break
Instagram's terms and get accounts restricted.

## 1. Read the business first

Follow `references/business-files.md`: the active business, its tone, words to avoid,
proof and off-limits topics. A DM from a lunch truck and a DM from a writing app should
not sound alike. Never invent proof, a shared moment, or a mutual friend.

## 2. The four kinds of DM worth writing

**1. The keyword reply.** They commented the word, answered a story, or asked. They
moved first, so this is most of the DMs worth sending.

**2. The warm first message.** Someone the user has been talking with in comments for a
while, or who engaged with several posts.

**3. The collab pitch.** A specific idea to a specific account. For a local business,
this is usually the strongest one: a nearby shop, office, venue or creator.

**4. The lead message.** Someone on the user's lead list. Only write it if there is a
real trigger (see below). If they have never interacted, say plainly that a cold DM is
the weakest use of the hour. Suggest commenting on their posts for two weeks first. Then
write it if the user still wants it.

## 3. Get the trigger

Ask in one message, only for what you do not have:

1. Who: handle, what they do, and how the user knows them.
2. The trigger: the real reason to write today. A keyword they commented, a story reply,
   a post they made, an event. "They fit our ICP" is not a trigger.
3. What the user wants: a sale, a call, a collab, a referral.

No trigger, no message. Say so, and offer the comment-first route.

## 4. Reading leads from sales/leads.csv

If `sales/leads.csv` exists (written by lead-gen in biz-boost-skills), use it. It has one
shared layout across Aya's repos:

```
business_slug,name,company,role,email,linkedin_url,instagram_handle,website,city,source,source_url,fit_score,fit_reason,status,last_contact,notes
```

```bash
python3 scripts/leads.py pick sales/leads.csv --business <active slug> --top 5 --min-fit 60
```

It keeps only rows whose `business_slug` is the active business, uses `instagram_handle`,
skips `do-not-contact` (and leads already contacted, replied, in a meeting, won or lost),
and sorts by `fit_score`. It prints each lead's `fit_reason` and `notes`.

- The trigger lives in `notes` ("commented LUNCH on the Nov 9 reel"). A lead with no trigger
  gets no DM yet. List it under "comment first" instead.
- Use `fit_reason` to make the message specific. Do not add facts the row does not have.
- No `instagram_handle`? Skip that lead for Instagram. Never go looking for someone's
  personal account or contact details to fill the gap.
- If the file is missing the shared columns, the tool says which. Ask the user to rerun
  lead-gen, or paste handles.

After the user says they sent a message, show the change to make in `leads.csv`, and make it
only with their yes:

```bash
python3 scripts/leads.py sent sales/leads.csv --business <slug> --handle @them --date YYYY-MM-DD
```

It prints the new `status` (contacted) and `last_contact` (the send date). Keeping these
current stops linkedin-dm, lead-email and follow-up from writing to the same person twice.

## 5. The keyword reply

They asked for the thing. Give it in message one, with no gate.

```
{name}, here it is: {the thing or the link}.

{one line on how to use it}

{one short question they can answer in a few words}
```

A keyword post that answers "before I send it, what do you do?" is a bait and switch,
and people remember it. The question at the end starts the conversation, and answering it
is optional for them.

Instagram allows automated replies to people who messaged or commented first, through its
own tools or an approved partner. If the user wants that, point them there. This skill
still only writes the text.

## 6. The warm first message

- **Two to four sentences.** A wall of text gets skipped.
- **Name the specific thing** they said or posted, in their words.
- **Give before asking**: an answer, a tip, a name, a free seat.
- **One small ask.** "Want me to send the menu?" beats "let me walk you through it".
- **No link or calendar in message one.** It reads as a funnel.
- Keep it under 1,000 characters (the DM limit, checked Oct 2026). Most should be under 300.

## 7. The collab pitch

Four lines, in this order: what you noticed about them, the idea, what they get, what you
need from them. Be concrete about who does what and when.

Concrete does not mean invented. Dates, prices, quantities and audience numbers come from
the user or the business file. Anything else is a placeholder, like `{{reply by date}}` or
`{{bags per week}}`, so the user fills it with the real number before sending. A made-up
deadline in a pitch is a promise the user did not make.

Good local collabs:

- a joint offer with the shop next door
- lunch for an office's team meeting
- a Collab post, which shows on both accounts' grids
- a pop-up at their venue, or a giveaway with a nearby business

Name the partner only if the user did.

Make "what they get" specific to them, not "exposure". Name who they reach (our weekday
regulars, the families who come on weekends) and one small, concrete thing the user can
easily give: a tag, a shout-out in stories, a spot on the counter for their cards. Flag that
thing next to the draft as a suggestion to confirm, since the user did not offer it.

Name the format of the idea (a Collab post, a pop-up, a joint offer), so they can picture
it. End with one specific ask, not a menu of options: what happens, who brings what, and
roughly when. "Can I bring a pie over Thursday to taste with the blend?" gets a yes or no.
"A chat, or maybe a tasting?" gets a maybe.

Keep the ask small and easy to say yes to: a quick chat, a tasting, a joint post. Do not
commit the user to money, discounts, buying stock or staff time. A pitch that opens with a
deal the owner never agreed to can't be walked back. If a bigger deal fits, suggest it to
the user next to the draft, not inside it.

## 8. Follow-ups

Two, then stop.

- **Day 4:** add something new. Never "just bumping this". Nothing new, no follow-up.
- **Day 10:** close the loop. Say you will stop, and mean it. This one often gets the reply,
  because the pressure is gone.

Write both out in full, ready to paste, with their dates. Advice like "add something new"
leaves the hard part to the user. For the day 4 message, use a real detail from the business
file or the user (a date, an item, an offer), or a placeholder like `{{new detail}}`.

Track them with the tool, so nothing is sent twice and nothing is forgotten:

```bash
python3 scripts/leads.py log ~/.founder/social/instagram/<slug>/dm-log.csv --handle @them --kind warm --sent YYYY-MM-DD
python3 scripts/leads.py due ~/.founder/social/instagram/<slug>/dm-log.csv
```

Log a message only after the user says they sent it.

## 9. Never

- Never send, schedule or automate outreach DMs.
- Never invent a shared moment, a mutual, a customer, or that you watched something.
- Never put the pitch in the same message as the compliment.
- Never message someone marked do not contact, or who asked you to stop.
- Never DM a minor about a sale, and never use personal data from a review to cold DM.

## 10. Output

For each message: who it is for, the trigger, the message, its character count, and the two
follow-ups with their dates. Run every message through `references/before-you-show.md`.

```
DM  ·  <business>  ·  @handle  ·  keyword reply
trigger: commented LUNCH on the Nov 9 reel

Sam, here's the founding seat link: {{link}}
...
(212 characters)

day 4  (Nov 13): ...
day 10 (Nov 19): ...

You send it. Tell me "sent" and I'll log it and suggest the leads.csv update.
```

Save drafts to `~/.founder/social/instagram/<slug>/dms/<YYYY-MM-DD>.md`.

Reads: business file, `sales/leads.csv`, `dm-log.csv`. Writes: `dms/`, `dm-log.csv`, and
`status` and `last_contact` in `sales/leads.csv` (after the user sends, with their yes). Next: `/instagram-comment` for leads with no trigger yet, `/instagram-reply`
for comment replies, `/follow-up` (biz-boost-skills) after a call.
