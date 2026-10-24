---
name: instagram-carousel
description: >-
  Builds an Instagram carousel for the active business: the cover that earns the swipe,
  slide by slide copy, the caption, alt text, and the slide files to upload. Can also
  write image prompts per slide and make AI images through generate-images, always
  showing the estimated cost first, waiting for the user's yes, and keeping under a spend
  cap. Works for apps and for local businesses (menus, offers, how to find you). Use it
  when the user says "carousel", "make slides for Instagram", "swipe post", "turn this
  into a carousel", "photo dump post with captions", "carousel with AI images", or has a
  list, steps or a before and after that would die as one image. For LinkedIn carousels
  or a single image, use another skill.
---

# instagram-carousel

> Based on ig-carousel by Jake Schincariol (MIT). Changed by Aya Taleb: follows the active business from founder-context, adds AI image prompts and images through generate-images with a cost check and spend cap, a local business mode, and dated platform limits.

A swipe is an interaction and a scroll is not, so carousels hold people longer than any
other feed post. Instagram can also show a carousel again from a later slide to someone
who skipped it, so slide 2 has to work on its own.

The format rewards one idea broken into steps. It punishes a caption cut into pieces.

Nothing here posts or uploads. The user posts the carousel.

## 1. Read the business first

Follow `references/business-files.md`: the active business from founder-context, its
`account.md`, and this week's `plan.md` if the slot came from there. Use the business's
tone, words to avoid, proof and off-limits topics. Never invent proof. A missing number is
`{{your number}}`.

If the user asks for a carousel for a business that is not active, use the one they named
and say which file you used.

## 2. Carousel or something else?

Use a carousel when the idea has steps or parts and is worth re-reading: a how-to, a
framework, a before and after, a menu, a list worth a screenshot. Use a Reel when the idea
needs motion, a face, or a payoff seen happening. If the idea is one claim, it is neither.
Say so and hand it to `/ig-reel`.

## 3. Structure

5 to 10 slides. Instagram allows up to 20 items, but long decks lose people. Under 5 and
the swipe never starts.

```
1        COVER    the hook, 6 words or fewer, big enough to read in the grid. One
                  line of promise under it.
2        STAKE    why it matters, one sentence. It may be shown first, so no setup.
3 to N   ONE IDEA PER SLIDE. Headline of 3 to 7 words, at most 25 words under it.
N+1      RECAP    the whole thing as a list. The slide people screenshot and send.
LAST     ASK      one action: save, send to a friend, comment a keyword, or visit.
```

Copy rules, and why:

- **Every line traces to a source.** Each headline and body line comes from the business
  file or the user's words. Shortening is fine if every condition stays ("free for your
  first month" is not "free"); adding is not. No counts the facts don't
  give ("3 steps" when you have 4), no urgency ("only now", "going fast"), no claims about
  what happens after a deadline, no outcomes or promises. People act on slides, and a line
  the founder can't back up costs trust. If a slide needs a fact you don't have, use a
  `{{placeholder}}` or cut the slide: 5 true slides beat 8 padded ones. Before showing,
  point each line to its field or the user's words, and rewrite any that point to nothing.
- **The cover does most of the work.** If nobody swipes, the rest does not exist.
- **Number the slides** (3/8). People finish more often when they can see the end.
- **No paragraphs.** Past 25 words, split the slide. People read these at a third of real
  size on a phone.
- **The recap stands alone.** Sends are the strongest signal a post can earn.
- **The handle on every slide**, small, bottom corner. Screenshots travel without you.
- **Alt text for every slide**, at least the cover. Screen readers read it, and so does
  Instagram.

## 4. Local business mode

For a shop, cafe, food truck, studio or lunch subscription (the business file has a
`## Local` block):

- Good local carousels: this week's menu, "how to find us" (with the real pickup point),
  "how it works" for a subscription, meet the people, the offer with its end date.
- Put the place on the slides: the street, the counter, the pickup point. Real photos of
  the place beat AI images here. Suggest the user shoots them and give a shot list.
- The last slide carries the practical bit: where, when, until when.
- Geotag from `account.md`, up to 5 hashtags, mostly local. Tag a nearby partner only if
  they agreed, and suggest a Collab post if the carousel features them.

## 5. Check the copy with the tool

Write the slides to `slides.md`, one `## <n> <LABEL>` heading per slide, headline on the
first line, body under it. Then run:

