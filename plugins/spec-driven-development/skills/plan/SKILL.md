---
name: plan
description: Transforms a SPEC.md, PRD.md, or ISSUE-N.md into a concrete TDD implementation plan saved as docs/<feature-id>-<idea-slug>-<file-id>-PLAN.md (or PLAN-N.md for issues). Enters plan-mode, invokes writing-plans, then runs an OpenAI Codex adversarial review of the drafted plan (task-level test coverage, ordering/dependencies, interface correctness, DoD-readiness — up to 5 rounds by default, extendable on request) before committing it. Stops before execution. When invoked with a PRD.md or ISSUE-N.md (complex workflow after /prd), first confirms slug and sets up a branch or worktree before planning. Use when user says "plan me", "plan this", "make a plan from", or wants to turn a spec, PRD, or issue into a step-by-step implementation plan.
---

# Plan-Me — Spec, PRD, or Issue to Implementation Plan

Reads a SPEC.md, PRD.md, or ISSUE-N.md file, produces a TDD implementation plan, then has OpenAI Codex adversarially review that plan before it lands. Stops before execution.

Two phases, two jobs:
- **Phase 1** (you ↔ Claude, via `writing-plans`) fixes the #1 failure mode: a plan that skips or misorders work.
- **Phase 2** (Claude ↔ Codex) fixes the #2 failure mode: a plan that reads fine but has gaps — missing test coverage per task, hidden ordering/dependency issues, wrong assumptions about the existing codebase, DoD gaps — that would otherwise only surface, expensively, across many `/verify` → `/revise` cycles after implementation.

## Model & Thinking

Use **Claude Sonnet** (`claude-sonnet`) with **high thinking effort** (`ultrathink`) for all reasoning in this skill.

## Language

Conduct all dialogue with the user — questions, checkpoints, granularity choices, status updates, Act 2 round summaries — exclusively in Romanian, regardless of the language the input file was written in.

All deliverables this skill writes (`docs/<feature-id>-<idea-slug>-<file-id>-PLAN.md` or `PLAN-N.md`, `docs/<feature-id>-<idea-slug>-<review-file-id>-PLAN-REVIEW.md` or `PLAN-N-REVIEW.md`, commit messages) must always be written in English, independent of the Romanian dialogue above. This applies to the `writing-plans` invocation too: hold the interview in Romanian, but write the plan document itself in English. Act 2's Codex exchange is also English throughout (Codex is prompted in English; only Claude's summaries of it back to the user are translated to Romanian).

## Invocation

Pass the input file path explicitly:

> `/plan-me docs/<feature-id>-<idea-slug>-<file-id>-SPEC.md`
> `/plan-me docs/<feature-id>-<idea-slug>-<file-id>-PRD.md`
> `/plan-me docs/<feature-id>-<idea-slug>-<file-id>-ISSUE-N.md`

If no path is provided, stop and ask: *"Please specify the input file path, e.g. `docs/01-auth-forms-3-SPEC.md`, `docs/01-auth-forms-2-PRD.md`, or `docs/01-auth-forms-5-ISSUE-1.md`."*

## Feature ID Prefix

Every file this skill writes under `docs/` (`PLAN.md`/`PLAN-N.md` and `PLAN-REVIEW.md`/`PLAN-N-REVIEW.md`) is named `<feature-id>-<idea-slug>-<file-id>-TYPE.md`, reusing the SAME `<feature-id>` carried by the input file's own filename — this plan belongs to the same feature as the SPEC/PRD/ISSUE it was generated from, not a new one — but each gets its OWN newly-computed `<file-id>` (see Algorithm A in Step 1). This skill writes two files: `PLAN.md` in Step 4 and `PLAN-REVIEW.md` at the start of Act 2 — each gets its own `<file-id>`, computed sequentially, so `PLAN-REVIEW.md`'s file-id lands one higher than `PLAN.md`'s (e.g. if `PLAN.md` gets file-id `4`, `PLAN-REVIEW.md` gets `5`, not `4` again), the same chaining spec.md uses for `SPEC.md`/`SPEC-REVIEW.md`. See Step 1 below.

## Output and Context Rules

These rules govern everything this skill prints to the main conversation — the `writing-plans` invocation and the generated plan document itself are unaffected.

