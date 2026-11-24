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
| `convert` | `/mcs:convert` | ready | Convert the extracted recipe into the Monsieur Cuisine Smart form fields |
| `upload` | `/mcs:upload` | ready | Fill the Monsieur Cuisine form in the browser from the convert output and save it |

### `extract` — `/mcs:extract`

Builds a clean recipe from the conversation context, pasted text, a website URL, or a video link (YouTube etc., via its transcript).

- **Input:** optional prompt. With no prompt it uses the recipe already in the conversation, and asks for text or a link if there is none.
- **Keeps:** ingredients, quantities, servings, difficulty, times, steps, serving, calories. Drops comments, ads and product placements.
- **Ingredient order:** by first use in the steps (garnish last), quantities untouched; groups only when the source has them.
- **Permissions:** `allowed-tools: Bash(python3:*), WebFetch, Read` in the skill's frontmatter, so its two scripts run without a prompt each time.
- **Output:** Romanian Markdown in chat, formatted as a printable cooking guide, ready to copy and save before `/mcs:convert`. Missing fields are marked `nespecificat`, never invented.
- **Web pages** are read with [skills/extract/scripts/fetch_page.py](skills/extract/scripts/fetch_page.py), which prefers the page's schema.org `Recipe` data (exact quantities) over summaries.
- **Video transcripts** use [skills/extract/scripts/get_transcript.py](skills/extract/scripts/get_transcript.py). If `yt-dlp` is missing it installs itself under `~/.cache/mcs` (venv+pip, then `uv`, then direct download of the `yt-dlp` file), never system-wide. If the video has no usable captions (missing, or only `[Music]`) or there is no network, the skill asks the user to paste the transcript.

See [skills/extract/SKILL.md](skills/extract/SKILL.md).

### `convert` — `/mcs:convert`

Converts the recipe from `/mcs:extract` into the exact content of the monsieur-cuisine.com "Creare rețetă" form for the Smart device.

- **Input:** the extract output, pasted in chat or already in the conversation.
- **Flow:** (1) asks the user, one question at a time with a recommended option, about anything ambiguous (over-capacity quantities, unclear portions, missing data); (2) maps the recipe to the form: units limited to the form's list (liquids converted to grams), ingredient additions as Cântar steps, cooking as device programs within their ranges; (3) estimates nutrition per portion from web research; (4) finds the recipe image on the source page and crops it to 1560×945 px, or asks the user for one — if none fits, it offers a ready-to-paste ChatGPT image prompt for the dish (it never stretches a small image).
- **Credits:** when the source was a website or video URL, the short description ends with a blank line and `Credits: <URL>`, always with a clean URL (tracking parameters such as `utm_*`, `si`, `feature`, `fbclid` removed); the 240-character limit counts that line too.
- **Output:** one Markdown block in chat (nothing written to disk except the image `<slug>-mcs.jpg`), ready for copy/paste and for the future `upload` skill.
- **References** (bundled in [skills/convert/references/](skills/convert/references/)): form schema, device capabilities (from the manual) and preparation tips.
- **Image script:** [skills/convert/scripts/prepare_image.py](skills/convert/scripts/prepare_image.py) (uses Pillow, installed temporarily through `uv` if missing).

See [skills/convert/SKILL.md](skills/convert/SKILL.md).

### `upload` — `/mcs:upload`

Fills the "Creare rețetă" form on monsieur-cuisine.com (MC smart) from the `/mcs:convert` block, using the browser pane.

- **Handed to the user:** login (it never types passwords), choosing the device if asked, the image file picker, and the "created with AI" declaration.
- **Asks first:** ticking the terms of use, saving as project, and finalizing.
- **Flow:** details → time → ingredients (groups, units) → steps (text, Cântar, Gătire manuală, Aluat moale and the other programs) → "Salvare proiect" (gives a `recipe-id`). "Completare rețetă → Salvare ca privat" only on the user's explicit request; it never publishes.
- **Quirks** (late-appearing controls, what `form_input` cannot set, sliders by keyboard) are listed in the skill.

See [skills/upload/SKILL.md](skills/upload/SKILL.md).

See [skills/workflow/SKILL.md](skills/workflow/SKILL.md) for the pipeline details.

## Maintaining this README

Update this file whenever a skill is added or changes status: the Skills table, and the Workflow section if the order changes. Bump `version` in [.claude-plugin/plugin.json](.claude-plugin/plugin.json) in the same commit.
