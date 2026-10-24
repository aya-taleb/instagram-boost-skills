# instagram-boost-skills

Claude skills that help a founder grow on Instagram, one business at a time, without handing over the account.

## What do you want to do?

| I want to... | run this |
| --- | --- |
| know what to post this week, and when | /instagram-plan |
| make a carousel, with or without AI images | /instagram-carousel |
| plan today's stories | /instagram-story |
| fix my bio, links, Highlights and pinned posts | /instagram-profile |
| reply to people who commented a keyword, or pitch a collab by DM | /instagram-dm |
| write comments for my daily engagement round | /instagram-comment |
| answer the comments on my own posts | /instagram-reply |
| turn a blog post, newsletter, talk or video I made into posts | /instagram-repurpose |
| see what worked last month and what to change | /instagram-audit |
| write a Reel script with a scored hook | /ig-reel (Jake's, linked) |
| write and lint a caption | /ig-caption (Jake's, linked) |

## Install

```
/plugin marketplace add aya-taleb/instagram-boost-skills
/plugin install instagram-boost-skills@instagram-boost-skills
```

Two skills here come from Jake Schincariol's
[instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill): ig-reel and
ig-caption. They ship his own Python tools, so we link to them instead of copying.
Get them, pinned to a fixed commit, with:

```
python3 scripts/get_linked.py
```

## Start here

Run `/founder-context` first so the skills know your business. If you run more than one, set
up each one and pick the active one. Then run `/instagram-plan`. It reads that business, asks
what happened this week, and gives you a dated plan with the next skill for each slot.

Running a shop, cafe, food truck or lunch subscription? Add your area, busy hours and offers
when it asks. The plan then times posts to your walk-past hours and adds geotags, local
hashtags and nearby collabs.

## Good to know

- You post everything yourself. No skill logs in, posts, schedules, comments, follows or sends
  a DM for you. That keeps your account inside Instagram's terms.
- Nothing is made up. Missing numbers, quotes and links show as `{{your number}}` for you to
  fill. No fake reviews, no fake customers.
- AI images cost money, so the carousel skill shows the estimated cost and waits for your yes.
  The default cap is $5 a session, and you can change it.
- Each business gets its own folder: `~/.founder/social/instagram/<business>/`. Plans, logs and
  DM trackers never mix.
- Platform limits (5 hashtags, 20 slides, 150 character bio) are checked and dated in each
  skill's `references/instagram-limits.md`. They change, so check the date.
- Optional, not installed: Jake's ig-viral finds what is working in your niche. We leave it
  out because it reads Instagram through your logged-in browser and downloads data with
  yt-dlp, which breaks the no-scraping rule above. Get it from his repo if you accept that.
- Jake's linked skills read one voice file, `~/.claude/instagram/voice.md`. When you switch
  business, instagram-plan offers to rewrite it from that business, and asks first.

## Credits

Made by Aya Taleb (github.com/aya-taleb). instagram-plan, instagram-carousel and instagram-dm
are built on Jake Schincariol's ig-plan, ig-carousel and ig-dm (MIT). The rest are our own,
written to beat his versions on the same tests. Thanks to Jake for a great pack to build on.
See CREDITS.md. MIT.
