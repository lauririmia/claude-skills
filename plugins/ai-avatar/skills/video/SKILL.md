---
name: video
description: >
  Generate short vertical video clips for an AI influencer character — talking-to-camera clips,
  off-camera interview clips, silent text-over b-roll, and continuations of a longer clip — using
  the character sheet, a location still, and the locked voice as references. Use whenever the user
  calls /aia:video, asks for a video prompt/clip for an AI avatar/influencer character, or wants to
  turn an approved script or b-roll idea into an actual video. Requires the character's profile,
  character sheet, a location, and (for talking/interview clips) the locked voice and an approved
  script — if any of these are missing, ask rather than inventing them.
---

# AI Avatar Video Generation (`/aia:video`)

This skill turns a character, a location, and (for anything with dialogue) the locked voice into a
finished video clip. It runs in three gated stages for every clip: **short brief → full prompt →
generation** — each one approved before the next starts, because generation spends credits and a
wrong prompt is expensive to discover only after rendering.

## Phase 0 — Check what's available

Before drafting anything, check this conversation for:

- The character's **profile** (name, niche, personality) — from `/aia:avatar`.
- The **character sheet** image — from `/aia:images`.
- A **location still** for the scene this clip is set in — from `/aia:images`.
- For talking or interview clips only: the **locked voice prompt/audio** from `/aia:voice`, and the
  specific **approved script** this clip is for, from `/aia:content`.

List what's present and what's missing, and ask the user for anything missing (or point you at the
file/image/audio that has it) rather than inventing a placeholder. Silent b-roll doesn't need a
voice or a script — it carries no dialogue by definition.

## Routing — pick the format

| Situation | Format |
|---|---|
| Character speaks to camera, films themselves | **Talking clip** (voice-locked) |
| Character answers an off-camera interviewer | **Interview clip** |
| No dialogue; a script/caption goes on top as a text overlay added in post | **Silent text-over b-roll** |
| Part 2+ of a longer clip, continuing from the last frame of Part 1 | **Continuation** |

**Credit-saving rules that apply to every format:**

- **30 seconds is the hard cap per generation.** A script that won't fit becomes two clips joined
  by exactly one hard cut (voice and ambience continuous across it), or a Continuation prompt for
  the next part — never more than one cut per generation.
- **One action per clip.** A clip is one small, complete thing with a start and an end — not several
  beats stitched together.
