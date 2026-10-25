---
name: finalize
description: Finalizes a development branch by committing all pending changes, creating or updating the root README.md and CLAUDE.md (without duplicating information between them), and then guiding the merge/PR flow. Use when the user says "finalize", "finish", "done with implementation", "merge this", "sdd:finalize", or wants to wrap up and integrate their work into main/master.
---

# SDD Finalize — Commit and Complete Development Branch

Commits all pending changes on the current branch (or worktree), makes sure the repo root has an up-to-date README.md and CLAUDE.md (creating them if missing, and keeping each fact in only one of the two), then hands off to `superpowers:finishing-a-development-branch` for merge/PR options. On a local merge into main, tags the merge commit with the feature's slug.

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
- **Summarize README/CLAUDE.md edits instead of dumping them.** Step 3 creates and edits these files directly, without asking first — report what changed as a one-line-per-file summary ("creat" / "actualizat" / "la zi", plus any content moved to avoid duplication), not the full file contents, the full diff, or the full branch diff that led to it. If more than ~5 sections changed across both files, give a one-line count + the most significant ones instead of listing every edit.
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

Note whether the changes committed here included anything other than documentation (`docs/`, README, CLAUDE.md). If they did — typically leftover code edits after `sdd:revise` — that code postdates the last test run; remember this as **untested code committed**, because Step 4's post-merge check depends on it.

### Step 3 — Create or update README.md / CLAUDE.md, without duplication

The two files have different readers, and that difference is what decides where each fact goes:

- **README.md** is for humans arriving at the repo: what the project is, how to install and use it, a short overview of what it contains.
- **CLAUDE.md** is for Claude working inside the repo: directory structure, conventions, workflows and commands to follow, constraints and gotchas that aren't obvious from reading the code.

Check whether a README and/or a CLAUDE file exist at the repo root, matched **case-insensitively** — `README.md`, `Readme.md`, `readme.md`, `ReadME.md`, and likewise for `CLAUDE.md`, all refer to the same file on a case-insensitive filesystem (macOS default) but are genuinely distinct paths on a case-sensitive one (Linux), so an exact-case check can silently miss the real file:

```bash
find . -maxdepth 1 -iname 'readme.md' -o -maxdepth 1 -iname 'claude.md'
```

Use whatever casing `find` actually reports for the rest of this step (don't assume it's `README.md`/`CLAUDE.md`). The repos this skill runs in may have both, one, or neither, in any casing — do not assume either exists or guess its casing.

#### 3a — Create whichever file is missing

For each file that does not exist, create it at the repo root (using the canonical `README.md` / `CLAUDE.md` casing) and populate it from what the repo actually contains — read the top-level layout, manifests (`package.json`, `plugin.json`, `pyproject.toml`, etc.), existing docs under `docs/`, and the branch's diff stat. Write only what you can verify from the repo; an accurate short file beats a long speculative one, since a wrong CLAUDE.md actively misleads future sessions.

- A new README.md covers: project name and one-line purpose, install/usage, and a brief overview of the main parts.
- A new CLAUDE.md covers: directory structure, conventions and workflows to follow, and non-obvious constraints. When the README already holds something Claude also needs (e.g., install steps), don't copy it — point to it.

Write both in English, like the other deliverables of this skill.

#### 3b — Update stale content

For files that already existed, compare what changed on this branch against what they describe:

```bash
git diff <merge-base>...HEAD --stat
```

(Use the branch's actual merge-base with its base branch — same target this skill's downstream `finishing-a-development-branch` step reasons about.) Skim the stat output and touched paths rather than the full diff — you're looking for the kind of change that makes documentation wrong, not every line changed. Things that typically warrant an update: a new skill or plugin added, a structural change to how the repo is organized, a workflow or install/update instruction that changed, a new dependency the docs promise doesn't exist yet. Most commits (bug fixes, internal refactors, test-only changes) don't touch what README/CLAUDE.md describe — don't propose an edit just because *something* changed.

If something does, update the affected file, putting each new fact in the file whose reader needs it (see the split above).

#### 3c — Remove duplication between the two files

Whether the files were just created, just edited, or already up to date, read both and make sure no piece of information appears in both. Duplicates drift apart over time and leave two conflicting versions of the truth, so each fact should live in exactly one place:

- **Keep it in CLAUDE.md** if it is about working inside the repo: structure, conventions, workflows, constraints.
- **Keep it in README.md** if it is for someone discovering or using the project: purpose, install, usage.
- If it genuinely serves both readers, keep the full version in one file and leave at most a one-line pointer in the other (e.g., "See CLAUDE.md for repo structure and conventions.").

Remove the duplicate from the file that shouldn't own it. This applies to existing content too, not only to what this step wrote.

#### 3d — Commit the result

If nothing changed in 3a-3c, say so in one line ("README/CLAUDE.md sunt la zi și fără duplicări.") and move on.

