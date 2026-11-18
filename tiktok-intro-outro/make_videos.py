#!/usr/bin/env python3
"""
Jana video intro & outro TikTok (1080x1920, 30fps) dengan logo UPTM.

Cara guna:
    1. Letak fail logo dalam folder ini dengan nama  logo.png
       (PNG latar telus paling cantik; JPG/PNG latar putih pun boleh,
       ia akan diletak atas kad putih secara automatik).
    2. Ubah teks di bahagian TETAPAN kalau nak.
    3. Jalankan:  python3 make_videos.py
    4. Hasil:  intro.mp4  dan  outro.mp4

Perlu: Python 3, Pillow, numpy, ffmpeg.
"""

import math
import os
import random
import subprocess
import sys
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

# ---------------------------------------------------------------- TETAPAN
HERE = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(HERE, "logo.png")

UNI_NAME = "UNIVERSITI POLY-TECH MALAYSIA"
SHOW_UNI_NAME = True                   # auto-sembunyi bila logo.png ada (logo dah ada nama)
INTRO_TAGLINE = ""                     # contoh: "Projek Algoritma TSP"
OUTRO_TITLE = "Thank You"
OUTRO_LINE = "for watching!"

BG_TOP = (8, 20, 56)        # biru gelap
BG_BOTTOM = (2, 6, 20)
ACCENT = (245, 184, 46)     # emas
TEXT = (255, 255, 255)

W, H, FPS = 1080, 1920, 30
INTRO_SEC, OUTRO_SEC = 3.5, 4.0
# Pusat kandungan dinaikkan sedikit supaya tak bertindih dengan UI TikTok di bawah
CY = int(H * 0.42)

FONT_BOLD = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"
FONT_SEMI = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
FONT_REG = "/usr/share/fonts/opentype/inter/Inter-Medium.otf"
FALLBACK = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.truetype(FALLBACK, size)


# ---------------------------------------------------------------- easing
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def prog(t, start, dur):
    return clamp((t - start) / dur)


def ease_out_cubic(x):
    return 1 - (1 - x) ** 3


def ease_in_out(x):
    return 3 * x * x - 2 * x * x * x


def ease_out_back(x, s=1.6):
    x -= 1
    return x * x * ((s + 1) * x + s) + 1


# ---------------------------------------------------------------- aset
def make_background():
    y = np.linspace(0, 1, H)[:, None]
    top, bot = np.array(BG_TOP), np.array(BG_BOTTOM)
    grad = top * (1 - y) + bot * y
    img = np.repeat(grad[:, None, :], W, axis=1).reshape(H, W, 3)
    # cahaya lembut di tengah
    yy, xx = np.mgrid[0:H, 0:W]
    d = np.sqrt((xx - W / 2) ** 2 + ((yy - CY) * 0.8) ** 2) / (W * 0.75)
    glow = np.clip(1 - d, 0, 1) ** 2 * 38
    img = img + glow[..., None] * np.array([0.6, 0.8, 1.0])
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8), "RGB")


def make_logo(max_w=560, max_h=560):
    """Muat logo (dibesarkan/dikecilkan ikut kotak); jika tiada, buat placeholder."""
    if os.path.exists(LOGO_PATH):
        logo = Image.open(LOGO_PATH).convert("RGBA")
        alpha = np.array(logo)[..., 3]
        has_transparency = (alpha < 250).mean() > 0.02
        pad = 0 if has_transparency else int(min(max_w, max_h) * 0.09)
        k = min((max_w - pad * 2) / logo.width, (max_h - pad * 2) / logo.height)
        logo = logo.resize((int(logo.width * k), int(logo.height * k)), Image.LANCZOS)
        if k > 1.2:
            logo = logo.filter(ImageFilter.UnsharpMask(radius=2, percent=80, threshold=2))
        if has_transparency:
            return logo
        # latar tak telus -> letak atas kad putih bucu bulat
        card = Image.new("RGBA", (logo.width + pad * 2, logo.height + pad * 2), (0, 0, 0, 0))
        ImageDraw.Draw(card).rounded_rectangle(
            [0, 0, card.width - 1, card.height - 1], radius=pad, fill=(255, 255, 255, 255))
        card.alpha_composite(logo, (pad, pad))
        return card

    s = min(max_w, max_h)
    print("!! logo.png tiada - guna placeholder. Letak logo sebenar dalam folder ini.")
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([10, 10, s - 10, s - 10], fill=(255, 255, 255, 255))
    d.ellipse([34, 34, s - 34, s - 34], outline=BG_TOP + (255,), width=10)
    f = font(FONT_BOLD, int(s * 0.25))
    d.text((s / 2, s / 2), "UPTM", font=f, fill=BG_TOP + (255,), anchor="mm")
    return img


