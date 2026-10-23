---
name: product
description: >
  Create a sellable low-ticket digital product (guide, 30-day challenge, workbook, swipe file,
  template pack) for an AI influencer character built with /aia:avatar — pitch 3 ranked product
  ideas, build the one the user picks into a finished styled PDF with the character's cover photo,
  audit it, and deliver it with a sales blurb, a longer marketing description, captions, and a
  price recommendation. Use whenever the user calls /aia:product, asks what a character could
  sell, or wants an ebook/challenge/workbook built for an AI avatar/influencer character. Requires
  the character's profile and niche; the cover needs the character sheet from /aia:images.
---

# AI Avatar Digital Product (`/aia:product`)

This skill takes one character and produces a finished, sellable low-ticket digital product
($9–$27) for them, from idea to delivered file. The flow is: pitch 3 ideas → user picks one (e.g.
"Build number 2.") → full build → internal audit → hand over the initial PDF → user reviews it and
requests changes → final delivery kit (blurb, description, captions, price, next upgrade).

## Phase 0 — Which character?

Chats can hold several characters. If the user names one, use that one — no questions. If they
don't and more than one character exists in this conversation, ask once, listing the characters you
can see. If no character exists anywhere in the conversation, ask for the profile (name, niche, who
they are, what they already sell or plan to), rather than inventing one.

Open your output by confirming who you're working on in one line (e.g. "Digital product — Amos,
101, health & natural living") so a mix-up gets caught immediately.

## Phase 1 — Pitch 3 product ideas

Triggered by something like "Create a [workbook/guide/challenge] as a digital product for
[name]" — the format in that phrase is just an example; which format actually fits is decided by
the rules below, not assumed from the trigger wording.

**The buyability rules — these decide everything:**

- **Systems and tools sell; information doesn't.** People pay for structure: a plan with a start
  and an end, something they fill in, exact words they can copy. Never pitch "an ebook about
  [niche]."
- **Chronic pain + concrete promise.** The best low-ticket products answer a pain the buyer feels
  right now with a promise they can picture.
- **The buyer must be able to picture *using* it** — daily pages, checklists, trackers, word-for-
  word scripts. Bought-and-used beats bought-and-read.
- **The character is the flavour, not the product.** Their voice wraps the product, but the
  purchase decision is the transformation, not the lore.
- **Never undercut what the character already sells or plans to sell.**
- **Impulse-priced**, $9–$27: a single thin document at $9–$17, a full system with a bonus stack at
  $27.

**Match the format to the buyer's moment** — the most important design decision in the process:

| Buyer's moment | Format | Shape |
|---|---|---|
| Daily, grinding pain (tired, unfit, scattered) | 30-day challenge | One habit per day, tick-box, themed weeks |
| Avoiding something shameful (money mess, clutter, admin) | Reckoning + ritual workbook | One guided honest sitting, then a short repeating ritual |
| Acute crisis, needs help now (dating meltdown, hard conversation) | Swipe file | Situation-indexed cards, word-for-word scripts |
| Wants a skill or an output (writing, cooking, planning) | Workbook / template pack | Fill-in artefacts that produce the thing |

**The lifestyle twist:** if the character's lifestyle seems at odds with the product (a jet-set
grandma teaching budgeting), don't hide it — make the reconciliation the product's opening
argument: the lifestyle is the receipt for the habits, not the contradiction of them.

**Output exactly 3 ranked ideas:**

```markdown
**#N — [Product name]**
- **What it is:** [format + one-line contents]
- **The promise (cover line):** "…"
- **Why people would pay — who buys it & the moment they buy:** [the pain + the exact moment
  they're most likely to hit buy]
- **Price:** $X
```

Then stop and ask which one to build (or whether to tweak one) — don't start building until they
choose. Expect the pick as something like "Build number 2."

## Phase 2 — Build the product

Once an idea is picked, go straight to the full build — there's no separate sample-approval pause
here. Before writing, settle internally (and note briefly to the user) the handful of things every
page needs to agree on: a title + subtitle (title is the promise or the method's name; subtitle is
"[Character]'s [thing]"), the cover promise line, the full structure skeleton (every part and every
section/day/card, named), and a visual identity derived from the character's wardrobe and world
(e.g. earthy greens and cream for a farmer, burgundy and gold for old money) plus a running footer
"TITLE · NAME". The character's catchphrase belongs on the cover and at one or two designed moments
inside — never on every page.

Then write the full product:

### Front matter, in this order

1. **A letter from the character**, at full voice strength — removes the buyer's shame, states the
   promise, delivers the lifestyle twist if there is one, ends on the catchphrase.
2. **"Why this works"** — the honest theory page: mechanism in plain language, real hedged evidence
   where it exists, never invented citations, and a plainly honest paragraph on what the product is
   not (not medical/financial/therapy advice).
3. **The measurement loop, opening half** — a self-score table or usage log the buyer fills in now
   and revisits at the end, so they can see their own result.
4. **"What to expect"** — pre-warns the emotional timeline, especially the dip.
5. **The failure page** — the rule, in the character's voice: no restarts, no catching up, just do
   the next one.
