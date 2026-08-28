# Step 00 — Read Spec and Explore Codebase

**Reads:** The SPEC.md path passed at invocation.

**Does:**

### Read the spec

Read the file at the provided path. Extract `<feature-id>` and `<idea-slug>` from the filename:
- `docs/01-auth-forms-SPEC.md` → feature-id = `01`, idea-slug = `auth-forms`
- `docs/02-youtube-funnel-SPEC.md` → feature-id = `02`, idea-slug = `youtube-funnel`

If the file does not exist, stop and tell the user.

Reuse this SAME `<feature-id>` for every file this skill writes (PRD and all issue files) — this PRD belongs to the same feature as the SPEC.md it was generated from, not a new one. Never mint a new id here.

### Explore the codebase

Explore the repo to understand current state. Search/grep for the relevant seams first, then read only the files or sections that inform the PRD — do not read whole directories or unrelated files end to end. Use the project's domain glossary vocabulary throughout. Respect any ADRs in the area being touched.

**Stop condition:** SPEC.md read, codebase explored.

**Hands off:** `<feature-id>`, `<idea-slug>`, SPEC.md content, and codebase context to `01-seams.md`.
