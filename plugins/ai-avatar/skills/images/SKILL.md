---
name: images
description: >
  Generate the full image set for an AI influencer character via Higgsfield: a character sheet
  (full body + close-up, multiple angles, white background, realistic unretouched skin), three or
  four niche-appropriate locations, and Instagram-style profile/candid photos using the Soul 2.0
  model. Use whenever the user calls /aia:images, asks to generate images/photos for an AI
  avatar/influencer character, or wants a Higgsfield prompt for a character built with /aia:avatar.
  Requires the character profile from /aia:avatar — if it isn't already in context, ask the user to
  paste it or point to the file that has it, don't invent one.
---

# AI Avatar Image Generation (`/aia:images`)

This skill turns a character profile (from `/aia:avatar`) into a full image set, in three
sequential stages: character sheet → locations → Instagram photos. Each stage is **drafted,
approved by the user, then executed** before moving to the next — never skip ahead on an
unapproved draft, and never generate images for a stage whose prompt hasn't been approved.

Image generation itself runs through whatever Higgsfield-capable image tools are available in this
session (e.g. a `generate_image` / `generate_image_batch` tool). If a tool requires a specific model
ID for "Soul 2.0" and it isn't obvious, look it up (e.g. via that connector's model-listing tool)
rather than guessing a name.

## Phase 0 — Get the character profile

Check whether the character's full profile (name, backstory, USP, look, signature anchors,
catchphrase) is already present earlier in this conversation. If it is not, ask the user to either
paste the profile into the chat or tell you which file contains it (then read that file). Do not
proceed to Phase 1 without the actual profile — the anchors in particular must come from the real
profile, never be invented here.

## Phase 1 — Character sheet prompt

Write a single Higgsfield prompt that produces a character reference sheet: a full body shot and a
close-up, a couple of different angles, on a clean white background, with realistic, non-airbrushed
skin. Follow every one of these rules — they come from hard-won experience with what Higgsfield
actually does with a prompt, not stylistic preference:

1. **Front-load the important details.** Age, gender, anything unusual about the character, and
   "fully clothed" all belong in the first paragraph. Higgsfield silently truncates long prompts, so
   put anything that must survive a cut near the top, and keep the whole prompt under **~3,500
   characters**.
2. **Say strong features three times**: once in the opening paragraph, once per angle/panel
   description, and once again in the character description section. ("Bald head, long beard, big
   glasses" pattern — repeat the character's most visually defining 1-3 features, not every detail.)
3. **Anchors go in word-for-word.** Copy the character's signature anchors from their profile
   exactly as written — do not paraphrase or summarize them.
4. **Force the age band explicitly.** For an older character: "genuinely elderly, visibly aged,
   wrinkled face, NOT young, NOT middle-aged." For a young character: "clearly reads EARLY TWENTIES,
   NOT thirty, NOT mature." Pick the wording that matches the character's actual age and state both
   what they are and what they are explicitly not.
5. **Describe states positively**, never as a negated absence. "Completely bare face, eyes fully
   visible" — not "no makeup," not "sunglasses off."
6. **Count jewellery exactly.** If the character wears jewellery, state the exact count and
   placement — "exactly two slim gold bangles on one wrist" — not "some bangles" or "jewellery."
7. **Texture, not adjectives.** Specify what realistic skin looks like — "visible pores, faint
   freckles" — rather than labeling it "ultra realistic" or "8K," which Higgsfield treats as empty
   adjectives, not texture instructions.

Present the drafted prompt to the user in a code block and ask for corrections or approval — do not
generate images yet. Iterate on the prompt itself until the user approves it.

Once approved: run it through the available Higgsfield image tool. Show the result, and keep
iterating with the user (adjusting the prompt and regenerating) until they're happy with the
character sheet before moving to Phase 2.

## Phase 2 — Locations

Propose three or four locations to generate scenes in, appropriate to the character's niche.
Locations should be **lived-in** (not showroom-clean), have **no visible brands**, and **no
readable text**. Use the niche to pick settings a real person like this would actually be in —
for example:

- A 100-year-old subsistence farmer (health niche): porch, farmhouse kitchen, vegetable garden, yard.
- A wealthy grandmother (wealth niche): private jet, sports car, drawing room, terrace.
- A 22-year-old (relationships niche): apartment living room, bedroom, hallway.

Write each location as its own short, concrete, visual description — empty-scene environment
prompts work well here (no people in them), in the spirit of a cinematic establishing shot: time of
day/light, materials and objects actually present, atmosphere. Present the set to the user for
approval before treating it as final; these locations become the settings used in Phase 3.

## Phase 3 — Instagram photos

Once the locations are approved, generate a profile picture and a handful of candid photos for the
character's Instagram grid, using the **Higgsfield Soul 2.0** model, with the character sheet
already in context as the identity reference.

If the user hasn't specified situations, default to a mix like: a selfie in an airport seat, a
mirror photo before a night out, a coffee on a balcony — adjusted to fit the approved locations and
the character's niche where it makes sense.

Every prompt you write for this stage follows this exact shape:

- **Opens with:** `keep this exact person's face and identity unchanged`
- **Middle:** the specific situation/pose/location for this shot
- **Closes with this exact phone-photo block:** `casual imperfect framing, mild HDR, true-to-life
  colours, natural skin texture, subtle sensor grain, no retouching.`

Generate the profile picture and the candid set through the Higgsfield Soul 2.0 model via the
available image tool. Work with the user on each image — regenerate or adjust individual shots —
until the set is approved.
