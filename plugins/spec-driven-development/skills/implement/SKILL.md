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

All deliverables this skill writes (`docs/<feature-id>-<idea-slug>-<file-id>-ISSUE-N-LOG.md`, code, code comments, commit messages) must always be written in English, independent of the Romanian dialogue above. Subagent dispatch prompts (Steps 2 and 4) also stay in English — they are instructions to other Claude agents, not user-facing dialogue.

## Invocation

Pass the plan file path explicitly:

> `/implement-me docs/<feature-id>-<idea-slug>-<file-id>-PLAN.md`
> `/implement-me docs/<feature-id>-<idea-slug>-<file-id>-PLAN-N.md`

If no path is provided, stop and ask: *"Please specify the plan file path, e.g. `docs/01-auth-forms-7-PLAN.md` or `docs/01-auth-forms-7-PLAN-1.md`."*

## Feature ID Prefix

Every file under `docs/` for a feature shares one `<feature-id>`, assigned once when the slug was first seen. This skill reuses the SAME `<feature-id>` parsed from the plan filename (Step 1) for the one new file it writes (`ISSUE-N-LOG.md`, Step 6) and for locating the feature's `SPEC.md` (Step 3) — never a different id. Each individual file also carries its own `<file-id>` (see Step 1 for parsing an existing file's `<file-id>`, and Step 6 for computing or reusing one when writing a new file).

## Output and Context Rules

These rules govern everything this skill prints to the main conversation — subagent dispatch prompts (which go to a clean subagent context) are unaffected.

- **Never paste full file contents into the main conversation.** Subagents receive the plan's absolute path and read it themselves, in their own context; in the main thread, refer to files by path (`docs/<feature-id>-<idea-slug>-<file-id>-PLAN.md`), not by quoting them.
- **Subagent reports must come back as short summaries**, not raw logs: task count done/total, pass/fail test counts, and a one-line verdict. Do not relay a subagent's full internal transcript.
- **On test failures, show only the essentials**: failing test names and a 1–3 line error excerpt each (assertion message, not full stack trace). Full stack traces or raw command output are shown only if the user explicitly asks for them.
- **Batch divergences instead of dumping them.** If Step 3 finds more than ~5 divergences, first give a one-line count + the 3–5 most significant ones, then ask whether to walk through the rest one by one — don't flood the chat with every proposed edit at once.
- **Status updates are one line each** ("Step 2: implementation subagent dispatched", "Step 4: 12/12 tests passing") — no restating of plan content or prior steps.
- **Default to the minimal useful output.** If unsure how much detail to show, show less and offer to expand on request.

## Subagent Timeout & Escalation

