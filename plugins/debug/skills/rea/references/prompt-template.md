# Investigation prompt template

Fill the brackets from the interview. Drop sections that don't apply (e.g. the clone section for
an investigate-only run). Keep the user's own wording for their goals and pain points. Save the final
text to `<output>/prompt.md`.

The prompt below is modelled on a run that worked very well: it names the targets, describes what the
user already observed, lists what to find, forbids modification, and asks for evidence plus
improvements.

```text
[Context: where the target is installed and what the user already knows about it, e.g. the
extension IDs / store URLs, version, and what the screenshots show.]

Targets (read-only copies are in [output]/work/target-copy/):
- [target 1: name, type, id, version]
- [target 2 ...]

Use REA [and Ghidra, if the tooling check required it] to understand how [each target] works.
Do not modify the originals; work only on the copies.

Find out and document:
- [what data it collects and from where (endpoints, pages, APIs, local storage)]
- [how it authenticates / reuses the user's session]
- [how often it refreshes, how alerts/notifications are scheduled]
- [how the UI is built and which features it offers]
- [anything else the user asked for]

Write everything to [output]/EVIDENCE.md: for each finding give the file/function it comes
from and how it was established, list what could not be verified, and do not paste
secrets or tokens (record that they exist and where).

Then tell me what can be improved, ranked by how well it addresses these problems:
- [pain point 1, in the user's words]
- [pain point 2 ...]

[Clone only] Using what you learned, build [clone name] in [output]/[clone-name]/ as an
original implementation (do not copy the targets' code, assets or branding). Requirements:
- [required features, platforms, accounts model, UI parity targets]
- [installation targets]
Verify it and state exactly what you tested.
```
