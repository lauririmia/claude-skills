# mcs — Monsieur Cuisine Smart

Plugin for converting an existing recipe into a format compatible with the **Monsieur Cuisine Smart** multi cooker and uploading it to the device through the Monsieur Cuisine account.

Invoked as `/mcs:<skill>`. Start with `/mcs:workflow`, which defines the order the skills run in.

## Workflow

```
source  ──►  extract  ──►  convert  ──►  upload  ──►  recipe on device
```

Supported recipe sources: web URL, pasted text, screenshot/PDF, local Markdown/text file, YouTube video link (the transcript is extracted first).

Upload is done through browser automation against the Monsieur Cuisine account (no public API is assumed).

## Skills

| Skill | Command | Status | Purpose |
|---|---|---|---|
| `workflow` | `/mcs:workflow` | ready | Orchestrator: defines the order of the skills below and which ones exist yet |
| `extract` | `/mcs:extract` | planned | Turn any supported source into a normalized recipe |
| `convert` | `/mcs:convert` | planned | Map the normalized recipe to the Monsieur Cuisine Smart format |
| `upload` | `/mcs:upload` | planned | Save the recipe to the Monsieur Cuisine account via the browser |

See [skills/workflow/SKILL.md](skills/workflow/SKILL.md) for the pipeline details.

## Maintaining this README

Update this file whenever a skill is added or changes status: the Skills table, and the Workflow section if the order changes. Bump `version` in [.claude-plugin/plugin.json](.claude-plugin/plugin.json) in the same commit.
