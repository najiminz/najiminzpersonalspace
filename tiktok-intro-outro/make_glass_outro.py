#!/usr/bin/env python3
"""
Outro TikTok gaya sama dengan intro kaca (terbalik):
bangunan UPTM + logo -> "Thank You / for watching!" -> kaca tertutup -> gelap.

Guna:  python3 make_glass_outro.py      ->  outro_glass.mp4
"""

import math
import os
import subprocess
import wave

import numpy as np
from PIL import Image, ImageFilter

import make_videos as mv
import make_glass_intro as gi
from make_videos import clamp, prog, ease_out_cubic, ease_in_out, ease_out_back

OUT = os.path.join(mv.HERE, "outro_glass.mp4")
W, H, FPS = mv.W, mv.H, mv.FPS
SECONDS = 5.0

TITLE = "Thank You"
SUBTITLE = "for watching!"
TITLE_COLOR = (22, 72, 155)      # biru logo UPTM
SUB_COLOR = (215, 30, 40)        # merah logo UPTM

# Masa (saat)
T_FADE_IN = (0.0, 0.45)
T_LOGO = (0.15, 0.8)
T_TITLE = (0.85, 0.6)
T_SUB = (1.1, 0.6)
T_GLINT = (1.9, 0.75)
T_CLOSE = (3.05, 1.0)            # kaca tertutup
T_DARK = (4.15, 0.85)            # jadi gelap


def styled_text(text, fnt, color):
    """Teks dengan garis luar putih + cahaya putih (sama gaya logo)."""
    core = mv.text_layer(text, fnt, color + (255,))
    pad = 70
    a = Image.new("L", (core.width + pad * 2, core.height + pad * 2), 0)
    a.paste(core.split()[3], (pad, pad))
    stroke = a.filter(ImageFilter.MaxFilter(11)).filter(ImageFilter.GaussianBlur(1.2))
    glow = a.filter(ImageFilter.MaxFilter(15)).filter(ImageFilter.GaussianBlur(28))
    out = Image.new("RGBA", a.size, (255, 255, 255, 0))
    out.putalpha(glow.point(lambda v: int(min(255, v * 1.5))))
    st = Image.new("RGBA", a.size, (255, 255, 255, 0))
    st.putalpha(stroke)
    out.alpha_composite(st)
    out.alpha_composite(core, (pad, pad))
    return out


def seam_light(t):
    """Kilat cahaya bila dua panel kaca bertemu di tengah."""
    a = math.exp(-((t - (T_CLOSE[0] + T_CLOSE[1])) / 0.18) ** 2)
    if a < 0.01:
        return None
    xs = gi.XS
    gx = np.exp(-((xs - W / 2) / 10) ** 2) * 240 + np.exp(-((xs - W / 2) / 110) ** 2) * 90
    gy = 0.55 + 0.45 * np.exp(-((gi.YS - H * 0.42) / (H * 0.35)) ** 2)
    return (gy[:, None] * gx[None, :] * a)[..., None]


