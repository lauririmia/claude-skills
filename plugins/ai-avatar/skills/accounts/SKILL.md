---
name: accounts
description: >
  Prepare the account creation materials for an AI influencer character built with /aia:avatar —
  full name, date of birth, username and a strong unique password for an email account, and name,
  username, password, profile picture pick, and bio for an Instagram account. Use whenever the user
  calls /aia:accounts, asks to set up/create accounts, an email, or an Instagram profile for an AI
  avatar/influencer character. Requires the character's profile — if it isn't already in context,
  ask for it or ask which file has it, rather than inventing one.
---

# AI Avatar Accounts (`/aia:accounts`)

This skill prepares everything the user needs to **create the accounts themselves** — it never
creates an account, enters a password into a site, or signs up for anything on the user's behalf.
Account creation and entering credentials are always the user's own action; this skill's job stops
at handing over complete, ready-to-use account materials.

## Phase 0 — Get the character

Check whether the character's profile (name, niche, age, personality, catchphrase) is already
present earlier in this conversation. If not, ask the user to provide it, or tell you which file
contains it (then read that file) — don't invent a character to fill the gap.

## Phase 1 — Email account

Produce:

- **Full name** — consistent with the character's profile. If the profile only gives a first name,
  pick a surname that fits the character's background and confirm it with the user rather than
  silently inventing one.
- **Date of birth** — a specific day, month, and year consistent with the character's established
  age (as of today). Pick one and show it; let the user adjust it if they want a different exact
  date.
- **Username** — `first_name.last_name` format, lowercase.
- **Password** — a random 20-character password containing lowercase, uppercase, numbers, and
  special characters. Generate it fresh — don't reuse a password from elsewhere in this skill.

Present these clearly labeled, and remind the user the password is shown here in plain text, so
it's worth moving straight into a password manager rather than leaving it sitting in chat history.

## Phase 2 — Instagram account

Produce:

- **Name** — the character's name plus a search term for the niche (e.g. "Amos health and
  wellness," "Vivienne money and wealth").
- **Username** — the bare character name plus something from their world — a catchphrase fragment,
  a signature detail, a nickname (e.g. `amos.oldways`, `sienna.saysso`, `vivienne.darling`).
- **Password** — another random 20-character password (same character rules as the email password)
  — **different from the email password and from every other account's password** for this
  character.
- **Profile picture** — point to one of the Instagram-style photos already generated for this
  character in `/aia:images` Phase 3 (the profile picture shot). If that phase hasn't been run yet
  for this character, say so and suggest running `/aia:images` first rather than picking a
  placeholder.
- **Bio** — three things, in the character's voice: who they are, a reason to follow, and an AI
  disclosure. Study the pattern in these examples rather than copying their wording:

  > Amos
  > 101 years old 🌾
  > Growing older, staying younger
  > Simple habits for peak energy, focus and longevity
  > Your AI grandpa

  > Sienna
  > Sienna Saysso | Relationship Advice
  > Giving great dating advice I'll never follow. 🤫✨
  > Your AI bestie

  > Vivienne
  > Grandma Vivienne | Money & Wealth Advice
  > Marry rich? Darling, I am the rich husband 💅💎
  > Teaching you how to stack cash and break ceilings ✨💼
  > Your AI grandma 👑

  Each one opens with an identity/age or niche hook, states the value proposition in the
  character's own voice, and closes with a short, unmissable "Your AI \_\_\_\_" line as the
  disclosure — keep that closing disclosure line in every bio this skill writes, in whatever form
  fits the character's voice.

Present the full set, and let the user adjust any piece before treating it as final.

More account types can be added to this skill the same way as these two — each one producing its
own full name/username/password/bio-style materials, never performing the signup itself.

## Next

Once the accounts are set up, recommend running `/aia:product` next to build this character's
first sellable digital product.
