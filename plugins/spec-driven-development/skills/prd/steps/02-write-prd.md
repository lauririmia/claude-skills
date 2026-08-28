# Step 02 — Write the PRD

**Reads:** Confirmed seams from `01-seams.md`.

**Does:**

Write directly to `docs/<feature-id>-<idea-slug>-PRD.md`, **in Romanian**, without displaying its full content in the console. Just confirm the path. Then tell the user: *"PRD-ul a fost scris în `docs/<feature-id>-<idea-slug>-PRD.md`. Te rog să-l revizuiești și să-mi spui dacă ai modificări înainte să trecem la descompunerea în issue-uri."* If the user provides feedback, update the file (still in Romanian) and ask again.

The PRD structure to use:

```markdown
# <Feature Name> — PRD

## Enunțul problemei

Problema cu care se confruntă utilizatorul, din perspectiva utilizatorului.

## Soluție

Soluția la problemă, din perspectiva utilizatorului.

## Poveștile utilizatorilor

1. Ca <actor>, vreau <funcționalitate>, ca să <beneficiu>

## Decizii de implementare

- Schimbări de interfață
- Decizii arhitecturale
- Schimbări de schemă
- Contracte de API (doar acolo unde sunt relevante extern — vezi Scope Boundary mai jos)
- Interacțiuni specifice

Nu include căi de fișiere sau fragmente de cod decât dacă un fragment dintr-un prototip
codifică o decizie mai precis decât proza (mașină de stări, schemă, formă de tip) — inclu-l
inline și notează că provine dintr-un prototip.

## Decizii de testare

- Ce face un test bun pentru această funcționalitate
- Ce module vor fi testate
- Precedente pentru teste în codebase

## În afara scopului

Listă explicită a ceea ce acest PRD nu acoperă.

## Note suplimentare

Orice context adițional.
```

## Scope Boundary: What, Not How

Applies to `docs/<feature-id>-<slug>-PRD.md` only — NOT to `docs/<feature-id>-<slug>-ISSUE-N.md` files, which may continue to inline a prototype snippet per the existing rule ("unless a prototype snippet encodes a decision more precisely than prose").

This rule is about *content*, not language — apply it to the Romanian draft, before translation. In the Enunțul problemei / Soluție / Poveștile utilizatorilor sections: no code snippets, no method/function names, no file paths, no internal module names (these stay recognizable regardless of the surrounding language, since identifiers aren't translated). User-facing or third-party platform/integration names ARE allowed where the user genuinely interacts with them (e.g. "autentificare cu Google", "export în Notion") — the boundary is *implementation technology* (how it's built), not *product surface* (what the user sees and touches).

Example — disallowed: "apelează `validateSession()` din `auth/middleware.ts` folosind JWT." Example — allowed: "utilizatorul rămâne autentificat între reîncărcările paginii."

The Implementation Decisions section may name modules, schemas, and API contracts per the existing template, but only for contracts that are externally relevant (e.g. a public API shape another team integrates with) — not internal file/module references. The Testing Decisions section ("Which modules will be tested") is NOT subject to this boundary — naming internal modules there is fine, since it describes test scope rather than product-facing solution content. Before writing the PRD, scan the Implementation Decisions section against this rule and strip violations.

**Once approved — translate to English:**

`03-issue-breakdown.md`, `04-write-issues.md`, and the `plan` skill that later consumes this PRD all work in English (the Scope Boundary rule above and the rest of the plugin's tooling are written against English content). Translate `docs/<feature-id>-<idea-slug>-PRD.md` in full into English, preserving the original header structure (`## Problem Statement`, `## Solution`, `## User Stories`, `## Implementation Decisions`, `## Testing Decisions`, `## Out of Scope`, `## Further Notes`), and overwrite the file with the English version — do not keep the Romanian copy on disk. This is a faithful rendering of what the user just approved, not a content change, so it doesn't need a separate approval round. Do not print the translated content in the console.

**Stop condition:** User explicitly approves the PRD content (after the Scope Boundary scan), and the file has been translated to English on disk.

**Hands off:** Approved, English-language `docs/<feature-id>-<idea-slug>-PRD.md` to `03-issue-breakdown.md`.
