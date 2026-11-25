#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["playwright", "jsonschema"]
# ///
"""mcs upload: fills the monsieur-cuisine.com "Creare reteta" form (MC smart) from <slug>-mcs.json.

Run:  uv run upload.py RECIPE.json [--manual-terms] [--save [--finalize-private]] [--recipe-id N --finalize-private] [--no-ai-declaration] [--reject-cookies] [--email ADDRESS] [--fresh-session] [--inspect]

Without --save the form is only filled (nothing is stored). --save clicks "Salvare proiect" and prints the
recipe-id; --finalize-private then does "Completare rețetă -> Salvare ca privat" (never publishes).
The terms of use are ticked automatically too (--manual-terms to do it yourself).
Cookie banners are accepted automatically (the user's choice; --reject-cookies declines).
The "image created with AI" box is ticked by default (the user's standing choice for private recipes).
The login is always done by the user in the opened Chrome window. The saved session
(~/.cache/mcs/chrome-profile) is kept between runs, so the login is needed only when it expires
(--fresh-session clears it first);
Chrome's password manager is switched off, so it never offers to save the password. Passwords are never typed by this script.
"""
import argparse, json, os, re, shutil, sys, time
from pathlib import Path

FORM_URL = "https://www.monsieur-cuisine.com/ro/creare-reteta?devices=mc-smart"
PROFILE = Path.home() / ".cache" / "mcs" / "chrome-profile"
SCHEMA = Path(__file__).resolve().parents[2] / "convert" / "references" / "recipe.schema.json"


def log(*a):
    print(*a, flush=True)


def validate(recipe):
    from jsonschema import Draft202012Validator as V
    errs = [e.message for e in V(json.load(open(SCHEMA))).iter_errors(recipe)]
    d = recipe["details"]
    desc = d.get("short_description", "")
    if d.get("credits_url"):
        desc += "\n\nCredits: " + d["credits_url"]
    if len(desc) > 240:
        errs.append(f"descriere compusa {len(desc)} > 240")
    if recipe["time"]["total_minutes"] < recipe["time"]["prep_minutes"]:
        errs.append("Gata in < Pregatire")
    if d["image"] is None:
        errs.append("imaginea lipseste (image: null)")
    elif not os.path.exists(d["image"]["path"]):
        errs.append("fisierul imagine nu exista: " + d["image"]["path"])
    return errs, desc


def inspect(page, label):
    """Print the form controls currently visible, to maintain selectors."""
    js = """() => [...document.querySelectorAll('input,textarea,select,button,[role=radio],[role=combobox],[role=switch],[role=checkbox]')]
      .filter(e => e.offsetParent !== null)
      .map(e => ({tag: e.tagName.toLowerCase(), type: e.type || '', role: e.getAttribute('role') || '', id: e.id || '',
                  ph: e.getAttribute('placeholder') || '', aria: e.getAttribute('aria-label') || '',
                  text: (e.innerText || e.value || '').trim().slice(0, 40)}))"""
    log(f"--- {label} ---")
    for e in page.evaluate(js):
        log(json.dumps(e, ensure_ascii=False))


COOKIE_ACCEPT = re.compile(r"^\s*(accept(ă)? toate|accept all|allow all|accept)( cookie-?uri(le)?)?\s*$", re.I)
COOKIE_REJECT = re.compile(r"^\s*(respinge(ți)?( toate)?|reject all|refuz[aă]( toate)?)\s*$", re.I)


def handle_cookies(page, reject=False):
    """Click the cookie banner away if it is showing (default: accept all, the user's choice)."""
    try:
        sel = "#onetrust-reject-all-handler" if reject else "#onetrust-accept-btn-handler"
        btn = page.locator(sel)
        if not (btn.count() and btn.first.is_visible()):
            btn = page.locator("button", has_text=COOKIE_REJECT if reject else COOKIE_ACCEPT)
        if btn.count() and btn.first.is_visible():
            btn.first.click(timeout=3000)
            page.wait_for_timeout(500)
            log("Banner cookie-uri:", "respins" if reject else "acceptat")
    except Exception:
        pass


BUSY = re.compile(r"capacitate\s+maxim|reîncercați|reincercati|try again later|at capacity", re.I)