- **Never paste full file contents into the chat.** Do not quote the SPEC/PRD/ISSUE input, the predecessor log, or the generated plan verbatim in the conversation — refer to them by path. OVERRIDE 5 already keeps the plan itself out of the console; extend the same discipline to every file this skill reads.
- **Never dump Codex's raw JSON or full verdict text into the chat.** In Act 2, `PLAN-REVIEW.md` keeps the full transcript on disk (per "Each round" below); when relaying a round to the user, summarize in 3-5 bullets (the most material issues) plus the verdict line — do not read or paste the entire contents of `/tmp/codex-plan-verdict.txt` into the conversation.
- **Checkpoints and choices stay short.** Present the fixed option lists (branch strategy, granularity, the round-checkpoint continue/stop choice) exactly as specified, with no extra restating of file contents or prior context around them.
- **Status updates are one line each** ("Step 1: input read, slug=`auth-forms`", "Act 2 round 2: REVISE, 2 findings addressed", "Step 6: plan committed") — no recap of steps or rounds already completed.
- **If the predecessor log or `git diff` reveals a discrepancy, summarize it in 1-3 lines** in the generated plan (as already specified in Step 1), not as a full quoted diff in the chat.
- **At a round checkpoint, list open points compactly** (one line per point), not the full round-by-round history already stored in `PLAN-REVIEW.md`.
- **Default to the minimal useful output.** If unsure how much detail to show in dialogue, show less and offer to expand on request.

## Process

### Step 1 — Read the input file

Read the file at the provided path. If it does not exist, stop and tell the user.

Determine the **input type** and extract `<feature-id>`, `<idea-slug>`, and `<file-id>` from the input filename, then compute the output path — the output reuses the SAME `<feature-id>` as the input, since the plan belongs to the same feature, but gets its OWN newly-computed `<file-id>`:

Given a name like `01-auth-forms-3-SPEC.md` or `01-auth-forms-5-ISSUE-1.md`: `<feature-id>` is the numeric segment at the start (`01`). Strip the `.md` extension and the `<feature-id>-` prefix. Then strip the known type suffix from the right (`-SPEC`, `-PRD`, or `-ISSUE-<N>` — keep `<N>` as the issue number when present). What remains ends in `-<file-id>` — that is the file-id. The rest, with that trailing numeric suffix removed, is `<idea-slug>`.

Examples:
- `docs/01-auth-forms-3-SPEC.md` → type = SPEC, feature-id = `01`, slug = `auth-forms`, file-id = `3`
- `docs/01-auth-forms-2-PRD.md` → type = PRD, feature-id = `01`, slug = `auth-forms`, file-id = `2`
- `docs/01-auth-forms-5-ISSUE-1.md` → type = ISSUE, feature-id = `01`, slug = `auth-forms`, file-id = `5`, issue = `1`

The output path always gets a freshly-computed `<file-id>` (see Algorithm A just below) — it never reuses the input's own file-id:
- SPEC or PRD input → output = `docs/<feature-id>-<idea-slug>-<new-file-id>-PLAN.md` (e.g. `docs/01-auth-forms-4-PLAN.md`)
- ISSUE-N input → output = `docs/<feature-id>-<idea-slug>-<new-file-id>-PLAN-N.md` (e.g. `docs/01-auth-forms-6-PLAN-1.md`)

**Algorithm A — computing `<file-id>` for a new file.** Before writing the output plan file (in OVERRIDE 5 / Step 4), calculate `<file-id>`:
1. List the files in `docs/` that start with `<feature-id>-<idea-slug>-` (e.g. `ls docs/ | grep '^<feature-id>-<idea-slug>-'`).
2. From each name found, extract the numeric segment immediately after `<idea-slug>-` and before the next hyphen — that is the existing file-id of that file.
3. The new `<file-id>` = (the largest number extracted) + 1, or `1` if no file starts with `<feature-id>-<idea-slug>-`.

#### Predecessor log check (ISSUE inputs only)

If the input type is ISSUE and `N > 1`:
1. Check whether a predecessor log exists using **Algorithm B**: search with the glob `docs/<feature-id>-<idea-slug>-*-ISSUE-(N-1)-LOG.md` — same `<feature-id>` as this run's input, since every file for this feature shares it. If more than one result appears, use the one with the highest file-id.
2. If it does not exist (the prior issue not yet implemented or not yet logged), no-op — current behavior unchanged.
3. If it exists, read only that one file (not a glob of all prior issues) and hold it as **supplemental** context for Step 4 — it never overrides the current issue's spec, the PRD, or what the actual code shows.
   - If the log's `## Verification` reads "Not yet verified," treat its claims as lower-confidence and say so in the generated plan.
   - If the log's content contradicts the codebase, follow the codebase and add a short "Prior log discrepancy" note in the generated plan describing what differed.

