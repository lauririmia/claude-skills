#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["playwright"]
# ///
"""mcs shopping-list: reads the user's shopping list from monsieur-cuisine.com and prints it as Markdown.

Run:  uv run shopping_list.py [--clear] [--json] [--reject-cookies] [--email ADDRESS] [--fresh-session]

Opens https://www.monsieur-cuisine.com/ro/lista-de-cumparaturi in Chrome (same saved session as /mcs:upload,
~/.cache/mcs/chrome-profile), then
  1. tab "Pe categorii": reads every item and its quantity, grouped by category;
  2. tab "Conform rețetei": counts the recipes on the list and reads each recipe's items and quantities.
Without --clear it is READ-ONLY: it never ticks an item, deletes anything or adds a recipe/item.
With --clear, AFTER everything was read (and a copy saved to ~/.cache/mcs/shopping-list-last.md), it empties the
whole shopping list on the site ("Golire listă de cumpărături" -> "ȘTERGERE TOATE": all items and recipes) and checks it is empty.
It never clears when nothing was read.

stdout = the result only (Markdown, or JSON with --json); progress goes to stderr.
Each list is its own fenced ```markdown block (one click to copy). Every item is a task-list line ("- [ ] name - quantity"), so it renders as a checkbox.
The login is always done by the user in the opened Chrome window; passwords are never typed by this script.
"""
import argparse, json, os, re, shutil, sys, time, unicodedata
from fractions import Fraction
from pathlib import Path

URL = "https://www.monsieur-cuisine.com/ro/lista-de-cumparaturi"
PROFILE = Path.home() / ".cache" / "mcs" / "chrome-profile"
TAB_CATEGORIES = re.compile(r"^\s*Pe categorii\s*$", re.I)
TAB_RECIPES = re.compile(r"^\s*Conform re[țt]etei\s*$", re.I)
COOKIE_ACCEPT = re.compile(r"^\s*(accept(ă)? toate|accept all|allow all|accept)( cookie-?uri(le)?)?\s*$", re.I)
COOKIE_REJECT = re.compile(r"^\s*(respinge(ți)?( toate)?|reject all|refuz[aă]( toate)?)\s*$", re.I)
BUSY = re.compile(r"capacitate\s+maxim|reîncercați|reincercati|try again later|at capacity", re.I)

READ_GROUPS_JS = """() => [...document.querySelectorAll('.shopping-item-group')].map(g => {
  const hdr = g.querySelector('.v-expansion-panel-header');
  const lines = hdr ? hdr.innerText.split('\\n').map(s => s.trim()).filter(Boolean) : [];
  const txt = e => e ? e.innerText.trim() : '';
  const items = [...g.querySelectorAll('.item-content')].map(c => ({
    name: txt(c.querySelector('.item-content-title')),
    qty: txt(c.querySelector('.item-content-subtitle'))}));
  return {title: lines[0] || '', subtitle: lines[1] || '', open: !!g.querySelector('.v-expansion-panel--active'), items};
})"""


def log(*a):
    print(*a, file=sys.stderr, flush=True)


def handle_cookies(page, reject=False):
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


