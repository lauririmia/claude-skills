# Step 05 — Phase 3: Sharpen

**Reads:** Confirmed direction from `04-converge.md`.

**Does:**

After the user confirms a direction, write `docs/<feature-id>-<idea-slug>-IDEATE.md`, **in Romanian**:

```markdown
# Ideate: <Idea Name>
Data: <YYYY-MM-DD>

## Enunțul problemei
<formulare de tip "How Might We" — o singură propoziție>

## Direcția recomandată
<direcția aleasă și de ce — 2-3 paragrafe maxim>

## Asumpții cheie de validat
- [ ] <Asumpție — cum se testează>
- [ ] <Asumpție — cum se testează>

## Scop MVP
<Versiunea minimă care testează asumpția principală. Ce intră, ce nu intră.>

## Ce nu facem (și de ce)
- <Lucru> — <motiv>
- <Lucru> — <motiv>

## Întrebări deschise
- <Întrebare care are nevoie de răspuns înainte de a construi>
```

Tell the user: *"IDEATE.md a fost scris în `docs/<feature-id>-<idea-slug>-IDEATE.md`. Te rog să-l revizuiești și să-mi spui dacă ai modificări sau dacă îl aprobi."*

If the user provides feedback, update the file (still in Romanian) and ask again. When they explicitly approve, proceed to the translation below.

**Once approved — translate to English:**

The committed `IDEATE.md` and the `sdd:spec` handoff run in English (see SKILL.md, Language section). Translate the file in full into English, preserving the same structure (`# Ideate: <Idea Name>`, `## Problem Statement`, `## Recommended Direction`, `## Key Assumptions to Validate`, `## MVP Scope`, `## Not Doing (and Why)`, `## Open Questions`), and overwrite `docs/<feature-id>-<idea-slug>-IDEATE.md` with the English version — do not keep the Romanian copy on disk. This is a faithful rendering of what the user just approved, not a content change, so it doesn't need a separate approval round. Do not print the translated content in the console.

**Stop condition:** User explicitly approves the IDEATE.md content, and the file has been translated to English on disk.

**Hands off:** Approved, English-language `docs/<feature-id>-<idea-slug>-IDEATE.md` to `06-commit-and-handoff.md`.
