#!/usr/bin/env python3
"""Print title, description and transcript of a video URL (YouTube etc.).

Usage: get_transcript.py URL [--langs ro,en] [--whisper [--model small|medium] [--keep-model]]

--whisper is a fallback for videos without usable captions: it downloads the audio
(yt-dlp) and transcribes it locally with faster-whisper (installed in
~/.cache/mcs/whisper-venv; the model is downloaded on first use, about 0.5 GB for
"small", 1.5 GB for "medium"). Without --model it picks one: "small" if the description
lists quantities, "medium" otherwise. It is never started without the flag, because it downloads files.

Tools are located in this order: PATH, then ~/.cache/mcs. If yt-dlp is missing,
it is installed there (never system-wide), trying: venv+pip, uv, then a direct
download of the yt-dlp zipapp (needs only Python). youtube-transcript-api is a
bonus fallback installed only by the venv/uv routes.
Output goes to stdout; progress and errors go to stderr.
Exit codes: 0 ok, 2 no usable transcript (missing, or only music markers),
3 tools could not be installed, 4 the Whisper fallback failed.
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


WHISPER_VENV = Path.home() / ".cache" / "mcs" / "whisper-venv"
WHISPER_CODE = """
import sys
from faster_whisper import WhisperModel
path, model, lang = sys.argv[1], sys.argv[2], sys.argv[3] or None
m = WhisperModel(model, device="cpu", compute_type="int8")
segs, info = m.transcribe(path, language=lang, vad_filter=True, beam_size=5)
print("LANG:" + info.language, file=sys.stderr)
print(" ".join(s.text.strip() for s in segs))
"""


def whisper_python():
    """Create (once) a private venv with faster-whisper; python 3.12 via uv when available,
    because the audio/ML wheels lag behind the newest Python versions."""
    py = WHISPER_VENV / ("Scripts" if os.name == "nt" else "bin") / ("python.exe" if os.name == "nt" else "python")
    if py.exists():
        return str(py)
    log("[mcs] installing faster-whisper under ~/.cache/mcs/whisper-venv (first time only)")
    shutil.rmtree(WHISPER_VENV, ignore_errors=True)
    uv = shutil.which("uv")
    if uv:
        r = subprocess.run([uv, "venv", "-q", "--python", "3.12", str(WHISPER_VENV)])
        if r.returncode != 0:
            subprocess.run([uv, "venv", "-q", str(WHISPER_VENV)], check=True)
        subprocess.run([uv, "pip", "install", "-q", "--python", str(py), "faster-whisper", "av>=14,<17"], check=True)
    else:
        subprocess.run([sys.executable, "-m", "venv", str(WHISPER_VENV)], check=True)
        subprocess.run([str(py), "-m", "pip", "install", "-q", "faster-whisper", "av>=14,<17"], check=True)
    return str(py)


def delete_model(model):
    """Remove the downloaded faster-whisper model from the Hugging Face cache."""
    hub = os.environ.get("HF_HUB_CACHE") or os.path.join(os.environ.get("HF_HOME") or str(Path.home() / ".cache" / "huggingface"), "hub")
    d = Path(hub) / f"models--Systran--faster-whisper-{model}"
    if d.is_dir():
        shutil.rmtree(d, ignore_errors=True)
        log(f"[mcs] model '{model}' deleted from {d} (use --keep-model to keep it)")


def via_whisper(ytdlp, url, model, lang):
    """Download the audio and transcribe it locally. Returns (text, detected_language)."""
    with tempfile.TemporaryDirectory(prefix="mcs-audio-") as d:
        log("[mcs] downloading the audio track (yt-dlp)")
        r = subprocess.run([ytdlp, "-f", "bestaudio[ext=m4a]/bestaudio", "--no-warnings", "--no-playlist",
                            "-o", os.path.join(d, "audio.%(ext)s"), url], capture_output=True, text=True)
        files = [f for f in Path(d).iterdir() if f.name.startswith("audio.")]
        if r.returncode != 0 or not files:
            log("[mcs] audio download failed:", (r.stderr or "")[-300:])
            return "", ""
        log(f"[mcs] transcribing with faster-whisper '{model}' (first run downloads the model; this takes a few minutes)")
        r = subprocess.run([whisper_python(), "-c", WHISPER_CODE, str(files[0]), model, lang],
                           capture_output=True, text=True)
        if r.returncode != 0:
            log("[mcs] whisper failed:", (r.stderr or "")[-400:])
            return "", ""
        m = re.search(r"LANG:(\w+)", r.stderr or "")
        return r.stdout.strip(), (m.group(1) if m else "")


UNITS = r"(?:kg|g|gr|grame?|ml|l|litri?|dl|cl|linguri(?:ț[ae]|te)?|lingur[ăa]|lingurit[ăa]|cani?|ceșt[ie]|buc(?:ăț[ie]|ata)?|felii|cățe|plicuri?|pachet(?:e)?|cutii?|căni|kilograme?)"
QTY_RE = re.compile(rf"(?:^|\s|-)\d+(?:[.,/]\d+)?\s*{UNITS}\b|(?:^|\s|-)\d+\s+[^\W\d_]{{3,}}", re.I)


def pick_model(description):
    """'small' when the description lists quantities (the voice only confirms them),
    otherwise 'medium' (quantities come from the voice alone). Returns (model, reason)."""
    lines = [l for l in (description or "").splitlines() if not re.search(r"https?://|www\.", l)]
    n = sum(1 for l in lines if QTY_RE.search(l))
    if n >= 3:
        return "small", f"the description lists quantities ({n} lines), the voice only confirms them"
    return "medium", f"the description has no quantities ({n} lines), they come from the voice alone"


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
    model = args[args.index("--model") + 1] if "--model" in args else None
    ytdlp = find_ytdlp() or install()
    meta, text = via_ytdlp(ytdlp, url, langs + ",.*")
    if not text:
        log("[mcs] yt-dlp returned no subtitles; trying youtube-transcript-api")
        text = via_api(url, langs)
    source = "captions"
    if not is_speech(text):
        log("[mcs] No usable transcript: captions are missing or contain only "
            "music/sound markers (e.g. '[Music]', 'foreign').")
        if "--whisper" not in args:
            log("[mcs] Re-run with --whisper to transcribe the audio locally (downloads the audio and a model).")
            sys.exit(2)
        if model:
            log(f"[mcs] model '{model}' (chosen by the user)")
        else:
            model, why = pick_model(meta.get("description"))
            log(f"[mcs] model '{model}': {why}")
        try:
            text, lang = via_whisper(ytdlp, url, model, "")
        finally:
            if "--keep-model" not in args:
                delete_model(model)
        if not is_speech(text):
            log("[mcs] The Whisper fallback produced no usable text.")
            sys.exit(4)
        source = f"Whisper '{model}' (speech-to-text, language: {lang or 'auto'}; numbers and ingredient names may be misheard)"
    print("TITLE:", meta.get("title", ""))
    print("CHANNEL:", meta.get("uploader", ""))
    print("\nDESCRIPTION:\n" + (meta.get("description") or ""))
    print(f"\nTRANSCRIPT ({source}):\n" + text)


if __name__ == "__main__":
    main()
