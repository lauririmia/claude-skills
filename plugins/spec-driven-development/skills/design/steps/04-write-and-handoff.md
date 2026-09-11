# Step 04 — Write DESIGN.md, Commit, Handoff

**Reads:** Confirmed restat from `03-confirm.md`.

**Does:**

### Write DESIGN.md

After explicit "yes", before writing the file, calculate `<file-id>`:
1. List the files in `docs/` that start with `<feature-id>-<idea-slug>-` (e.g. `ls docs/ | grep '^<feature-id>-<idea-slug>-'`).
2. From each name found, extract the numeric segment immediately after `<idea-slug>-` and before the next hyphen — this is that file's existing file-id.
3. The new `<file-id>` = (the highest number extracted) + 1, or `1` if no file starting with `<feature-id>-<idea-slug>-` exists yet.

Write `docs/<feature-id>-<idea-slug>-<file-id>-DESIGN.md`, **in Romanian** — the interview and the restat the user just confirmed were in Romanian, so the first draft on disk matches:

```markdown
# Intenție: <Idea Name>
Confirmat: <YYYY-MM-DD>

## Rezultat
<un rând>

## Utilizator
<un rând>

## De ce acum
<un rând>

## Criterii de succes
<un rând>

## Constrângeri
<un rând>

## În afara scopului
<un rând>
```

### Translate to English

The committed `DESIGN.md` and its handoff to `sdd:ideate`/`sdd:spec` run in English (see SKILL.md, Language section), because the rest of the plugin's tooling works in English. There is no separate file-review step here — the user already gave their explicit "yes" on the restat in `03-confirm.md`, so translate immediately, without asking again: it's a faithful rendering of what was just confirmed, not a content change.

Translate the file in full into English, preserving the same structure (`# Intent: <Idea Name>`, `Confirmed: <date>`, `## Outcome`, `## User`, `## Why Now`, `## Success Criteria`, `## Constraints`, `## Out of Scope`), and overwrite `docs/<feature-id>-<idea-slug>-<file-id>-DESIGN.md` with the English version — do not keep the Romanian copy on disk. Do not print the translated content in the console.

### Commit

`docs/<feature-id>-<idea-slug>-SESSION.md` exists only to survive a context compaction mid-session — once DESIGN.md is written (now in English) and about to be committed, its job is done. Delete it rather than committing it, so it never pollutes git history as a scratch file:

```bash
rm -f docs/<feature-id>-<idea-slug>-SESSION.md
git add docs/<feature-id>-<idea-slug>-<file-id>-DESIGN.md
git commit -m "docs: <idea-slug> intent confirmed"
```

### Handoff

Say: *"Intent confirmed and saved to `docs/<feature-id>-<idea-slug>-<file-id>-DESIGN.md`. Run `/sdd:ideate docs/<feature-id>-<idea-slug>-<file-id>-DESIGN.md` to explore solutions, or `/sdd:spec docs/<feature-id>-<idea-slug>-<file-id>-DESIGN.md` to go straight to spec."*

**Stop condition:** DESIGN.md written and committed.

**Hands off:** Terminal step — control returns to the user.