Otherwise apply everything directly — do not propose edits and wait for approval first. Stage any newly created files (`git add`), then fold the changes into the commit from Step 2 with `git commit --amend --no-edit` if that commit hasn't been pushed anywhere yet (check with `git status -sb` or `git log @{u}..HEAD` — if the branch has no upstream, or HEAD is still ahead of it, amending is safe); if Step 2 made no commit, or the commit was already pushed, create a small separate commit ("docs: update README/CLAUDE.md for <branch>") rather than rewriting already-pushed history. Report what was done in one line per file per the Output and Context Rules above (e.g., "CLAUDE.md creat: structură, convenții, workflow-uri." / "README.md actualizat: secțiunea de structură mutată în CLAUDE.md.") — the user sees the result, not a pre-edit proposal.

### Step 4 — Finish the branch

Tests were already run during `sdd:implement` and `sdd:verify` — do not ask the user whether to re-run them, and do not re-run them before the merge. The one exception is the post-merge check inside Option 1 (Merge Locally), which runs only when the merge result could differ from the code already tested. Invoke `superpowers:finishing-a-development-branch` to handle the remainder:

> Using `superpowers:finishing-a-development-branch` to complete the branch.

Always include these two overrides with the invocation:

> **OVERRIDE:** Tests were already verified during `sdd:implement`/`sdd:verify` in this same session — skip Step 1 (test verification) and proceed directly to Step 2 (Detect Environment).
>
> **OVERRIDE (Option 1, Merge Locally):** After `git pull` and `git merge`, before running "Verify tests on merged result", compare the code that was tested with the code that was merged: `git rev-parse HEAD^{tree}` (the base branch after the merge) against `git rev-parse <feature-branch>^{tree}` (the feature branch tip, i.e. what was tested). If the two tree ids are identical — and Step 2 did not record *untested code committed* — skip the test command and say in one line that the merged tree is identical to the tested one. In every other case (the ids differ, or untested code was committed) run the test command as usual and treat a failure exactly as that skill describes.

Why the comparison happens after the merge and not before: `git pull` runs as part of the merge, so the base branch can still advance at that moment (a colleague pushed while the feature was in progress). The tree ids answer the real question — "is what is now on the base branch exactly what the tests ran on?" — whether the merge was a fast-forward, a plain merge commit with no other changes, or one that pulled in someone else's work or needed conflict resolution (those produce a different tree, so the check runs). A green suite proves only the tree it ran on; when the tree is the same, a second run of a long suite adds nothing.

This skill will then:
1. Detect environment (normal repo vs worktree)
2. Present options: merge locally, create PR, keep as-is, or discard
3. Execute the chosen option and clean up if applicable

Follow that skill's instructions exactly from this point forward, but relay only decision points and outcomes to the user, per the Output and Context Rules above.

### Step 5 — Tag the merge commit (local-merge outcome only)

If Step 4 resulted in anything other than a **local merge into the repo's main branch** (a PR, "keep as-is", or a discard), skip this step entirely — there is no new commit on the main branch yet to tag, or the branch is going away. A PR's eventual merge is out of this skill's control and out of scope here.

If Step 4 did merge locally into the main branch, tag that merge commit with the feature's slug:

1. **Determine the slug.** Two sources, in order of preference:
   - The current branch name, if it carries the slug directly (branches created by `superpowers:using-git-worktrees` or other skills in this plugin are typically named after the slug, e.g. `auth-forms` or `feature/auth-forms`) — branch names never carry a feature-id prefix, only the slug.
   - `docs/<feature-id>-<slug>-<file-id>-SPEC.md` / `docs/<feature-id>-<slug>-<file-id>-PLAN.md` / `docs/<feature-id>-<slug>-<file-id>-PLAN-N.md` files touched on this branch (`git diff --name-only <merge-base>...HEAD -- docs/`) — extract the slug by stripping the leading two-digit `<feature-id>-` prefix, the trailing `-SPEC`/`-PLAN`/`-PLAN-N` type suffix, AND the numeric `<file-id>` segment that remains just before that suffix (e.g. `03-auth-forms-9-PLAN-1.md` → strip `03-` and `-PLAN-1` → `auth-forms-9` → strip the trailing `-9` → `auth-forms`). The tag itself must be the bare slug — never include `<feature-id>` or `<file-id>`.

   If both sources point to the same slug, or only one source yields a slug, use it directly — no need to ask. If they disagree, or neither yields anything, ask the user once, briefly: *"Care e slug-ul feature-ului pentru tag? (ex: auth-forms)"* — do not let this block or unwind the merge that already happened; the tag can be added after the fact once you have an answer.

2. **Check for a name collision:** `git tag -l <slug>`. If a tag with that name already exists, tell the user in one line and ask how to proceed — overwrite (`git tag -f`), use a different name, or skip tagging — rather than silently overwriting an existing tag.

3. **Create the tag** on the merge commit: `git tag <slug> <merge-commit-sha>`. A lightweight tag is enough — this marks a feature's landing point for reference, not a release, so it doesn't need the annotation metadata (tagger, date, message) an annotated tag carries.

4. **Do not push the tag.** Pushing is a shared-state operation outside this skill's scope, same as it is for branches/commits elsewhere in this process — leave it for the user or the existing push flow to do explicitly.

Report the outcome in one line ("Tag `<slug>` creat pe commit-ul de merge.") or the reason it was skipped, per the Output and Context Rules above.
