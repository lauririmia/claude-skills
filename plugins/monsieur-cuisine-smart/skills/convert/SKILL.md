---
name: convert
description: Converts a clean recipe (the Markdown produced by /mcs:extract, pasted in chat or already in the conversation) into a recipe compatible with the Monsieur Cuisine Smart (SKMS 1200 C1) multi cooker, as a copy/paste-ready Markdown block holding every field of the monsieur-cuisine.com "Creare rețetă" form - details, nutrition, categories, times, ingredients, device steps with programs, and the recipe image. Resizes quantities that exceed the bowl, asks the user about anything ambiguous first, estimates nutrition from web research, and finds or requests a 1560x945 image. Second step of the mcs workflow. Use whenever the user says "/mcs:convert", wants to adapt, convert or "make compatible" a recipe for Monsieur Cuisine / MC smart, or has just run /mcs:extract, even if they only say "now convert it".
---

# mcs:convert

Turn a clean recipe into the exact content of the Monsieur Cuisine "Creare rețetă" form, written for the Smart device. The output is later used by `/mcs:upload` to fill the web form, so every value must already fit the form's limits. A value that the form would reject, or a device setting the machine cannot run, only shows up at upload time or in the kitchen, so catch it here.

## Reference files (read them, do not rely on memory)

All in `references/` next to this file.

- `schema_formular_monsieur_cuisine_v5.md` — the form: every field, limit, allowed value, program and its ranges. **Read it fully before mapping.** It is the contract for the output.
- `Monsieur_Cuisine_SKMS1200C1_capabilities_EN.md` — what the device can do (bowl capacity, programs, speeds, temperatures). Read the sections you need through its section map, always when a quantity looks large or a technique is unusual.
- `Sfaturi_pentru_preparare_RO.md` — guide values (kneading, pureeing, chopping, steaming, sous-vide, slow cook, fermenting, smoothie). Use them to pick times/speeds and to size quantities.
- `recipe.schema.json` — JSON Schema of the machine-readable output (`<slug>-mcs.json`), and `example-papanasi-prajiti-mcs.json`, a complete valid example. Read the example before writing the JSON in step 6.

## Flow

### 1. Get the recipe
Use the recipe pasted with the call, or the `/mcs:extract` output already in the conversation. If there is none, ask the user to paste it (or run `/mcs:extract` first). Keep the `Sursă:` line: the image step needs the source URL, and the short description ends with a credit to it when it is a web page or a video link (see "Credits" in step 3).

### 2. Find what needs clarifying, then ask, one question at a time
Read the whole recipe against the form and the device limits and list the items that need the user's judgment. Typical ones:

- **Over capacity:** total fill above 3.0 L (MAX mark), more than the program limits (e.g. kneading above 1000 g flour), weights outside Cântar's 5–5000 g. Propose a scaled-down version with the ratios kept, and say what the new yield is.
- **Unclear portion:** the source says "1 bucată"/"1 piece" for something obviously several servings (a loaf cake, a whole roast). The form's nutrition is per portion, so ask how to divide it.
- **Missing data that changes quantities** (no water amount, no servings at all) and **an ingredient used in the steps but absent from the ingredient list** (e.g. a pepper in the method that the list never mentions). Never drop such an ingredient silently or recommend leaving it out: the source's author used it. Offer to include it with a typical amount as the recommended answer (and the alternatives: another amount, or leave it out because it looks like a leftover from another version), then carry the answer into the list, the steps and the nutrition. Missing difficulty or times are estimated, not asked.
- **`(?)` marks or inconsistencies** left by `extract`, but only where the doubt changes the dish (a main ingredient with no quantity, or one used in the steps but missing from the list). A minor ingredient or a guessed title is decided and noted, not asked.
- **Steps the device cannot do** (oven baking, grilling, resting in the fridge): these stay as plain text steps. Ask only if the whole recipe depends on something the device cannot do, or if you could reasonably map a step two ways (e.g. sauté as Prăjire vs Gătire manuală).

Ask only when the answer really changes the recipe and the references cannot settle it. Things with a conventional default (difficulty, categories, a rough prep/total time, whether a vanilla extract is "to taste") are not worth interrupting for: decide them, and list them in the closing note so the user can object. A simple recipe should need zero or one question, not five.

