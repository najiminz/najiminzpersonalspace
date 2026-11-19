#!/usr/bin/env python3
"""
Intro TikTok "kaca terbuka": mula gelap -> kaca kabur menyala -> kaca terbuka
macam pintu gelangsar -> nampak bangunan UPTM dengan logo di depan.

Guna:  python3 make_glass_intro.py      ->  intro_glass.mp4
Perlu: assets/building.jpg, logo.png (sama folder), Pillow, numpy, ffmpeg.
"""

import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import make_videos as mv
from make_videos import clamp, prog, ease_out_cubic, ease_in_out, ease_out_back

HERE = mv.HERE
BUILDING = os.path.join(HERE, "assets", "building.jpg")
OUT = os.path.join(HERE, "intro_glass.mp4")

W, H, FPS = mv.W, mv.H, mv.FPS
SECONDS = 5.0
NAVY = np.array([10, 24, 60], np.float32)

# Masa (saat)
T_GLASS_ON = (0.25, 1.1)    # kaca kabur muncul dari gelap
T_CRACK = (1.05, 0.45)      # cahaya di celah tengah
T_OPEN = (1.35, 1.15)       # kaca terbuka
T_LOGO = (2.05, 0.8)        # logo masuk
T_GLINT = (3.15, 0.75)      # kilauan atas logo
T_FADE_OUT = 0.4


# ---------------------------------------------------------------- aset
def load_building():
    img = Image.open(BUILDING).convert("RGB")
    scale = H / img.height * 1.12           # ruang lebih untuk pan & zoom
    big = img.resize((int(img.width * scale), int(img.height * scale)), Image.LANCZOS)
    big = big.filter(ImageFilter.UnsharpMask(radius=3, percent=70, threshold=2))
    # warna sedikit lebih "punchy"
    arr = np.asarray(big).astype(np.float32)
    arr = (arr - 128) * 1.06 + 128
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)), scale


def building_frame(big, scale, t, x_from=300, x_to=490, seconds=SECONDS):
    """Pan perlahan (x_from -> x_to, koordinat gambar asal) + zoom masuk sikit."""
    k = 1.0 - 0.06 * ease_in_out(t / seconds)
    cw, ch = W * k, H * k
    # pusat dalam koordinat gambar asal (1024x768)
    cx_src = x_from + (x_to - x_from) * ease_in_out(t / seconds)
    cx = cx_src * scale
    cy = big.height * 0.47
    cx = clamp(cx, cw / 2, big.width - cw / 2)
    cy = clamp(cy, ch / 2, big.height - ch / 2)
    box = (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2)
    return np.asarray(big.resize((W, H), Image.BICUBIC, box=box)).astype(np.float32)


