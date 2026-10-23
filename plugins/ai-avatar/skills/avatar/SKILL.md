---
name: avatar
description: >
  Create a character profile for an AI influencer in a given niche: name, backstory, one-line look,
  fixed signature anchors, a catchphrase, a USP built on contrast, and a reason they're online. Use
  whenever the user calls /aia:avatar, asks to create an AI influencer / AI avatar / virtual
  character / synthetic persona, or wants a persona for a faceless-channel or UGC content concept.
  If the user does not name a niche, infer it from the conversation and confirm before building the
  character — never invent a niche silently.
---

# AI Avatar Character Creation (`/aia:avatar`)

This skill is the entry point of the `ai-avatar` plugin. It turns a niche into a fully specified AI
influencer character — a persona concrete enough that every future image/video prompt for this
character reproduces the same person.

## Phase 1 — Establish the niche

1. Check whether the user already named a niche when invoking the skill (e.g. `/aia:avatar wealth`,
   "make me an avatar for a skincare brand", "I need a fitness influencer persona").
2. If no niche was given, look at the current conversation for context — prior messages, files open,
   a product or brand already being discussed — and infer the most likely niche from that.
3. Either way, **state the niche back to the user and get explicit confirmation before building the
   character**. Do not proceed on an assumed or inferred niche without confirmation. If nothing in
   the conversation points to a niche, just ask directly instead of guessing.

Example confirmation: "I'm reading this as a **personal finance / wealth** niche — is that the one
you want the character for?"

## Phase 2 — Build the character

A strong AI influencer character has six parts. Fill in all six — a character missing any one of
these tends to feel generic or drifts across generations.

1. **Name** — fits the niche and the persona's age/background.
2. **USP built on contrast** — the opposite of what this niche normally looks like. The niche sets an
   expectation (young biohacker for health, polished guru for wealth, confident 20-something for
   relationships); the character should violate that expectation in a specific, memorable way. The
   contrast *is* the hook — without it the character is just another face in the niche.
3. **A look you can say in one line.** Dense, concrete, visual — something you could read aloud and
   have someone sketch. Not "stylish and confident," but specific garments, colors, and objects.
4. **Two or three signature anchors** — fixed physical details that never change: a mole, a scar, a
   specific wrinkle pattern, a liver spot, a gap tooth, bled lipstick, age spots on the hands. These
   exist so that every image/video prompt generated for this character later includes them
   word-for-word, which is what keeps the character recognizable across many separate generations.
   Pick details that are small, specific, and physically grounded — not generic ("piercing eyes") but
   literal and locatable ("a comma-shaped scar through the left eyebrow").
5. **A catchphrase** — the line they end every video with. Short, quotable, and consistent with their
   backstory and worldview.
6. **A reason they're online** — one sentence. Not a biography, a motive: why does someone like this
   make content at all?

Plus a **backstory** — a few sentences of life history that justifies the USP, the look, and the
catchphrase. The backstory is what makes the contrast believable instead of arbitrary.

### Reference characters

- **Amos (health)** — 101, lived off the land, grandkids talked him online. Signs off: *"None of
  this is new. You've just forgotten it."* Contrast: ancient outsider in a niche obsessed with
  biohacking and the newest protocol.
- **Grandma Vivienne (wealth)** — 82, self-made in property, three husbands, private jets. Anchors:
  bled red-orange lipstick, age spots on the hands, silver bouffant. Contrast: a grandmother in a
  niche that performs youth and hustle.
- **Sienna (relationships)** — 22, stylish, dating and situationship drama, big-sister energy.
  Anchors: freckles across the nose bridge, beauty mark under the left eye, mole above the right
  eyebrow. Contrast: lives the chaos she narrates, rather than giving advice from above it.

## Phase 3 — Present the profile

Once the niche is confirmed, generate the character in one pass and present it in this exact
structure:

```markdown
## <Name> (<niche>)

**Backstory:** <a few sentences>

**USP:** <the contrast — what this character is the opposite of, in this niche>

**Look:** <one line>

**Signature anchors:**
- <anchor 1>
- <anchor 2>
- <anchor 3, if used>

**Catchphrase:** "<line>"

**Why they're online:** <one sentence>
```

Tell the user the signature anchors are meant to be copied word-for-word into every future
image/video prompt for this character — that's what keeps the character consistent across
generations, and changing that wording later will drift the character's appearance.

Ask if they want any part regenerated or adjusted before treating the character as final.