def wait_for_list(page, reject_cookies=False, email=None):
    """Get to the shopping-list page; login and device choice are the user's (terms/consent are accepted as in /mcs:upload)."""
    told, typed, busy_n = set(), {}, 0
    deadline = time.time() + 15 * 60
    page.goto(URL)
    while time.time() < deadline:
        page.wait_for_timeout(1000)
        handle_cookies(page, reject_cookies)
        body = page.locator("body").inner_text()[:4000]
        if page.get_by_role("tab", name=TAB_CATEGORIES).count() and page.get_by_role("tab", name=TAB_CATEGORIES).first.is_visible():
            return
        if BUSY.search(body):
            busy_n += 1
            if busy_n > 8:
                sys.exit("Site-ul raportează în continuare „capacitate maximă”. Reia mai târziu.")
            log(f"Site la capacitate maximă; reîncerc ({busy_n}/8).")
            page.wait_for_timeout(15000 * busy_n)
            page.goto(URL)
            continue
        if page.get_by_text(re.compile("selectați aparatul", re.I)).first.is_visible():
            if "device" not in told:
                told.add("device"); log("Aleg aparatul MC SMART.")
            try:
                page.locator(".device-selector-item", has_text=re.compile(r"mc smart", re.I)).first.click(timeout=6000)
                page.wait_for_timeout(500)
                ok = page.locator("button", has_text=re.compile(r"^\s*ok\s*$", re.I))
                if ok.count() and ok.first.is_enabled():
                    ok.first.click(timeout=3000)
                    page.wait_for_timeout(1500)
                    page.goto(URL)
            except Exception:
                pass
        elif page.get_by_text(re.compile("prelucrarea datelor|prelucrare a datelor|prelucrării datelor", re.I)).first.is_visible() \
                and page.locator("button, input[type=submit]", has_text=re.compile(r"^\s*accept(ă|a)\s*$", re.I)).count():
            try:
                page.locator("button, input[type=submit]", has_text=re.compile(r"^\s*accept(ă|a)\s*$", re.I)).first.click(timeout=3000)
                log("Prelucrarea datelor: acceptată (implicit, alegerea utilizatorului).")
                page.wait_for_timeout(1500)
            except Exception:
                pass
        elif page.get_by_text("Accept condițiile de utilizare").first.is_visible():
            box = page.locator("input[type=checkbox]").filter(visible=True).first
            page.get_by_text("Accept condițiile de utilizare").first.click()
            page.wait_for_timeout(500)
            if box.count() and not box.is_checked():
                box.check(force=True)
            page.locator("button", has_text=re.compile(r"începeți acum", re.I)).click(timeout=5000)
            log("Condițiile de utilizare: bifate (implicit, alegerea utilizatorului).")
        elif "accounts.lidl.com" in page.url or "autentificare" in page.url:
            if email and "email" not in told:
                field = page.locator("input[type=email], input[name*=mail i], input[id*=mail i]").filter(visible=True)
                if field.count():
                    field.first.fill(email)
                    told.add("email"); log("E-mail completat în câmpul de login.")
                    nxt = page.locator("button, input[type=submit]", has_text=re.compile(r"^\s*continu(ă|a|e)\s*$", re.I))
                    if nxt.count():
                        nxt.first.click(timeout=3000)
            pw = page.locator("input[type=password]").filter(visible=True)
            if pw.count() and "pw_click" not in told:
                n = pw.first.evaluate("e => e.value.length")
                if n != typed.get("n"):
                    typed["n"], typed["t"] = n, time.time()
                elif n > 0 and time.time() - typed["t"] >= 3:
                    nxt = page.locator("button, input[type=submit]", has_text=re.compile(r"^\s*continu(ă|a|e)\s*$", re.I))
                    if nxt.count():
                        told.add("pw_click"); nxt.first.click(timeout=3000)
                        log("Parola introdusă de tine; apăsat „Continuă”.")
            if "login" not in told:
                told.add("login"); log(">> Autentifică-te tu în fereastra Chrome (scriptul nu introduce parole). Aștept...")
    sys.exit("Timeout: lista de cumpărături nu s-a deschis în 15 minute.")


def open_tab(page, pattern):
    tab = page.get_by_role("tab", name=pattern).first
    tab.click(timeout=8000)
    page.wait_for_timeout(800)
    return tab


def read_groups(page):
    """Read every group (category or recipe). Collapsed groups that look empty are expanded to read them."""
    for _ in range(20):                      # wait for the list to render
        if page.locator(".shopping-item-group").count():
            break
        page.wait_for_timeout(500)
    page.wait_for_timeout(800)
    groups = page.evaluate(READ_GROUPS_JS)
    for i, g in enumerate(groups):
        if not g["items"] and not g["open"]:
            try:
                page.locator(".shopping-item-group").nth(i).locator(".v-expansion-panel-header").first.click(timeout=3000)
                page.wait_for_timeout(700)
                groups[i] = page.evaluate(READ_GROUPS_JS)[i]
            except Exception:
                pass
    return groups


PLURALS = {"bucată": "bucăți", "linguriță": "lingurițe", "lingură": "linguri", "priză": "prize",
           "vârf de cuțit": "vârfuri de cuțit", "strat": "straturi", "legătură": "legături",
           "crenguță": "crenguțe", "cățel": "căței"}
SINGULARS = {v: k for k, v in PLURALS.items()}
NUM = r"\d+(?:[.,]\d+)?(?:/\d+)?"
QTY_RE = re.compile(rf"^(?P<lo>{NUM})(?:\s*[-–]\s*(?P<hi>{NUM}))?\s*(?P<unit>.*?)\s*$")