def frosted(sharp):
    small = Image.fromarray(sharp.astype(np.uint8)).resize((W // 8, H // 8), Image.BOX)
    small = small.filter(ImageFilter.GaussianBlur(5))
    blur = np.asarray(small.resize((W, H), Image.BICUBIC)).astype(np.float32)
    return blur * 0.5 + NAVY * 0.5 + 12


def make_vignette():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((xx - W / 2) / (W * 0.75)) ** 2 + ((yy - H * 0.45) / (H * 0.7)) ** 2)
    return np.clip(1.08 - 0.55 * d ** 2, 0.35, 1.0)[..., None]


def make_grain(seed=3):
    rng = np.random.default_rng(seed)
    g = rng.normal(0, 1, (H // 2, W // 2)).astype(np.float32)
    g = np.asarray(Image.fromarray(((g * 20) + 128).clip(0, 255).astype(np.uint8))
                   .resize((W, H), Image.BILINEAR)).astype(np.float32) - 128
    return g[..., None] * 0.35


def make_logo_card():
    """Logo tanpa latar putih + garis luar putih + cahaya putih lembut."""
    src = Image.open(mv.LOGO_PATH).convert("RGB")
    up = 4
    big = src.resize((src.width * up, src.height * up), Image.LANCZOS)
    rgb = np.asarray(big).astype(np.float32)
    h, w = rgb.shape[:2]

    # putih -> telus ("color to alpha")
    alpha = np.clip((255 - rgb).max(axis=2) / 255 * 1.15, 0, 1)

    # heksagon biru & heksagon merah kecil: kekalkan putih di dalamnya
    keep = np.zeros((h, w), bool)
    blue = (rgb[..., 2] > 120) & (rgb[..., 0] < 110)
    red = (rgb[..., 0] > 150) & (rgb[..., 1] < 110)
    for mask, x_max, y_max in ((blue, 108 * up, h), (red, 135 * up, 36 * up)):
        sub = mask[:y_max, :x_max]
        for y in range(sub.shape[0]):
            xs = np.nonzero(sub[y])[0]
            if xs.size:
                keep[y, xs.min():xs.max() + 1] = True
    alpha = np.where(keep, 1.0, alpha)

    a = alpha[..., None]
    color = np.where(a > 0.01, (rgb - 255 * (1 - a)) / np.maximum(a, 1e-3), 255)
    color = np.where(keep[..., None], rgb, color)
    logo = Image.fromarray(np.clip(np.dstack([color, alpha * 255]), 0, 255).astype(np.uint8), "RGBA")

    target_w = 900
    logo = logo.resize((target_w, int(h * target_w / w)), Image.LANCZOS)
    logo = logo.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=1))

    pad = 140
    la = Image.new("L", (logo.width + pad * 2, logo.height + pad * 2), 0)
    la.paste(logo.split()[3], (pad, pad))

    stroke = la.filter(ImageFilter.MaxFilter(15)).filter(ImageFilter.GaussianBlur(1.5))
    glow = la.filter(ImageFilter.MaxFilter(21)).filter(ImageFilter.GaussianBlur(45))

    out = Image.new("RGBA", la.size, (255, 255, 255, 0))
    out.putalpha(glow.point(lambda v: int(min(255, v * 1.6))))
    st = Image.new("RGBA", la.size, (255, 255, 255, 0))
    st.putalpha(stroke)
    out.alpha_composite(st)
    out.alpha_composite(logo, (pad, pad))
    return out, logo, pad


# ---------------------------------------------------------------- efek kaca
XS = np.arange(W, dtype=np.float32)
YS = np.arange(H, dtype=np.float32)


def glass_layers(offset, t, open_p):
    """Pulangkan (mask panel kaca, lapisan cahaya tambahan) sebagai array."""
    half = W / 2
    left_edge = half - offset            # tepi dalam panel kiri
    right_edge = half + offset           # tepi dalam panel kanan
    mask_x = ((XS < left_edge) | (XS > right_edge)).astype(np.float32)
    mask = np.broadcast_to(mask_x[None, :, None], (H, W, 1))

    light = np.zeros((H, W), np.float32)

    # kilauan serong pada permukaan kaca, bergerak bersama panel
    for edge, sign in ((left_edge, -1), (right_edge, 1)):
        local = (XS[None, :] - edge) * sign      # jarak dari tepi dalam ke arah luar
        diag = local + (YS[:, None] - H * 0.5) * 0.35
        band = np.exp(-((diag - (260 + 120 * math.sin(t * 0.9))) / 70) ** 2) * 38
        band += np.exp(-((diag - 520) / 26) ** 2) * 22
        light += band * (local > 0)

    # garisan terang di tepi dalam setiap panel
    edge_glow = (np.exp(-((XS - left_edge) / 5) ** 2) + np.exp(-((XS - right_edge) / 5) ** 2)) * 150
    edge_glow += (np.exp(-((XS - left_edge) / 40) ** 2) + np.exp(-((XS - right_edge) / 40) ** 2)) * 40
    light += edge_glow[None, :] * (1 - 0.6 * open_p)

    return mask, light[..., None]


def crack_light(t):
    """Cahaya keluar dari celah tengah sebelum kaca terbuka."""
    a = ease_out_cubic(prog(t, *T_CRACK)) * (1 - ease_in_out(prog(t, T_OPEN[0] + 0.2, 0.6)))
    if a <= 0:
        return None
    gx = np.exp(-((XS - W / 2) / 10) ** 2) * 230 + np.exp(-((XS - W / 2) / 90) ** 2) * 70
    gy = 0.55 + 0.45 * np.exp(-((YS - H * 0.45) / (H * 0.35)) ** 2)
    return (gy[:, None] * gx[None, :] * a)[..., None]


# ---------------------------------------------------------------- audio
def write_audio(path):
    sr = mv.SR
    n = int(sr * SECONDS)
    tr = np.zeros(n)
    t = np.arange(n) / sr

    # dengung rendah gelap di awal
    hum = (np.sin(2 * np.pi * 55 * t) + 0.5 * np.sin(2 * np.pi * 82.5 * t))
    hum *= np.clip(t / 0.8, 0, 1) * np.clip((2.2 - t) / 0.8, 0, 1) * 0.25
    tr += hum

    # kilauan kaca (ping frekuensi tinggi) bila kaca menyala
    rng = np.random.default_rng(5)
    for _ in range(14):
        at = rng.uniform(0.5, 1.3)
        f = rng.uniform(2400, 5200)
        dur = 0.6
        tt = np.arange(int(sr * dur)) / sr
        ping = np.sin(2 * np.pi * f * tt) * np.exp(-tt * 9) * np.minimum(1, tt / 0.002)
        mv.place(tr, ping, at, rng.uniform(0.05, 0.12))

    mv.place(tr, mv.whoosh(1.4, 0.7), T_OPEN[0] - 0.35, 1.0)     # kaca terbuka
    mv.place(tr, mv.chime(2.4, 659.25), T_LOGO[0] + 0.25, 0.5)   # logo masuk
    mv.place(tr, mv.chime(2.4, 987.77), T_LOGO[0] + 0.45, 0.32)
    mv.place(tr, mv.chime(1.6, 1975.5), T_GLINT[0] + 0.2, 0.12)  # kilauan

    f = int(sr * 0.4)
    tr[-f:] *= np.linspace(1, 0, f)
    tr = (tr / (np.abs(tr).max() or 1) * 0.8 * 32767).astype(np.int16)
    import wave
    with wave.open(path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(tr.tobytes())


# ---------------------------------------------------------------- render
def main():
    big, scale = load_building()
    vignette = make_vignette()
    grain = make_grain()
    card_with_shadow, card, card_pad = make_logo_card()
    card_alpha = np.asarray(card.split()[3]).astype(np.float32) / 255
    logo_cy = int(H * 0.40)

    # kabus putih lembut di belakang logo (macam contoh) supaya logo jelas
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    behind = np.exp(-(((xx - W / 2) / 650) ** 2 + ((yy - logo_cy) / 380) ** 2))[..., None]

    def frame(t):
        sharp = building_frame(big, scale, t)
        open_p = ease_in_out(prog(t, *T_OPEN))
        offset = open_p * (W / 2 + 80)

        frost = frosted(sharp) + grain
        mask, light = glass_layers(offset, t, open_p)
        glass_on = ease_out_cubic(prog(t, *T_GLASS_ON))
        img = sharp * (1 - mask) + (frost + light * glass_on) * mask

        cl = crack_light(t)
        if cl is not None:
            img = img + cl * mask

        logo_p = ease_out_cubic(prog(t, *T_LOGO))
        img = img + (255 - img) * (0.22 * behind * logo_p)
        img = img * (1 - (1 - vignette) * (1 - 0.6 * open_p))

        # kecerahan: mula gelap
        bright = 0.08 + 0.92 * glass_on
        img = img * bright

        canvas = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).convert("RGBA")

        # logo
        if logo_p > 0:
            s = 0.82 + 0.18 * ease_out_back(prog(t, *T_LOGO), 1.4)
            s *= 1 + 0.008 * math.sin(max(0, t - 2.8) * 2.5)
            mv.paste_center(canvas, card_with_shadow, W / 2, logo_cy, s, clamp(logo_p * 1.6))

            g = prog(t, *T_GLINT)
            if 0 < g < 1:
                # jalur kilauan serong dalam kad logo
                ch, cw = card_alpha.shape
                yy2, xx2 = np.mgrid[0:ch, 0:cw].astype(np.float32)
                pos = -300 + (cw + 600) * ease_in_out(g)
                band = np.exp(-((xx2 + (yy2 - ch / 2) * 0.6 - pos) / 45) ** 2) * 0.55
                glint = Image.new("RGBA", (cw, ch), (255, 255, 255, 0))
                glint.putalpha(Image.fromarray((band * card_alpha * 255).astype(np.uint8)))
                mv.paste_center(canvas, glint, W / 2, logo_cy, s, 1.0)

        mv.fade(canvas, ease_in_out(prog(t, SECONDS - T_FADE_OUT, T_FADE_OUT)))
        return canvas

    # guna render() dari make_videos tetapi dengan audio sendiri
    wav = OUT + ".wav"
    write_audio(wav)
    import subprocess
    cmd = ["ffmpeg", "-y", "-loglevel", "error",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-i", wav,
           "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", OUT]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    total = int(SECONDS * FPS)
    for i in range(total):
        proc.stdin.write(frame(i / FPS).convert("RGB").tobytes())
    proc.stdin.close()
    proc.wait()
    os.remove(wav)
    if proc.returncode != 0:
        raise SystemExit("ffmpeg gagal")
    print(f"Siap: {os.path.basename(OUT)} ({total} frame)")


if __name__ == "__main__":
    main()
