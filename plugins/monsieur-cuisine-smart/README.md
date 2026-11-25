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
| `upload` | `/mcs:upload` | ready | Run a Playwright script that fills the Monsieur Cuisine form from `<slug>-mcs.json` and saves it |

### `extract` — `/mcs:extract`

Builds a clean recipe from the conversation context, pasted text, a website URL, or a video link (YouTube etc., via its transcript).

- **Input:** optional prompt. With no prompt it uses the recipe already in the conversation, and asks for text or a link if there is none.
- **Keeps:** ingredients, quantities, servings, difficulty, times, steps, serving, calories. Drops comments, ads and product placements.
- **Ingredient order:** by first use in the steps (garnish last), quantities untouched; groups only when the source has them.
- **Permissions:** `allowed-tools: Bash(python3:*), WebFetch, Read` in the skill's frontmatter, so its two scripts run without a prompt each time.
- **Output:** Romanian Markdown in chat, formatted as a printable cooking guide, ready to copy and save before `/mcs:convert`. Missing fields are marked `nespecificat`, never invented.
- **Web pages** are read with [skills/extract/scripts/fetch_page.py](skills/extract/scripts/fetch_page.py), which prefers the page's schema.org `Recipe` data (exact quantities) over summaries.
- **Video transcripts** use [skills/extract/scripts/get_transcript.py](skills/extract/scripts/get_transcript.py). If `yt-dlp` is missing it installs itself under `~/.cache/mcs` (venv+pip, then `uv`, then direct download of the `yt-dlp` file), never system-wide. If the video has no usable captions (missing, or only `[Music]`), the skill offers to transcribe the audio locally with Whisper (`--whisper`: downloads the audio and, once, a `faster-whisper` model, chosen automatically: `small` ~0.5 GB if the description lists quantities, `medium` ~1.5 GB if not (`--model` overrides); the model is deleted right after the transcription unless `--keep-model` is passed; only with the user's yes). With no network, or if Whisper fails, it asks the user to paste the transcript.

See [skills/extract/SKILL.md](skills/extract/SKILL.md).

### `convert` — `/mcs:convert`

Converts the recipe from `/mcs:extract` into the exact content of the monsieur-cuisine.com "Creare rețetă" form for the Smart device.

- **Input:** the extract output, pasted in chat or already in the conversation.
- **Flow:** (1) asks the user, one question at a time with a recommended option, about anything ambiguous (over-capacity quantities, unclear portions, missing data); (2) maps the recipe to the form: units limited to the form's list (liquids converted to grams), ingredient additions as Cântar steps, cooking as device programs within their ranges; (3) estimates nutrition per portion from web research; (4) finds the recipe image on the source page and crops it to 1560×945 px, or, if none fits, gives a ready-to-paste ChatGPT image prompt for the dish that also names the file to save (`<slug>.jpg`); it never stretches a small image and never asks for a ready-made one.
- **Credits:** when the source was a website or video URL, the short description ends with a blank line and `Credits: <URL>`, always with a clean URL (tracking parameters such as `utm_*`, `si`, `feature`, `fbclid` removed); the 240-character limit counts that line too.
- **Output:** one Markdown block in chat for copy/paste, plus two files next to each other: the image `<slug>-mcs.jpg` and `<slug>-mcs.json`, the machine-readable version of the same recipe (ASCII step types, `notes`), validated against [recipe.schema.json](skills/convert/references/recipe.schema.json) before it is reported. The JSON is the contract for a future script-based `upload`.
- **References** (bundled in [skills/convert/references/](skills/convert/references/)): form schema, device capabilities (from the manual) and preparation tips.
- **Image script:** [skills/convert/scripts/prepare_image.py](skills/convert/scripts/prepare_image.py) (uses Pillow, installed temporarily through `uv` if missing).

See [skills/convert/SKILL.md](skills/convert/SKILL.md).

### `upload` — `/mcs:upload`

Uploads the recipe to the user's Monsieur Cuisine account by running [skills/upload/scripts/upload.py](skills/upload/scripts/upload.py) (Playwright, system Chrome) on the `<slug>-mcs.json` from `convert`.

- **Needs:** `uv` and Google Chrome. Dependencies (`playwright`, `jsonschema`) are installed by `uv` on the fly; the Chrome profile lives in `~/.cache/mcs/chrome-profile` and is **kept between runs**, so the login is needed only when the session expires (`--fresh-session` clears it first); Chrome's password manager is disabled.
- **Handed to the user:** login and the device choice, in the Chrome window (the script never types passwords). The terms of use are ticked automatically (the user's standing choice; `--manual-terms` to do it yourself).
- **Options:** no flag = fill only, nothing stored; `--save` = "Salvare proiect" (prints the `recipe-id`, then checks the image); `--finalize-private` = "Salvare ca privat" (never publishes; with `--recipe-id <id>` it finalizes an already saved project without refilling); `--reject-cookies` declines the cookie banner (default: accepted automatically); `--no-ai-declaration` leaves the "image created with AI" box unticked (it is ticked by default); `--inspect` lists the form controls when the site changes.
- **Skill role:** asks for the confirmations (terms, save, finalize), runs the script, reads the screenshot, reports. The old browser-pane flow is kept as [skills/upload/references/manual_flow.md](skills/upload/references/manual_flow.md), for when the script cannot run.

See [skills/upload/SKILL.md](skills/upload/SKILL.md).

See [skills/workflow/SKILL.md](skills/workflow/SKILL.md) for the pipeline details.

## Maintaining this README

Update this file whenever a skill is added or changes status: the Skills table, and the Workflow section if the order changes. Bump `version` in [.claude-plugin/plugin.json](.claude-plugin/plugin.json) in the same commit.
