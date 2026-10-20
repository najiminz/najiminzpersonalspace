"""Generate a whole coloring book with the Gemini API, then bundle it into an A4 300 DPI PDF.

    GEMINI_API_KEY=...  python3 gemini_jana.py siri-7            # all 32 images, then the PDF
    GEMINI_API_KEY=...  python3 gemini_jana.py siri-7 --hanya 5,12  # redo pages 5 and 12 only
    python3 gemini_jana.py siri-7 --pdf                           # just rebuild the PDF

Every prompt from data.py is sent with two reference pictures (rujukan/): the
"Keluarga Saya" sample page (layout and style) and the character sheet, so all
pages match. Images land in hasil/<siri>/00.png (front cover), 01.png ... 30.png
and 31.png (back cover). Pages that already exist are skipped, so a stopped run
can simply be started again.
"""
import argparse
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request

import data

HERE = os.path.dirname(os.path.abspath(__file__))
API = "https://generativelanguage.googleapis.com/v1beta"
MODEL = os.environ.get("GEMINI_IMAGE_MODEL", "gemini-2.5-flash-image")
REFS = [("contoh-keluarga-saya.jpg", "Reference 1: the exact page layout and drawing style to follow."),
        ("helaian-watak.jpg", "Reference 2: the character sheet. The children must look exactly like these.")]
A4 = (2480, 3508)


def key():
    k = os.environ.get("GEMINI_API_KEY")
    if not k:
        sys.exit("GEMINI_API_KEY belum ditetapkan. Tambah dalam tetapan persekitaran, kemudian buka sesi baharu.")
    return k


def post(path, body):
    req = urllib.request.Request(f"{API}/{path}", data=json.dumps(body).encode(), method="POST",
                                 headers={"Content-Type": "application/json", "x-goog-api-key": key()})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.load(r)


def generate(prompt, aspect="3:4"):
    parts = []
    for name, note in REFS:
        with open(os.path.join(HERE, "rujukan", name), "rb") as fh:
            parts += [{"text": note}, {"inline_data": {"mime_type": "image/jpeg",
                                                       "data": base64.b64encode(fh.read()).decode()}}]
    parts.append({"text": prompt})
    body = {"contents": [{"role": "user", "parts": parts}],
            "generationConfig": {"responseModalities": ["TEXT", "IMAGE"], "imageConfig": {"aspectRatio": aspect}}}
    try:
        res = post(f"models/{MODEL}:generateContent", body)
    except urllib.error.HTTPError as e:
        msg = e.read().decode(errors="replace")
        if e.code == 400 and "imageConfig" in msg:  # older models without aspect-ratio support
            del body["generationConfig"]["imageConfig"]
            res = post(f"models/{MODEL}:generateContent", body)
        else:
            raise RuntimeError(f"HTTP {e.code}: {msg[:400]}")
    for cand in res.get("candidates", []):
        for part in cand.get("content", {}).get("parts", []):
            blob = part.get("inlineData") or part.get("inline_data")
            if blob:
                return base64.b64decode(blob["data"])
    raise RuntimeError("Tiada gambar dalam jawapan: " + json.dumps(res)[:400])


def series(sid):
    for s in data.SERIES:
        if s["id"] == sid:
            return s
    sys.exit("Siri tidak dikenali. Pilih: " + ", ".join(s["id"] for s in data.SERIES))


def run(sid, only=None):
    out = os.path.join(HERE, "hasil", sid)
    os.makedirs(out, exist_ok=True)
    prompts = data.series_prompts(series(sid))
    for i, (label, prompt) in enumerate(prompts):
        dst = os.path.join(out, f"{i:02d}.png")
        if only is not None and i not in only:
            continue
        if only is None and os.path.exists(dst):
            continue
        for attempt in range(3):
            try:
                img = generate(prompt)
                with open(dst, "wb") as fh:
                    fh.write(img)
                print(f"siap  {i:02d}  {label}", flush=True)
                break
            except Exception as e:  # rate limits and the odd empty answer: wait and retry
                print(f"cuba semula {i:02d} ({e})", flush=True)
                time.sleep(20 * (attempt + 1))
        else:
            print(f"GAGAL {i:02d}  {label}", flush=True)


def pdf(sid):
    from PIL import Image
    import img2pdf
    out = os.path.join(HERE, "hasil", sid)
    pages = []
    for name in sorted(f for f in os.listdir(out) if f[:2].isdigit() and f.endswith(".png")):
        im = Image.open(os.path.join(out, name)).convert("RGB")
        scale = min(A4[0] / im.width, A4[1] / im.height)
        im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
        page = Image.new("RGB", A4, "white")
        page.paste(im, ((A4[0] - im.width) // 2, (A4[1] - im.height) // 2))
        dst = os.path.join(out, "a4", name)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        page.save(dst, dpi=(300, 300))
        pages.append(dst)
    a4 = img2pdf.get_layout_fun((img2pdf.mm_to_pt(210), img2pdf.mm_to_pt(297)))
    path = os.path.join(out, f"{sid}-gemini-A4-300dpi.pdf")
    with open(path, "wb") as fh:
        fh.write(img2pdf.convert(pages, layout_fun=a4))
    print(f"PDF: {path} ({len(pages)} muka)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("siri", help="siri-4, siri-7, siri-8 atau siri-10")
    ap.add_argument("--hanya", help="nombor halaman untuk dijana semula, contoh 5,12 (0 = kulit depan, 31 = kulit belakang)")
    ap.add_argument("--pdf", action="store_true", help="hanya bina semula PDF")
    a = ap.parse_args()
    if not a.pdf:
        run(a.siri, {int(n) for n in a.hanya.split(",")} if a.hanya else None)
    pdf(a.siri)