def _num(s):
    s = s.replace(",", ".")
    return Fraction(s)


def parse_qty(q):
    """'1,5 lingurițe' -> (Fraction(3,2), Fraction(3,2), 'linguriță'); 'după gust' -> None."""
    m = QTY_RE.match(q or "")
    if not m:
        return None
    lo = _num(m["lo"])
    hi = _num(m["hi"]) if m["hi"] else lo
    unit = m["unit"]
    return lo, hi, SINGULARS.get(unit, unit)


def fmt_num(v):
    if v.denominator == 1:
        return str(v.numerator)
    if v < 1:
        return f"{v.numerator}/{v.denominator}"
    return f"{float(v):.2f}".rstrip("0").rstrip(".").replace(".", ",")


def fmt_qty(lo, hi, unit):
    """Plural unit when the amount is above 1 (1 and 1/2 stay singular), as in Romanian."""
    amount = fmt_num(lo) if lo == hi else f"{fmt_num(lo)}-{fmt_num(hi)}"
    if unit and hi > 1:
        unit = PLURALS.get(unit, unit)
    return f"{amount} {unit}".strip()


def pluralize(q):
    p = parse_qty(q)
    return fmt_qty(*p) if p else q


OPTIONAL_RE = re.compile(r"\s*\(\s*op[țtş]ional\s*\)", re.I)
PAREN_RE = re.compile(r"\s*\([^)]*\)")


def clean_name(name, drop_all_parens=False):
    """'sos chili (opțional)' -> 'sos chili'. With drop_all_parens also 'usturoi (căței)' -> 'usturoi'."""
    return (PAREN_RE if drop_all_parens else OPTIONAL_RE).sub("", name).strip()


def sort_key(name):
    """Alphabetical, diacritics ignored (ă/â -> a, î -> i, ș -> s, ț -> t)."""
    return unicodedata.normalize("NFD", name.lower()).encode("ascii", "ignore").decode()


def dedupe(groups):
    """One line per ingredient, alphabetical. Same name and unit are summed; different units are listed with ' + '.
    A non-numeric quantity ('după gust') is kept only when the ingredient has no numeric quantity at all."""
    merged = {}
    for g in groups:
        for it in g["items"]:
            name = clean_name(it["name"], drop_all_parens=True)
            entry = merged.setdefault(name.lower(), {"name": name, "sums": {}, "texts": []})
            p = parse_qty(it["qty"])
            if p:
                lo, hi, unit = p
                a = entry["sums"].get(unit, (Fraction(0), Fraction(0)))
                entry["sums"][unit] = (a[0] + lo, a[1] + hi)
            elif it["qty"] and it["qty"] not in entry["texts"]:
                entry["texts"].append(it["qty"])
    items = []
    for e in merged.values():
        parts = [fmt_qty(lo, hi, unit) for unit, (lo, hi) in e["sums"].items()] or e["texts"]
        items.append({"name": e["name"], "qty": " + ".join(parts)})
    return sorted(items, key=lambda i: sort_key(i["name"]))


def clear_list(page):
    """Empty the whole shopping list: top trash icon -> dialog 'Golire listă de cumpărături' -> 'ȘTERGERE TOATE'.
    Only that dialog is confirmed (its title is checked first). Returns True when the list is verified empty."""
    page.goto(URL)
    page.get_by_role("tab", name=TAB_CATEGORIES).first.wait_for(timeout=15000)
    page.wait_for_timeout(1500)
    page.locator("button.ml-auto.v-btn--icon:has(i.mdi-delete)").first.click(timeout=8000)
    dlg = page.locator(".v-dialog--active")
    dlg.wait_for(state="visible", timeout=8000)
    if not re.search(r"golire list[ăa] de cump[ăa]r[ăa]turi", dlg.inner_text(), re.I):
        page.get_by_role("button", name=re.compile(r"revocare", re.I)).click(timeout=3000)
        log("!! Dialogul de ștergere nu e cel așteptat; nu am șters nimic.")
        return False
    dlg.get_by_role("button", name=re.compile(r"[șş]tergere toate", re.I)).click(timeout=5000)
    page.wait_for_timeout(2500)
    page.goto(URL)
    page.get_by_role("tab", name=TAB_CATEGORIES).first.wait_for(timeout=15000)
    page.wait_for_timeout(2000)
    left = page.locator(".item-content").count()
    open_tab(page, TAB_RECIPES)
    page.wait_for_timeout(1000)
    left += page.locator(".item-content").count()
    return left == 0


