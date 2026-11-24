#!/usr/bin/env python3
"""Prepare the recipe image required by the Monsieur Cuisine form.

Usage: prepare_image.py SOURCE OUT.jpg
  SOURCE  a recipe page URL (its image is looked up), a direct image URL,
          or a local image path.

The form needs JPEG/PNG, at least 1560x945 px, subject centred. This script
finds the best candidate image (also trying the full-size original behind resized-image URLs), centre-crops it to the 1560:945 ratio and saves
it as JPEG at 1560x945. It enlarges by at most 5% (needed for typical 1536x1024
AI-generated images); anything smaller is reported as too_small, not stretched,
because a larger upscale would look blurry.

Prints one JSON object on stdout:
  {"status": "ok", "path": ..., "size": [w, h], "source_image": url_or_path, "crop_loss_pct": n}
  {"status": "too_small", "best": [w, h], "source_image": ...}
  {"status": "not_found"}
Exit code is 0 for all three statuses (the caller decides what to do); 3 if
Pillow is unavailable and cannot be provided.
"""
import io, json, os, re, shutil, sys, urllib.parse, urllib.request

try:
    from PIL import Image
except ImportError:
    uv = shutil.which("uv")
    if uv and not os.environ.get("MCS_UV_REEXEC"):
        os.environ["MCS_UV_REEXEC"] = "1"
        os.execvp(uv, [uv, "run", "--quiet", "--with", "pillow", "python", __file__] + sys.argv[1:])
    print("Pillow is required: pip install pillow (or install uv)", file=sys.stderr)
    sys.exit(3)

W, H = 1560, 945
MAX_UPSCALE = 1.05  # a 5% enlargement is invisible; more would look blurry
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=30).read()


def collect_urls(node, out):
    if isinstance(node, str):
        out.append(node)
    elif isinstance(node, list):
        for n in node:
            collect_urls(n, out)
    elif isinstance(node, dict) and "url" in node:
        collect_urls(node["url"], out)


def candidates_from_page(html, base):
    urls = []
    for m in re.finditer(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', html, re.S | re.I):
        try:
            data = json.loads(m.group(1))
        except json.JSONDecodeError:
            continue
        stack = [data]
        while stack:
            n = stack.pop()
            if isinstance(n, list):
                stack.extend(n)
            elif isinstance(n, dict):
                t = n.get("@type")
                if t == "Recipe" or (isinstance(t, list) and "Recipe" in t):
                    collect_urls(n.get("image"), urls)
                stack.extend(v for v in n.values() if isinstance(v, (dict, list)))
    for m in re.finditer(r'<meta[^>]+(?:property|name)=["\'](?:og:image|twitter:image)["\'][^>]*>', html, re.I):
        c = re.search(r'content=["\']([^"\']+)', m.group(0))
        if c:
            urls.append(c.group(1))
    seen, out = set(), []
    for u in urls:
        u = urllib.parse.urljoin(base, u)
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out


def originals(url):
    """Variants of a resized-image URL that usually point to the full-size original,
    e.g. .../656x440_name.jpg -> .../name.jpg and name-500x500.jpg -> name.jpg."""
    out = []
    a = re.sub(r"/\d+x\d+_", "/", url)
    b = re.sub(r"-\d+x\d+(\.\w+)(\?.*)?$", r"\1", url)
    for v in (a, b):
        if v != url and v not in out:
            out.append(v)
    return out


def load(src):
    data = open(src, "rb").read() if os.path.exists(src) else get(src)
    return Image.open(io.BytesIO(data))


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    source, out_path = sys.argv[1], sys.argv[2]
    cands = [source]
    if re.match(r"https?://", source):
        try:
            blob = get(source)
            try:
                Image.open(io.BytesIO(blob)).verify()  # it is already an image
            except Exception:  # noqa: BLE001
                cands = candidates_from_page(blob.decode("utf-8", "ignore"), source)
        except Exception as e:  # noqa: BLE001
            print(f"[mcs] fetch failed: {e}", file=sys.stderr)
            cands = []
    best = None
    cands = cands + [o for c in cands for o in originals(c)]
    for c in cands:
        try:
            im = load(c)
        except Exception:  # noqa: BLE001
            continue
        if best is None or im.size[0] * im.size[1] > best[0].size[0] * best[0].size[1]:
            best = (im, c)
    if best is None:
        print(json.dumps({"status": "not_found"}))
        return
    im, src = best
    w, h = im.size
    target = W / H
    if w / h > target:
        nw, nh = int(round(h * target)), h
    else:
        nw, nh = w, int(round(w / target))
    scale = max(W / nw, H / nh)
    if scale > MAX_UPSCALE:
        print(json.dumps({"status": "too_small", "best": [w, h], "source_image": src}))
        return
    left, top = (w - nw) // 2, (h - nh) // 2
    im = im.convert("RGB").crop((left, top, left + nw, top + nh))
    if (nw, nh) != (W, H):
        im = im.resize((W, H), Image.LANCZOS)
    im.save(out_path, "JPEG", quality=90)
    loss = round((1 - (nw * nh) / (w * h)) * 100)
    print(json.dumps({"status": "ok", "path": out_path, "size": list(im.size),
                      "source_image": src, "crop_loss_pct": loss, "upscaled_pct": round((scale - 1) * 100, 1) if scale > 1 else 0}))


if __name__ == "__main__":
    main()