def busy_retry(page, told, typed, state):
    """The site sometimes answers 'Lucrăm la capacitate maximă... reîncercați'. Back off and retry."""
    state["n"] = state.get("n", 0) + 1
    if state["n"] > 8:
        sys.exit("Site-ul raportează în continuare „capacitate maximă” după 8 încercări. Reia mai târziu.")
    wait = 15 * state["n"]
    log(f"Site-ul e la capacitate maximă; reîncerc peste {wait} s (încercarea {state['n']}/8).")
    page.wait_for_timeout(wait * 1000)
    nxt = page.locator("button, input[type=submit]", has_text=re.compile(r"^\s*continu(ă|a|e)\s*$", re.I))
    pw = page.locator("input[type=password]").filter(visible=True)
    if pw.count() and pw.first.evaluate("e => e.value.length") > 0 and nxt.count():
        nxt.first.click(timeout=3000)   # the password is still in the field: just press Continuă again
        log("Apăsat din nou „Continuă”.")
    else:
        page.goto(FORM_URL)             # start over; e-mail is refilled, the password is typed by the user
        for k in ("email", "login", "pw_click"):
            told.discard(k)
        typed.clear()


def wait_for_form(page, accept_terms, reject_cookies=False, email=None):
    """Get to the 'Creare reteta' form; login/device choice are the user's."""
    told = set()
    typed = {}
    busy = {}
    deadline = time.time() + 15 * 60
    page.goto(FORM_URL)
    while time.time() < deadline:
        page.wait_for_timeout(1000)
        handle_cookies(page, reject_cookies)
        if BUSY.search(page.locator("body").inner_text()[:4000]) and not page.get_by_placeholder("Dați rețetei un nume.").count():
            busy_retry(page, told, typed, busy)
            continue
        if page.get_by_text("Aparat").first.is_visible() and page.get_by_placeholder("Dați rețetei un nume.").is_visible():
            return
        if page.get_by_text(re.compile("selectați aparatul", re.I)).first.is_visible():
            # device choice page (its URL is autentificare-necesara, so test it before the login branch)
            if "device" not in told:
                told.add("device"); log("Aleg aparatul MC SMART.")
            try:
                page.locator(".device-selector-item", has_text=re.compile(r"mc smart", re.I)).first.click(timeout=6000)
                page.wait_for_timeout(500)
                ok = page.locator("button", has_text=re.compile(r"^\s*ok\s*$", re.I))
                if ok.count() and ok.first.is_enabled():
                    ok.first.click(timeout=3000)
                    log("Aparat confirmat (OK).")
                    page.wait_for_timeout(1500)
            except Exception as e:  # usually a first attempt while the dialog animates; the loop retries
                busy["dev_err"] = busy.get("dev_err", 0) + 1
                if busy["dev_err"] >= 3:
                    log("device:", str(e)[:200])
        elif page.get_by_text(re.compile("prelucrarea datelor|prelucrare a datelor|prelucrării datelor", re.I)).first.is_visible() \
                and page.locator("button, input[type=submit]", has_text=re.compile(r"^\s*accept(ă|a)\s*$", re.I)).count():
            # data-processing consent page shown after login: the user asked for it to be accepted automatically
            try:
                page.locator("button, input[type=submit]", has_text=re.compile(r"^\s*accept(ă|a)\s*$", re.I)).first.click(timeout=3000)
                log("Prelucrarea datelor: acceptată (implicit, alegerea utilizatorului).")
                page.wait_for_timeout(1500)
            except Exception as e:
                log("consimțământ:", str(e)[:120])
        elif page.get_by_text("Accept condițiile de utilizare").first.is_visible():
            if accept_terms:
                box = page.locator("input[type=checkbox]").filter(visible=True).first
                page.get_by_text("Accept condițiile de utilizare").first.click()
                page.wait_for_timeout(500)
                if box.count() and not box.is_checked():
                    box.check(force=True)
                page.locator("button", has_text=re.compile(r"începeți acum", re.I)).click(timeout=5000)
                log("Condițiile de utilizare: bifate (implicit, alegerea utilizatorului).")
            elif "terms" not in told:
                told.add("terms"); log(">> Bifeaza tu 'Accept conditiile de utilizare' si apasa 'Incepeti acum' in fereastra Chrome.")
        elif "accounts.lidl.com" in page.url or "autentificare" in page.url:
            if email and "email" not in told:
                # only the e-mail (a username) is filled; the password is always typed by the user
                field = page.locator("input[type=email], input[name*=mail i], input[id*=mail i]").filter(visible=True)
                if field.count():
                    field.first.fill(email)
                    told.add("email"); log("E-mail completat în câmpul de login.")
                    nxt = page.locator("button, input[type=submit]", has_text=re.compile(r"^\s*continu(ă|a|e)\s*$", re.I))
                    if nxt.count():
                        nxt.first.click(timeout=3000)
                        log("Apăsat „Continuă”; parola o introduci tu.")
            pw = page.locator("input[type=password]").filter(visible=True)
            if pw.count() and "pw_click" not in told:
                # The user types the password. Press "Continuă" only once the field has been left unchanged
                # for ~3 s, i.e. after the whole password was typed (not after its first character).
                n = pw.first.evaluate("e => e.value.length")
                if n != typed.get("n"):
                    typed["n"], typed["t"] = n, time.time()
                elif n > 0 and time.time() - typed["t"] >= 3:
                    nxt = page.locator("button, input[type=submit]", has_text=re.compile(r"^\s*continu(ă|a|e)\s*$", re.I))
                    if nxt.count():
                        told.add("pw_click"); nxt.first.click(timeout=3000)
                        log("Parola introdusă de tine; apăsat „Continuă”.")
            if "login" not in told:
                told.add("login"); log(">> Autentifica-te tu in fereastra Chrome (scriptul nu introduce parole). Astept...")
    sys.exit("Timeout: formularul nu s-a deschis in 15 minute.")