6. **"Make it fit your life"** — 3-4 honest adaptations for buyers the default shape excludes, plus
   the serious-case route naming real professional help.

### The body

One unit per page, identical structure throughout. Every unit or section gets a **named rule**
("The Well Rule"), which becomes the product's quotable IP. Interactivity the buyer writes into —
tick-boxes and a line for sequential products, fill-in pages for workbooks, a central usage log for
swipe/card products. Progress indicators on sequential products. A midpoint letter, in voice, on
anything spanning more than ~3 weeks. The ending closes the measurement loop against the front page
and gives a continuation mechanism that turns the product into a permanent routine.

### The back of the book

A short divider page with a line of copy under the title (never a bare heading). The working pages
(the whole method on one page, a printable tracker or card). A bonus stack of 3-6 items **mined
from seams already in the content** (a passing mention becomes a bonus) — consider a quickstart
version, a printable, and, for reactive products, an "offence" asset. Bonuses add or condense; they
never duplicate body content. The honest small print: the character is a character (say so), what
the product is not, real named free help for serious cases, written warm, closing in voice.

### Voice, writing, and safety

The character's voice soaks every page — if a paragraph could appear in a generic PDF, rewrite it
until only this character could have said it. Facts stay honest and hedged; specifics beat
adjectives; never pad. British spelling if the character is British. No em dashes.

Safety is stricter here than for content, because money is changing hands: health products are
habits/routines/traditions only, no cures or dosages; money products are principles/organisation
only, no investment advice or promised returns; relationship products are clarity/self-respect
only, never manipulation, with a real helpline named for unsafe situations. Nothing that would get
the product refunded, reported, or the account banned.

## Phase 3 — Production (the actual file)

Build the finished product as one styled document — a real designed PDF if document tools are
available. Serif type, generous margins, a thin full-page border frame, the running footer, page
numbers on every page, a contents page verified against the real built pages.

**Put the character's face on the cover automatically** if a character sheet image exists from
`/aia:images` — that's what turns a PDF into *their* book. If none exists, ship a typographic cover
and flag the portrait as the one upgrade. To swap in a different shot later, a prompt like "Add
this photo of [name] to the front cover" replaces the cover image without touching anything else.

**Rendering traps to check every time** (each has actually happened):

- No raw unicode arrows/ticks/boxes (→ ✔ ☐) in document text — use ">" and drawn bordered cells
  instead.
- Table columns sized to fit their headers — no vertically wrapped headers.
- Long tables fit one page or split deliberately with repeated headers.
- Bold/italic markers inside table cells are processed, not printed as literal asterisks.
- Fill-in blank lines inside table cells stay short enough not to wrap.
- No bare divider pages, no floating centred elements breaking an otherwise left-aligned page.
- Recurring flourishes (the catchphrase) appear only at the designed moments, never on every page.

## Phase 4 — Internal audit (before handing anything over)

Run both halves before delivery:

- **Systematic:** every unit present and in order, one per page; every unit's required elements
  present; no font artifacts; no near-empty pages; every contents entry matches its real page
  number; every table intact.
- **Buyer-eyes read:** read the finished pages as a sceptical customer would — typos, off-voice
  sentences, wrapped headers, anything that whispers "AI-generated."

Fix what's found, rebuild, re-verify. Report honestly what the audit found and fixed — never
invent findings to look thorough, and never claim a clean pass that wasn't actually checked.

## Phase 5 — Hand over the initial PDF for the user's own read

Deliver the built PDF to the user and tell them plainly this is the pass for *their* read: checking
it's logically sound and safe, and stripping anything that still sounds like a machine wrote it.
Apply whatever changes they come back with — without relitigating the rules above — and re-run the
audit on anything substantially rewritten.

## Phase 6 — Delivery + the selling kit

Once the user is happy with the content, close with:

- A 2-3 sentence **sales blurb** for the link-in-bio page, in the character's voice.
- A longer **marketing description**, in the character's voice, following this shape: a one-line
  hook stating the transformation and the timeframe, a short "this is for you if" list of concrete
  outcomes, a line on what's included (trackers, bonuses, printables), and a close on the
  character's catchphrase. For example:

  > Thirty forgotten habits. One a day. More energy in a month than you've had in years.
  > This guide is for you if you're looking to:
  > - Wake up with more energy, without needing five coffees to do it
  > - Build habits that actually stick, one simple day at a time
  > - Eat, move, and sleep the way people did before it got complicated
  >
  > Includes a full 30-day tracker, bonus recipes, and a printable wall chart to keep you going
  > long after day 30.
  > "None of this is new. You've just forgotten it."

- **Three short caption lines** the character can drop into content without sounding like an ad.
- The **price recommendation**, with one line of justification (the system + page count + bonus
  stack).
- The one honest **next upgrade**, if there is one.

## Rules throughout

- One product, one character, per run.
- Never pad, never invent audit findings, never let a bonus duplicate body content.
- The user's product, their call — if they ask to change format, price, angle, or voice at any
  point, do it without relitigating the rules above.