Every subagent dispatched by this skill (the implementation subagent in Step 2, the testing subagent in Step 4, and any fix subagent spawned during Step 4's failure loop) is watched under the same rule, so a stuck subagent never silently stalls the whole run:

There is no tool that blocks until a subagent finishes: subagents run in the background and their completion arrives as a notification in a later turn. So a stall can't be detected by a timeout on the subagent itself — it is detected by looking for outside evidence of progress. Elapsed time only decides *when to look*; the evidence decides whether the subagent is stuck. This matters because a healthy subagent can legitimately go many minutes without finishing (a browser test suite alone can take ~5 minutes), and restarting it would throw away real work.

1. **Dispatch, then wait for the completion notification.** Do not poll in a loop. When the notification arrives, read the report and proceed normally. Record the dispatch time and the current `git rev-parse HEAD` so later checks have a baseline. To be woken by a concrete event instead of guessing, arm a watcher rather than sleeping for a fixed time: for a single wake-up (e.g. "a new commit appeared on `HEAD`") run a Bash command with `run_in_background` that loops `until [ "$(git rev-parse HEAD)" != "$base" ]; do sleep 1; done` and exits — you get one notification when it ends. For a stream of events plus stall detection, use `Monitor` with a loop that prints one line per new commit and a `STALL` line (then exits) after a chosen stretch with no new commit and no live test process. Always make the stall condition print something: a watcher that only reports the happy path stays silent exactly when the subagent is stuck.
2. **After ~5 minutes with no notification, check for progress.** Gather these signals (cheap, read-only):
   - `ListAgents` — the "Subagents" section lists each one with its state (`running`/`completed`) and how long ago it started. Note that `completed` can be an interim state if the subagent still has background work of its own running.
   - `git log --oneline <baseline>..HEAD` and `git status --short` — new commits since dispatch, or changed/new files compared with the previous check.
   - Active test or build processes, adjusted to the plan's test commands. Use `ps -eo pid,etime,args | grep -E '[p]ytest|[n]pm|[p]laywright|[v]itest|[j]est' | grep -v 'bash -c'`. A plain `pgrep -f` matches the very shell running the check (its command line contains the pattern) and would report a live test process every time; the `[p]` bracket trick plus dropping the `bash -c` wrapper line avoids that false positive. `etime` shows how long the process has been running.

   Any one of these counts as progress: a new commit, a different set of modified files than at the last check, or a live test/build process. A subagent running a long test suite is active even with no new commits. If there is progress, it is not stuck — keep waiting and check again after another ~5 minutes.
3. **No progress since the previous check** (no new commit, `git status` unchanged, no test/build process, subagent still listed as running or already gone without a report) means it is stuck. The first time this happens for a given task:
   1. Stop it with `TaskStop`.
   2. Make the working tree clean before relaunching, so the fresh subagent starts from a known state and doesn't build on half-written edits. If `git status` shows uncommitted changes, set them aside with `git stash push -u -m "stalled subagent: <task>"` — nothing is lost, and the user can recover it. Never discard changes with `reset` or `checkout`.
   3. Tell the user in one line that the subagent stalled, was restarted, and whether anything was stashed.
   4. Re-dispatch the same task (same prompt, same plan path) via the `Agent` tool as a fresh subagent, appending a short note listing which tasks are already committed (from `git log`) so it resumes after them instead of redoing them. Return to step 1 for the new subagent.
4. **Second time the same task's subagent is stuck:** stop it with `TaskStop` (and clean the tree as above) and stop delegating that task to a subagent entirely. Tell the user in one line that delegation failed twice and execution is moving inline. Take over the task yourself, running it directly in the main thread instead of a subagent — this sacrifices the clean-context benefit of subagents, but running it inline is what lets you observe the exact commands and output as they happen, which is what's needed to debug why it kept stalling. Continue the skill's process from there once the inline run finishes.

The signals in step 2 only exist if subagents leave them behind, which is why the dispatch prompts below require a commit after every task. The testing subagent in Step 4 makes no commits by design, so for it the signals are `ListAgents` and live test processes.

This escalation is per-task: a fresh task dispatched later in the skill (e.g. the testing subagent after implementation succeeds) starts its own fresh two-strike count.

### Step 1 — Read the plan file

Read the file at the provided path. If it does not exist, stop and tell the user.

Extract `<feature-id>`, `<idea-slug>`, `<file-id>`, and (for issue plans) the plan number from the filename. Given a name like `01-auth-forms-7-PLAN.md` or `01-auth-forms-7-PLAN-1.md`: `<feature-id>` is the numeric segment at the start (`01`). Strip the `.md` extension and the `<feature-id>-` prefix. Then strip the known type suffix from the right (`-PLAN` or `-PLAN-<N>`). What remains ends with `-<file-id>` — that's the file-id (`7`). The rest, with that trailing numeric suffix removed, is `<idea-slug>` (`auth-forms`).

Examples:
- `docs/01-auth-forms-7-PLAN.md` → feature-id = `01`, slug = `auth-forms`, file-id = `7`
- `docs/01-auth-forms-7-PLAN-1.md` → feature-id = `01`, slug = `auth-forms`, file-id = `7`, plan = `1`

**Resolve the test commands.** Read the plan's `## Test Commands` section and hold two things for the rest of the run:

- **`<FEATURE_TESTS>`** — the command(s) that run only the tests this plan adds or modifies.
- **`<FULL_SUITE>`** — the command that runs the whole project's test suite.

They are kept apart because a mature project's full suite can take many minutes, and running it on every implementation and fix iteration multiplies that cost for no extra signal: the feature's own tests catch problems in the new code quickly, and the full suite only needs to run once, at the end, to prove nothing pre-existing broke.

If the section is missing (a plan written before it existed) or `<FULL_SUITE>` reads `TO CONFIRM`: build `<FEATURE_TESTS>` from the per-task test commands in the plan, and find `<FULL_SUITE>` in `CLAUDE.md`, `README`, `package.json` / `pyproject.toml` / `Makefile` or CI config. If it still can't be determined, ask the user once for the command — never guess one. Then state both commands to the user in one line so a wrong one is caught before it is used.

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
- Commit after every completed task (a normal commit with a short message naming the task), before starting the next one. The dispatching agent cannot see inside your work, so commits are the only way it can tell you are progressing rather than stuck — and if you are ever restarted, committed tasks are skipped instead of redone. Also begin each task by checking `git log` to see which tasks are already committed, and resume after them.
- For framework-specific patterns (React hooks, routing, auth, database ORM, etc.), verify against official documentation before implementing.
- Run only the tests of this feature while implementing — each task's own test commands from the plan. Do NOT run the project's full test suite: it is slow, and a separate verification step runs it once after you finish. Running it here would repeat that cost without adding a signal the feature tests don't already give.
- After all tasks are complete, run the Feature tests command below once and confirm it passes:
  <FEATURE_TESTS>
- Report back concisely: task count completed/total, Feature tests pass/fail counts, and any issues encountered in 1-2 lines each. State explicitly that the full suite was not run. Do not paste full test output or file contents in your report.
```

Replace `<PLAN_PATH>` with the absolute path of the plan file read in Step 1 and `<FEATURE_TESTS>` with the command(s) resolved in Step 1. Read that file yourself, in your own context, before starting work — do not rely on any plan content being pasted into this prompt.

Apply the **Subagent Timeout & Escalation** rules above to this dispatch; when re-dispatching after a stall, append the note listing already-committed tasks. Once it completes (directly or after escalation), relay its report to the user as the short summary described in **Output and Context Rules**, not the raw subagent transcript.

### Step 3 — Spec divergence check

After the implementation subagent completes, locate the feature's `SPEC.md`: search with the glob `docs/<feature-id>-<idea-slug>-*-SPEC.md` (same `<feature-id>` and `<idea-slug>` as the plan read in Step 1). If more than one result comes back, use the one with the highest file-id. Read that file and run `git diff` to compare the current working tree against the spec. Read only what's needed to spot divergences — skim `git diff` for changed sections rather than re-reading the entire spec and full diff verbatim into your response.

For each divergence (architectural decision changed, scope adjusted, data model differs from what the spec describes), propose a concrete edit to the `SPEC.md` file found above, at its exact existing path — do not assign it a new file-id. Present proposed edits per the batching rule in **Output and Context Rules**, and wait for approval or rejection before continuing.

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
- Phase A — Feature tests. Run every per-task test and verification command from the plan, the Feature tests command below, and any extra tests listed below. This is fast and tells us whether the new work is correct.
  Feature tests: <FEATURE_TESTS>
  Extra tests to include: <EXTRA_TESTS>
- Phase B — Full suite. Run it only if every Phase A command passed; if anything in Phase A failed, skip Phase B and say so (a failing feature makes a 20-minute regression run pointless). Full suite: <FULL_SUITE>. Run it to completion even if it takes many minutes; do not cut it short. Print the exact command you ran in your report.
- Report concisely: for each phase, pass/fail counts; an overall PASS / FAIL verdict (PASS only if both phases ran and passed); and for each failing test only its name plus a 1-3 line error excerpt (not the full stack trace or raw command output).
- Before every use of the `Edit` tool on an existing file — even one you believe a prior task already created — use the `Read` tool on it first, in this subagent's own context; using `Write` to create a genuinely new file needs no prior Read. If `Edit` or `Write` fails, `Read` the file (or confirm it doesn't exist) and retry the same tool — never fall back to a raw shell command (e.g. `sed`, `cat >`) to force the change through.
- Do NOT fix anything — only report what you find.
```

Replace `<PLAN_PATH>` with the absolute path of the plan file read in Step 1, and `<FEATURE_TESTS>` / `<FULL_SUITE>` with the commands resolved in Step 1. Replace `<EXTRA_TESTS>` with `none` on the first round, and in later rounds with the names of the tests that failed in the previous round (so a regression found by the full suite is re-checked quickly in Phase A before the long Phase B reruns). Read the plan file yourself, in your own context, before starting work — do not rely on any plan content being pasted into this prompt.

Apply the **Subagent Timeout & Escalation** rules above to this dispatch (and to every fix subagent dispatch below). The testing subagent makes no commits, so judge its progress by `ListAgents` and live test processes — a Phase B that runs for 20 minutes is not a stall.

If the testing subagent reports any failures:
1. Spawn a new **fix subagent** using the Agent tool, giving it the failing test output and the plan file's absolute path (instruct it to read the plan file itself, not a pasted copy). Instruct it to fix only the failing implementation (minimal change, do not alter tests), to make the fix itself directly rather than spawning any subagent of its own (same reasoning as the testing subagent above — this is a bounded, single-context fix, not a controller task), to verify its fix by running only the previously failing tests plus the Feature tests command (never the full suite — the testing subagent runs that), to commit the fix when done, and to report back with a 1-2 line summary of the fix, not a diff dump.
2. Re-dispatch the testing subagent, passing the names of the tests that failed as `<EXTRA_TESTS>`.
3. Repeat until both phases pass.

Show the user only the current round's pass/fail counts between iterations, not a running log of every prior round.

### Step 5 — Confirm

Only when the testing subagent reports PASS for both phases (Feature tests and Full suite) — a Phase A pass alone is not enough, since the full suite has not yet proven nothing pre-existing broke — say:

> *"Implementation complete. All tests defined in `docs/<feature-id>-<idea-slug>-<file-id>-PLAN.md` pass."*

### Step 6 — Write issue log

Only if the plan file is `docs/<feature-id>-<idea-slug>-<file-id>-PLAN-N.md` (an issue-derived plan, not a plain `docs/<feature-id>-<idea-slug>-<file-id>-PLAN.md`):

To check whether an `ISSUE-N-LOG.md` already exists for this `<feature-id>-<idea-slug>` and this issue number, search with the glob `docs/<feature-id>-<idea-slug>-*-ISSUE-N-LOG.md` (replace `N` with the literal issue number). If more than one result comes back, use the one with the highest file-id. When you write over this file to update it (not create a new one), write to the exact path found — do NOT assign it a new file-id. This skill regenerates the whole `ISSUE-N-LOG.md` (it does not merge with a prior version) but must still keep the file's existing file-id if the file already existed.

If no such file exists yet, compute a new `<file-id>` before writing:
1. List the files in `docs/` that start with `<feature-id>-<idea-slug>-` (e.g. `ls docs/ | grep '^<feature-id>-<idea-slug>-'`).
2. From each name found, extract the numeric segment immediately after `<idea-slug>-` and before the next hyphen — that's the existing file-id of that file.
3. The new `<file-id>` = (the highest number extracted) + 1, or `1` if no file starts with `<feature-id>-<idea-slug>-`.

Write `docs/<feature-id>-<idea-slug>-<file-id>-ISSUE-N-LOG.md` (same `<feature-id>` as the plan, and the file-id determined above — overwrite if it already exists — regenerate the whole file, do not merge with a prior version):

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

If the plan is a plain `docs/<feature-id>-<idea-slug>-<file-id>-PLAN.md` (SPEC- or PRD-derived, no issue number), skip Step 6 entirely — no log file is written.

## Hard Rules

- Do NOT run implementation or tests inline — always dispatch to subagents via the Agent tool, except for the second-stall inline takeover defined in **Subagent Timeout & Escalation**.
- Do NOT modify tests to make them pass — fix the implementation instead.
- Run the full test suite only as the Phase B gate of the testing subagent (Step 4) — never in the implementation or fix subagents, which run only Feature tests.
- Do NOT offer to merge, create a PR, or clean up branches/worktrees — that belongs in `/verify`, after the implementation has been validated.