def click_center(loc):
    """Vuetify selects sit under the fixed header: scroll to the middle first."""
    loc.evaluate("e => e.scrollIntoView({block: 'center'})")
    loc.click()


def click_option(page, text):
    """Custom dropdowns render their options ~1 s late; click the visible option with exactly this text."""
    page.wait_for_timeout(1000)
    opts = page.locator(".menuable__content__active [role=option]").filter(has_text=re.compile(r"^\s*" + re.escape(text) + r"\s*$"))
    if opts.count():
        opts.first.click()
    else:
        page.get_by_text(text, exact=True).last.click()


def open_program_menu(page, clear=False):
    """The program select is locked once a program is chosen: the trash button clears it first."""
    if clear:
        page.locator(".v-dialog button:has(.mdi-delete)").first.click()
        page.wait_for_timeout(800)
        page.locator("button", has_text=re.compile("eliminarea programului automat", re.I)).click()
        page.wait_for_timeout(800)
    page.locator(".v-dialog .v-select").first.click(timeout=5000)
    page.wait_for_timeout(800)


def fill_details(page, r, desc, ai_declared):
    d = r["details"]
    page.get_by_placeholder("Dați rețetei un nume.").fill(d["name"])
    page.locator("textarea").first.fill(desc)
    # difficulty: three checkbox-like radios, clicked through their visible label
    page.get_by_text(d["difficulty"], exact=True).first.click()
    nums = page.locator("input[type=number]")
    nums.nth(0).fill(str(d["portion"]["amount"]))
    click_center(page.locator(".v-select").first)  # unit dropdown
    click_option(page, d["portion"]["unit"])
    n = d.get("nutrition_per_portion", {})
    for i, k in enumerate(["kcal", "protein_g", "carbs_g", "fat_g"], start=1):
        if k in n:
            nums.nth(i).fill(str(n[k]))
    cat = page.locator(".v-select--is-multi").first
    for c in d["categories"]:
        click_center(cat)
        click_option(page, c)
    page.keyboard.press("Escape")
    # image: the hidden file input accepts the path directly
    page.locator("input[type=file]").first.set_input_files(d["image"]["path"])
    page.wait_for_timeout(2000)
    # The user's standing choice: the recipe is private, so the AI-image box is ticked by default.
    if ai_declared:
        page.get_by_text(re.compile("creată folosind inteligența artificială")).first.click()
        if not page.locator(".photo-editor-actions__checkbox input").is_checked():
            sys.exit("Nu am putut bifa declaratia AI.")
    page.locator("button", has_text=re.compile(r"^\s*salvare\s*$", re.I)).last.click()
    page.wait_for_timeout(2500)


def next_step(page):
    page.locator("button", has_text=re.compile(r"^\s*mai departe\s*$", re.I)).first.click()
    page.wait_for_timeout(1500)


