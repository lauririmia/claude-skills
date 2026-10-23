---
name: content
description: >
  Research a niche and generate content ideas, then full scripts, for an AI influencer character
  built with /aia:avatar. Use whenever the user calls /aia:content, asks for content ideas, video
  ideas, hooks, or scripts for an AI avatar/influencer character, or wants to plan what a
  character's channel should post. Requires the character's profile and niche — if neither is
  already in context, ask the user for the character profile rather than inventing one.
---

# AI Avatar Content Ideas & Scripts (`/aia:content`)

This skill turns a character into a content plan, in two approve-then-proceed stages: ideas →
scripts. Don't write any script before the user has told you which ideas from Phase 1 to carry
forward into Phase 2.

## Phase 0 — Get the character and niche

Check whether the character's profile (name, niche, backstory, USP, catchphrase) is already present
earlier in this conversation. If it is not, ask the user for it — don't guess a niche or invent a
character to fill the gap.

## Phase 1 — Content ideas

Research the niche before proposing ideas — look at what's actually landing in that space right now
(common hooks, formats, pain points, questions an audience in this niche keeps asking) rather than
generating ideas purely from the character sheet. Use whatever search tool is available in this
session for this.

Return a **ranked list** of ideas, each with four parts:

- **Opening line** — the literal first line of the video. This is the part doing the actual work:
  write it like a hook you'd stop scrolling for, not a topic summary. Weak ideas with a strong
  opening line still beat strong ideas with a flat one — rank mainly on this.
- **Format** — the shape of the video (e.g. numbered list, myth-vs-truth, a story with a twist, a
  reaction, a "confirm or deny" prompt to the audience).
- **Setting** — where/how it's shot, consistent with the character (e.g. podcast desk, kitchen
  table, porch at golden hour).
- **Why it should work** — one line connecting the idea to the character's USP, niche, or a
  specific audience pain point. Not generic ("this is engaging") — specific to this character.

Present the ranked list to the user and **wait for them to tell you which ideas to carry into
Phase 2** — never generate scripts for ideas that weren't picked. While presenting, tell the user
they should aim for about **ten scripts per character before launch**, so they know how many
rounds of this they'll likely want.

## Phase 2 — Scripts

For each idea the user approved, write a full script and present it as its own card:

```markdown
**Caption:** <short caption for the post itself>
**Setting:** <where/how it's shot>
**Script:** <the spoken script>
```

A good script:

- **15–30 seconds spoken, roughly 40–90 words.** Longer scripts don't get watched.
- **The first line is the hook** — it should read as the same opening line approved in Phase 1, not
  a softer rewrite of it.
- **Sounds like talking, not writing.** Contractions, sentence fragments, direct address to the
  viewer, the rhythm of someone actually speaking the character's voice — not an essay read aloud.
- **No medical claims, no financial advice, no cures.** This holds regardless of niche — a
  health-niche character shares experience and opinion, never a diagnosis or treatment claim; a
  wealth-niche character shares perspective, never specific investment advice or guaranteed
  outcomes.

### Reference example

> **Caption:** how to make him nervous and give him butterflies.
> **Setting:** podcast desk, side view, headphones off.
> **Script:** This is how to make him nervous and give him butterflies. Guys, confirm or deny in
> the comments. Number one, The Alexa. Say his name. Actually use it in conversation instead of
> just talking at him. The second you say it, it's like you woke something up. Number two, The
> Mona Lisa. Forehead, eyes, lips. Hold real eye contact, then glance at his lips for a second.
> It's foolproof. Babe, you're basically a painting right now, I'm just appreciating the art.

Note what this example does: it opens with the exact hook line, uses a numbered format, stays
conversational throughout, and closes on an in-character line rather than trailing off.

Present each script to the user and work with them on revisions until the batch is approved.
