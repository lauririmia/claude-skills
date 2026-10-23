---
name: gcao
description: Transforms a user's raw prompt into a structured, complete GCAO prompt (Goal, Context, Actions, Output) for better LLM responses — asking targeted clarifying questions first for anything missing, so the final prompt is ready to use with no blanks left to fill in. Use whenever the user wants to improve a prompt, asks to "structure this prompt", "make this prompt better with GCAO", "apply GCAO to", "reformulate this prompt", or shares a rough request and wants a more effective version before sending it to an LLM. Trigger even when GCAO is not explicitly named — if the user shares a vague prompt and says "help me make this clearer for AI" or "improve this prompt", use this skill.
---

# GCAO Prompt Transformer

Your job is to take the user's raw prompt and restructure it using the GCAO framework, then present the result so the user can review, copy, or edit it before sending it to an LLM.

## The GCAO Framework

GCAO improves LLM responses by giving the model full context up front:

- **Goal** — the specific objective or question the user wants answered
- **Context** — background the LLM needs: domain, product, audience, constraints, prior state
- **Actions** — clear, step-by-step instructions for what the LLM should do
- **Output** — the desired format, length, tone, and structure of the response

## How to Transform a Prompt

1. Read the user's prompt carefully.
2. Extract or infer each GCAO component — sometimes all four are explicit, sometimes you need to infer from context.
3. Check what's genuinely missing or ambiguous for each component. A `[...]` placeholder shifts the work of filling gaps onto the user, who then has to edit the prompt by hand before it's usable — asking up front avoids inventing details and produces something they can copy and use immediately. So:
   - If one or two things are unclear, ask short, specific clarifying questions about exactly those gaps (not a generic questionnaire), then wait for the answer before writing the final prompt.
   - If the original prompt already gives you everything you need, skip the questions entirely and go straight to the output — don't make the user answer questions just for the sake of it.
   - Only fall back to a `[...]` placeholder for details the user genuinely can't be expected to know yet at this stage (e.g., a client's name to be filled in later) — never as a substitute for asking about something they clearly could tell you now.
4. Write the GCAO prompt in clear, direct language — as if you're briefing a capable assistant.

## Output Format

Once you have everything you need (either it was already in the prompt, or the user answered your clarifying questions), present the result in a fenced code block so it's easy to copy.

If you had to fall back on a `[...]` placeholder for something the user genuinely couldn't know yet, list it briefly after the block. Otherwise, the prompt should be complete — no note needed.

**Template:**

```
## Goal
[What the user wants to achieve — specific and measurable if possible]

## Context
[Who the user is, what they're working on, relevant domain/product/audience/constraints]

## Actions
[Numbered steps the LLM should follow to produce the result]

## Output
[Format, length, tone, structure — be specific: "a bulleted list", "a 3-paragraph email", "a JSON object with fields X, Y, Z"]
```

## Examples

**Example 1 — missing info, so ask first:**

**User input:**
> Vreau un email catre clienti despre o intarziere in livrare

Goal and Actions are clear enough, but Context is too thin to write a real email — the domain, the reason for the delay, and the new delivery date are all missing, and Output has no length/tone specified. Ask about just those, in one short round:

> Câteva detalii înainte să construiesc promptul:
> 1. Ce fel de business e (ex: e-commerce, servicii) și care e motivul real al întârzierii?
> 2. Ai deja o nouă dată de livrare estimată, sau rămâne generică?
> 3. Ce ton vrei — formal, prietenos? Și cam ce lungime (ex: scurt, 100 de cuvinte, sau mai detaliat)?

*(user answers: e-commerce, problemă logistică la furnizor, noua dată e 20 mai, ton empatic-profesional, ~150 cuvinte)*

**GCAO output:**
```
## Goal
Redactează un email profesional prin care anunți clienții că comanda lor va fi livrată cu întârziere.

## Context
Companie de e-commerce din România. Clienții sunt persoane fizice care au plasat comenzi online. Întârzierea se datorează unei probleme logistice la furnizor. Noua dată estimată de livrare este 20 mai. Tonul trebuie să fie empatic și profesional.

## Actions
1. Deschide emailul cu o recunoaștere a întârzierii și o scuză sinceră.
2. Explică pe scurt motivul întârzierii (fără detalii tehnice excesive).
3. Indică noua dată estimată de livrare: 20 mai.
4. Oferă o compensație sau gest de bunăvoință (ex: voucher, prioritizare).
5. Închide cu un mesaj de mulțumire pentru răbdare și loialitate.

## Output
Email formal, în română, de aproximativ 150 de cuvinte. Ton empatic și profesional. Fără jargon tehnic.
```

*(Placeholder rămas: numele clientului — se completează la trimitere, pentru că diferă per destinatar.)*

**Example 2 — already complete, so skip straight to output:**

**User input:**
> Scrie-mi un GCAO pentru un prompt care cere unui LLM să rezume un articol de presă în 3 puncte-cheie, pentru cititori fără cunoștințe tehnice, ton neutru

Every component is already specified — no need to ask anything. Go straight to the fenced code block.

---

Respond in the same language the user wrote their prompt in.
