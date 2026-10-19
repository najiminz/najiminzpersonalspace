"""Front cover ("Kulit Hadapan") for the Siri Kenderaan coloring book.

Bright, full-color cartoon style: bubbly multicolor title, wooden sign, a bear
mascot holding a coloring book, a bird perched on a school bus and an open
book at the bottom showing a colored and an uncolored vehicle.
"""
import math
import os

from PIL import ImageFont

import vehicles as V
from draw import Pen, blob_d, star_d

W, H = 905, 1280
OUTLINE = "#4a2c17"
NAVY = "#1c2a5a"


def p(d, fill, stroke=OUTLINE, w=4, extra=""):
    return (f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{w}" stroke-linejoin="round" '
            f'stroke-linecap="round" {extra}/>')


def ell(cx, cy, rx, ry, fill, stroke=OUTLINE, w=4, rot=0, extra=""):
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="{w}" '
            f'transform="rotate({rot} {cx} {cy})" {extra}/>')


def vehicle(fn, x, y, s, colored=True, prefix="v"):
    pen = Pen(colored, prefix)
    pen.k = 1 / s
    svg, _ = fn(pen)
    return f'<g transform="translate({x},{y}) scale({s})">{svg}</g>'


# ---------------------------------------------------------------- background

def background():
    out = '<rect width="905" height="1280" fill="url(#sky)"/>'
    for k in range(14):
        a = 2 * math.pi * k / 14
        out += (f'<path d="M{805 + 70 * math.cos(a - 0.09):.1f},{120 + 70 * math.sin(a - 0.09):.1f} '
                f'L{805 + 112 * math.cos(a):.1f},{120 + 112 * math.sin(a):.1f} '
                f'L{805 + 70 * math.cos(a + 0.09):.1f},{120 + 70 * math.sin(a + 0.09):.1f} Z" fill="#ffd54f"/>')
    out += '<circle cx="805" cy="120" r="62" fill="url(#sun)" stroke="#f9a825" stroke-width="4"/>'
    for x, y, s in ((300, 40, 1.0), (560, 150, 0.7), (720, 300, 0.8), (40, 470, 0.6)):
        out += (f'<g transform="translate({x},{y}) scale({s})">'
                + p(blob_d(90, 40, 85, 34, 9, int(x + y), flat_bottom=True), "#ffffff", stroke="#9fd3ef", w=3)
                + "</g>")
    # mountains + hills
    out += p("M-20,700 L120,560 L220,650 L340,540 L470,660 L600,560 L740,650 L860,570 L940,640 L940,760 L-20,760 Z",
             "#8fc6e8", stroke="none")
    out += p("M-20,720 Q160,610 360,690 Q560,620 760,680 Q860,650 940,690 L940,820 L-20,820 Z", "url(#hill1)",
             stroke="#4e9a2c", w=3)
    out += p("M-20,770 Q200,700 450,750 Q700,700 940,750 L940,830 L-20,830 Z", "url(#hill2)", stroke="#4e9a2c", w=3)
    # fence
    out += '<rect x="-10" y="760" width="925" height="10" rx="4" fill="#d9a066" stroke="#8a5a2f" stroke-width="2.5"/>'
    out += '<rect x="-10" y="782" width="925" height="10" rx="4" fill="#d9a066" stroke="#8a5a2f" stroke-width="2.5"/>'
    for x in range(10, 905, 44):
        out += p(f"M{x},810 L{x},752 L{x + 7},744 L{x + 14},752 L{x + 14},810 Z", "#e8b47a", stroke="#8a5a2f", w=2.5)
    # road
    out += '<rect x="-10" y="806" width="925" height="80" fill="#8e98a4" stroke="#5f6770" stroke-width="3"/>'
    for x in range(-20, 905, 120):
        out += f'<rect x="{x}" y="842" width="64" height="8" rx="4" fill="#ffffff"/>'
    # grass
    out += p("M-20,880 Q200,860 450,876 Q700,862 940,880 L940,1300 L-20,1300 Z", "url(#grass)", stroke="#4e9a2c", w=3)
    return out