```bash
python3 scripts/slides.py check slides.md
```

It fails a cover over 6 words, a body over 25 words, more than 20 slides, and em dashes,
and warns on open placeholders. Fix every FAIL before showing the user.

## 6. Visuals: three routes

Ask which one the user wants, unless they already said. Default to route A.

**A. Text slides.** Build HTML and export images. No cost.

```bash
python3 scripts/slides.py html slides.md --out carousel.html --handle @handle --accent "#hex" --ratio 4:5
```

Then print each `<section>` to an image with any HTML to image tool the user has (Chrome
headless, a screenshot tool). If the business has a brand kit, use its colors and fonts.

**B. Prompts only.** Write one image prompt per slide into `prompts.md`, so the user can
run them in any tool. Keep a shared style line across all prompts so the set looks like
one post. Leave clear space where the text goes, and say where.

**C. AI images through generate-images.** Only if `/generate-images` is installed (from
multimedia-skills). If it is not, say so and fall back to route B.

Paid image runs cost the user money, so follow these steps every time:

1. Write the prompts first and show them.
2. Get the model's price per image from generate-images. It works with the account the user
   has (Replicate, Cloudflare or OpenAI) and needs no key to price:
   `python3 ../generate-images/scripts/generate.py price <model> -i prompt="..."`.
   Replicate prices come live from the model page; the others from a dated table with a
   source link. Never use a remembered price.
3. Run the cost math, including what this session already spent:
   ```bash
   python3 scripts/slides.py cost --images <n> --price <per image> --spent <so far> --cap 2
   ```
   The default cap is $2 a session. The user can change it.
4. Show the estimate in one line: "7 images x $0.04 = about $0.28. Spent so far $0.00,
   cap $2. Run it?" Then stop and wait for a clear yes. Silence, "maybe" or "looks good"
   about the copy is not a yes to spend.
5. If the run would pass the cap, do not run it. Offer fewer images or ask the user to
   raise the cap.
6. After the yes, hand the prompts to `/generate-images` and save the images it returns
   into the carousel folder right away.

Rules for AI images, and why:

- **No fake proof.** Never generate customers, reviews, food photos passed off as the real
  menu, before and after results, or screenshots of numbers. People trust what looks real.
- **No real people's faces or other brands' logos.**
- **Label it if it looks like a photo.** Meta labels images it detects as AI, and can
  penalize accounts that post photoreal AI video without saying so (see the limits file).
  Tell the user to keep the label and not to strip the image's metadata.
- Keep text off the AI image. Put text on top in the HTML route, so it stays sharp.

## 7. Sizes (checked 2026-10-23)

See `references/instagram-limits.md` for sources. When you tell the user a limit, give the
date it was checked ("5 hashtags max, checked Oct 2026"). Limits move, and a dated number
tells the user how much to trust it. In short: up to 20 items. All slides take
the first slide's shape. 1080x1350 (4:5) is the safe default. 1080x1440 (3:4) also works
and fills the 3:4 profile grid, so use it when the cover must not be cropped. Keep cover
text away from the outer 120 px.

## 8. Output

Show the copy first, so the user can edit before anything is built or paid for:

```
CAROUSEL  ·  <business>  ·  8 slides  ·  1080x1350

1  COVER   Lunch in six minutes flat
           Four trucks, one pickup, zero lines.
2  STAKE   ...
...
7  RECAP   ...
8  ASK     Save this for Monday.

alt text   1: ... 2: ...
visuals    route A (text slides), or prompts in prompts.md, or AI images (cost shown)
check      slides.py: READY
humanize   ran / not installed, checked by hand
```

Then the caption. A carousel caption carries the hook line again in its first 125
characters, then context, one ask, and up to 5 hashtags. If Jake's `/ig-caption` is
installed, hand the caption to it (Job B). Run all words through
`references/before-you-show.md`.

Save to `~/.founder/social/instagram/<slug>/carousels/<YYYY-MM-DD>-<short-name>/`:
`slides.md`, `caption.md`, `alt-text.md`, `prompts.md` if any, `carousel.html`, `images/`.

When the user says it is posted, add a line to `log.md` (see business-files.md).

Reads: business file, `account.md`, `plan.md`. Writes: the carousel folder, `log.md`.
Next: `/ig-caption` for the caption lint, `/instagram-story` to push it in stories,
`/instagram-dm` if the ask is a comment keyword.
