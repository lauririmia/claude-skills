#!/usr/bin/env python3
"""Fetch a recipe web page and print the best material for extraction.

Usage: fetch_page.py URL

Prints, in order of reliability:
  1. the schema.org Recipe from <script type="application/ld+json"> (exact
     quantities, times, steps, nutrition) - when the page has one;
  2. the page's visible text (scripts/styles stripped), truncated.
Why this exists: summarising web-fetch tools paraphrase pages and blur
quantities; the raw structured data does not.
Exit codes: 0 ok, 2 page could not be fetched.
"""
import json, re, sys, urllib.request
from html.parser import HTMLParser

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"


def find_recipes(node, out):
    if isinstance(node, list):
        for n in node:
            find_recipes(n, out)
    elif isinstance(node, dict):
        t = node.get("@type")
        if t == "Recipe" or (isinstance(t, list) and "Recipe" in t):
            out.append(node)
        for v in node.values():
            if isinstance(v, (dict, list)):
                find_recipes(v, out)


class Text(HTMLParser):
    SKIP = {"script", "style", "noscript", "svg", "nav", "footer", "header", "form"}

    def __init__(self):
        super().__init__()
        self.depth, self.parts = 0, []

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.depth += 1

    def handle_endtag(self, tag):
        if tag in self.SKIP and self.depth:
            self.depth -= 1

    def handle_data(self, data):
        if not self.depth and data.strip():
            self.parts.append(data.strip())


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    url = sys.argv[1]
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en,ro;q=0.8"})
        html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore")
    except Exception as e:  # noqa: BLE001
        print(f"[mcs] fetch failed: {e}", file=sys.stderr)
        sys.exit(2)
    recipes = []
    for m in re.finditer(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', html, re.S | re.I):
        try:
            find_recipes(json.loads(m.group(1)), recipes)
        except json.JSONDecodeError:
            continue
    tm = re.search(r"<title[^>]*>(.*?)</title>", html, re.S | re.I)
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S | re.I)
    clean = lambda m: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(1))).strip() if m else ""
    print("PAGE TITLE:", clean(tm))
    print("PAGE H1:", clean(h1))
    if recipes:
        print("SOURCE: schema.org Recipe (structured data)\n")
        print(json.dumps(recipes[0], ensure_ascii=False, indent=1))
    else:
        t = Text()
        t.feed(html)
        text = "\n".join(t.parts)
        print("SOURCE: page text (no structured Recipe data found)\n")
        print(text[:20000])


if __name__ == "__main__":
    main()
