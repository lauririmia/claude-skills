# Step 04 — Write Issue Files

**Reads:** Approved issue list from `03-issue-breakdown.md`.

**Does:**

Write issues in dependency order (blockers first). For each approved issue, before writing its file, calculate `<file-id>`:

> Înainte de a scrie fișierul, calculează `<file-id>`:
> 1. Listează fișierele din `docs/` care încep cu `<feature-id>-<idea-slug>-` (ex: `ls docs/ | grep '^<feature-id>-<idea-slug>-'`).
> 2. Din fiecare nume găsit, extrage segmentul numeric imediat după `<idea-slug>-` și înainte de următoarea cratimă — acesta e file-id-ul existent al acelui fișier.
> 3. `<file-id>` nou = (cel mai mare număr extras) + 1, sau `1` dacă nu există niciun fișier care să înceapă cu `<feature-id>-<idea-slug>-`.

Recompute `<file-id>` this way for EACH issue file, one at a time, right before writing it — each `ISSUE-N.md` gets its own distinct, sequentially-next `<file-id>` (e.g. if `PRD.md` took `<file-id>` 4, `ISSUE-1.md` takes 5, `ISSUE-2.md` takes 6, and so on). Do not reuse one `<file-id>` across multiple issue files.

Write directly to `docs/<feature-id>-<idea-slug>-<file-id>-ISSUE-N.md`, **in Romanian**, without displaying its full content in the console. After all files are written, tell the user: *"N fișiere de issue scrise în `docs/<feature-id>-<idea-slug>-<file-id>-ISSUE-1.md` … `docs/<feature-id>-<idea-slug>-<file-id>-ISSUE-N.md`. Te rog să le revizuiești și să-mi spui dacă ai modificări sau dacă le aprobi."* If the user provides feedback, update the relevant files (still in Romanian) and ask again.

Issue structure:

```markdown
# <Feature Name> — Issue N: <Title>

**Type:** AFK / HITL
**Blocked by:** None / `<feature-id>-<idea-slug>-<file-id>-ISSUE-N.md`

## Ce trebuie construit

Descriere concisă a acestei felii verticale — comportament de la un capăt la altul, nu strat cu strat.
Evită căi de fișiere sau fragmente de cod decât dacă un fragment dintr-un prototip codifică
o decizie mai precis decât proza — include-l inline și notează că provine dintr-un prototip.

## Criterii de acceptare

- [ ] Criteriul 1
- [ ] Criteriul 2
```

`**Type:**` and `**Blocked by:**` are process metadata, not prose — keep them as-is (untranslated) in both the Romanian draft and the English version below.

**Once approved — translate to English:**

Only after the user explicitly approves all issue files: translate every `docs/<feature-id>-<idea-slug>-<file-id>-ISSUE-N.md` in full into English, preserving the original header structure (`## What to build`, `## Acceptance criteria`), and overwrite each file with its English version — these are the same files written above, at their exact paths; do not compute new file-ids. Do not keep the Romanian copies on disk. This is a faithful rendering of what was just approved, not a content change, so it doesn't need a separate approval round. Do not print the translated content in the console.

Only commit all docs (PRD + issues — both already translated to English) to git when the user **explicitly approves** (e.g. "looks good", "approve", "done", "ok"). Do NOT commit automatically. Do NOT commit while any of these files is still in Romanian.

**Stop condition:** User explicitly approves all issue files; all files translated to English; PRD + issues committed.

**Hands off:** Committed, English-language PRD and issue files to `05-handoff.md`.
