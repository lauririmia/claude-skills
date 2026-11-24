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
| `extract` | `/mcs:extract` | ready | Turn a source into a clean, print-ready Romanian Markdown recipe |
| `convert` | `/mcs:convert` | planned | Map the normalized recipe to the Monsieur Cuisine Smart format |
| `upload` | `/mcs:upload` | planned | Save the recipe to the Monsieur Cuisine account via the browser |

### `extract` — `/mcs:extract`

Builds a clean recipe from the conversation context, pasted text, a website URL, or a video link (YouTube etc., via its transcript).

- **Input:** optional prompt. With no prompt it uses the recipe already in the conversation, and asks for text or a link if there is none.
- **Keeps:** ingredients, quantities, servings, difficulty, times, steps, serving, calories. Drops comments, ads and product placements.
- **Output:** Romanian Markdown in chat, formatted as a printable cooking guide, ready to copy and save before `/mcs:convert`. Missing fields are marked `nespecificat`, never invented.
- **Web pages** are read with [skills/extract/scripts/fetch_page.py](skills/extract/scripts/fetch_page.py), which prefers the page's schema.org `Recipe` data (exact quantities) over summaries.
- **Video transcripts** use [skills/extract/scripts/get_transcript.py](skills/extract/scripts/get_transcript.py). If `yt-dlp` is missing it installs itself under `~/.cache/mcs` (venv+pip, then `uv`, then direct download of the `yt-dlp` file), never system-wide. If the video has no usable captions (missing, or only `[Music]`) or there is no network, the skill asks the user to paste the transcript.

See [skills/extract/SKILL.md](skills/extract/SKILL.md).

See [skills/workflow/SKILL.md](skills/workflow/SKILL.md) for the pipeline details.

## Maintaining this README

Update this file whenever a skill is added or changes status: the Skills table, and the Workflow section if the order changes. Bump `version` in [.claude-plugin/plugin.json](.claude-plugin/plugin.json) in the same commit.
