# AI Avatar Plugin

Tools for creating and managing AI avatars.

## Plugin Metadata

- Name: `aia`
- Description: AI Avatar tools

## Available Commands

1. `/aia:avatar` — **Entry point skill.** Creates a character profile for an AI influencer in a given
   niche — name, backstory, one-line look, fixed signature anchors, a catchphrase, a contrast-based
   USP, and a reason they're online. If no niche is given, infers one from context and confirms with
   the user before building the character.
2. `/aia:images` — Generates the character's image set via Higgsfield: a locked face anchor, a
   3-panel character sheet (full body, side profile, frontal close-up, realistic unretouched skin),
   three or four niche-appropriate locations, and Instagram-style profile/candid photos using the
   Soul 2.0 model. Requires the character profile from `/aia:avatar`.
3. `/aia:content` — Researches the character's niche and proposes a ranked list of content ideas
   (opening line, format, setting, why it should work), then writes full 15-30 second scripts for
   the ideas the user picks. Requires the character profile and niche.
4. `/aia:voice` — Builds a detailed, lockable voice prompt (accent, age, register, energy, expanded
   into a full description) for the character, then renders their approved scripts into audio once
   the voice is approved. Requires the character profile, and the scripts to render.
5. `/aia:video` — Generates short vertical video clips (talking, interview, silent text-over
   b-roll, continuation) from the character sheet, a location still, and the locked voice, in three
   approved stages: short brief → full house-method prompt (with a mandatory relight block) → the
   rendered clip. Requires the character sheet and a location; talking/interview clips also need
   the locked voice and an approved script.

More skills will be added under `skills/`, each invoked as `/aia:<skill-name>`.