def tree():
    out = p("M40,820 Q60,640 30,470 Q20,400 -20,360 L-20,820 Z", "#9c6b3c")
    out += p("M110,820 Q90,640 120,520 Q140,440 200,400 L170,380 Q100,420 70,470 Q60,400 40,360 L10,370 "
             "Q40,430 40,520 Q50,660 30,820 Z", "#a8743f")
    out += p("M70,600 Q76,640 70,700 M90,520 Q100,560 92,600", "none", stroke="#6d4421", w=3)
    crown = ""
    for cx, cy, rx, ry, c in ((60, 120, 170, 140, "#3f9a2e"), (210, 60, 140, 100, "#4caf50"),
                              (40, 300, 140, 110, "#43a047"), (190, 250, 120, 90, "#5cbf4a"),
                              (100, 210, 110, 90, "#66c653")):
        crown += p(blob_d(cx, cy, rx, ry, 12, cx + cy), c, stroke="#2e7d32", w=3.5)
    for x, y in ((40, 90), (150, 160), (230, 60), (80, 270), (190, 250), (20, 200)):
        crown += ell(x, y, 16, 9, "#8ad46f", stroke="none", rot=-30)
    return out + crown


def flower(x, y, s=1.0, petal="#ffffff", center="#fdd835"):
    out = ""
    for k in range(6):
        a = 2 * math.pi * k / 6
        out += ell(x + 10 * s * math.cos(a), y + 10 * s * math.sin(a), 8 * s, 5.5 * s, petal,
                   stroke="#c9c9c9", w=1.5, rot=math.degrees(a))
    return out + f'<circle cx="{x}" cy="{y}" r="{6 * s}" fill="{center}" stroke="#f9a825" stroke-width="1.5"/>'


def butterfly(x, y, s, c1, c2, rot=0):
    g = (ell(-14, -10, 16, 20, c1, stroke=OUTLINE, w=2.5, rot=-25) + ell(14, -10, 16, 20, c1, stroke=OUTLINE, w=2.5, rot=25)
         + ell(-10, 12, 10, 12, c2, stroke=OUTLINE, w=2.5, rot=20) + ell(10, 12, 10, 12, c2, stroke=OUTLINE, w=2.5, rot=-20)
         + ell(0, 0, 4, 16, "#4a2c17", stroke="none")
         + p("M-2,-14 Q-8,-28 -14,-30 M2,-14 Q8,-28 14,-30", "none", w=2))
    return f'<g transform="translate({x},{y}) rotate({rot}) scale({s})">{g}</g>'


# ---------------------------------------------------------------- title + sign

LETTER_COLORS = ["e8402f", "ff9800", "fdd835", "43a047", "1e88e5", "8e24aa", "ec407a", "00acc1", "e8402f"]


def bubbly(word, base_y=318, max_w=820, font_size=150, colors=LETTER_COLORS):
    """Big multicolor bubble letters with a white rim, navy outline, shadow and stitching."""
    font = ImageFont.truetype(os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts", "Fredoka-Bold.ttf"),
                              font_size)
    adv = [font.getlength(ch) for ch in word]
    gap = -4
    total = sum(adv) + gap * (len(word) - 1)
    scale = min(1.0, max_w / total)
    fs = font_size * scale
    x = (W - total * scale) / 2
    out = ""
    for i, ch in enumerate(word):
        cx = x + adv[i] * scale / 2
        dy = -10 if i % 2 else 6
        rot = -5 if i % 2 else 4
        base = base_y + dy
        attrs = (f'x="{cx:.1f}" y="{base}" text-anchor="middle" font-family="Fredoka" font-weight="700" '
                 f'font-size="{fs:.1f}" transform="rotate({rot} {cx:.1f} {base - fs * 0.35:.1f})"')
        out += f'<text {attrs} fill="{NAVY}" stroke="{NAVY}" stroke-width="22" stroke-linejoin="round" dx="4" dy="8">{ch}</text>'
        out += f'<text {attrs} fill="#fff" stroke="#fff" stroke-width="20" stroke-linejoin="round">{ch}</text>'
        out += f'<text {attrs} fill="url(#g{colors[i % len(colors)]})" stroke="{NAVY}" stroke-width="5" stroke-linejoin="round">{ch}</text>'
        out += (f'<text {attrs} fill="none" stroke="#ffffff" stroke-opacity="0.85" stroke-width="2.2" '
                f'stroke-dasharray="7 6" transform="rotate({rot} {cx:.1f} {base - fs * 0.35:.1f}) '
                f'translate({cx:.1f} {base - fs * 0.35:.1f}) scale(0.88) translate({-cx:.1f} {-(base - fs * 0.35):.1f})">'
                f'{ch}</text>')
        x += adv[i] * scale + gap * scale
    return out