def fill_time(page, r):
    t = r["time"]
    nums = page.locator("input[type=number]")
    for i, m in enumerate([t["prep_minutes"], t["total_minutes"]]):
        nums.nth(2 * i).fill(str(m // 60))
        nums.nth(2 * i + 1).fill(str(m % 60))


def fill_group_rows(page, items, first_row):
    """Rows are contiguous per group, so the global row index is first_row + i."""
    plus = page.locator("button.v-btn--icon:has(.mdi-plus)")
    names = page.get_by_placeholder("Ingredient")
    have = names.count() - first_row
    for _ in range(len(items) - have):
        plus.nth(plus.count() - 1).click() if False else page.locator("button.v-btn--icon:has(.mdi-plus)").last.click()
        page.wait_for_timeout(300)
    for i, it in enumerate(items):
        k = first_row + i
        names.nth(k).click()
        names.nth(k).fill(it["name"])
        qty = page.get_by_placeholder("0").nth(k)
        qty.fill(it["quantity"])
        if it["unit"]:
            units = page.locator(".v-select:has(input[type=text]:not([placeholder]))")
            click_center(units.nth(k))
            click_option(page, it["unit"])
        page.keyboard.press("Escape")
        page.mouse.click(1262, 450)  # click the blank margin: closes the suggestion list that can cover the next row
        page.wait_for_timeout(200)
    for i, it in enumerate(items):
        k = first_row + i
        got = (names.nth(k).input_value(), page.get_by_placeholder("0").nth(k).input_value())
        if got != (it["name"], it["quantity"]):
            log(f"!! rand {k}: asteptat {(it['name'], it['quantity'])}, gasit {got}")


def fill_ingredients(page, r):
    first_row = 0
    for g, grp in enumerate(r["ingredient_groups"]):
        if g > 0:
            page.get_by_text("Crearea unui grup nou").click()
            page.wait_for_timeout(1000)
            page.locator("button.v-btn--icon:has(.mdi-grease-pencil)").last.click()
            page.keyboard.type(grp["name"])
            page.keyboard.press("Enter")
            page.wait_for_timeout(500)
        carrots = page.locator("button.v-btn--icon:has(img)")
        click_center(carrots.nth(g))
        page.wait_for_timeout(500)
        fill_group_rows(page, grp["items"], first_row)
        first_row += len(grp["items"])


PROGRAMS = {
    "dough_firm": "Aluat ferm", "dough_soft": "Aluat moale", "dough_liquid": "Aluat lichid",
    "steam": "Gătire la aburi", "fry": "Prăjire", "scale": "Cântar", "manual": "Gătire manuală",
    "sous_vide": "Sous-vide", "slow_cook": "Slow Cook", "egg_boil": "Fierberea ouălor",
    "prewash": "Prespălare", "ferment": "Fermentare", "turbo": "Turbo", "rice": "Fierberea orezului",
    "food_processor": "Food Processor", "puree": "Pasare", "smoothie": "Smoothie",
}
TEMPS_MANUAL = [0, 37, 40] + list(range(45, 131, 5))
TEMPS_SLOW = [37, 40] + list(range(45, 96, 5))
TEMPS_FERMENT = [37, 40] + list(range(45, 66, 5))
EGG_SIZE = {"small": "mic", "medium": "mediu", "large": "mare"}
DONENESS = {"soft": "moale", "semi_soft": "semi-moale", "hard": "tare"}


def set_slider(page, index, position):
    """Sliders cannot be typed into: focus the handle, go to the start, press Right `position` times."""
    h = page.locator(".v-dialog [role=slider]").nth(index)
    h.focus()
    page.keyboard.press("Home")
    for _ in range(position):
        page.keyboard.press("ArrowRight")
    got = h.get_attribute("aria-valuenow")
    if got is not None and int(float(got)) != position:
        log(f"!! cursor {index}: cerut pozitia {position}, are {got}")


def type_number(loc, value):
    loc.click(click_count=3)
    loc.press_sequentially(str(value))


def dialog_button(page, pattern):
    return page.locator(".v-dialog button", has_text=re.compile(pattern, re.I))


def fill_steps(page, r):
    for n, st in enumerate(r["steps"], start=1):
        page.get_by_text("Adăugare etapă").first.click()
        page.wait_for_timeout(1500)
        page.get_by_placeholder("de exemplu, pregătirea cepei").fill(st["title"])
        t = st["type"]
        if t != "text":
            page.locator(".v-dialog input[role=switch]").evaluate("e => e.click()")
            page.wait_for_timeout(1200)
            open_program_menu(page)
            click_option(page, PROGRAMS[t])
            page.wait_for_timeout(1200)
            fill_program(page, st)
        if "instructions" in st:
            page.locator(".v-dialog textarea").fill(st["instructions"])
        dialog_button(page, r"^\s*adăugare\s*$").click()
        page.wait_for_timeout(1500)
        log(f"etapa {n}/{len(r['steps'])}: {st['title']}")


def fill_program(page, st):
    t, nums = st["type"], page.locator(".v-dialog input[type=number]")
    d = st.get("duration_sec", 0)
    if t == "scale":
        type_number(nums.first, st["grams"])
    elif t == "manual":
        dialog_button(page, "sens antiorar" if st["rotation"] == "ccw" else "sens orar").click()
        set_slider(page, 0, TEMPS_MANUAL.index(st["temperature_c"]))
        type_number(nums.nth(0), d // 60); type_number(nums.nth(1), d % 60)
        set_slider(page, 1, st["speed"])
    elif t == "fry":
        set_slider(page, 0, TEMPS_MANUAL.index(st["temperature_c"]))
        type_number(nums.nth(0), d // 60); type_number(nums.nth(1), d % 60)
    elif t == "sous_vide":
        type_number(nums.nth(0), st["temperature_c"])
        type_number(nums.nth(1), d // 3600); type_number(nums.nth(2), (d // 60) % 60)
    elif t in ("slow_cook", "ferment"):
        temps = TEMPS_SLOW if t == "slow_cook" else TEMPS_FERMENT
        set_slider(page, 0, temps.index(st["temperature_c"]))
        type_number(nums.nth(0), d // 3600); type_number(nums.nth(1), (d // 60) % 60)
    elif t == "egg_boil":
        dialog_button(page, "^\\s*" + EGG_SIZE[st["egg_size"]] + "\\s*$").click()
        dialog_button(page, "^\\s*" + DONENESS[st["doneness"]] + "\\s*$").click()
    elif t == "prewash":
        dialog_button(page, "^\\s*" + ("scurt" if st["length"] == "short" else "lung") ).click()
    elif t == "turbo":
        page.locator(".v-dialog .v-select").nth(1).click()
        click_option(page, str(st["seconds"]))
    else:  # dough_*, steam, rice, food_processor, puree, smoothie: Min. + sec.
        type_number(nums.nth(0), d // 60); type_number(nums.nth(1), d % 60)


def save_project(page):
    page.locator("button", has_text=re.compile(r"^\s*salvare proiect\s*$", re.I)).first.click()
    try:
        page.wait_for_url(re.compile(r"recipe-id=\d+"), timeout=20000)  # the toast is too short-lived to wait for
    except Exception:
        sys.exit("Am apăsat „Salvare proiect”, dar URL-ul nu a primit recipe-id. Verifică „Rețetele mele” înainte de a rula din nou (poate exista un proiect).")
    return re.search(r"recipe-id=(\d+)", page.url).group(1)


def preview(page, rid):
    page.goto(f"https://www.monsieur-cuisine.com/ro/previzualizare-reteta?recipe-id={rid}")
    page.wait_for_timeout(4500)


def check_image(page, rid):
    """Read-only: the recipe image is an <img> on the tecpal CDN; report whether it loaded."""
    preview(page, rid)
    imgs = page.evaluate("() => [...document.querySelectorAll('img')].filter(i => /tecpal/.test(i.currentSrc || i.src)).map(i => i.complete && i.naturalWidth > 0)")
    if not imgs:
        log("!! Imaginea NU e salvată (nu există <img> tecpal): repetă încărcarea imaginii.")
    elif all(imgs):
        log("Imagine: încărcată și se vede.")
    else:
        log("!! Imagine: înregistrată, dar nu se încarcă aici (probabil certificatul CDN): verific-o pe alt dispozitiv.")


def finalize_private(page, rid):
    # The author's buttons (Editor / Salvare proiect / Completare rețetă) show only when the preview is
    # opened from the editor, not when its URL is loaded directly.
    page.goto(f"https://www.monsieur-cuisine.com/ro/creare-reteta?devices=mc-smart&recipe-id={rid}")
    page.get_by_placeholder("Dați rețetei un nume.").wait_for(timeout=30000)
    page.wait_for_timeout(1500)
    page.locator("button", has_text=re.compile(r"^\s*previzualizare\s*$", re.I)).first.click()
    page.wait_for_timeout(4500)
    page.locator("button", has_text=re.compile(r"completare rețetă", re.I)).first.click()
    page.wait_for_timeout(1500)
    page.get_by_text("Salvare ca privat").first.click()
    page.wait_for_timeout(800)
    page.locator("button", has_text=re.compile(r"confirmare și salvare", re.I)).click()
    page.wait_for_timeout(5000)  # the toast is short-lived; verify the state on the preview instead
    preview(page, rid)
    if not page.locator("button", has_text=re.compile(r"^\s*privat\s*$", re.I)).count():
        sys.exit("Nu pot confirma starea „Privat” pe previzualizare: verifică „Rețetele mele”.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("recipe")
    ap.add_argument("--manual-terms", action="store_true", help="do NOT tick the terms of use (default: ticked automatically, the user's standing choice)")
    ap.add_argument("--save", action="store_true", help="user confirmed 'Salvare proiect'")
    ap.add_argument("--no-ai-declaration", action="store_true", help="do NOT tick 'image created with AI' (default: ticked, by the user's standing choice)")
    ap.add_argument("--finalize-private", action="store_true", help="user confirmed 'Salvare ca privat' (needs --save)")
    ap.add_argument("--recipe-id", help="an already saved project: skip the form and only finalize it (with --finalize-private)")
    ap.add_argument("--reject-cookies", action="store_true", help="reject non-essential cookies instead of accepting all (default: accept all)")
    ap.add_argument("--email", help="fill this e-mail in the login form (or set MCS_EMAIL); the password is never filled")
    ap.add_argument("--fresh-session", action="store_true", help="clear the saved Chrome session first, so this run starts logged out (default: the session is kept)")
    ap.add_argument("--screenshot", default="/tmp/mcs-form.png")
    ap.add_argument("--inspect", action="store_true", help="only dump the form controls of each step")
    a = ap.parse_args()

    recipe = json.load(open(a.recipe))
    errs, desc = validate(recipe)
    if errs and not a.inspect:
        sys.exit("JSON invalid:\n- " + "\n- ".join(errs))

    from playwright.sync_api import sync_playwright
    if a.fresh_session:
        shutil.rmtree(PROFILE, ignore_errors=True)
    PROFILE.mkdir(parents=True, exist_ok=True)
    # Chrome must not offer to save the password: switch its password manager off in the (fresh) profile
    (PROFILE / "Default").mkdir(exist_ok=True)
    prefs = PROFILE / "Default" / "Preferences"
    if not prefs.exists():
        prefs.write_text(json.dumps({"credentials_enable_service": False, "credentials_enable_autosignin": False,
                                     "profile": {"password_manager_enabled": False}}))
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(str(PROFILE), channel="chrome", headless=False, chromium_sandbox=True,
                                                   args=["--disable-save-password-bubble"],
                                                   viewport={"width": 1280, "height": 900})
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        wait_for_form(page, not a.manual_terms, a.reject_cookies, a.email or os.environ.get("MCS_EMAIL"))
        log("Formular deschis.")
        if a.inspect and not a.save:
            inspect(page, "pas 1 Detalii")
            ctx.close(); return
        if a.recipe_id:
            if not a.finalize_private:
                sys.exit("--recipe-id se folosește doar cu --finalize-private.")
            finalize_private(page, a.recipe_id)
            log("Rețeta", a.recipe_id, "a fost salvată ca PRIVATĂ.")
            check_image(page, a.recipe_id)
            ctx.close(); return
        fill_details(page, recipe, desc, not a.no_ai_declaration)
        next_step(page)
        fill_time(page, recipe)
        next_step(page)
        fill_ingredients(page, recipe)
        next_step(page)
        fill_steps(page, recipe)
        page.screenshot(path=a.screenshot, full_page=True)
        log("Formular completat (nesalvat). Captura:", a.screenshot)
        if a.save:
            rid = save_project(page)
            log("Proiect salvat. recipe-id =", rid)
            check_image(page, rid)
            if a.finalize_private:
                finalize_private(page, rid)
                log("Rețeta a fost salvată ca PRIVATĂ.")
                check_image(page, rid)
        else:
            page.wait_for_timeout(5000)
        ctx.close()


if __name__ == "__main__":
    main()
