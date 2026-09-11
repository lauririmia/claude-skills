# Step 00 — Read Spec and Explore Codebase

**Reads:** The SPEC.md path passed at invocation.

**Does:**

### Read the spec

Read the file at the provided path. Extract `<feature-id>` and `<idea-slug>` from the filename:

Dat fiind un nume ca `01-auth-forms-3-SPEC.md`: `<feature-id>` e segmentul numeric de la început (`01`). Elimină extensia `.md` și prefixul `<feature-id>-`. Elimină apoi sufixul de tip cunoscut din dreapta (`-SPEC`, `-DESIGN`, `-IDEATE`, `-PRD`). Ce rămâne se termină cu `-<file-id>` — acela e file-id-ul (`3`). Restul, fără acest sufix numeric final, e `<idea-slug>` (`auth-forms`).

- `docs/01-auth-forms-3-SPEC.md` → feature-id = `01`, idea-slug = `auth-forms` (file-id of the SPEC itself, `3`, is not reused)
- `docs/02-youtube-funnel-1-SPEC.md` → feature-id = `02`, idea-slug = `youtube-funnel`

If the file does not exist, stop and tell the user.

Reuse this SAME `<feature-id>` and `<idea-slug>` for every file this skill writes (PRD and all issue files) — this PRD belongs to the same feature as the SPEC.md it was generated from, not a new one. Never mint a new feature-id or idea-slug here. The `<file-id>` of the input SPEC.md is NOT reused — each new file this skill writes (PRD.md, then each ISSUE-N.md) gets its own freshly computed `<file-id>`, per `steps/02-write-prd.md` and `steps/04-write-issues.md`.

### Explore the codebase

Explore the repo to understand current state. Search/grep for the relevant seams first, then read only the files or sections that inform the PRD — do not read whole directories or unrelated files end to end. Use the project's domain glossary vocabulary throughout. Respect any ADRs in the area being touched.

**Stop condition:** SPEC.md read, codebase explored.

**Hands off:** `<feature-id>`, `<idea-slug>`, SPEC.md content, and codebase context to `01-seams.md`.