def write_audio(path):
    sr = mv.SR
    n = int(sr * SECONDS)
    tr = np.zeros(n)
    t = np.arange(n) / sr

    mv.place(tr, mv.chime(2.4, 659.25), T_LOGO[0] + 0.3, 0.5)
    mv.place(tr, mv.chime(2.4, 987.77), T_TITLE[0] + 0.15, 0.35)
    mv.place(tr, mv.chime(1.6, 1975.5), T_GLINT[0] + 0.2, 0.12)
    mv.place(tr, mv.whoosh(1.4, 0.7), T_CLOSE[0] + 0.25, 1.0)

    rng = np.random.default_rng(8)
    close_t = T_CLOSE[0] + T_CLOSE[1]
    for _ in range(12):
        f = rng.uniform(2400, 5200)
        tt = np.arange(int(sr * 0.6)) / sr
        ping = np.sin(2 * np.pi * f * tt) * np.exp(-tt * 9) * np.minimum(1, tt / 0.002)
        mv.place(tr, ping, close_t + rng.uniform(-0.05, 0.5), rng.uniform(0.05, 0.12))

    hum = (np.sin(2 * np.pi * 55 * t) + 0.5 * np.sin(2 * np.pi * 82.5 * t)) * 0.25
    hum *= np.clip((t - close_t + 0.3) / 0.6, 0, 1)
    tr += hum

    f = int(sr * 0.6)
    tr[-f:] *= np.linspace(1, 0, f)
    tr = (tr / (np.abs(tr).max() or 1) * 0.8 * 32767).astype(np.int16)
    with wave.open(path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(tr.tobytes())


def main():
    big, scale = gi.load_building()
    vignette = gi.make_vignette()
    grain = gi.make_grain()
    logo_fx, logo, _ = gi.make_logo_card()
    logo_alpha = np.asarray(logo.split()[3]).astype(np.float32) / 255

    logo_cy = int(H * 0.36)
    title = styled_text(TITLE, mv.font(mv.FONT_BOLD, 150), TITLE_COLOR)
    sub = styled_text(SUBTITLE, mv.font(mv.FONT_SEMI, 72), SUB_COLOR)
    title_cy = int(H * 0.555)
    sub_cy = title_cy + 125

    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    haze = np.exp(-(((xx - W / 2) / 650) ** 2 + ((yy - H * 0.45) / 520) ** 2))[..., None]

    def frame(t):
        # 1) babak: bangunan + kabus putih + logo + teks
        img = gi.building_frame(big, scale, t, x_from=470, x_to=300, seconds=SECONDS)
        img = img + (255 - img) * (0.22 * haze * ease_out_cubic(prog(t, *T_LOGO)))
        img = img * vignette ** 0.4
        scene = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).convert("RGBA")

        lp = prog(t, *T_LOGO)
        if lp > 0:
            s = (0.82 + 0.18 * ease_out_back(lp, 1.4)) * (1 + 0.008 * math.sin(t * 2.5))
            mv.paste_center(scene, logo_fx, W / 2, logo_cy, s, clamp(ease_out_cubic(lp) * 1.6))
            g = prog(t, *T_GLINT)
            if 0 < g < 1:
                ch, cw = logo_alpha.shape
                y2, x2 = np.mgrid[0:ch, 0:cw].astype(np.float32)
                pos = -300 + (cw + 600) * ease_in_out(g)
                band = np.exp(-((x2 + (y2 - ch / 2) * 0.6 - pos) / 45) ** 2) * 0.55
                glint = Image.new("RGBA", (cw, ch), (255, 255, 255, 0))
                glint.putalpha(Image.fromarray((band * logo_alpha * 255).astype(np.uint8)))
                mv.paste_center(scene, glint, W / 2, logo_cy, s, 1.0)

        for img_t, cy, (st, du) in ((title, title_cy, T_TITLE), (sub, sub_cy, T_SUB)):
            q = ease_out_cubic(prog(t, st, du))
            if q > 0:
                mv.paste_center(scene, img_t, W / 2, cy + 50 * (1 - q), 1, q)

        img = np.asarray(scene.convert("RGB")).astype(np.float32)

        # 2) kaca tertutup dari tepi ke tengah
        close_p = ease_in_out(prog(t, *T_CLOSE))
        if close_p > 0:
            offset = (1 - close_p) * (W / 2 + 80)
            frost = gi.frosted(img) + grain
            mask, light = gi.glass_layers(offset, t, 1 - close_p)
            img = img * (1 - mask) + (frost + light * close_p) * mask
            sl = seam_light(t)
            if sl is not None:
                img = img + sl

        # 3) jadi gelap
        dark = ease_in_out(prog(t, *T_DARK))
        img = img * (1 - 0.95 * dark)

        canvas = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).convert("RGBA")
        mv.fade(canvas, 1 - ease_out_cubic(prog(t, *T_FADE_IN)))
        mv.fade(canvas, ease_in_out(prog(t, SECONDS - 0.25, 0.25)))
        return canvas

    wav = OUT + ".wav"
    write_audio(wav)
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