For each item use `AskUserQuestion` with 2–4 concrete answer options, the recommended one first and marked "(Recomandat)", and a short description of what each choice changes. Ask one item at a time and wait for the answer before the next; later questions often depend on earlier answers. Do not ask about things you can decide from the references. If nothing needs clarifying, say so in one line and continue. Ask in Romanian.

### 3. Map the recipe to the form
Follow the schema exactly. The points that most often go wrong:

- **Limits:** name ≤ 86 chars, short description ≤ 240, step title ≤ 80, step instructions ≤ 240. Cut by rewording, never by chopping a sentence in the middle. Write the name and the texts in Romanian.
- **Credits (short description):** when the recipe came from a URL (a website or a video such as YouTube, i.e. the `Sursă:` line of `/mcs:extract` holds a URL, or the user gave one in the first step), the short description ends with a blank line and then `Credits: <URL>`. When the source is pasted text, an image or the conversation, with no URL, there is no credits line. **The URL must be clean: always remove tracking parameters**, whatever the length: `utm_*`, `si`, `feature`, `fbclid`, `gclid`, `igshid`, `ref`, `ref_src`, `mc_cid`, `mc_eid`, and similar share/campaign tags, plus a `#fragment` that only marks a position or time. Keep every parameter that identifies the content (`v=` on YouTube, `p=` or `id=` on pages that use them), the scheme and the host. Examples: `https://www.youtube.com/watch?v=Pd85QmPTPRI&si=abc123` → `https://www.youtube.com/watch?v=Pd85QmPTPRI`; `https://youtu.be/Pd85QmPTPRI?si=abc123` → `https://youtu.be/Pd85QmPTPRI`; `https://site.ro/reteta/?utm_source=fb` → `https://site.ro/reteta/`. Never cut or abbreviate the URL itself. If you removed anything, say so in the closing note. The 240-character limit counts the whole field, including the credits line and the blank line (2 newline characters): description text budget = 240 − 2 − 9 (`Credits: `) − clean URL length. Write the descriptive sentence to fit that budget (reword, do not chop). If the budget is still below about 40 characters, keep one very short sentence rather than shortening the URL.
- **Difficulty:** one of `ușor`, `mediu`, `dificil`. **Categories:** one or more of the 20 listed values, spelled exactly.
- **Portion size:** how many portions the recipe yields, as a number plus the *plural* unit from the allowed 14 (`4 porții`, `10 felii`, `6 bucăți`; singular only for 1). Nutrition is then per single portion (one `porție`, one `felie`). Keep both consistent: if the dish makes 4 servings, write `4 porții` and divide the nutrition totals by 4. Never write `1 porție` for a dish that feeds several people.
- **Times:** `Pregătire` = hands-on preparation, `Gata în` = total time; `Gata în` ≥ `Pregătire`, and neither may be 0. A single time in the source is usually the total, and sources are often optimistic: add up the steps (device programs, baking, resting, cooling) and when the sum is larger than the source's time, use the sum and say so in the closing note.
- **Ingredients:** the ingredient list keeps counted items as `bucată` (there is no plural unit) with the number in the quantity field, and a spoon quantity as `lingură` for 1 and `linguri` for anything else (1,5 → `linguri`), `linguriță`/`lingurițe` likewise. Units are limited to `g`, `linguriță/lingurițe`, `lingură/linguri`, `priză/prize`, `vârf de cuțit`, `bucată`, `strat/straturi`, or none. There is no ml, l, cup or oz: convert volumes (ml, l, cups) and imperial weights to grams, because that is a unit change and not an approximation (water and milk ≈ 1 g per ml; oil ≈ 0.92 g per ml; honey ≈ 1.4; use the ingredient's real density when it differs), and use `bucată` for things counted (eggs, cloves). Quantities are kept exactly as the source writes them, never approximated: a range stays a range (`1–2` with unit `linguri`), a bunch stays a bunch (quantity `1 legătură`, no unit, ingredient `mărar`), a sprig stays a sprig (`2 crenguțe`), and an ingredient with no quantity gets `după gust` with no unit. The form has no unit for bunch or sprig, but its quantity field accepts any text, so the word goes into the quantity. Weigh in grams only what a Cântar step needs, and then say in the closing note which weights are your estimates. Otherwise use a plain number or a clear fraction (`200`, `0,5`, `1/2`). Group ingredients (`Ingrediente generale`, plus groups like `Pentru sos`) when the recipe does. Write names with diacritics, in the singular/neutral form a catalogue would use (`făină`, not `făina`).
- **Steps** (the form's last step; ingredients are not linked to steps, so the step text must name what to add):
  - An ingredient measured by weight or volume that goes into the bowl and weighs 5 g or more gets its own **Cântar** step (title like `Adăugare făină`, `Greutate: 200 g`; spoon measures are converted to grams for this, e.g. 1 lingură maioneză = 15 g). Counted ingredients (eggs, whole vegetables, cloves) are not weighed: they go in the text of the step that adds them (`Sparge 5 ouă în vas.`). The same goes for pinches, extracts, fresh herbs and seasonings under 5 g (`Adaugă sarea și piperul în vas.`), and dry spices measured in lingurițe (a level teaspoon of paprika weighs about 2,5 g, so a 5 g Cântar step would double the dose; the user measures them with the spoon, as written in the ingredient list), and for anything prepared outside the bowl (a mixture whisked in a separate dish, fruit tossed in flour); those are text steps.
  - Cooking is a **program step**: Gătire manuală (temperature, time, speed, rotation), Prăjire, Gătire la aburi, Sous-vide, Slow Cook, Fierberea orezului, Food Processor, Pasare, Smoothie, Aluat ferm/moale/lichid, Turbo and the others in the schema. Pick the program the technique really calls for, and take times and speeds from the guide values when the source gives none. Typical settings seen in converted recipes for this device, to use when the source and the references give none: sautéing aromatics with oil 110 °C for 5 min (Prăjire; up to 130 °C when the recipe wants colour); simmering soups 100 °C, speed 1, antiorar, 15–25 min; whisking eggs with sugar 4 min at speed 4, temperature 0, with the stirring attachment; folding in yogurt or oil 30 s at speed 3; folding in flour and baking powder 30 s at speed 3; mixing a marinade or sauce 20–30 s at speed 3; finishing a liaison (sour cream, egg yolk) 2 min at 90 °C, speed 1, antiorar. List every such value you used in the closing note. Write rotation exactly as the form's buttons say: `în sens orar` or `în sens antiorar`.
  - **The device does the work it can do, so chop and sauté in it by default.** The user wants a recipe the Monsieur Cuisine really cooks, not a recipe that only uses it as a pot. The pattern for aromatics (onion, carrot, parsley root, garlic, herbs) is: text step to put them in the bowl peeled and cut in large pieces; **Gătire manuală at temperature 0, speed 5–6, clockwise, a few seconds** to chop them (guide values from the tips file: onion 6 s at speed 6, carrot 8 s at speed 6, herbs 8 s at speed 6, garlic 5 s at speed 8); a text step to scrape the sides down with the spatula; **Cântar** for the oil; **Prăjire** (110–130 °C, about 5 min, up to 500 g) to sauté them in the same bowl. Whipping is Gătire manuală at temperature 0 with the stirring attachment, pureeing is Pasare, and boiling or simmering is Gătire manuală at 100 °C. Only vegetables or meat that must keep a specific shape (cubes, rounds, slices) or that the device cannot handle are prepared by hand in a text step, and they are added to the bowl afterwards. If a recipe chops something by hand that the device could chop, convert it to the device version.
  - Everything the device does not do (peeling, cutting, oven, resting, serving) is a **text step** (title + instructions).
  - **Hard rules for Gătire manuală:** temperature only at the allowed positions (`0`, `37`, `40`, then every 5 up to `130` °C); speed 4–10 only at temperature 0 with clockwise rotation, otherwise 0–3; total time within the program's range. Durations must be inside each program's interval in the schema.
  - Keep the recipe's order, and keep steps short and imperative.
- **Prăjire** takes at most 500 g of food (plus the fat), at up to 130 °C for up to 14 min, with a fixed speed 1; more than that must be split or cooked with Gătire manuală.
- **Capacity:** check the largest fill against the bowl's 3.0 L MAX and the program limits after every addition, not only at the end.

### 4. Estimate nutrition
The form wants kcal, protein, carbohydrates and fat **per portion**, as whole numbers. Look the values up on the web for each ingredient. Prefer USDA FoodData Central's own food pages (found through web search). Its API with the demo key allows only about 10 requests per hour, so do not build the calculation on it; use it for a check or two and otherwise rely on pages that mirror its data. Mirrors often disagree (white wine 72 vs 122 kcal/100 g; mayonnaise 390 vs 680), so for the ingredients that contribute most to the total, check two sources and keep the one that matches the product the recipe really uses. An ingredient the source lists with no quantity but that adds real calories (oil, butter, sugar, cream) must still be counted at a typical amount for the dish (e.g. 2 linguri of oil for a marinade), stated in the closing note; leaving it out understates the calories. Take an ingredient's density or edible part into account (with-bone meat, pitted fruit), scale by the quantities in the converted recipe, add them up and divide by the number of portions. Do not guess from memory, and do not copy the "kcal" shown on the source page unless it is clearly per portion and matches your sum within reason. If the numbers differ a lot, trust your computation and mention the difference. Present them as estimates.

### 5. Image
The form needs a JPEG/PNG of at least 1560 × 945 px with a centred subject.

1. If the source is a web page, run `python3 <this skill's directory>/scripts/prepare_image.py "<source URL>" "<slug>-mcs.jpg"` from the user's working directory (`<slug>` = the recipe name in lowercase ASCII with hyphens). It looks for the page's recipe image (including the full-size original behind resized URLs), centre-crops it to the right ratio and saves it. It needs Pillow and installs it temporarily through `uv` when missing.
2. `status: ok` → open the saved image and look at it: it must show the finished dish (not a step photo, a logo or a collage) with the subject reasonably centred after the crop. If it fails that check, treat it like `too_small`. Otherwise tell the user its path. Mention `crop_loss_pct` if it is above about 25 %, since the subject may have been cut.
3. `status: too_small` or `not_found`, or the recipe came from pasted text or a video, or the image failed the check above: **do not stretch a small image and do not invent one, and do not ask the user for a ready-made image.** Say in one line why the source image cannot be used (and its size, if there was one), then go straight to the ChatGPT prompt (step 4). If the user says they would rather add the image later, put `LIPSĂ` in the output.
4. **ChatGPT prompt block.** This is part of the conversation with the user, before the final output: show the prompt, wait for the image, and only then return the output block (with `LIPSĂ` if the user postponed it). The closing note still comes after the output block.  Give it as a single Markdown code block so it copies cleanly, written in English because image generators follow English best, and built from this recipe, not from a template: the dish name, the visible main ingredients and colours, how it is served (bowl, plate, tray, sliced loaf) and a garnish that really belongs to it. Always include these constraints, with the reason in mind: the format and size written into the prompt itself, as its first sentence, so the user only pastes and runs it and never has to choose settings (for example: `Generate a landscape image, 1536 x 1024 pixels (3:2), not square.`), because the form needs at least 1560 x 945 px and crops to about 1.65:1, trimming some top and bottom; the dish centred with generous margin around it, so the crop cannot cut it; photorealistic food photography, natural soft daylight, shallow depth of field, clean neutral background; no text, logos, watermarks, hands or people, because the image will be published under the user's name. The prompt must also say, as its last sentence, under what name and extension the generated image is to be saved: `Save the image as <slug>.jpg.` (with the real slug, e.g. `gulas-de-vita.jpg`), and the message around the block repeats it in Romanian, so the file lands in the user's working directory with a name you already know. Never leave any step to the user besides pasting the prompt and saving the result under that name: the prompt must be self-contained. After the block, tell the user to save the generated image as `<slug>.jpg` in the working directory and to tell you when it is there (no path needed); then run `prepare_image.py` on `<slug>.jpg` (it accepts a local path and writes `<slug>-mcs.jpg`), look at the result as in step 2, and report the final path. An image straight from ChatGPT is typically 1536 × 1024, which the script enlarges by about 1.6 % to reach 1560 × 945, which is invisible.

### 6. Output
Produce two things from the same data: the Markdown block below, in chat, for the user to read and copy, and the JSON file `<slug>-mcs.json` (step 6b), which the upload step reads. They must say the same thing; the Markdown is never parsed by a script.

#### Markdown block
Return the result in chat as a single Markdown block. Use this structure so it can be copied as-is:

```markdown
# <Nume rețetă>

## Detalii despre rețetă
- **Numele rețetei:** …
- **Scurtă descriere:** …

  Credits: <URL folosit pentru rețetă>   — only when the source was a URL; as a second paragraph of this bullet (blank line before it), it becomes the last line of the field
- **Dificultate:** ușor | mediu | dificil
- **Dimensiunea porției:** <număr> <unitate>
- **Valoare calorică:** <n> kcal
- **Proteine:** <n> g
- **Carbohidrați:** <n> g
- **Grăsime:** <n> g
- **Categorie:** <valoare>, <valoare>
- **Imagine:** <cale fișier> (<lățime>×<înălțime>)   — or `LIPSĂ`

## Timp
- **Pregătire:** <h> oră <m> min
- **Gata în:** <h> oră <m> min

## Ingrediente

**Ingrediente generale**

| Ingredient | Cantitate | Unitate |
|---|---|---|
| făină | 200 | g |

## Etape

**Etapa 1 — <Titlu>**
- **Tip:** Text
- **Instrucțiuni:** …

**Etapa 2 — Adăugare făină**
- **Tip:** Cântar
- **Greutate:** 200 g
- **Instrucțiuni:** …

**Etapa 3 — <Titlu>**
- **Tip:** Gătire manuală
- **Temperatură:** 100 °C
- **Timp:** 15 min 0 sec
- **Viteză:** 1
- **Rotație:** în sens antiorar
```

Other programs list the fields their schema entry names (e.g. Prăjire: temperatură, timp; Sous-vide: temperatură, durată; Turbo: activare în sec + instrucțiuni).

#### 6b. JSON file
Write `<slug>-mcs.json` next to the image (same folder as `<slug>-mcs.jpg`, the user's working directory) with the Write tool, following `references/recipe.schema.json`. Rules that differ from the Markdown:

- `details.short_description` is the sentence **without** the `Credits:` line; the clean URL goes in `details.credits_url` (`null` when the source is not a URL). The upload script composes `text + "\n\nCredits: " + url`.
- Step `type` is an ASCII identifier: `text`, `scale`, `manual`, `dough_firm`, `dough_soft`, `dough_liquid`, `steam`, `fry`, `sous_vide`, `slow_cook`, `egg_boil`, `prewash`, `ferment`, `turbo`, `rice`, `food_processor`, `puree`, `smoothie`. Durations are always `duration_sec` (Turbo: `seconds`), temperatures `temperature_c`, rotation `cw` / `ccw` (not the Romanian button text).
- `time` is in minutes; `image` is `null` when the image is `LIPSĂ`; `image.ai_generated` is `true` when the image came from a generator.
- `notes` holds the assumptions and estimates from the closing note (one short string each); they are not sent to the form.
- Ingredient `quantity` is always a string; `unit` is `null` when empty.

Then validate it, and fix the file (not the schema) until it passes:

```bash
uv run --quiet --with jsonschema python3 - <<'PY'
import json, os
from jsonschema import Draft202012Validator as V
d = "<this skill's directory>/references"
f = "<slug>-mcs.json"
r = json.load(open(f)); errs = [e.message for e in V(json.load(open(d + "/recipe.schema.json"))).iter_errors(r)]
desc = r["details"].get("short_description", ""); u = r["details"].get("credits_url")
if u: desc += "\n\nCredits: " + u
if len(desc) > 240: errs.append(f"descriere compusă {len(desc)} > 240")
if r["time"]["total_minutes"] < r["time"]["prep_minutes"]: errs.append("Gata în < Pregătire")
im = r["details"]["image"]
if im and not os.path.exists(im["path"]): errs.append("imaginea nu există pe disc")
print(errs or "OK")
PY
```

Report the file path in the closing note.

#### Closing note
After the block, add a short note in Romanian, outside it: that the nutrition values are estimates (and how the portion was defined), anything scaled or assumed, the path of the JSON file, and that the next step is `/mcs:upload`, or that the block can be copied into the form by hand. Before returning, check every limit once against the schema, since the form will not forgive a title over 80 characters. For the short description, count the credits line too (total ≤ 240); if you removed tracking parameters from the URL, mention it in the note (the credits URL is always the clean one).
