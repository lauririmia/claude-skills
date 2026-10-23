---
name: images
description: >
  Generate the full image set for an AI influencer character via Higgsfield: a locked face anchor,
  a 3-panel character sheet (full body, side profile, frontal close-up, realistic unretouched
  skin), three or four niche-appropriate locations, and Instagram-style profile/candid photos using
  the Soul 2.0 model. Use whenever the user calls /aia:images, asks to generate images/photos for an
  AI avatar/influencer character, or wants a Higgsfield prompt for a character built with
  /aia:avatar. Requires the character profile from /aia:avatar — if it isn't already in context,
  ask the user to paste it or point to the file that has it, don't invent one.
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

## Phase 1 — Character sheet

Build the sheet in **two passes, not one**. Soul 2.0 holds a face far better when it is fitting an
already-locked reference than when it is inventing the face and the body/angles at the same time.

### Step 1 — Lock the face (face anchor)

Write a single tight head-and-shoulders portrait prompt whose only job is maximum facial identity
detail — no costume, no pose, nothing to distract from the face:

- Opening: a cinematic close-up portrait, head-and-shoulders framing, face filling the frame at
  maximum identity detail.
- The photo block + anti-plastic skin block (see **Reusable blocks** below).
- A no-celebrity/no-real-person-likeness line.
- A character block: ethnicity, age, skin, face, hair, and the signature anchors **copied
  word-for-word from the profile** — do not paraphrase or summarize them.
- The grooming/makeup line for this character's gender (see **Reusable blocks**).
- A neutral clothing base (e.g. a plain shirt) so nothing competes with the face.
- A lighting note that every pore and scar should read clearly.

Present it, get approval, generate once. **Treat this face as permanent** — once approved, never
regenerate it from scratch. Every later prompt in this skill (the sheet, Instagram photos) describes
this same face, not a new one.

### Step 2 — Build the 3-panel sheet, fitted to the locked face

Panel 1 (left third) — full body shot. Panel 2 (center third) — side profile, strict 90°, medium
bust. Panel 3 (right third) — frontal, medium bust. For panels 2 and 3: the face occupies the
upper-middle third of the panel, with shoulders and upper chest visible — never a tight crop on just
the face.

Prompt order:

```
[Opener: background + photo block + no-IP + face-consistency + critical identity details
 (age, gender, anything unusual) + "FULLY CLOTHED in the same outfit in all three panels"]
Panel 1 (left third) — Full body shot: [pose + expression]
Panel 2 (center third) — Side profile, strict 90°, medium bust: [what is visible]
Panel 3 (right third) — Frontal, medium bust: [expression]
Framing rule for panels 2 and 3: face in the upper-middle third, shoulders and chest showing,
no tight face crops.
Character — strict facial consistency: [ethnicity, age, skin, face, hair, (anchors verbatim),
grooming/makeup line, build]. Realistic human anatomy, five fingers per hand.
Outfit (identical in all three panels): [items] + Modest block.
Lighting & rendering: [light] + same bone structure and anchors across all three panels — the
same person photographed three times. [palette] palette, [quality line].
```

### Reusable blocks

Reach for these rather than reinventing the wording each time — they're phrased the way they are
because Higgsfield responds to them specifically:

- **Background — white (default for this skill):** `clean pure white seamless background`.
  Alternative, if the result looks pasted-on/sticker-like: a neutral mid-grey seamless backdrop
  with a soft mottled texture and gentle vignette, plus a line stating the subject casts a soft
  natural shadow behind them for real photographic depth and separation from the wall.
- **Photo block:** editorial-style characters → shot on a Hasselblad, 85mm f1.4, shallow depth of
  field, hyperrealistic, ultra detailed skin texture. Darker/cinematic characters → shot on a
  cinema camera, 85mm, hyperrealistic, ultra detailed material textures.
- **Anti-plastic skin block (always follows the photo block):** `photorealistic with completely
  matte unretouched natural skin showing authentic visible pores, fine peach fuzz, natural skin
  imperfections, real human texture, no plastic skin, no doll-like overdone features, no
  airbrushing, no skin smoothing, no porcelain finish, no CGI rendering`. Never write "porcelain
  skin" as a positive descriptor — it produces plastic-looking skin, the opposite of the intent.
- **Modest block:** `Modest fully-clothed editorial styling, no sexualized framing, no revealing
  styling, opaque thick fabric only, no see-through fabric, no body emphasis, conservative natural
  styling, fully covering torso.`
- **No-IP block:** `No real brand logos, no commercial branding, no copyrighted graphics or text,
  no monogram patterns, no designer brand prints. No celebrity likeness, no real-person likeness —
  an original character with their own original face.`
- **Grooming/makeup line (gender-specific, pick one):**
  - Men: a grooming line (soft natural masculine grooming, no visible makeup, matte-natural skin
    finish) plus specific facial hair or a clean-shaven line. Always add a **lean block** too —
    Soul tends to fatten men: `LEAN ANGULAR face — NOT round, NOT chubby, NO double chin, sharp
    defined jawline with visible bone structure`, and in the build: `LEAN build — NOT heavyset,
    NOT bulky`.
  - Women: a mandatory makeup line — either a completely bare, no-makeup face, or a specific
    makeup description. If the character wears makeup as part of their look, treat that
    description as an anchor and keep it consistent across panels, not a one-off detail.

