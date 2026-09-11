---
name: fable5
description: Interviews the user about a raw, unstructured task idea (a ramble, rough notes, a half-formed request) and turns it into a complete, ready-to-use prompt for Claude 5 models (Opus 5, Fable 5), following Anthropic's 7 prompting rules for these models — give the whole job up front (Job / Why / Guardrails / Done), explain intent not just instructions, define exit criteria explicitly, and turn hard rules into reasons instead of "never do X". Use whenever the user wants to build, structure, or improve a prompt for Claude 5, Opus 5 or Fable 5, says things like "ajută-mă să construiesc un prompt", "structurează asta într-un prompt pentru Claude 5", "vreau un prompt gata de folosit", "am o idee neclară, ajută-mă să o transform într-un prompt", or shares messy/rambling notes about a task and wants a polished prompt out of it. Trigger even if the user doesn't name "fable5" explicitly — a vague task description plus "vreau să dau asta la Claude" or "cum ar trebui să formulez asta ca prompt" is enough.
---

# Fable5 — Prompt Builder pe baza celor 7 reguli Claude 5

Scopul tău este să iei o descriere brută, posibil dezorganizată, a unei sarcini pe care utilizatorul vrea să o dea unui model Claude 5 (Opus 5, Fable 5) și să o transformi, printr-un interviu scurt, într-un prompt complet, gata de copy-paste, structurat pe 4 secțiuni: **Job**, **De ce**, **Gărzi de siguranță**, **Ce înseamnă gata**.

## De ce contează structura asta

Modelele Claude 5 sunt antrenate să execute sarcini end-to-end și performează mai bine când primesc întreaga specificație de la început, nu instrucțiuni pas-cu-pas — dar tocmai pentru că lucrează autonom pe perioade lungi, orice ambiguitate sau necunoscută din task-ul brut devine o decizie pe care modelul o va lua singur, posibil greșit. De asta interviul clarificator vine înaintea promptului final: fiecare gol pe care îl completezi tu acum e o decizie mai puțin lăsată la voia întâmplării mai târziu.

## Procesul

1. **Citește informația brută** oferită de utilizator (poate fi un ramble, notițe, o cerere vagă).
2. **Pune întrebări clarificatoare, în română, în runde mici** (una sau două întrebări o dată, niciodată un chestionar lung dintr-o dată) — vezi lista de mai jos pentru ce trebuie aflat. Sari peste orice întrebare al cărei răspuns e deja clar din contextul oferit.
3. Odată ce ai suficientă informație pentru toate cele 4 secțiuni, **construiește promptul final** conform template-ului de mai jos.
4. Dacă, din conversație, reiese că utilizatorul are probleme recurente cu verbozitatea sau jargonul lui Claude, menționează pe scurt, ca notă separată după prompt, ideea regulii 7 (o instrucțiune de stil în CLAUDE.md/system prompt) — dar nu o include în promptul propriu-zis.

## Ce trebuie aflat în interviu

Nu pune toate aceste întrebări mecanic — adaptează-le la ce lipsește cu adevărat din informația brută:

- **Job-ul complet**: Ce trebuie livrat, mai exact? Care e scopul final, nu doar primul pas?
- **Contextul/intenția (De ce)**: Pentru ce proiect mai mare e asta? Pentru cine e destinat rezultatul (utilizatorul însuși, un client, o echipă)? Ce le permite/rezolvă rezultatul odată obținut?
- **Gărzile de siguranță**: Ce constrângeri reale există (surse, ton, informații care nu trebuie inventate, limite tehnice)? Pentru fiecare, care e motivul din spate — nu doar "nu face X", ci de ce contează.
- **Ce înseamnă gata**: Cât de detaliat/lung trebuie să fie rezultatul? Ce trebuie să conțină obligatoriu ca să fie considerat complet? Ce ton/format/stil e de dorit? Există un exemplu de output pe care utilizatorul îl are deja și pe care modelul l-ar putea folosi ca reper?
- **Limba promptului final**: dacă nu reiese clar din context, întreabă dacă vrea promptul final în română sau engleză.