### Step 2 — Branch setup (PRD and ISSUE inputs only)

**Skip this step entirely if the input is a SPEC.md** — the branch or worktree was already established by `/spec`.

When invoked with a PRD.md or ISSUE-N.md, the session is on the main branch because `/prd` merges back before handing off. Before planning, establish the workspace.

#### ⛔ CHECKPOINT 1 — Slug confirmation (MANDATORY, do not skip)

The slug was extracted from the filename. Propose it to the user and **wait for explicit confirmation before continuing**. The user may correct it if the filename doesn't reflect the right slug. Do NOT proceed until the user approves or corrects it.

#### ⛔ CHECKPOINT 2 — Branch strategy (MANDATORY, do not skip)

Present exactly these three options and ask the user to choose one — do not reduce to two:
- **1. main** — plan directly on the current branch
- **2. branch** — create and switch to `feature/<idea-slug>` (or `feature/<idea-slug>-<N>` for an ISSUE input)
- **3. worktree** — create a git worktree at `../<idea-slug>` on branch `feature/<idea-slug>` (isolated workspace, recommended for larger plans)

After the user picks, invoke `superpowers:using-git-worktrees` if option 3 was chosen. Set up the chosen environment before proceeding.

### Step 3 — Enter plan-mode

Call `EnterPlanMode` immediately. All work happens in plan-mode to prevent accidental execution.

### Step 4 — Run writing-plans

#### Granularity choice (before invoking writing-plans)

Default to **"Balanced — one step per logical unit of work"** and proceed silently — do not ask the user, since Balanced is already the documented default and re-asking on every run adds friction without adding signal in the common case.

Only surface the three-option question when the input content clearly signals, in qualitative terms (no numeric thresholds), unusually large/complex or unusually trivial scope. Example signals:
- The scope spans multiple independent subsystems or user-facing flows.
- The description itself calls out unusual risk, migration, or rollback complexity.
- The change is a single-line/trivial fix with no meaningful design decisions.

These examples guide judgment — they don't replace it with a threshold. When one of these (or a comparable) signal is present, present exactly these three options in chat and wait for the user's choice:
- **1. Fewer, larger steps** — faster execution, less intermediate validation
- **2. Balanced** (default — recommend this unless the input suggests otherwise) — one step per logical unit of work
- **3. More, smaller steps** — maximum checkpoints, more context-switch overhead

Wording must differ by input type: when the input is `ISSUE-N.md` (already a single vertical slice from `prd`), the three options size **implementation tasks within that slice**, not features — replace "steps" wording with "implementation tasks" in the ISSUE-N.md case to avoid re-litigating PRD-level decomposition.

Hold the resulting choice — whether auto-selected Balanced or the user's literal answer to the three-option question (e.g. `"Balanced — one step per logical unit of work"`) — it is interpolated into OVERRIDE 7 below when invoking `writing-plans`.

Use the `Skill` tool to invoke `superpowers:writing-plans` with these overrides:

