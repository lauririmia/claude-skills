---
name: ideate
description: Divergent/convergent exploration of the solution space before writing a spec. Use when intent is known but direction is unclear. Reads DESIGN.md if available. Produces docs/<feature-id>-<slug>-IDEATE.md. Handoff goes to sdd:spec.
---

# Ideate — Solution Space Exploration

Answers "how might this look?" through three structured phases: diverge, converge, sharpen. Does not write a spec — only narrows direction before design.

## Model & Thinking

Use **Claude Sonnet** (`claude-sonnet`) with **high thinking effort** (`ultrathink`) for all reasoning in this skill.

## Language

Conduct all dialogue with the user — questions, confirmations, status updates — exclusively in Romanian, regardless of the language the input document or user description was written in.

`docs/<feature-id>-<idea-slug>-SESSION.md` is a scratch file that never leaves this skill and is deleted before handoff (see Output below) — write it in Romanian, matching the dialogue it mirrors.

`docs/<feature-id>-<idea-slug>-IDEATE.md` starts in Romanian too: `steps/05-sharpen.md` writes the initial draft in Romanian so the user reviews and approves it in the same language as the rest of the conversation. The moment the user gives explicit approval, translate the file in place into English, before handing off to `steps/06-commit-and-handoff.md` — see that step for the translation instruction. From that point on the committed `IDEATE.md` and its handoff to `sdd:spec` are in English, because the rest of the plugin's tooling (and the spec skill's own artifacts) works in English.

## Invocation

```
/sdd:ideate docs/<feature-id>-<slug>-DESIGN.md    ← recommended: starts from confirmed intent
/sdd:ideate                                        ← no input: derive slug interactively
```

The input path (if given) already carries `<feature-id>` — this skill's own outputs (IDEATE.md, SESSION.md) reuse that exact same id, since IDEATE.md belongs to the same feature as the DESIGN.md it followed (see `steps/01-slug-and-branch.md`).

## Feature ID Prefix

Every file this skill writes under `docs/` is named `<feature-id>-<idea-slug>-TYPE.md`. `<feature-id>` identifies the feature (this slug) — it's the same id the upstream DESIGN.md (if any) already carries, or a freshly assigned one if this slug has never been seen before. It is never part of the slug itself: the slug alone names branches and tags (see `sdd:finalize`). `steps/01-slug-and-branch.md` computes it right after the slug is confirmed.

## Output and Context Rules

This skill generates lists (variations, directions) — the risk here is genuine volume, not just echoed files. Apply these rules throughout:

- Phase 1 (diverge): generate at most 5–8 variations, never more. Each variation is one label + one line — not a paragraph. Do not justify every variation at length; a single sharp sentence per idea is enough.
- Phase 2 (converge): cluster into at most 2–3 directions. Present each direction's stress-test (user value, feasibility, differentiation) and hidden assumptions as short bullets, not prose paragraphs — one line per bullet.
- Phase 3 (sharpen): keep "Recommended Direction" to 2–3 paragraphs max, as already specified in `steps/05-sharpen.md`. Do not restate the full Phase 1/2 history inside IDEATE.md — only the confirmed outcome.
- When reading an upstream `docs/<feature-id>-<slug>-DESIGN.md` (`steps/02-read-upstream.md`), do not print its contents back to the user — announce that it was found and used as seed, nothing more.
- After writing `docs/<feature-id>-<idea-slug>-IDEATE.md`, do not print its full contents in the console — the review request already points the user at the file path.
- Read files under `steps/` one at a time, immediately before executing that step — not all seven upfront.
- Never dump raw file contents, git output, or command logs into the conversation. State the one-line conclusion instead.
- Between phases, give a one-line status update, not a recap of everything generated so far.
- If ever unsure how much detail to show, default to the shorter option — fewer, sharper items beat an exhaustive list.

## Process

Read and follow each file in `steps/` **one at a time, in numeric order, immediately before executing it**. Each step file is mandatory context for its own step — do not pre-load later step files, and do not rely on the index summary below as a substitute for reading the step file itself.

1. `steps/00-setup.md` — git dirty-state check, enter plan-mode
2. `steps/01-slug-and-branch.md` — slug confirmation, session file, branch detection (Checkpoints 1-3)
3. `steps/02-read-upstream.md` — read upstream DESIGN.md if available
4. `steps/03-diverge.md` — Phase 1: Diverge
5. `steps/04-converge.md` — Phase 2: Converge
6. `steps/05-sharpen.md` — Phase 3: Sharpen, write IDEATE.md
7. `steps/06-commit-and-handoff.md` — commit, handoff

## Output

- `docs/<feature-id>-<idea-slug>-IDEATE.md` — structured direction document. Written once, not echoed back to the user after writing.
- `docs/<feature-id>-<idea-slug>-SESSION.md` — scratch file used only to survive context compaction mid-session; deleted (not committed) once IDEATE.md is written. Never printed to the user.

## Hard Rules

- Do NOT skip Phase 1 and 2 and jump straight to Phase 3
- Do NOT validate weak ideas without pushing back
- Do NOT write `docs/<feature-id>-<idea-slug>-IDEATE.md` before Phase 2 direction is confirmed by the user
- Do NOT write code or invoke other skills
- Do NOT generate more than 5–8 variations in Phase 1 or more than 2–3 directions in Phase 2
- Do NOT print full file contents (DESIGN.md, IDEATE.md, SESSION.md, git output, command logs) in the conversation unless the user explicitly asks to see them
- `IDEATE.md` is Romanian until the user approves at the end of `05-sharpen.md`, then English from that point on — never commit or hand off to `06-commit-and-handoff.md` with a Romanian `IDEATE.md` still on disk
