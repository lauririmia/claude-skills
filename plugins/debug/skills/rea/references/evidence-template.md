# EVIDENCE.md template

```markdown
# Evidence: <target name(s)>

## 1. Scope
- Question asked: <the user's goal in one or two lines>
- Outcome: investigate | investigate + clone
- Date, machine OS

## 2. Targets
| Target | Type | ID / path | Version | Copy analysed |
|---|---|---|---|---|

## 3. Method and tools
Tools with versions (REA, Ghidra/JDK if used, others), commands or REA operations run, and
confirmation that originals were not modified (e.g. checksums before/after).

## 4. Findings
For each finding:
### F<n> <short title>
- **Claim:** what it does
- **Evidence:** file path + line / function / REA result (short excerpt, no secrets)
- **Confidence:** confirmed | inferred
- **Relevance:** why it matters for the user's goal

Cover, where applicable: permissions and host access, background logic, data sources and
endpoints, authentication/session handling, storage, scheduling and alerts, UI structure and
features, update/telemetry behavior.

## 5. Could not verify
What was not determined, and why (obfuscation, runtime-only behavior, not tested).

## 6. Risks and fragility
Private/undocumented APIs, terms-of-service concerns, privacy implications, breakage risks.

## 7. Improvement proposals
| # | Proposal | Addresses (user's pain point) | Effort | Value |
|---|---|---|---|---|

## 8. Clone notes (if applicable)
Design derived from the findings, requirements confirmed with the user, location of the
clone, what was tested.
```