> **OVERRIDE 1 — input:** The feature description comes from the file read in Step 1, not from conversation context. If a predecessor log was found per the Predecessor log check above, include it as supplemental context (with any lower-confidence or discrepancy notes) alongside the primary input.
>
> **OVERRIDE 2 — output:** Save the final plan to `docs/<feature-id>-<idea-slug>-<file-id>-PLAN.md` (or `docs/<feature-id>-<idea-slug>-<file-id>-PLAN-N.md` for an issue input), using the `<file-id>` computed with Algorithm A in Step 1. Do NOT use the default plan file location.
>
> **OVERRIDE 3 — tests:** For each implementation step, include the specific tests or verification commands that confirm that step is complete. Write tests before implementation code (TDD order).
>
> **OVERRIDE 4 — terminal state:** Stop after the plan is written and has gone through Act 2's Codex review (see below). Do NOT proceed to `executing-plans` or any implementation step.
>
> **OVERRIDE 6 — agentic worker instruction:** In the generated plan document, replace any "For agentic workers" line with exactly:
> `**For agentic workers:** Use superpowers:subagent-driven-development to implement this plan task-by-task. Each task must follow superpowers:test-driven-development.`
> Do NOT mention superpowers:executing-plans anywhere in the plan.
>
> **OVERRIDE 5 — plan writing:** When the plan is ready to be written:
> 1. Before writing, calculate `<file-id>` using Algorithm A (Step 1) if not already computed. Apply OVERRIDE 8's Task N/TOTAL numbering to every task heading, then write the plan directly to `docs/<feature-id>-<idea-slug>-<file-id>-PLAN.md` (or `PLAN-N.md`) without displaying its full content in the console. Just confirm the path.
> 2. Tell the user: *"Plan written to `docs/<feature-id>-<idea-slug>-<file-id>-PLAN.md`. Starting the Codex adversarial review before this lands."*
> 3. Return control to the skill — do NOT ask the user to approve this draft and do NOT commit here. There is no separate approval gate on the plan draft any more: Act 2 below (and, if it revises the plan's content, the revision itself) is now the gate a plan passes through before it lands. If Act 2 changes the task list, reapply OVERRIDE 8's numbering.

> **OVERRIDE 7 — granularity:** A granularity was determined above this invocation (auto-selected Balanced, or the user's explicit choice). Include that choice **verbatim** here (e.g. "OVERRIDE 7 — granularity: the user chose 'Balanced — one step per logical unit of work'; size all plan steps accordingly"), since writing-plans is an invoked skill, not a typed API — the constraint only takes effect if it is literally present in this prompt.

> **OVERRIDE 8 — task numbering:** Write every task heading as `### Task N/TOTAL: [Component Name]` instead of the default `### Task N: [Component Name]`, where `TOTAL` is the total number of tasks in the plan's current draft. This lets anything that echoes a task's title later — most importantly the per-task subagent labels `superpowers:subagent-driven-development` produces during `/implement` (e.g. "Implement Task 4: ...") — carry the total task count too, so progress is visible without opening the plan file. Count the `### Task` headings once the full task list is drafted to get `TOTAL`, then stamp it into every heading; recompute and restamp `TOTAL` on every write of the plan document, not just the first — OVERRIDE 5 steps 1 and 3 both call back to this, since a feedback round can add, remove, or merge tasks and leave a stale count otherwise. This numbering lives only in this plan's headings; it doesn't require any change to `writing-plans` itself.

Follow every other writing-plans step as written.

---

## ACT 2 — CODEX REVIEW (Claude ↔ Codex)

`writing-plans` just returned a plan draft that was never shown to the user for approval — OVERRIDE 5 sends it straight here instead. Act 2 is now the gate: it exists because a bad task breakdown is cheap to fix on paper and expensive to fix after `/implement` has already turned it into code, tests, and several `/verify` → `/revise` cycles. Codex reviews for plan-level defects only, not scope — scope and requirements were already settled upstream in `/spec`; re-litigating them here would just repeat that work with a worse model context (Codex has no view of the brainstorming that produced the spec).

### Step 5 — Codex review loop

#### Prerequisites
- `codex --version` ≥ 0.130
- Codex authenticated (`codex login`; ChatGPT account is fine)
- Do NOT pin `-m` — ChatGPT-account auth rejects `gpt-5.x-codex` variants

If the `codex` binary is unavailable, the command exits non-zero (auth failure, etc.), report that Act 2 could not run and let the user decide whether to proceed straight to Step 6 (commit) without a Codex review, or stop and fix Codex access first — do not silently skip this step.

#### Tunables (read from args, else default)
| Var | Default | Meaning |
|-----|---------|---------|
| `MAX_ROUNDS` | `5` | Rounds before the first continue/stop checkpoint (see below) |
| `PLAN_FILE` | `docs/<feature-id>-<idea-slug>-<file-id>-PLAN.md` (or `PLAN-N.md`) | The exact path Step 4 wrote — reuse it, do not recompute `<file-id>` |
| `LOG_FILE` | `docs/<feature-id>-<idea-slug>-<review-file-id>-PLAN-REVIEW.md` (or `PLAN-N-REVIEW.md`) | Computed once, at the start of Act 2, the same way `<file-id>` was computed for `PLAN_FILE` (Algorithm A) — `PLAN_FILE` is already on disk at this point, so `<review-file-id>` lands one higher |

Before Round 1, initialize `LOG_FILE`:
```
# Plan Review Log: <feature>
Plan drafted — starting Codex adversarial review. MAX_ROUNDS=<n>.
```

#### Review prompt strategy

Plan content is passed **inline** in the prompt — do NOT rely on Codex reading from the filesystem (bwrap sandbox blocks it). Claude reads `$PLAN_FILE` and embeds it directly. The prompt directs Codex at plan-specific defects, explicitly out of scope for requirements debate:

- Does every task have a test that fails without the change, in TDD order (test before implementation)?
- Are there hidden ordering or dependency issues between tasks — a later task assuming something an earlier task doesn't actually establish?
- Does each task's interface/contract assumption about the existing codebase actually hold?
- Are there edge cases the TDD steps don't cover?
- Is the plan DoD-ready — rollback path for anything risky, backward compatibility for public interfaces, security implications for untrusted input or auth handling?

##### Round 1 — fresh session (capture thread_id)
```bash
PLAN_CONTENT=$(cat "$PLAN_FILE")
REVIEW_PROMPT="You are an adversarial reviewer for a software implementation plan (TDD task breakdown). The plan's scope and requirements were already agreed with the user upstream — do NOT question scope, only the plan's execution quality. Here is the plan to review:

---
${PLAN_CONTENT}
---

Identify concrete flaws: tasks missing a test that fails without the change, TDD ordering violations, hidden task ordering/dependency issues, wrong assumptions about interfaces/contracts with the existing codebase, missed edge cases in the TDD steps, and DoD gaps (rollback path, backward compatibility, security implications). For each flaw, give a one-line fix. Do NOT modify any files. Do NOT raise scope or requirements concerns. End your reply with EXACTLY one line: \`VERDICT: APPROVED\` if the plan is sound enough to implement, or \`VERDICT: REVISE\` if it still has material problems."

codex exec --json -o /tmp/codex-plan-verdict.txt "$REVIEW_PROMPT" \
  2>/dev/null | grep '"type":"thread.started"'
```
Parse `thread_id` from `{"type":"thread.started","thread_id":"..."}`. Critique is in `/tmp/codex-plan-verdict.txt`.

##### Rounds 2+ — resume same session
```bash
PLAN_CONTENT=$(cat "$PLAN_FILE")
codex exec resume "$THREAD_ID" --json \
  -o /tmp/codex-plan-verdict.txt \
  "I revised the plan. Here is the updated version:

---
${PLAN_CONTENT}
---

Re-review — check whether your prior findings are addressed and flag anything new (still no scope/requirements concerns). End with VERDICT: APPROVED or VERDICT: REVISE." \
  2>/dev/null >/dev/null
```

#### Each round
1. Append Codex output to the log:
```bash
echo "## Round <n> — Codex" >> "$LOG_FILE"
cat /tmp/codex-plan-verdict.txt >> "$LOG_FILE"
```
2. Check the last line of `/tmp/codex-plan-verdict.txt` for the verdict:
   - `VERDICT: APPROVED` → Step 6 (Resolution).
   - `VERDICT: REVISE` → Claude decides what's worth acting on (Claude is final arbiter — see Hard Rules). Revise `PLAN_FILE` (reapplying OVERRIDE 8's task numbering if the task list changed). Then append Claude's response to the log:
```bash
echo "### Claude's response" >> "$LOG_FILE"
echo "<what changed, what was rejected, why>" >> "$LOG_FILE"
```
   Increment `round`.
3. If `round` is a multiple of `MAX_ROUNDS` (5, 10, 15, ...) and the verdict is still `VERDICT: REVISE` → go to the round checkpoint below instead of looping silently.

#### Round checkpoint (every `MAX_ROUNDS` rounds without APPROVED)

Ask the user, in Romanian:

> *"Codex a ajuns la runda <n> și încă găsește probleme (vezi rezumatul de mai sus). Vrei să continui cu încă <MAX_ROUNDS> runde, sau oprim aici și mergem mai departe cu planul așa cum e, cu problemele deschise notate?"*
> - **Continuă** — rulează încă `MAX_ROUNDS` runde, cu o nouă verificare la runda <n + MAX_ROUNDS>.
> - **Oprim aici** — Act 2 se încheie cu problemele deschise notate în `PLAN-REVIEW.md`; se trece direct la Step 6.

The loop never continues past a checkpoint without asking — this is deliberate: it's the same trade-off `/spec`'s `MAX_ROUNDS` deadlock hands to the user, just revisited every `MAX_ROUNDS` rounds instead of only once, since a plan review that's still finding things after 5 rounds may keep finding things for a while and the user should decide whether that's worth the wall-clock/cost.

If the user picks **Oprim aici**, append to the log:
```bash
echo "## Stopped by user at round <n> — open issues carried into commit, not resolved" >> "$LOG_FILE"
```
and proceed to Step 6 with the open issues intact.

### Step 6 — Commit

Once Act 2 concludes — `VERDICT: APPROVED`, the user chose **Oprim aici** at a checkpoint, or Act 2 could not run per Prerequisites above and the user chose to proceed anyway:

1. `git add docs/<feature-id>-<idea-slug>-<file-id>-PLAN.md docs/<feature-id>-<idea-slug>-<review-file-id>-PLAN-REVIEW.md` (or the `PLAN-N.md`/`PLAN-N-REVIEW.md` pair for an issue-derived plan)
2. `git commit -m "docs: add implementation plan for <idea-slug> (Codex-reviewed, N rounds)"` — adjust the message if Act 2 didn't run (e.g. "docs: add implementation plan for <idea-slug> (Codex review skipped)")

Do NOT push. Do NOT skip this step. Do NOT ask for a separate approval before committing — Act 2 (and, if it triggered, the user's checkpoint decision) is the approval gate now; there is no additional "approve the plan draft" step.

### Step 7 — Confirm stop

After committing, say:

> *"Planul a fost salvat în `docs/<feature-id>-<idea-slug>-<file-id>-PLAN.md`, revizuit adversarial de Codex (`docs/<feature-id>-<idea-slug>-<review-file-id>-PLAN-REVIEW.md`, <N> runde<, cu probleme deschise notate, dacă e cazul>). Pentru implementare, rulează `/implement` cu calea către fișierul de plan."*

⛔ **HARD STOP — do not continue past this point.** ExitPlanMode approval is approval of the plan document only — it is NOT authorization to implement. The plan file is the only deliverable of this skill. Return control to the user immediately after Step 7.

## Output

- `docs/<feature-id>-<idea-slug>-<file-id>-PLAN.md` — TDD implementation plan derived from a SPEC.md or PRD.md
- `docs/<feature-id>-<idea-slug>-<file-id>-PLAN-N.md` — TDD implementation plan for a single vertical slice, derived from an ISSUE-N.md
- `docs/<feature-id>-<idea-slug>-<review-file-id>-PLAN-REVIEW.md` — Codex adversarial review transcript for the plan above (`PLAN-N-REVIEW.md` for an issue-derived plan)

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll figure it out as I go" | That's how you get a tangled mess and rework. 10 minutes of planning saves hours. |
| "The tasks are obvious, no need to write them" | Writing tasks surfaces hidden dependencies and forgotten edge cases. |
| "Planning is overhead" | Planning is the task. Implementation without a plan is just typing. |
| "I can hold it all in my head" | Context windows are finite. Written plans survive session boundaries and compaction. |
| "Codex already approved the spec, the plan doesn't need its own review" | A spec review checks scope and requirements. A plan translates those into concrete tasks, test coverage, and sequencing — a different failure surface that only exists once the plan is drafted. |

## Hard Rules

- Do NOT invoke `executing-plans` or any implementation skill.
- Do NOT write code, in Phase 1 or during Act 2.
- Do NOT start executing — that is the user's decision in a new session.
- Always read the input file before invoking writing-plans.
- Always run Step 2 (branch setup) for PRD and ISSUE inputs — do NOT skip it even if you think the branch already exists.
- Act 2 always follows the plan draft — no commit until Act 2 has concluded (APPROVED, a user checkpoint decision, or Codex being unavailable per Prerequisites with explicit user sign-off to proceed without it).
- Pass plan content **inline** every round — do NOT use `-s read-only` or `-c sandbox_mode="read-only"` (bwrap blocks filesystem reads, Codex will fail silently and hallucinate).
- The loop never continues past a `MAX_ROUNDS` checkpoint without asking the user — no silent infinite looping.
- Claude is final arbiter on every REVISE — don't cave to everything, don't ignore it.
- Always commit after Act 2 concludes — do NOT skip Step 6. Do NOT push.