- **Never write "tripod."** The camera is always propped (leaning against a real object, with an
  opening settle-wobble) or genuinely handheld (a person's natural sway and micro-corrections) —
  state which, and write its imperfections in.
- **Props exist from frame one.** Anything that moves during the clip (glasses, a cup, a phone) must
  already be visibly present at the start — never materialize mid-clip.
- **Other people stay at the edges, blurred, faces never visible** — this protects both focus and
  character consistency.

## Phase 1 — Draft the short brief

Write the clip as one short line first, and get that approved before expanding it — this is the
cheap, fast checkpoint where format/location/duration mistakes get caught before any detailed
prompt work.

- **Silent text-over b-roll:**
  `Silent text-over b-roll: [name] [doing what, where], [propped or handheld], [seconds]. Image 1
  is the character sheet, image 2 is [location].`
- **Talking clip / interview clip:**
  `[Talking clip / Interview clip]: [name] in [location], [propped or handheld]. Image 1 is the
  character sheet, image 2 is [location], audio 1 is the voice track.`
- **Continuation:**
  `Continuation: [name] continuing from [previous clip], [propped or handheld], [seconds]. Video 1
  is the previous clip, audio 1 is the voice track.`

Present this line and wait for approval before moving on.

## Phase 2 — Expand into the full prompt

Once the brief is approved, assemble the full prompt in this order — every section exists to head
off a specific, observed failure, not for ceremony:

```
TOP PRIORITY (read first): the 4-6 rules this specific clip lives or dies by
=== REFERENCE KEY === @image1 character / @image2 location / @audio1 voice (or @video1 for a continuation)
CRITICAL — RELIGHT
IMAGE QUALITY
Style
Camera movement (or CAMERA & EDIT STRUCTURE when there's a cut)
ACTING TASK (talking/interview) or Performance (b-roll)
Physics
Composition
Consistency
Editing
Technical
ON-SCREEN TEXT: none. (Added in post by the team.)
Audio
Mood & tempo
SHOT BREAKDOWN (timed beats)
```

### Reference key

- `@image1` = the character sheet. Describe the identity anchors verbatim and identically to the
  profile every time (face, hair, eyes, jewellery) — the outfit is described per-clip. Always add:
  "identity reference ONLY (face, hair, outfit), NEVER its lighting."
- `@image2` = the location still. "Scene reference only, generic, no brands, no readable text."
  Reusing the same still across clips set in the same place is what keeps the character's world
  consistent.
- `@audio1` = the pre-generated voice track (talking/interview clips): "this audio file is the ONLY
  spoken content; use it exactly as recorded," plus a one-line note on the delivery register so the
  face can match it.

### CRITICAL — RELIGHT (mandatory on every clip)

The character sheet is a flat image on a white studio background. Without an explicit instruction,
the model pastes it into the scene like a sticker. Every clip needs a relight line that discards
the sheet's lighting and relights the character from scratch to the scene: name the key light and
its direction, the fill, at least one color bounce off a named surface in the room, and real contact
shadows grounding them. Close with something like: "must look physically present and photographed
in the location — never a cut-out pasted from a white background; never brighter than the
environment." If a drafted prompt is missing this, add it before presenting it — don't let a
prompt through without it.

If the light must stay constant through the take (e.g. a fixed dawn), add a light-stability line —
otherwise models tend to compress a sunrise or sunset into the clip's duration like a time-lapse.

### Image quality — pick one look per character and keep it

- **Clean modern flagship** (luxury/young characters): clean, bright, sharp; no noise, haze, or
  vignette; real skin, no smoothing, no cinematic grade, no film grain.
- **Retro ~2016 old phone** (folksy/nostalgic characters): soft 720p-1080p, narrow dynamic range
  with blown windows/sky, warm-yellow white balance, faint shadow noise, slight compression — but
  never a stylized film-grain/vignette/aged filter; the degradation should read as honest, not as a
  look applied on top.

Both share: pore-level skin realism, no waxy or plastic/AI-smooth skin.

### Camera — alive, never produced

"Propped" or "handheld" always comes with its own imperfections written in:

- **Propped**: leaned against a real object (books, a vase, a teapot); opens with one soft
  settle-wobble as it finds its lean, then locks with a slight casual tilt and subtle sensor
  breathing.
- **Handheld selfie**: the character's own extended arm, a walking bob, mild wide-lens distortion;
  angle changes come from the character's own hand, never from a cut.
- **Handheld by another person**: natural standing micro-sway, one small human reframe.
- **Mounted in a vehicle**: locked framing that still carries the ride's true vibration and sway.

No spins or turns away from camera unless asked. All angle changes are motivated by the character's
own hands or body.

### ACTING TASK (talking/interview) or Performance (b-roll)

Never direct a result ("look sad") as the core instruction — direct an invested task instead: a
scene direction, a motive rooted in the character's backstory, a goal, an obstacle, a tactic, and
eye-work as action. Mark where the character's delivery breaks or shifts — that break is the
delivery. For b-roll, the equivalent is one small, complete physical action with a clear start and
end (not a pose, not several beats) — this is the "one action per clip" rule in practice.

Any signature gesture from the character's profile is rationed — used at one key beat, not every
clip, so it stays a trademark rather than a tic.

### Props, other people, and no-IP

- Any prop that moves exists from frame one, with a line stating it doesn't appear, disappear, or
  change design, and moves only in the scripted beat.
- Other people are at the edges of frame, soft-blurred, faces never visible.
- No real brands, logos, badges, number plates, readable signage, place names, or copyrighted
  music. Vehicles and products are generic, unbadged. Modest, fully-clothed styling throughout.

### Audio

Talking/interview: lip-synced exactly to `@audio1`, lips completely still when the audio is silent,
dialogue quoted verbatim from the approved script, an off-camera interviewer is off-mic with a
different timbre and never in frame, voice runs seamlessly across any cut. Silent b-roll: no
dialogue anywhere, only 3-5 specific diegetic sounds. No music in either case.

### On-screen text

Always `none. (Added in post by the team.)` — this skill never generates burned-in text. For silent
text-over b-roll specifically, also keep the **top third of the frame visually calm** so there's
room for the overlay the user will add afterward, and keep the clip loop-friendly where it suits the
idea (last pose close to the first).

### Shot breakdown

Timed beats keyed to the dialogue phrases or the single physical action, ending in a clean finish at
the clip's duration.

### Continuation clips specifically

Open with: "CONTINUE THE VIDEO from the last frame of the attached reference clip — seamlessly, with
no visual reset of any kind." All visuals (character, room, outfit, light, framing, camera position)
come from that last frame — don't redescribe framing, closeness, lighting, or location. Keep only:
top priority, reference key (`@video1` + `@audio1`), the resume line ("picks up mid-gesture exactly
where the last frame leaves them"), the acting task, minimal physics ("everything continues as in
the reference"), editing, audio, and the shot breakdown.

Present the full assembled prompt to the user and wait for approval before generating — this is the
second gate, and the one that actually guards credits.

## Phase 3 — Generate

Once the full prompt is approved, generate the clip through whatever Higgsfield/Seedance-capable
video tool is available in this session, attaching the character sheet, location still, and
voice/previous-clip references exactly as specified in the prompt's reference key. Show the result
and work with the user until it's approved.

If a render comes back with a known problem, fix the specific line that causes it rather than
rewriting the whole prompt:

| Symptom | Fix |
|---|---|
| Pasted-sticker character | RELIGHT block missing or weak — name key light direction + color bounce + contact shadows |
| Props appear out of nowhere | State the prop exists from frame one and only moves in its scripted beat |
| Sunrise/sunset compresses into a time-lapse | Add the light-stability line |
| Looks too polished/produced | Strengthen the "alive camera" language — settle-wobble, casual tilt, autofocus breath; remove any lingering "tripod"-style wording |
| Dead, glassy eyes | Rewrite the acting task around eye-work as action, plus a natural-blink safety line |
| Face drifts from the character sheet | Add "face and identity match @image1 100% for the entire take," with anchor wording identical to the profile |
| Overacting / puppet-like | Add "never staged, never stiff, never puppet-like"; lean on the task, not choreography |
| Wrong spoken language | State "speaks ONLY English throughout" (or the intended language) in both the top-priority list and the audio section |
| Doesn't fit in 30 seconds | Tighten pacing, or split into two clips with one hard cut / a Continuation prompt |

## Next

Once clips are approved, recommend running `/aia:accounts` next to prepare the character's email
and Instagram account materials, if that hasn't been done yet.