def to_markdown(categories, recipes, existing=()):
    """Each list is its own fenced ```markdown block, so it can be copied with one click."""
    def item_line(it):
        q = pluralize(it["qty"]) if "+" not in it["qty"] else it["qty"]
        name = clean_name(it["name"])
        return f"- [ ] {name} — {q}" if q else f"- [ ] {name}"

    def block(title, lines):
        return "```markdown\n" + title + "\n\n" + "\n".join(lines) + "\n```\n"

    items = dedupe(categories)
    out = [block(f"## Lista de cumpărături ({len(items)} articole)", [item_line(it) for it in items] or ["_Lista este goală._"])]
    out.append(f"Conform rețetei — {len(recipes)} {'rețetă' if len(recipes) == 1 else 'rețete'}:\n")
    for g in recipes:
        head = g["title"] + (f" ({g['subtitle']})" if g["subtitle"] else "")
        out.append(block(f"### {head}", [item_line(it) for it in g["items"]] or ["_fără articole_"]))
    if existing:
        out.append("Deja existent:\n")
        out.append(block("### Deja existent", [item_line(it) for g in existing for it in g["items"]]))
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--clear", action="store_true", help="after reading, empty the whole shopping list on the site (items and recipes)")
    ap.add_argument("--json", action="store_true", help="print JSON instead of Markdown")
    ap.add_argument("--reject-cookies", action="store_true", help="reject non-essential cookies instead of accepting all")
    ap.add_argument("--email", help="fill this e-mail in the login form (or set MCS_EMAIL); the password is never filled")
    ap.add_argument("--fresh-session", action="store_true", help="clear the saved Chrome session first")
    a = ap.parse_args()

    from playwright.sync_api import sync_playwright
    if a.fresh_session:
        shutil.rmtree(PROFILE, ignore_errors=True)
    PROFILE.mkdir(parents=True, exist_ok=True)
    (PROFILE / "Default").mkdir(exist_ok=True)
    prefs = PROFILE / "Default" / "Preferences"
    if not prefs.exists():
        prefs.write_text(json.dumps({"credentials_enable_service": False, "credentials_enable_autosignin": False,
                                     "profile": {"password_manager_enabled": False}}))
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(str(PROFILE), channel="chrome", headless=False, chromium_sandbox=True,
                                                   args=["--disable-save-password-bubble"],
                                                   viewport={"width": 1280, "height": 900})
        try:
            page = ctx.pages[0] if ctx.pages else ctx.new_page()
            wait_for_list(page, a.reject_cookies, a.email or os.environ.get("MCS_EMAIL"))
            log("Lista de cumpărături deschisă.")
            open_tab(page, TAB_CATEGORIES)
            groups = read_groups(page)
            categories = [g for g in groups if g["title"].lower() != "deja existent"]
            existing = [g for g in groups if g["title"].lower() == "deja existent" and g["items"]]
            log("Pe categorii:", sum(len(g["items"]) for g in categories), "articole în", len(categories), "grupuri.")
            open_tab(page, TAB_RECIPES)
            groups = read_groups(page)
            recipes = [g for g in groups if g["title"].lower() != "deja existent"]
            log("Conform rețetei:", len(recipes), "rețete.")
            cleared = None
            if a.clear:
                read_any = any(g["items"] for g in categories + recipes + existing)
                if not read_any:
                    log("Nu am citit niciun articol; nu șterg nimic.")
                else:
                    backup = Path.home() / ".cache" / "mcs" / "shopping-list-last.md"
                    backup.write_text(to_markdown(categories, recipes, existing), encoding="utf-8")
                    log("Copie de siguranță:", backup)
                    cleared = clear_list(page)
                    log("Lista de cumpărături a fost golită și verificată." if cleared else "!! Golirea nu a putut fi verificată; verifică lista pe site.")
        finally:
            ctx.close()
    if a.json:
        print(json.dumps({"categories": categories, "recipes": recipes, "already_have": existing, "cleared": cleared}, ensure_ascii=False, indent=2))
    else:
        print(to_markdown(categories, recipes, existing))
        if a.clear:
            print("STERS" if cleared else "NESTERS", file=sys.stderr)


if __name__ == "__main__":
    main()
