---
name: voice
description: >
  Generate a detailed, lockable voice prompt for an AI influencer character built with /aia:avatar,
  then run the character's approved scripts through it and produce the audio files. Use whenever
  the user calls /aia:voice, asks for a voice for an AI avatar/character, wants a voice prompt
  (accent, age, register, energy), or wants scripts turned into voiced audio. Requires the
  character's profile — if it isn't already in context, ask for it rather than inventing one.
---

# AI Avatar Voice Generation (`/aia:voice`)

This skill has two stages: design the voice prompt and get it approved and locked, then use that
locked voice to render the character's scripts into audio. Don't render anything before the voice
itself is approved.

## Phase 0 — Get the character

Check whether the character's profile (name, niche, backstory, personality, age) is already present
earlier in this conversation. If not, ask for it rather than guessing — the voice has to match a
real character, not a generic one.

## Phase 1 — Collect the four basics

A voice prompt here always starts from four short inputs. Check whether the user already gave them
when invoking the skill (e.g. "I'm thinking elderly, posh British, slow"); if any are missing, ask
for them, suggesting sensible defaults drawn from the character's profile but letting the user
confirm or override each one:

1. **Accent** — the specific regional/national accent.
2. **Age** — matches the character's established age.
3. **Register — one word** (e.g. posh, gravelly, warm, sharp).
4. **Energy — one word** (e.g. slow, upbeat, blunt, gentle).

These four words are the seed. The actual prompt you write is a full paragraph built out from them
— not just the four words themselves.

## Phase 2 — Write the full voice prompt

Expand the four basics into one dense bracketed voice prompt, in the same spirit as these (study
what each one does, not just what it says):

> **Vivienne.** [voice: elderly woman, early 80s, refined aristocratic British accent (classic RP,
> genuinely posh, finishing-school diction), low velvety slightly smoky timbre with a natural light
> rasp of age, strong and controlled, never frail or shaky; slow deliberate pacing, entirely
> comfortable with pauses, every word placed with intention; dry amused delivery with a permanent
> hint of a knowing smirk in the voice; a signature drawled "darling", warm, indulgent and faintly
> condescending at once; the wisdom of old money: she never rushes, never raises her voice, never
> explains twice.]

> **Sienna.** [voice: young woman, early 20s, light natural British accent (soft South-East England
> / London, not posh, not heavy), casual conversational tone, energetic and hyped, warm big-sister
> girly energy, genuine audible smile in the voice.]

> **Amos.** [voice: speaking English, English language only, elderly man, mid-to-late 70s, deep
> weathered baritone with a slight gravelly rasp of age, calm and unhurried delivery, warm
> grandfatherly tone like he's sharing something he's proven true himself, measured pacing with
> natural deliberate pauses between phrases letting each line land, quiet certainty with no urgency
> or performance, faint audible smile on warmer lines, soft rural British English accent (gentle
> West Country lilt, countryside farmer cadence), recorded on a phone propped a few steps away
> outdoors on a wooden porch, voice slightly distant and off-axis from the mic, open-air ambience
> with faint birdsong and light breeze, lo-fi phone-mic texture]

Each of these builds the same four basics out into: a specific accent variant (not just "British" —
*which* British, described concretely), a timbre description, a pacing description, a delivery
quirk or two tied to the character's personality, and often a signature verbal tic consistent with
their catchphrase. Match that density — a one-line voice prompt is under-specified.

**Always include a disambiguating negation next to any accent or register word that has an obvious
stereotype nearby**, the same way these examples do ("not posh, not heavy" next to Sienna's casual
British accent; "never frail or shaky" next to Vivienne's age). Without it, voice models tend to
slide toward the nearest stereotype of that descriptor. Pick the specific stereotype this
character's combination of traits would otherwise fall into, and rule it out explicitly.

**Never name a real person** as a reference point for the voice (no "sounds like [celebrity]") —
describe the qualities directly instead.

If the character's content has a consistent recording context (e.g. always outdoors on a porch,
always close to a phone mic), it's fine to fold that into the prompt as texture, the way Amos's does
— but only when it's a real, established detail about how this character's content is shot, not
decoration added for its own sake.

## Phase 3 — Approve and lock

Present the full voice prompt to the user for approval. The rule here is **generate once and lock
it** — once approved, this voice prompt doesn't get regenerated wholesale. If something's off, the
user will say what, and you change exactly that one attribute (e.g. swap "upbeat" for "blunt", or
adjust the accent detail) while leaving everything else untouched, rather than rewriting the whole
prompt from scratch. Keep iterating this way until approved, then treat it as final.

## Phase 4 — Render the scripts

Once the voice is locked, run the character's approved scripts (from `/aia:content`) through it and
produce the audio files.

If the scripts aren't already present in this conversation, ask the user to paste them in or upload
the file containing them — don't invent or improvise script text here.

Generate audio through whatever voice-generation tool is available in this session (e.g. a
`create_voice` / `generate_audio` / `generate_audio_batch` tool), using the locked voice prompt for
every script so they all come out as the same consistent voice. Save/download each resulting audio
file and tell the user where to find them. If a script fails to render well, fix the issue with the
specific script or a targeted line in the voice prompt — not by relocking a different voice.

## Next

Once the audio is approved, recommend running `/aia:video` next to turn the character sheet,
locations, and this voice into actual video clips.
