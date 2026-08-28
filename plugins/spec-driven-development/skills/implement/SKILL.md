---
name: implement
description: Implements a TDD plan from a PLAN.md or PLAN-N.md file. Invokes executing-plans and verifies all tests pass. Use when user says "implement me", "implement this plan", or wants to execute a plan file produced by /plan-me.
---

# Implement-Me — Plan to Working Code

Reads a PLAN.md or PLAN-N.md file and implements it step by step, verifying tests after each step.

## Model & Thinking

Use **Claude Sonnet** (`claude-sonnet`) with **medium thinking effort** for all reasoning in this skill.

## Language

Conduct all dialogue with the user — questions, confirmations, status updates — exclusively in Romanian, regardless of the language the plan was written in.

All deliverables this skill writes (`docs/<feature-id>-<idea-slug>-ISSUE-N-LOG.md`, code, code comments, commit messages) must always be written in English, independent of the Romanian dialogue above. Subagent dispatch prompts (Steps 2 and 4) also stay in English — they are instructions to other Claude agents, not user-facing dialogue.

## Invocation

Pass the plan file path explicitly:

> `/implement-me docs/<feature-id>-<idea-slug>-PLAN.md`
> `/implement-me docs/<feature-id>-<idea-slug>-PLAN-N.md`

If no path is provided, stop and ask: *"Please specify the plan file path, e.g. `docs/01-auth-forms-PLAN.md` or `docs/01-auth-forms-PLAN-1.md`."*

## Feature ID Prefix

Every file under `docs/` for a feature shares one `<feature-id>`, assigned once when the slug was first seen. This skill reuses the SAME `<feature-id>` parsed from the plan filename (Step 1) for the one new file it writes (`ISSUE-N-LOG.md`, Step 6) and for locating the feature's `SPEC.md` (Step 3) — never a different id.

## Output and Context Rules

These rules govern everything this skill prints to the main conversation — subagent dispatch prompts (which go to a clean subagent context) are unaffected.

- **Never paste full file contents into the main conversation.** Subagents receive the plan's absolute path and read it themselves, in their own context; in the main thread, refer to files by path (`docs/<feature-id>-<idea-slug>-PLAN.md`), not by quoting them.
- **Subagent reports must come back as short summaries**, not raw logs: task count done/total, pass/fail test counts, and a one-line verdict. Do not relay a subagent's full internal transcript.
- **On test failures, show only the essentials**: failing test names and a 1–3 line error excerpt each (assertion message, not full stack trace). Full stack traces or raw command output are shown only if the user explicitly asks for them.
- **Batch divergences instead of dumping them.** If Step 3 finds more than ~5 divergences, first give a one-line count + the 3–5 most significant ones, then ask whether to walk through the rest one by one — don't flood the chat with every proposed edit at once.
- **Status updates are one line each** ("Step 2: implementation subagent dispatched", "Step 4: 12/12 tests passing") — no restating of plan content or prior steps.
- **Default to the minimal useful output.** If unsure how much detail to show, show less and offer to expand on request.

## Subagent Timeout & Escalation