def ribbon(label, y=150):
    out = p(f"M330,{y} L575,{y} L560,{y + 22} L575,{y + 44} L330,{y + 44} L345,{y + 22} Z", "#e8402f", stroke=NAVY, w=4)
    out += (f'<text x="452" y="{y + 34}" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="30" '
            f'letter-spacing="3" fill="#fff">{label}</text>')
    return out


def title():
    return bubbly("KENDERAAN") + ribbon("SIRI")


def sign():
    board = "M110,368 Q300,352 452,360 Q620,352 800,368 L792,520 Q620,532 452,526 Q290,534 116,520 Z"
    out = p("M180,368 L170,340 M730,368 L740,340", "none", stroke="#8a5a2f", w=6)
    out += p(board, "url(#wood)", stroke="#6b3e1a", w=5)
    for d in ("M140,404 Q300,396 420,402", "M480,486 Q640,478 770,488", "M150,500 Q240,494 330,500",
              "M560,392 Q660,386 760,394"):
        out += p(d, "none", stroke="#b5733a", w=2.5)
    for x, y in ((130, 386), (780, 386), (134, 504), (776, 504)):
        out += f'<circle cx="{x}" cy="{y}" r="6" fill="#8d6e63" stroke="#4e342e" stroke-width="2"/>'
    out += (f'<text x="452" y="450" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="74" '
            f'fill="{NAVY}" stroke="#ffffff" stroke-width="10" stroke-linejoin="round" paint-order="stroke">'
            f'Buku Mewarna</text>')
    out += (f'<text x="452" y="503" text-anchor="middle" font-family="Fredoka" font-weight="600" font-size="40" '
            f'fill="#4a2c17">untuk Kanak-kanak</text>')
    for x in (232, 672):
        out += p(f"M{x},496 C{x - 20},480 {x - 14},466 {x},476 C{x + 14},466 {x + 20},480 {x},496 Z", "#ec407a",
                 stroke="#ad1457", w=2.5)
    return out


def badge():
    out = p(star_d(812, 552, 82, 66, 18), "#fdd835", stroke=NAVY, w=4, extra='transform="rotate(10 812 552)"')
    out += f'<circle cx="812" cy="552" r="58" fill="#e8402f" stroke="#ffffff" stroke-width="4"/>'
    out += (f'<g transform="rotate(10 812 552)"><text x="812" y="562" text-anchor="middle" font-family="Fredoka" '
            f'font-weight="700" font-size="56" fill="#fff">30</text>'
            f'<text x="812" y="590" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="20" '
            f'fill="#fff">GAMBAR</text></g>')
    return out


# ---------------------------------------------------------------- characters

