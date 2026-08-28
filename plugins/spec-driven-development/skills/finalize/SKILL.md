---
name: finalize
description: Finalizes a development branch by committing all pending changes and then guiding the merge/PR flow. Use when the user says "finalize", "finish", "done with implementation", "merge this", "sdd:finalize", or wants to wrap up and integrate their work into main/master.
---

# SDD Finalize — Commit and Complete Development Branch

Commits all pending changes on the current branch (or worktree), then hands off to `superpowers:finishing-a-development-branch` for merge/PR options. On a local merge into main, tags the merge commit with the feature's slug.

## Model & Thinking

Use **Claude Haiku** (`claude-haiku`) with **medium thinking effort** for all reasoning in this skill. This skill is orchestration, not judgment — checking git status, delegating to `commit-message`, and handing off to `finishing-a-development-branch` — so it does not need a larger model.

## Language

Conduct all dialogue with the user — questions, status updates, presented options — exclusively in Romanian, regardless of the language used elsewhere in the session.

All deliverables this skill produces or drives (commit messages, merge/PR content) must always be written in English, independent of the Romanian dialogue above.

## Output and Context Rules

This skill orchestrates git operations and other skills — the risk here is echoing raw command output or another skill's full output instead of a short conclusion. Apply these rules throughout:

- Never paste raw `git status --short` (or any git command) output into the conversation. Summarize it in one line (e.g., "3 fișiere modificate, niciun fișier nou" or "niciun fișier modificat — sar la Step 3").
- After `commit-message` completes, report only the commit message subject line and the fact that it succeeded — do not reproduce the full diff or the full body of the commit message unless the user asks.
- When invoking `finishing-a-development-branch`, relay only the decision points and final outcome to the user (options presented, choice made, result) — do not reproduce that skill's internal logs, git command output, or intermediate reasoning in the conversation.
- **Summarize README/CLAUDE.md edits instead of dumping them.** Step 3 applies changes directly, without asking first — report what changed as a one-line-per-file summary, not the full diff or the full branch diff that led to it. If more than ~5 sections changed across both files, give a one-line count + the most significant ones instead of listing every edit.
- If any step's underlying command fails or produces an error, report the one-line cause, not the full stack trace or raw error dump — offer to show more only if the user asks.
- Default to the shortest accurate status update between steps (e.g., "Commit creat." / "Testele au fost deja verificate — sar peste re-rulare." / "README/CLAUDE.md sunt la zi.").

## Process

### Step 1 — Check for pending changes

```bash
git status --short
```

If there are **no staged or unstaged changes** and no untracked files relevant to the work, skip to Step 3.

If there are pending changes, proceed to Step 2. Do not print the raw command output — summarize per the Output and Context Rules above.

### Step 2 — Commit all changes

Invoke the `commit-message` skill to stage and commit everything:

> Using `commit-message` to stage and commit all pending changes.

The `commit-message` skill will:
- Stage all modified and new files
- Generate a descriptive commit message
- Create the commit

Wait for the commit to complete before proceeding. Report only the commit subject line back to the user.

### Step 3 — Check README.md / CLAUDE.md for staleness

Check whether a README and/or a CLAUDE file exist at the repo root, matched **case-insensitively** — `README.md`, `Readme.md`, `readme.md`, `ReadME.md`, and likewise for `CLAUDE.md`, all refer to the same file on a case-insensitive filesystem (macOS default) but are genuinely distinct paths on a case-sensitive one (Linux), so an exact-case check can silently miss the real file:

```bash
find . -maxdepth 1 -iname 'readme.md' -o -maxdepth 1 -iname 'claude.md'
```

Use whatever casing `find` actually reports for the rest of this step (don't assume it's `README.md`/`CLAUDE.md`). This project has a README at the root but no root CLAUDE file; other repos this skill runs in may have both, one, or neither, in any casing — do not assume either exists or guess its casing.

If **neither file exists**, note it in one line ("Niciun README.md sau CLAUDE.md la rădăcină — sar peste acest pas.") and move on to Step 4. Do not create either file.

If **one or both exist**, compare what changed on this branch against what those files describe:

```bash
git diff <merge-base>...HEAD --stat
```