Every subagent dispatched by this skill (the implementation subagent in Step 2, the testing subagent in Step 4, and any fix subagent spawned during Step 4's failure loop) is watched under the same rule, so a stuck subagent never silently stalls the whole run:

1. **Arm a 5-minute check right after dispatch.** Call `TaskOutput` on the subagent's task with `block: true` and `timeout: 300000` (5 minutes). If it returns because the subagent finished, proceed normally — read its report and move on.
2. **If the call times out instead of completing**, the subagent has gone 5 minutes with no result. Call `TaskOutput` again with `block: false` to snapshot its current output, and check `ListAgents` to confirm whether it's still listed as running. Use that snapshot to judge whether it's making real progress (output growing, distinguishable steps happening) or genuinely stuck (output frozen, repeating the same action, or erroring silently).
3. **First time a given subagent looks stuck:** stop it with `TaskStop`, tell the user in one line that the subagent stalled and is being restarted, then re-dispatch the exact same task (same prompt, same plan path) via the `Agent` tool as a fresh subagent, and re-arm a new 5-minute `TaskOutput` check (back to step 1) for it.
4. **Second time the same task's subagent stalls** (i.e. the restarted subagent also fails to complete within its 5-minute window): stop it with `TaskStop` and stop delegating that task to a subagent entirely. Tell the user in one line that delegation failed twice and execution is moving inline. Take over the task yourself, running it directly in the main thread instead of a subagent — this sacrifices the clean-context benefit of subagents, but running it inline is what lets you observe the exact commands and output as they happen, which is what's needed to debug why it kept stalling. Continue the skill's process from there once the inline run finishes.

This escalation is per-task: a fresh task dispatched later in the skill (e.g. the testing subagent after implementation succeeds) starts its own fresh two-strike count.

### Step 1 — Read the plan file

Read the file at the provided path. If it does not exist, stop and tell the user.

Extract `<feature-id>`, `<idea-slug>`, and (for issue plans) the plan number from the filename:
- `docs/01-auth-forms-PLAN.md` → feature-id = `01`, slug = `auth-forms`
- `docs/01-auth-forms-PLAN-1.md` → feature-id = `01`, slug = `auth-forms`, plan = `1`

### Step 2 — Dispatch implementation subagent

**Always** dispatch implementation to a subagent — never run it inline, regardless of plan size. A clean, uncontaminated context is required for reliable implementation.

Use the `Agent` tool to spawn a subagent with this prompt (substitute the absolute plan path):

```
You are implementing a TDD plan. Read this plan carefully and execute it step by step.

<plan_path>
<PLAN_PATH>
</plan_path>

Read the plan file at the path above before doing anything else.

Instructions:
- Use the `superpowers:subagent-driven-development` skill to implement this plan task-by-task.
- Each task must follow `superpowers:test-driven-development`.
- Do NOT skip any step.
- The dispatching this skill asks you to do is limited to what `superpowers:subagent-driven-development` itself defines (its per-task implementer and reviewer subagents). Do not invent any further layer of delegation beyond that — e.g. don't have a per-task implementer spawn its own helper subagent, and don't route work through any subagent mechanism this skill doesn't call for.
- Before every use of the `Edit` tool on an existing file — even one you believe a prior task already created — use the `Read` tool on it first, in this subagent's own context; using `Write` to create a genuinely new file needs no prior Read. If `Edit` or `Write` fails, `Read` the file (or confirm it doesn't exist) and retry the same tool — never fall back to a raw shell command (e.g. `sed`, `cat >`) to force the change through.
- Do NOT modify tests to make them pass — fix the implementation instead.
- For framework-specific patterns (React hooks, routing, auth, database ORM, etc.), verify against official documentation before implementing.
- After all tasks are complete, run the full test suite and confirm all tests pass.
- Report back concisely: task count completed/total, overall test pass/fail counts, and any issues encountered in 1-2 lines each. Do not paste full test output or file contents in your report.
```

Replace `<PLAN_PATH>` with the absolute path of the plan file read in Step 1. Read that file yourself, in your own context, before starting work — do not rely on any plan content being pasted into this prompt.

Apply the **Subagent Timeout & Escalation** rules above to this dispatch. Once it completes (directly or after escalation), relay its report to the user as the short summary described in **Output and Context Rules**, not the raw subagent transcript.

### Step 3 — Spec divergence check

After the implementation subagent completes, read `docs/<feature-id>-<idea-slug>-SPEC.md` (same `<feature-id>` as the plan read in Step 1) and run `git diff` to compare the current working tree against the spec. Read only what's needed to spot divergences — skim `git diff` for changed sections rather than re-reading the entire spec and full diff verbatim into your response.

For each divergence (architectural decision changed, scope adjusted, data model differs from what the spec describes), propose a concrete edit to `docs/<feature-id>-<idea-slug>-SPEC.md`. Present proposed edits per the batching rule in **Output and Context Rules**, and wait for approval or rejection before continuing.

Only after the user has reviewed all proposed spec edits (or confirmed there are none), proceed to the testing subagent.

### Step 4 — Dispatch testing subagent

After the implementation subagent completes, dispatch a **separate** testing subagent — never run tests inline. A separate subagent ensures the test run happens with a clean context, independent of implementation decisions.

Use the `Agent` tool to spawn a subagent with this prompt:

```
You are verifying an implementation against a TDD plan. Do NOT modify any code.

<plan_path>
<PLAN_PATH>
</plan_path>

Read the plan file at the path above before doing anything else.

Instructions:
- Do NOT delegate any part of this task to another subagent — no spawning via the `Agent` tool or any similar mechanism. Run every command yourself, directly, in this thread. This task is simple enough to not need a controller/worker split, and sub-delegating would hand the actual verification to an agent nobody is tracking, making your report describe results you didn't personally observe.
- Read the test commands and verification steps defined in the plan above.
- Run every test and verification command.
- Report concisely: pass/fail counts, an overall PASS / FAIL verdict, and for each failing test only its name plus a 1-3 line error excerpt (not the full stack trace or raw command output).
- Before every use of the `Edit` tool on an existing file — even one you believe a prior task already created — use the `Read` tool on it first, in this subagent's own context; using `Write` to create a genuinely new file needs no prior Read. If `Edit` or `Write` fails, `Read` the file (or confirm it doesn't exist) and retry the same tool — never fall back to a raw shell command (e.g. `sed`, `cat >`) to force the change through.
- Do NOT fix anything — only report what you find.
```

Replace `<PLAN_PATH>` with the absolute path of the plan file read in Step 1. Read that file yourself, in your own context, before starting work — do not rely on any plan content being pasted into this prompt.

Apply the **Subagent Timeout & Escalation** rules above to this dispatch (and to every fix subagent dispatch below).

If the testing subagent reports any failures:
1. Spawn a new **fix subagent** using the Agent tool, giving it the failing test output and the plan file's absolute path (instruct it to read the plan file itself, not a pasted copy). Instruct it to fix only the failing implementation (minimal change, do not alter tests), to make the fix itself directly rather than spawning any subagent of its own (same reasoning as the testing subagent above — this is a bounded, single-context fix, not a controller task), and to report back with a 1-2 line summary of the fix, not a diff dump.
2. Re-dispatch the testing subagent.
3. Repeat until all tests pass.

Show the user only the current round's pass/fail counts between iterations, not a running log of every prior round.

### Step 5 — Confirm

When the testing subagent reports all tests pass, say:

> *"Implementation complete. All tests defined in `docs/<feature-id>-<idea-slug>-PLAN.md` pass."*

### Step 6 — Write issue log

Only if the plan file is `docs/<feature-id>-<idea-slug>-PLAN-N.md` (an issue-derived plan, not a plain `docs/<feature-id>-<idea-slug>-PLAN.md`):

Write `docs/<feature-id>-<idea-slug>-ISSUE-N-LOG.md` (same `<feature-id>` as the plan — overwrite if it already exists — regenerate the whole file, do not merge with a prior version):

```markdown
# Issue N Log: <issue title>

## What's new in the app
<bulleted, non-technical, user-facing capabilities added — scannable by a
non-technical reviewer. If this issue has no user-facing change (infra,
tests, refactor), write "No user-facing change.">

## What was built
<files created/modified, models/schema changes, routes/endpoints added,
public contracts, migrations, and any other decision a future issue may
depend on. Keep concise — target well under ~100 lines unless the issue
genuinely requires more detail.>

## Verification
Not yet verified
```

Base `<issue title>` and the content on the actual final code/worktree state produced by Steps 2–4 — not the plan's intended work — in case implementation diverged from the plan (this is what Step 3's divergence check already surfaces).

If the plan is a plain `docs/<feature-id>-<idea-slug>-PLAN.md` (SPEC- or PRD-derived, no issue number), skip Step 6 entirely — no log file is written.

## Hard Rules

- Do NOT run implementation or tests inline — always dispatch to subagents via the Agent tool, except for the second-stall inline takeover defined in **Subagent Timeout & Escalation**.
- Do NOT modify tests to make them pass — fix the implementation instead.
- Do NOT offer to merge, create a PR, or clean up branches/worktrees — that belongs in `/verify`, after the implementation has been validated.