def bear(cx=290):
    fur, light, dark = "#b07240", "#f3c9a0", OUTLINE
    out = ell(cx, 850, 150, 140, "url(#fur)")
    out += ell(cx, 870, 92, 88, light, stroke="none")
    # waving arm
    out += ell(cx - 165, 720, 42, 82, "url(#fur)", rot=-28)
    out += f'<circle cx="{cx - 200}" cy="648" r="48" fill="url(#fur)" stroke="{dark}" stroke-width="4"/>'
    out += ell(cx - 200, 656, 26, 22, light, stroke="none")
    for dx, dy in ((-22, -22), (0, -32), (22, -22)):
        out += ell(cx - 200 + dx, 648 + dy, 9, 8, light, stroke="none")
    # head
    for ex in (-108, 108):
        out += f'<circle cx="{cx + ex}" cy="548" r="46" fill="url(#fur)" stroke="{dark}" stroke-width="4"/>'
        out += f'<circle cx="{cx + ex}" cy="552" r="25" fill="#f4a7a0"/>'
    out += f'<circle cx="{cx}" cy="640" r="128" fill="url(#fur)" stroke="{dark}" stroke-width="4"/>'
    out += p(f"M{cx - 30},516 L{cx - 18},498 L{cx - 6},516 L{cx + 6},494 L{cx + 18},516 L{cx + 30},500 L{cx + 36},520",
             "url(#fur)", stroke=dark, w=3.5)
    out += ell(cx, 690, 64, 48, light, stroke=dark, w=3)
    for ex in (-50, 50):
        out += ell(cx + ex, 622, 20, 26, "#2b1a10", stroke="none")
        out += f'<circle cx="{cx + ex + 7}" cy="612" r="8" fill="#fff"/><circle cx="{cx + ex - 6}" cy="630" r="4" fill="#fff"/>'
        out += p(f"M{cx + ex - 18},584 Q{cx + ex},572 {cx + ex + 18},584", "none", stroke=dark, w=3.5)
        out += ell(cx + ex * 1.6, 680, 22, 13, "#ff8a80", stroke="none", extra='opacity="0.7"')
    out += ell(cx, 670, 22, 15, "#2b1a10", stroke="none")
    out += ell(cx - 6, 665, 7, 4, "#ffffff", stroke="none", extra='opacity="0.8"')
    out += p(f"M{cx - 34},696 Q{cx},740 {cx + 34},696 Q{cx},708 {cx - 34},696 Z", "#7a2e1c", stroke=dark, w=3)
    out += p(f"M{cx - 16},716 Q{cx},732 {cx + 16},716 Q{cx},708 {cx - 16},716 Z", "#ff7a8a", stroke="none")
    # the book bear is holding
    out += p(f"M{cx - 60},770 L{cx + 140},748 L{cx + 150},920 L{cx - 50},944 Z", "url(#cover)", stroke=NAVY, w=4)
    out += p(f"M{cx - 60},770 L{cx - 76},780 L{cx - 66},952 L{cx - 50},944 Z", "#0d47a1", stroke=NAVY, w=4)
    out += (f'<g transform="rotate(-6 {cx + 45} 845)">'
            f'<text x="{cx + 45}" y="808" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="30" '
            f'fill="#fdd835" stroke="{NAVY}" stroke-width="5" paint-order="stroke">WARNA!</text>'
            + vehicle(V.kereta, cx - 25, 900, 0.21, prefix="bk") + "</g>")
    out += p(blob_d(cx + 150, 880, 40, 34, 7, 3), "url(#fur)", stroke=dark, w=4)
    out += p(blob_d(cx - 72, 890, 36, 32, 7, 4), "url(#fur)", stroke=dark, w=4)
    # feet
    for fx, rot in ((cx - 112, 18), (cx + 112, -18)):
        out += ell(fx, 960, 72, 56, "url(#fur)", rot=rot)
        out += ell(fx, 966, 36, 30, light, stroke="none", rot=rot)
        for k in (-1, 0, 1):
            out += ell(fx + k * 24, 926 + abs(k) * 6, 10, 9, light, stroke="none")
    return out