### Hard rules (each exists because of a specific, observed failure mode)

1. **Front-load critical details and keep the whole prompt under ~3,500 characters.** Higgsfield
   silently truncates long prompts — age, gender, anything unusual, and "fully clothed" have all
   been lost this way in practice (an elderly character rendering as middle-aged, a clothed
   character rendering nude). Put anything that must survive a cut in the opening paragraph.
2. **Say strong features three times**: in the opener, in each panel description, and again in the
   character block. Otherwise Higgsfield drops them on at least one panel.
3. **Anchors go in word-for-word**, copied from the profile — never paraphrased.
4. **Force the age band explicitly, stating both what it is and isn't.** Elderly: "genuinely
   elderly, visibly aged, wrinkled face, NOT young, NOT middle-aged." Young: "clearly reads EARLY
   TWENTIES, NOT thirty, NOT mature." For a character meant to look unusually well-preserved for
   their age, say so explicitly too (e.g. "an exceptionally well-preserved 82-year-old who looks
   like she's in her late 60s") plus what to avoid ("no deep heavy furrows, no leathery texture").
5. **Describe states positively, never as a negated absence.** "Completely bare face, eyes fully
   visible, no eyewear of any kind" — not "sunglasses off." Negations are ignored outright.
   Relatedly, "high neckline" is also ignored — write `TURTLENECK` (or the literal garment) instead.
   Note for the user: an accessory present in panel 1 can still visually bleed into panel 2 even
   when it's absent from that panel's own description — this is a known Soul quirk, cured by
   rerolling, not by more negation.
6. **Describe ethnicity through physical features, not a label.** A label like "Caucasian" is often
   ignored — write it as, e.g., "European woman/man with fair, light, pale skin."
7. **Count jewellery exactly and place it.** "Exactly two slim gold bangles on one wrist, none on
   the other" — not "some bangles." If a piece sits partly hidden (under a beard, a collar), spell
   out where it remains visible.
8. **Lock the outfit three times to stop it drifting between panels**: once in the opener ("one
   single outfit across the entire sheet"), once in panels 2/3 ("wearing the same [item] as in the
   full body shot"), and once more in the outfit heading itself ("identical in all three panels").
9. **Describe eyes to avoid a "colored contact lens" look** when the eye color is a distinctive
   trait — muted/undertone language ("muted sage-green with warm hazel flecks") plus an explicit
   "no colored-contact-lens look" reads as natural; a flat saturated color name alone does not.
10. **Texture, not adjectives.** "Visible pores, faint freckles" — not "ultra realistic" or "8K,"
    which Higgsfield treats as empty adjectives rather than texture instructions.
11. **Aliveness over AI sterility.** Perfectly flat, even lighting with no specular highlights and a
    dead-neutral pose reads as a sticker, not a photo. Prefer a textured backdrop, a soft shadow
    behind the subject, directional (not flat) light, and a lookbook-style pose with a faint hint
    of warmth in the expression — unless the user explicitly wants a deadpan ID-photo look.
12. **Spell out symmetry when a pose is meant to be symmetrical.** "Both arms hanging identically,
    shoulders perfectly level" in the pose, matched by "perfectly symmetrical physique" in the
    build — otherwise mismatched hand positions in the description produce tilted shoulders in the
    generation.
13. **Critical styling items stay identical across all panels** — glasses, face paint, jewellery,
    wet hair, visible paint or dirt — state this explicitly, since Soul does not infer continuity on
    its own.

### Masked or face-painted characters

If the face is covered or painted, anchors move onto whatever skin *is* visible (stubble, a scar on
the chin/jaw) and onto a fixed costume detail (a groove on a helmet, a specific buckle). Face paint
should be described as real greasepaint sitting on real skin — visible pores and stubble showing
through, cracked and faded in places — with the pattern itself treated as an anchor, identical
across panels.

### Step 3 — Fixing a single bad panel

If one panel comes back mushy or with a drifted face, don't regenerate the whole sheet — edit just
that panel, explicitly keeping the rest of the layout, background, outfits, and other panels
unchanged, and match the face to one of the other panels in the same sheet:

```
Edit the existing image. Keep the three-panel layout, background, outfits, poses, and the other
panels completely unchanged.

In the [panel] panel, redraw ONLY the head and face of the [man/woman] so it becomes the same
identical face as in [reference panel] — identical facial structure, identical features,
[anchors verbatim]. Make the face sharp, crisp, photorealistic, with natural matte skin texture
and correct proportions — no blurry, no mushy, no simplified face. Do not change the pose, body,
outfit, or framing of this panel.

Photorealistic result, no plastic skin, no smoothing, preserve the original lighting and colors.
```

Iterate with the user — on the face anchor, the sheet, and any panel fixes — until they're happy
with the character sheet before moving to Phase 2.

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
day/light, materials and objects actually present, atmosphere. The same **no-IP block** from Phase 1
applies here too — no readable text or recognizable branding in the environment. Present the set to
the user for approval before treating it as final; these locations become the settings used in
Phase 3.

## Phase 3 — Instagram photos

Once the locations are approved, generate a profile picture and a handful of candid photos for the
character's Instagram grid, using the **Higgsfield Soul 2.0** model, with the locked face anchor
and character sheet already in context as the identity reference.

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

## Next

Once the image set is approved, recommend running `/aia:content` next to plan what this character
should actually post.