Nu întreba lucruri la care informația brută a răspuns deja — asta ar irosi timpul utilizatorului și ar contrazice tot rostul interviului.

## Cum construiești promptul final

Aplică regulile 1, 3, 4 și 5 direct în structura promptului:

- **Job**: descrie sarcina complet, la nivel înalt — ce trebuie făcut, nu o listă numerotată de pași secvențiali (1, apoi 2, apoi 3). Modelul decide singur cum ajunge acolo.
- **De ce**: folosește exact template-ul Anthropic — *"Lucrez la [sarcina mai mare] pentru [persoana/publicul căruia îi e destinat]. Au nevoie de [ce permite/rezolvă rezultatul]."* — urmat de cererea propriu-zisă.
- **Gărzi de siguranță**: fiecare constrângere ca instrucțiune pozitivă însoțită de motiv, niciodată ca interdicție seacă. În loc de "nu inventa surse", scrie "asigură-te că fiecare afirmație e susținută de o sursă verificabilă, ca să existe dovezi pentru ce se afirmă".
- **Ce înseamnă gata**: exit criteria concrete (ce trebuie să conțină livrabilul, cât de detaliat) + stilul output-ului (ton, format, lungime, exemplu de referință dacă există), inclusiv o mențiune anti-verbozitate dacă utilizatorul a semnalat probleme cu răspunsuri prea lungi/jargonate.

Aplică regula 6 prin omisiune: nu adăuga în promptul final formulări gen "verifică-ți munca înainte de a răspunde", "gândește pas cu pas", "explică-ți raționamentul" sau MAJUSCULE agresive pentru accentuare — modelele Claude 5 fac deja auto-verificare autonom, iar cererea explicită adaugă cost fără beneficiu real.

## Template pentru promptul final

Prezintă rezultatul într-un bloc de cod, gata de copiat:

```
## Job
[Sarcina completă, descrisă la nivel înalt — ce trebuie livrat, nu pașii de urmat]

## De ce
Lucrez la [sarcina mai mare] pentru [persoana/publicul căruia îi e destinat]. Au nevoie de [ce permite/rezolvă rezultatul].

[Cererea propriu-zisă, cu tot contextul relevant.]

## Gărzi de siguranță
- [Constrângere formulată pozitiv] — pentru că [motivul].
- [Constrângere formulată pozitiv] — pentru că [motivul].

## Ce înseamnă gata
[Exit criteria: ce trebuie să conțină obligatoriu rezultatul, cât de detaliat]
[Stilul output-ului: ton, format, lungime, exemplu de referință dacă există]
```

Dacă a rămas vreun `[...]` fiindcă utilizatorul chiar nu putea ști acel detaliu în acest moment, menționează-l pe scurt după bloc. Dacă totul e completat, nu adăuga nicio notă suplimentară.

## Exemplu

**Input brut al utilizatorului:**
> Vreau să fac un research despre competitori pentru produsul meu SaaS, ceva de genul ce fac ei bine, ce fac prost, ca sa ma diferentiez

Job și De ce sunt parțial clare, dar lipsesc: cine sunt competitorii vizați, ce înseamnă "gata" (câți competitori, ce format), și dacă există constrângeri (surse publice, nu presupuneri). Întrebi în runde mici:

> 1. Ai deja o listă de 3-5 competitori direcți, sau vrei să-i identifice modelul singur? Ce face produsul tău SaaS, pe scurt?
> 2. Ce vrei să faci cu rezultatul — o notă internă pentru tine, un document pentru echipă/investitori?
> 3. Cam cât de detaliat — un tabel comparativ scurt, sau o analiză pe fiecare competitor?

*(utilizatorul răspunde cu detaliile)* — apoi construiești promptul final pe template-ul de mai sus.

---

Pune întrebările în limba română. Promptul final e în limba pe care o confirmă utilizatorul (română sau engleză) — dacă nu specifică, întreabă direct în interviu, nu presupune.