def bird(x, y):
    g = p("M38,8 L78,-6 L72,10 L84,16 L40,22 Z", "#1e63c9", stroke=NAVY, w=3)
    g += ell(0, 0, 50, 42, "#3f8ee6", stroke=NAVY, w=3.5)
    g += ell(-6, 12, 32, 26, "#fde26a", stroke="none")
    g += f'<circle cx="-26" cy="-44" r="36" fill="#3f8ee6" stroke="{NAVY}" stroke-width="3.5"/>'
    g += p("M-30,-78 Q-40,-96 -26,-100 Q-24,-88 -16,-80", "#3f8ee6", stroke=NAVY, w=3)
    g += p("M4,-16 Q22,-92 92,-112 Q82,-90 92,-80 Q70,-74 76,-58 Q54,-52 54,-36 Q34,-22 20,4 Z", "#ffffff", stroke=NAVY, w=3)
    g += p("M16,-16 Q32,-82 84,-102 Q76,-86 84,-78 Q64,-72 68,-58 Q48,-52 48,-38 Q32,-26 22,-8 Z", "#64b5f6", stroke="none")
    for ex in (-40, -14):
        g += ell(ex, -50, 10, 13, "#ffffff", stroke=NAVY, w=2.5)
        g += f'<circle cx="{ex + 2}" cy="-48" r="6" fill="#1b1b1b"/><circle cx="{ex + 4}" cy="-51" r="2.2" fill="#fff"/>'
    g += p("M-58,-36 L-84,-28 L-58,-22 Z", "#ff9800", stroke="#e65100", w=2.5)
    g += p("M-60,-29 L-80,-28", "none", stroke="#e65100", w=2)
    g += p("M-10,40 L-12,54 M10,40 L12,54", "none", stroke="#e65100", w=4)
    return f'<g transform="translate({x},{y})">{g}</g>'


# ---------------------------------------------------------------- foreground props

def crayon_bucket(x, y):
    out = ""
    for i, (c, dx, h, rot) in enumerate((("#e53935", 14, 120, -14), ("#fdd835", 36, 134, -5),
                                         ("#43a047", 58, 128, 4), ("#1e88e5", 80, 118, 14))):
        out += (f'<g transform="rotate({rot} {x + dx} {y})">'
                + p(f"M{x + dx - 10},{y} L{x + dx - 10},{y - h + 20} L{x + dx},{y - h} L{x + dx + 10},{y - h + 20} "
                    f"L{x + dx + 10},{y} Z", c, stroke=NAVY, w=2.5)
                + f'<rect x="{x + dx - 10}" y="{y - h + 40}" width="20" height="10" fill="#fff" opacity="0.6"/></g>')
    out += p(f"M{x - 12},{y - 10} L{x + 108},{y - 10} L{x + 96},{y + 104} L{x},{y + 104} Z", "#1e88e5", stroke=NAVY, w=3.5)
    out += f'<rect x="{x - 16}" y="{y - 18}" width="128" height="16" rx="6" fill="#42a5f5" stroke="{NAVY}" stroke-width="3"/>'
    for dx, dy in ((14, 20), (50, 14), (84, 22), (30, 56), (68, 52), (20, 88), (56, 86), (88, 84)):
        out += f'<circle cx="{x + dx}" cy="{y + dy}" r="6" fill="#ffffff" opacity="0.9"/>'
    return out


def open_book():
    out = p("M50,1012 Q250,990 452,1006 Q660,990 860,1012 L872,1250 Q660,1232 452,1250 Q250,1232 36,1250 Z",
            "#1e63c9", stroke=NAVY, w=4)
    left = "M66,1000 Q260,982 452,996 L452,1232 Q260,1216 56,1234 Z"
    right = "M452,996 Q650,982 842,1000 L852,1234 Q650,1216 452,1232 Z"
    out += p(left, "#ffffff", stroke="#9e9e9e", w=3) + p(right, "#ffffff", stroke="#9e9e9e", w=3)
    out += p("M452,996 L452,1232", "none", stroke="#bdbdbd", w=3)
    for d in ("M80,1030 Q260,1014 440,1026", "M466,1026 Q650,1014 830,1030"):
        out += p(d, "none", stroke="#e0e0e0", w=2)
    out += (f'<text x="100" y="1052" font-family="Fredoka" font-weight="700" font-size="34" fill="#e8402f">Kk</text>'
            f'<text x="160" y="1052" font-family="Fredoka" font-weight="600" font-size="28" fill="{NAVY}">Kereta</text>')
    out += (f'<text x="486" y="1052" font-family="Fredoka" font-weight="700" font-size="34" fill="#1e88e5">Bb</text>'
            f'<text x="546" y="1052" font-family="Fredoka" font-weight="600" font-size="28" fill="{NAVY}">Bas</text>')
    out += vehicle(V.kereta, 120, 1206, 0.46, colored=True, prefix="bkL")
    out += vehicle(V.bas_sekolah, 510, 1210, 0.33, colored=False, prefix="bkR")
    # a crayon lying on the right page
    out += (f'<g transform="rotate(-24 760 1120)">'
            + p("M690,1110 L800,1110 L826,1120 L800,1130 L690,1130 Z", "#fb8c00", stroke=NAVY, w=2.5)
            + '<rect x="704" y="1110" width="14" height="20" fill="#fff" opacity="0.6"/></g>')
    return out


