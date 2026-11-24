#!/usr/bin/env python3
"""Print title, description and transcript of a video URL (YouTube etc.).

Usage: get_transcript.py URL [--langs ro,en]

Tools are located in this order: PATH, then ~/.cache/mcs. If yt-dlp is missing,
it is installed there (never system-wide), trying: venv+pip, uv, then a direct
download of the yt-dlp zipapp (needs only Python). youtube-transcript-api is a
bonus fallback installed only by the venv/uv routes.
Output goes to stdout; progress and errors go to stderr.
Exit codes: 0 ok, 2 no usable transcript (missing, or only music markers),
3 tools could not be installed.
"""
import json, os, re, shutil, subprocess, sys, tempfile, urllib.parse
from pathlib import Path

VENV = Path.home() / ".cache" / "mcs" / "venv"
BIN = VENV / ("Scripts" if os.name == "nt" else "bin")


def log(*a):
    print(*a, file=sys.stderr)


def find_ytdlp():
    p = shutil.which("yt-dlp")
    if p:
        return p
    for cand in (BIN / ("yt-dlp.exe" if os.name == "nt" else "yt-dlp"),
                 Path.home() / ".cache" / "mcs" / "bin" / "yt-dlp"):
        if cand.exists():
            return str(cand)
    return None


def _venv_python():
    return str(BIN / ("python.exe" if os.name == "nt" else "python"))


def _try_venv_pip():
    shutil.rmtree(VENV, ignore_errors=True)
    subprocess.run([sys.executable, "-m", "venv", str(VENV)], check=True,
                   capture_output=True)
    subprocess.run([_venv_python(), "-m", "pip", "install", "-q", "--upgrade",
                    "yt-dlp", "youtube-transcript-api"], check=True)


def _try_uv():
    uv = shutil.which("uv")
    if not uv:
        raise RuntimeError("uv not found")
    shutil.rmtree(VENV, ignore_errors=True)
    subprocess.run([uv, "venv", "-q", str(VENV)], check=True)
    subprocess.run([uv, "pip", "install", "-q", "--python", _venv_python(),
                    "yt-dlp", "youtube-transcript-api"], check=True)


def _try_download():
    # yt-dlp ships as a single self-contained Python zipapp: only Python is needed.
    import urllib.request
    dest = Path.home() / ".cache" / "mcs" / "bin" / "yt-dlp"
    dest.parent.mkdir(parents=True, exist_ok=True)
    url = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp"
    urllib.request.urlretrieve(url, dest)
    dest.chmod(0o755)


def install():
    log("[mcs] yt-dlp not found; installing it under ~/.cache/mcs (never system-wide)")
    for name, fn in (("venv+pip", _try_venv_pip), ("uv", _try_uv),
                     ("direct download", _try_download)):
        try:
            fn()
            path = find_ytdlp()
            if path:
                log(f"[mcs] installed via {name}")
                return path
        except Exception as e:  # noqa: BLE001
            log(f"[mcs] {name} failed: {e}")
    log("[mcs] Could not install yt-dlp automatically. Manual options: "
        "apt install python3-venv, or download "
        "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp "
        "to ~/.cache/mcs/bin/yt-dlp and chmod +x it.")
    sys.exit(3)


def clean_vtt(text):
    out, prev = [], None
    for line in text.splitlines():
        line = line.strip()
        if (not line or line.startswith(("WEBVTT", "Kind:", "Language:", "NOTE"))
                or "-->" in line or re.fullmatch(r"\d+", line)):
            continue
        line = re.sub(r"<[^>]+>", "", line).strip()
        if line and line != prev:
            out.append(line)
            prev = line
    return " ".join(out)


def video_id(url):
    u = urllib.parse.urlparse(url)
    if u.hostname and "youtu.be" in u.hostname:
        return u.path.strip("/")
    return urllib.parse.parse_qs(u.query).get("v", [None])[0]


def via_ytdlp(ytdlp, url, langs):
    meta = {}
    r = subprocess.run([ytdlp, "--skip-download", "--dump-single-json", "--no-warnings", url],
                       capture_output=True, text=True)
    if r.returncode == 0:
        meta = json.loads(r.stdout)
    with tempfile.TemporaryDirectory(prefix="mcs-sub-") as d:
        subprocess.run([ytdlp, "--skip-download", "--write-subs", "--write-auto-subs",
                        "--sub-langs", langs, "--sub-format", "vtt", "--no-warnings",
                        "-o", os.path.join(d, "s.%(ext)s"), url],
                       capture_output=True, text=True)
        files = sorted(Path(d).glob("*.vtt"))
        # prefer manual-looking order of requested langs
        for lang in langs.split(","):
            for f in files:
                if f".{lang}" in f.name:
                    return meta, clean_vtt(f.read_text("utf-8", "ignore"))
        if files:
            return meta, clean_vtt(files[0].read_text("utf-8", "ignore"))
    return meta, ""


def via_api(url, langs):
    vid = video_id(url)
    py = BIN / ("python.exe" if os.name == "nt" else "python")
    if not vid or not py.exists():
        return ""
    code = ("import sys;from youtube_transcript_api import YouTubeTranscriptApi as Y;"
            "l=sys.argv[2].split(',');a=Y();"
            "t=a.fetch(sys.argv[1],languages=l);print(' '.join(s.text for s in t))")
    r = subprocess.run([str(py), "-c", code, vid, langs], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else ""


def is_speech(text):
    """True if the text has real spoken content, not just [Music]/foreign markers."""
    t = re.sub(r"\[[^\]]*\]|\((?:music|applause)\)", " ", text or "", flags=re.I)
    words = [w for w in re.findall(r"[^\W\d_]+", t) if w.lower() != "foreign"]
    return len(words) >= 30


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)
    url = args[0]
    langs = "ro,en"
    if "--langs" in args:
        langs = args[args.index("--langs") + 1]
    ytdlp = find_ytdlp() or install()
    meta, text = via_ytdlp(ytdlp, url, langs + ",.*")
    if not text:
        log("[mcs] yt-dlp returned no subtitles; trying youtube-transcript-api")
        text = via_api(url, langs)
    if not is_speech(text):
        log("[mcs] No usable transcript: captions are missing or contain only "
            "music/sound markers (e.g. '[Music]', 'foreign').")
        sys.exit(2)
    print("TITLE:", meta.get("title", ""))
    print("CHANNEL:", meta.get("uploader", ""))
    print("\nDESCRIPTION:\n" + (meta.get("description") or ""))
    print("\nTRANSCRIPT:\n" + text)


if __name__ == "__main__":
    main()