def make_glow(logo, radius=40):
    a = logo.split()[3]
    pad = radius * 3
    base = Image.new("L", (logo.width + pad * 2, logo.height + pad * 2), 0)
    base.paste(a, (pad, pad))
    base = base.filter(ImageFilter.GaussianBlur(radius))
    glow = Image.new("RGBA", base.size, ACCENT + (0,))
    glow.putalpha(base.point(lambda v: int(v * 0.85)))
    return glow, pad


def paste_center(canvas, img, cx, cy, scale=1.0, alpha=1.0):
    if scale <= 0.01 or alpha <= 0.01:
        return
    if abs(scale - 1) > 1e-3:
        img = img.resize((max(1, int(img.width * scale)), max(1, int(img.height * scale))),
                         Image.BICUBIC)
    if alpha < 1:
        img = img.copy()
        img.putalpha(img.split()[3].point(lambda v: int(v * alpha)))
    canvas.alpha_composite(img, (int(cx - img.width / 2), int(cy - img.height / 2)))


def text_layer(text, fnt, fill, tracking=0):
    """Teks sebagai imej RGBA (dengan jarak huruf pilihan)."""
    if not text:
        return None
    dummy = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    widths = [dummy.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    asc, desc = fnt.getmetrics()
    img = Image.new("RGBA", (int(total) + 20, asc + desc + 20), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    x = 10
    for ch, w in zip(text, widths):
        d.text((x, 10), ch, font=fnt, fill=fill)
        x += w + tracking
    return img


class Particles:
    def __init__(self, n=55, seed=7):
        rnd = random.Random(seed)
        self.p = [(rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(2, 6),
                   rnd.uniform(20, 70), rnd.uniform(0, 6.28)) for _ in range(n)]

    def draw(self, canvas, t, strength=1.0):
        if strength <= 0:
            return
        layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        for x, y, r, speed, ph in self.p:
            yy = (y - speed * t) % H
            xx = x + math.sin(t * 1.3 + ph) * 18
            a = int((0.35 + 0.35 * math.sin(t * 2 + ph)) * 255 * strength)
            d.ellipse([xx - r, yy - r, xx + r, yy + r], fill=ACCENT + (max(0, a),))
        canvas.alpha_composite(layer)


def draw_ring(canvas, cx, cy, radius, progress, width=8, alpha=1.0):
    if progress <= 0 or alpha <= 0:
        return
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    box = [cx - radius, cy - radius, cx + radius, cy + radius]
    d.arc(box, -90, -90 + 360 * progress, fill=ACCENT + (int(255 * alpha),), width=width)
    canvas.alpha_composite(layer)


def light_sweep(canvas, x_pos, strength):
    """Jalur cahaya serong yang melintas skrin."""
    if strength <= 0:
        return
    band = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(band)
    w = 220
    d.polygon([(x_pos, 0), (x_pos + w, 0), (x_pos + w - 700, H), (x_pos - 700, H)],
              fill=int(60 * strength))
    band = band.filter(ImageFilter.GaussianBlur(60))
    white = Image.new("RGBA", (W, H), (255, 255, 255, 0))
    white.putalpha(band)
    canvas.alpha_composite(white)


def fade(canvas, amount, color=(0, 0, 0)):
    if amount <= 0:
        return
    canvas.alpha_composite(Image.new("RGBA", canvas.size, color + (int(255 * clamp(amount)),)))


# ---------------------------------------------------------------- audio
SR = 44100


def whoosh(dur, peak_at):
    n = int(SR * dur)
    t = np.arange(n) / SR
    noise = np.random.default_rng(1).standard_normal(n)
    # tapis low-pass ringkas yang bergerak (bunyi "swoosh")
    out = np.zeros(n)
    acc = 0.0
    for i in range(n):
        k = 0.02 + 0.25 * math.exp(-((t[i] - peak_at) / 0.18) ** 2)
        acc += k * (noise[i] - acc)
        out[i] = acc
    env = np.exp(-((t - peak_at) / 0.22) ** 2)
    return out * env


def chime(dur, freq=880.0):
    t = np.arange(int(SR * dur)) / SR
    s = sum(a * np.sin(2 * np.pi * freq * m * t) for m, a in [(1, 1), (2, 0.4), (3, 0.15), (4.2, 0.08)])
    return s * np.exp(-t * 3.2) * np.minimum(1, t / 0.005)


def place(track, clip, at, gain):
    i = int(at * SR)
    j = min(len(track), i + len(clip))
    track[i:j] += clip[: j - i] * gain


def write_audio(path, total, events):
    track = np.zeros(int(SR * total))
    for kind, at, gain, *extra in events:
        clip = whoosh(1.2, 0.5) if kind == "whoosh" else chime(2.0, *extra)
        start = at - 0.5 if kind == "whoosh" else at
        place(track, clip, max(0, start), gain)
    fade_n = int(SR * 0.3)
    track[-fade_n:] *= np.linspace(1, 0, fade_n)
    peak = np.abs(track).max() or 1
    track = (track / peak * 0.8 * 32767).astype(np.int16)
    with wave.open(path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(track.tobytes())


# ---------------------------------------------------------------- render
def render(path, seconds, frame_fn, audio_events):
    wav = path + ".wav"
    write_audio(wav, seconds, audio_events)
    cmd = ["ffmpeg", "-y", "-loglevel", "error",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-i", wav,
           "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", path]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    total = int(seconds * FPS)
    for i in range(total):
        frame = frame_fn(i / FPS)
        proc.stdin.write(frame.convert("RGB").tobytes())
    proc.stdin.close()
    proc.wait()
    os.remove(wav)
    print(f"  {os.path.basename(path)} ({total} frame)")
    if proc.returncode != 0:
        raise SystemExit("ffmpeg gagal")


def main():
    bg = make_background().convert("RGBA")
    particles = Particles()

    logo = make_logo(800, 560)
    glow, gpad = make_glow(logo)
    small_logo = make_logo(620, 380)
    small_glow, _ = make_glow(small_logo, 30)

    f_name = font(FONT_SEMI, 40)
    f_tag = font(FONT_REG, 50)
    f_title = font(FONT_BOLD, 120)
    f_line = font(FONT_REG, 54)

    # Logo sebenar dah ada nama universiti, jadi teks nama hanya untuk placeholder
    show_name = SHOW_UNI_NAME and not os.path.exists(LOGO_PATH)
    name_img = text_layer(UNI_NAME, f_name, TEXT + (255,), tracking=6) if show_name else None
    tag_img = text_layer(INTRO_TAGLINE, f_tag, ACCENT + (255,))
    ring_r = int(math.hypot(logo.width, logo.height) / 2) + 45

    # -------------------------------- INTRO
    def intro(t):
        c = bg.copy()
        particles.draw(c, t, prog(t, 0.6, 0.8))
        light_sweep(c, -900 + 2900 * ease_in_out(prog(t, 1.2, 1.1)), 1.0)

        draw_ring(c, W / 2, CY, ring_r, ease_out_cubic(prog(t, 0.15, 0.9)),
                  alpha=1 - 0.5 * prog(t, 1.4, 0.6))

        p = prog(t, 0.45, 0.75)
        s = ease_out_back(p) if p > 0 else 0
        breathe = 1 + 0.015 * math.sin(max(0, t - 1.2) * 3)
        glow_a = ease_out_cubic(prog(t, 0.9, 0.5)) * (0.75 + 0.25 * math.sin(t * 4))
        paste_center(c, glow, W / 2, CY, s * breathe, glow_a)
        paste_center(c, logo, W / 2, CY, s * breathe, clamp(p * 2))

        ty = CY + ring_r + 90
        tp = ease_out_cubic(prog(t, 1.2, 0.6))
        line_w = int(520 * ease_out_cubic(prog(t, 1.1, 0.6)))
        if line_w > 0:
            ImageDraw.Draw(c).rounded_rectangle(
                [W / 2 - line_w / 2, ty - 55, W / 2 + line_w / 2, ty - 49], 3, fill=ACCENT + (255,))
        if name_img:
            paste_center(c, name_img, W / 2, ty + 40 * (1 - tp), 1, tp)
        if tag_img:
            tp2 = ease_out_cubic(prog(t, 1.5, 0.6))
            ty2 = ty + (85 if name_img else 20)
            paste_center(c, tag_img, W / 2, ty2 + 40 * (1 - tp2), 1, tp2)

        fade(c, 1 - prog(t, 0, 0.25))                       # masuk dari hitam
        fade(c, ease_in_out(prog(t, INTRO_SEC - 0.45, 0.45)))  # keluar ke hitam
        return c

    render(os.path.join(HERE, "intro.mp4"), INTRO_SEC, intro,
           [("whoosh", 0.55, 0.9), ("chime", 0.95, 0.5, 880.0), ("chime", 1.25, 0.25, 1318.5)])

    # -------------------------------- OUTRO
    oy = int(H * 0.34)
    title_img = text_layer(OUTRO_TITLE, f_title, TEXT + (255,))
    line_img = text_layer(OUTRO_LINE, f_line, (210, 220, 240, 255))
    small_r = int(math.hypot(small_logo.width, small_logo.height) / 2) + 35

    def outro(t):
        c = bg.copy()
        particles.draw(c, t + 3, clamp(t / 0.6))

        p = prog(t, 0.1, 0.7)
        s = ease_out_back(p) if p > 0 else 0
        spin = ease_out_cubic(prog(t, 0.0, 1.0))
        draw_ring(c, W / 2, oy, small_r, spin, width=7, alpha=0.8)
        breathe = 1 + 0.015 * math.sin(t * 3)
        paste_center(c, small_glow, W / 2, oy, s * breathe, ease_out_cubic(prog(t, 0.5, 0.5)) * 0.8)
        paste_center(c, small_logo, W / 2, oy, s * breathe, clamp(p * 2))

        y = oy + small_r + 150
        for img, start, dy in [(title_img, 0.7, 0), (line_img, 0.9, 110)]:
            q = ease_out_cubic(prog(t, start, 0.6))
            paste_center(c, img, W / 2, y + dy + 50 * (1 - q), 1, q)

        if name_img:
            paste_center(c, name_img, W / 2, y + 260, 0.85, ease_out_cubic(prog(t, 1.3, 0.6)) * 0.7)

        fade(c, 1 - prog(t, 0, 0.3))
        fade(c, ease_in_out(prog(t, OUTRO_SEC - 0.6, 0.6)))
        return c

    render(os.path.join(HERE, "outro.mp4"), OUTRO_SEC, outro,
           [("whoosh", 0.35, 0.8), ("chime", 0.75, 0.45, 659.25), ("chime", 1.05, 0.4, 987.77)])

    print("Siap: intro.mp4 & outro.mp4")


if __name__ == "__main__":
    main()
