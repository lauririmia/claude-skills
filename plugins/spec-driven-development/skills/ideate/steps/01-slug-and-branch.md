# Step 01 — Slug and Branch

**Reads:** Optional `docs/<feature-id>-<slug>-<file-id>-DESIGN.md` path passed as invocation argument.

**Does:**

#### ⛔ CHECKPOINT 1 — Slug confirmation (MANDATORY, do not skip)

If a DESIGN.md path was passed as argument, parse it: given a name like `01-auth-forms-3-DESIGN.md`, `<feature-id>` is the numeric segment at the start (`01`). Strip the `.md` extension and the leading `<feature-id>-` prefix. Then strip the known type suffix from the right (`-DESIGN`). What remains ends with `-<file-id>` — that's the file's id (`3`). The rest, with that trailing numeric suffix removed, is `<idea-slug>` (`auth-forms`). Propose the slug and wait for explicit confirmation. Hold onto the `<feature-id>` too — it's this feature's id (see Checkpoint 2). The DESIGN.md's own `<file-id>` (`3`) is not reused — this skill's outputs get their own, freshly computed `<file-id>` (see `steps/05-sharpen.md`).

If no argument was passed, ask the user to describe what they want to explore, then derive the slug from their description. Propose it and wait for confirmation.

#### ⛔ CHECKPOINT 2 — Feature ID and session file (MANDATORY, do not skip)

Immediately after the slug is confirmed, determine `<feature-id>`:

1. If a DESIGN.md path was passed in Checkpoint 1, its id **is** `<feature-id>` — use it directly, no further lookup needed.
2. Otherwise, list `docs/` for any file matching `[0-9][0-9]-<idea-slug>-*.md`. If any match, this slug already has a feature id — use it. If none match, this slug has never been seen before: list `docs/` for **all** files matching `[0-9][0-9]-*.md` (any slug); `<feature-id>` is the highest two-digit prefix found, plus one — or `01` if none exist yet.

Reuse this same `<feature-id>` for every file this skill writes in this run.

Create or resume `docs/<feature-id>-<idea-slug>-SESSION.md`:

```markdown
# Ideate: <Idea Name>
Started: <YYYY-MM-DD>

## Summary
<one-paragraph description of what's being ideated>

## Decisions Reached
<!-- updated after each phase completes -->

## Open Questions
<!-- updated as new questions surface -->
```

**Checkpoint invariant:** If `docs/<feature-id>-<idea-slug>-SESSION.md` already exists, read it and resume — skip decisions already settled (e.g. a phase already confirmed).

#### Branch detection

Check whether `feature/<idea-slug>` already exists:
- If yes: announce *"Branch `feature/<idea-slug>` detected — reusing it."* Switch to it.
- If no: run **CHECKPOINT 3** — present exactly these three options and ask the user to choose one:
  - **1. main** — work directly on the current branch
  - **2. branch** — create and switch to `feature/<idea-slug>`
  - **3. worktree** — create a git worktree at `../<idea-slug>` on branch `feature/<idea-slug>` (isolated workspace)

  After the user picks, invoke `superpowers:using-git-worktrees` if option 3 was chosen.

**Stop condition:** Slug confirmed, feature ID determined, session file ready, branch resolved.

**Hands off:** Confirmed `<idea-slug>`, `<feature-id>`, and workspace state to `02-read-upstream.md`.
