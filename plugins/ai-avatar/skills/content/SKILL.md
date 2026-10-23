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
forward into Phase 2 — unless the user skips straight to a topic they already have in mind (see
Routing below).

## Phase 0 — Get the character and niche

A conversation can easily hold more than one character (users often build several influencers in
one chat). If the user names the character ("ideas for Sienna"), use that one without asking. If
they don't name one and more than one character exists in this conversation, ask once, listing the
characters you can see, rather than guessing which one they mean. Only if no character exists
anywhere in the conversation, ask the user for the profile (name, niche, who they are, backstory) —
never invent one to fill the gap.

Open your output by naming who you're working on in one line (e.g. "Content plan for Amos, 101,
health & natural living") so a wrong guess gets caught immediately.

## Routing — ideas, script, or both?

Work out which phase to run before doing anything else:

- **Only ideas asked for** ("give me content ideas", "what should X post") → run Phase 1 only, then
  stop and wait for the pick.
- **A specific topic or already-chosen idea is given** ("write a script about X", "script idea 2",
  or an idea sitting earlier in this same conversation's content plan) → skip Phase 1 entirely and
  go straight to Phase 2 for it.
- **The whole pipeline is asked for** ("come up with ideas and write the scripts") → run Phase 1,
  stop and wait for the pick same as always, then run Phase 2 once they've chosen. Don't skip the
  human decision just because they asked for "everything" — the pick is still theirs to make.

## Phase 1 — Content ideas

Research the niche before proposing ideas — look at what's actually landing in that space right now
(top creators and accounts in the niche, hooks/formats currently pulling views, the questions and
debates the niche's audience is obsessing over) rather than generating ideas purely from the
character sheet. Use whatever search tool is available in this session for this; if none is
available, say so in one line and fall back to general short-form content patterns, still tailored
hard to this character. Extract *patterns* from the research, not topics to copy outright.

Return a **ranked list** of ideas, each with four parts:

- **Opening line** — the literal first line of the video. This is the part doing the actual work:
  write it like a hook you'd stop scrolling for, not a topic summary. Front-load the most
  surprising or specific word — no warm-up, no "so", no "today I want to talk about". Draft a
  couple of alternative hooks for each idea in your own head and keep only the strongest one; hooks
  are worth over-producing and cutting down, never ship the first line you think of. Weak ideas with
  a strong opening line still beat strong ideas with a flat one — rank mainly on this.
- **Format** — the shape of the video (e.g. numbered list, myth-vs-truth, a story with a twist, a
  reaction, a "confirm or deny" prompt to the audience, a day-in-the-life).
- **Setting** — where/how it's shot, consistent with the character (e.g. podcast desk, kitchen
  table, porch at golden hour). Keep it to one simple, static, describable scene — it should work
  as-is as an image-generation prompt for a single consistent character, not a crowd or real
  product demo.
- **Why it should work** — one line connecting the idea to the character's USP, niche, or a
  specific audience pain point. Not generic ("this is engaging") — specific to this character.

**If the character sells something or monetizes a specific way**, factor that in: if they sell
their own product, make sure no idea argues against the problem that product solves, and let a
couple of ideas build interest in that problem so the product reads as the natural answer — without
turning the idea into an ad. If they rely on brand deals or affiliates instead, lean a couple of
ideas toward topics a relevant sponsor would be glad to sit next to. Either way, every idea still
has to earn the view on its own.

Before presenting the list, drop anything that wouldn't actually stop a stranger scrolling within a
couple of seconds, that lacks a specific hook, or whose setting isn't simple enough to generate as
one image — replace it rather than padding the list to hit a target count.

Present the ranked list to the user and **wait for them to tell you which ideas to carry into
Phase 2** — never generate scripts for ideas that weren't picked. While presenting, tell the user
they should aim for about **ten scripts per character before launch**, so they know how many
rounds of this they'll likely want.

## Phase 2 — Scripts

For each idea approved (or each topic the user handed you directly), write a full script and
present it as its own card:

```markdown
**Caption:** <short caption for the post itself>
**Setting:** <where/how it's shot>
**Script:** <the spoken script>
```

A good script:

- **15–30 seconds spoken, roughly 40–90 words.** Longer scripts don't get watched — cut rather than
  pad, and lean toward the low end unless the idea genuinely needs the room.
- **The first line is the hook** — it should read as the same opening line approved in Phase 1
  (tightened if needed, surprising word still first), not a softer rewrite of it. The rest of the
  script must deliver exactly what that hook promised — never bait-and-switch.
- **Sounds like talking, not writing.** Contractions, sentence fragments, direct address to the
  viewer, the rhythm of someone actually speaking the character's voice — not an essay read aloud.
  A few specific things that make a script read as AI-written instead of spoken — check every
  script against these:
  - Balanced lists or matched pairs ("same friends, same hobbies, same her") are a classic tell —
    break the symmetry instead of rounding to threes.
  - Don't summarize the point with an abstraction at the end ("so the loop never closes") — land it
    through the concrete example and trust the viewer to get it; real speakers don't label their
    own point.
  - Let in one self-interruption or restart ("wait, no—", a trail-off), placed in a boring middle
    stretch rather than bolted onto the punchline.
  - One uselessly specific detail beats a tidy generic one ("a guy she dated for like five minutes
    in school" beats "a guy from her past") — over-efficient language is its own tell.
  - Uneven rhythm — a few short fragments, then one that runs on — rather than a tidy alternating
    short-long pulse.
- **No medical claims, no financial advice, no cures.** This holds regardless of niche — a
  health-niche character shares experience and opinion, never a diagnosis or treatment claim; a
  wealth-niche character shares perspective, never specific investment advice or guaranteed
  outcomes. Nothing that would plausibly get an account flagged or demonetized.
- **Don't undercut what the character sells.** If they have their own product, the script never
  argues against the problem it solves; where it fits naturally, steer toward it without turning
  the script into an ad.
- **Ends on one line of CTA** when the format calls for it — a soft plug toward what they sell if
  relevant, otherwise a light in-character follow/engagement line. Skip it when the idea doesn't
  need one (a strong line already at the top, a quote clip, a joke that lands on the punchline) —
  use judgment rather than bolting a CTA onto everything.

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

## Next

Once scripts are approved, recommend running `/aia:voice` next to lock the character's voice and
render these scripts into audio.