(Use the branch's actual merge-base with its base branch — same target this skill's downstream `finishing-a-development-branch` step reasons about.) Skim the stat output and touched paths rather than the full diff — you're looking for the kind of change that makes documentation wrong, not every line changed. Things that typically warrant an update: a new skill or plugin added, a structural change to how the repo is organized, a workflow or install/update instruction that changed, a new dependency the docs promise doesn't exist yet. Most commits (bug fixes, internal refactors, test-only changes) don't touch what README/CLAUDE.md describe — don't propose an edit just because *something* changed.

If nothing rises to that bar, say so in one line ("README/CLAUDE.md sunt la zi.") and move on.

If something does, apply the edits directly — do not propose them and wait for approval first. Fold them into the commit from Step 2 with `git commit --amend --no-edit` if that commit hasn't been pushed anywhere yet (check with `git status -sb` or `git log @{u}..HEAD` — if the branch has no upstream, or HEAD is still ahead of it, amending is safe); otherwise create a small separate commit ("docs: update README/CLAUDE.md for <branch>") rather than rewriting already-pushed history. Report what was changed in one line per file per the Output and Context Rules above (e.g., "README.md actualizat: adăugat pluginul `foo` în tabelul de plugin-uri.") — the user sees the result, not a pre-edit proposal.

### Step 4 — Finish the branch

Tests were already run during `sdd:implement` and `sdd:verify` — do not ask the user whether to re-run them, and do not re-run them here. Invoke `superpowers:finishing-a-development-branch` to handle the remainder:

> Using `superpowers:finishing-a-development-branch` to complete the branch.

Always include this override with the invocation:

> **OVERRIDE:** Tests were already verified during `sdd:implement`/`sdd:verify` in this same session — skip Step 1 (test verification) and proceed directly to Step 2 (Detect Environment).

This skill will then:
1. Detect environment (normal repo vs worktree)
2. Present options: merge locally, create PR, keep as-is, or discard
3. Execute the chosen option and clean up if applicable

Follow that skill's instructions exactly from this point forward, but relay only decision points and outcomes to the user, per the Output and Context Rules above.

### Step 5 — Tag the merge commit (local-merge outcome only)

If Step 4 resulted in anything other than a **local merge into the repo's main branch** (a PR, "keep as-is", or a discard), skip this step entirely — there is no new commit on the main branch yet to tag, or the branch is going away. A PR's eventual merge is out of this skill's control and out of scope here.

If Step 4 did merge locally into the main branch, tag that merge commit with the feature's slug:

1. **Determine the slug.** Two sources, in order of preference:
   - The current branch name, if it carries the slug directly (branches created by `superpowers:using-git-worktrees` or other skills in this plugin are typically named after the slug, e.g. `auth-forms` or `feature/auth-forms`).
   - `docs/<slug>-SPEC.md` / `docs/<slug>-PLAN.md` / `docs/<slug>-PLAN-N.md` files touched on this branch (`git diff --name-only <merge-base>...HEAD -- docs/`) — the slug is the filename prefix before `-SPEC`/`-PLAN`.

   If both sources point to the same slug, or only one source yields a slug, use it directly — no need to ask. If they disagree, or neither yields anything, ask the user once, briefly: *"Care e slug-ul feature-ului pentru tag? (ex: auth-forms)"* — do not let this block or unwind the merge that already happened; the tag can be added after the fact once you have an answer.

2. **Check for a name collision:** `git tag -l <slug>`. If a tag with that name already exists, tell the user in one line and ask how to proceed — overwrite (`git tag -f`), use a different name, or skip tagging — rather than silently overwriting an existing tag.

3. **Create the tag** on the merge commit: `git tag <slug> <merge-commit-sha>`. A lightweight tag is enough — this marks a feature's landing point for reference, not a release, so it doesn't need the annotation metadata (tagger, date, message) an annotated tag carries.

4. **Do not push the tag.** Pushing is a shared-state operation outside this skill's scope, same as it is for branches/commits elsewhere in this process — leave it for the user or the existing push flow to do explicitly.

Report the outcome in one line ("Tag `<slug>` creat pe commit-ul de merge.") or the reason it was skipped, per the Output and Context Rules above.
