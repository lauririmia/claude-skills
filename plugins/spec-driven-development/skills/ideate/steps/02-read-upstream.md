# Step 02 — Read Upstream Artifact

**Reads:** `<idea-slug>` from `01-slug-and-branch.md`; optional `docs/<feature-id>-<slug>-<file-id>-DESIGN.md`.

**Does:**

If a DESIGN.md path was passed as the invocation argument, read that exact path and announce:
*"Found `docs/<feature-id>-<slug>-<file-id>-DESIGN.md` — starting from confirmed intent."*

If no path was passed, check whether a DESIGN.md exists anyway for this `<feature-id>-<idea-slug>` before falling back to a raw description: search with the glob `docs/<feature-id>-<idea-slug>-*-DESIGN.md`. If more than one result comes back, use the one with the highest `<file-id>`. If found, read it and make the same announcement as above. If none is found, proceed with no upstream seed.

Use the DESIGN.md content (if any) as the seed for Phase 1.

**Stop condition:** Upstream content read (or confirmed absent).

**Hands off:** Seed content (or none) to `03-diverge.md`.