def defs():
    grads = ""
    for c in ("e8402f", "ff9800", "fdd835", "43a047", "1e88e5", "8e24aa", "ec407a", "00acc1"):
        r, g, b = (int(c[i:i + 2], 16) for i in (0, 2, 4))
        light = "#%02x%02x%02x" % tuple(min(255, int(v + (255 - v) * 0.45)) for v in (r, g, b))
        grads += (f'<linearGradient id="g{c}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{light}"/>'
                  f'<stop offset="0.55" stop-color="#{c}"/><stop offset="1" stop-color="#{c}"/></linearGradient>')
    return ("<defs>" + grads +
            '<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3fb4f0"/>'
            '<stop offset="0.6" stop-color="#9fdcfa"/><stop offset="1" stop-color="#d9f3ff"/></linearGradient>'
            '<radialGradient id="sun" cx="0.4" cy="0.4" r="0.7"><stop offset="0" stop-color="#fff59d"/>'
            '<stop offset="1" stop-color="#fdd835"/></radialGradient>'
            '<linearGradient id="hill1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8bd16a"/>'
            '<stop offset="1" stop-color="#5fae3f"/></linearGradient>'
            '<linearGradient id="hill2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7cc95a"/>'
            '<stop offset="1" stop-color="#4f9f33"/></linearGradient>'
            '<linearGradient id="grass" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8fd36b"/>'
            '<stop offset="1" stop-color="#4c9c30"/></linearGradient>'
            '<linearGradient id="wood" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f7c483"/>'
            '<stop offset="1" stop-color="#d48d47"/></linearGradient>'
            '<radialGradient id="fur" cx="0.4" cy="0.35" r="0.8"><stop offset="0" stop-color="#cf9058"/>'
            '<stop offset="1" stop-color="#9a5f30"/></radialGradient>'
            '<linearGradient id="cover" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#42a5f5"/>'
            '<stop offset="1" stop-color="#1565c0"/></linearGradient>'
            "</defs>")


def cover_svg(px_w=2480, px_h=3508):
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{px_w}" height="{px_h}" viewBox="0 0 {W} {H}" '
           f'preserveAspectRatio="none">', defs(), background()]
    out.append(vehicle(V.helikopter, 360, 90, 0.17, prefix="heli"))
    out.append(vehicle(V.belon_udara, 640, 26, 0.13, prefix="bal"))
    out.append(tree())
    out.append(butterfly(70, 520, 1.0, "#ff9800", "#fdd835", rot=-15))
    out.append(butterfly(850, 740, 0.9, "#ec407a", "#f8bbd0", rot=12))
    out.append(vehicle(V.bas_sekolah, 520, 884, 0.4, prefix="bus"))
    out.append(bird(712, 666))
    for x, y, s in ((470, 920, 1.0), (560, 960, 0.8), (640, 930, 1.1), (760, 960, 0.9), (850, 920, 1.0),
                    (30, 1110, 1.0), (880, 1110, 1.1), (20, 1240, 0.9), (885, 1250, 0.9), (720, 990, 0.7)):
        out.append(flower(x, y, s))
    for x, y, s in ((520, 990, 0.8), (800, 990, 0.9)):
        out.append(flower(x, y, s, petal="#f8bbd0", center="#ff9800"))
    out.append(bear())
    out.append(crayon_bucket(28, 900))
    out.append(open_book())
    out.append(title())
    out.append(sign())
    out.append(badge())
    out.append("</svg>")
    return "\n".join(out)
