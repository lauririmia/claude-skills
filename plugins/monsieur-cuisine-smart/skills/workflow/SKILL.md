---
name: workflow
description: Entry point and orchestrator for the Monsieur Cuisine Smart (mcs) plugin. Use whenever the user wants to convert a recipe (URL, pasted text, screenshot/PDF, local Markdown file, or a YouTube video link) for the Monsieur Cuisine Smart multi cooker, upload a recipe to their Monsieur Cuisine account/device, or says "/mcs", "monsieur cuisine", "mcs workflow", "adaugă rețeta pe Monsieur Cuisine". Defines the order in which the mcs skills run and which of them already exist.
---

# mcs — workflow

This skill does not convert or upload anything itself. It decides which mcs skill runs next, in what order, and what is handed from one step to the next. Keeping the order here means each skill can stay small and single-purpose.

## Pipeline

```
source  ──►  1. extract  ──►  2. convert  ──►  3. upload  ──►  recipe on device
(any)        normalized        MCS-compatible    browser          (Monsieur Cuisine
             recipe            recipe            automation        account)
```

| # | Skill | Status | Input | Output |
|---|---|---|---|---|
| 1 | `extract` | ready | Recipe source: web URL, pasted text, screenshot/PDF, local Markdown/text file, or YouTube link (transcript is extracted first) | A clean Romanian Markdown recipe (title, servings, difficulty, times, calories, ingredients, steps, serving), returned in chat for copy/paste |
| 2 | `convert` | ready | The Markdown from `extract` (pasted in chat or in the conversation) | Three things, written from the same data: a copy/paste-ready Markdown block in chat with every field of the monsieur-cuisine.com form (details, estimated nutrition, times, ingredients, device steps with programs); the image `<slug>-mcs.jpg`; and `<slug>-mcs.json`, the schema-validated machine-readable version. Both files go in the user's working directory |
| 3 | `upload` | ready | The `<slug>-mcs.json` from `convert` (the Markdown block is not read) | A Playwright script (`upload/scripts/upload.py`) fills the form in Chrome, saves it as a project (`--save`) and, only on the user's explicit request, finalizes it as a private recipe (`--finalize-private`). The user types the password; cookies, terms, device choice and the AI-image box are handled by the script. The result is a `recipe-id` and an image check |

"Planned" means a skill has not been written yet. Skills are added one at a time, and the README is updated each time (see Maintenance).

## How to run

1. Identify the recipe source from the user's message. If there is none, ask for it.
2. Walk the pipeline in order. Before each step, check the Status column: if the skill exists (status `ready`), invoke it as `/mcs:<skill>`; if it is `planned`, tell the user that step is not defined yet and stop there rather than improvising it. An improvised conversion or upload would produce a recipe format nobody has verified against the real device.
3. Pass each step's output to the next explicitly: `extract`'s Markdown goes to `convert`, and `convert`'s JSON file path goes to `upload`. Show the user the result of `convert` before `upload`. Uploading changes the user's account, so saving and finalizing need their go-ahead.
4. The user may start mid-pipeline (e.g. they already have a normalized recipe). Skip the steps whose output they already have.

## Maintenance

When a new skill is added to the plugin:

1. Create `skills/<name>/SKILL.md`.
2. Change its row in the pipeline table above from `planned` to `ready` (or add a row and place it at the right position if it is a new step).
3. Update `README.md` (skill list and pipeline).
4. Bump `version` in `.claude-plugin/plugin.json`, since installed copies are cached by version.
