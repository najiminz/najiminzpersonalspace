"""Page layouts and the page list for Siri 10: ABC, Nombor dan Bentuk.

Three kinds of page, all in the shared template frame:
- huruf:  big hollow "Aa" + one object + the word, e.g. "A untuk Ayam"
- nombor: big hollow numeral + the number word + that many objects to colour
- bentuk: the shape with a friendly face, two dashed copies to trace, and an
          everyday object of that shape
"""
import os

from PIL import ImageFont

import objek as O
from characters import face
from draw import INK, W, star_d

FONT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "siri-kenderaan", "fonts", "Fredoka-Bold.ttf")
PALETTE = ["#e53935", "#1e88e5", "#43a047", "#fb8c00", "#8e24aa", "#00acc1", "#ec407a", "#fdd835"]


def text_width(s, size):
    return ImageFont.truetype(FONT, size).getlength(s)


def hollow(pen, x, y, s, size, color, anchor="start", w=4.6):
    """Outline lettering for colouring in (solid colour on the reference picture).

    The font's glyphs are built from overlapping pieces, so a plain stroke would show
    lines inside the letters. Instead a fat outline is drawn first and the fill on top.
    """
    attrs = (f'x="{x:.1f}" y="{y:.1f}" font-family="Fredoka" font-weight="700" font-size="{size:.1f}" '
             f'text-anchor="{anchor}"')
    return (f'<text {attrs} fill="{INK}" stroke="{INK}" stroke-width="{pen.sw(w) * 2:.2f}" '
            f'stroke-linejoin="round">{s}</text><text {attrs} fill="{pen.f(color)}">{s}</text>')


def backdrop(color):
    def scene(pen):
        return f'<rect width="{W}" height="1280" fill="{color}"/>' if pen.colored else ""
    return scene


def page(title, subject, bg, ref=(22, 330, 900)):
    return (title, lambda pen: (subject(pen), W), lambda pen: (bg(pen), ""), dict(x0=0, y=0, ref=ref))


# ---------------------------------------------------------------- huruf

# (letter, word, drawing, centre of the drawing in its own coordinates + size tweak)
WORDS = [
    ("A", "Ayam", O.ayam, {}), ("B", "Bola", O.bola, {}), ("C", "Cawan", O.cawan, {}),
    ("D", "Durian", O.durian, {}), ("E", "Epal", O.epal, {}), ("F", "Feri", O.feri, {}),
    ("G", "Gajah", O.gajah, {}), ("H", "Harimau", O.harimau, {}), ("I", "Ikan", O.ikan, {}),
    ("J", "Jam", O.jam, {}), ("K", "Kucing", O.kucing, {}), ("L", "Lebah", O.lebah, {}),
    ("M", "Matahari", O.matahari, {}), ("N", "Nanas", O.nanas, {}), ("O", "Oren", O.oren, {}),
    ("P", "Payung", O.payung, dict(dx=20, dy=-80, s=0.78)), ("Q", "Quran", O.quran, {}),
    ("R", "Rama-rama", O.rama_rama, {}), ("S", "Siput", O.siput, {}), ("T", "Tembikai", O.tembikai, {}),
    ("U", "Ular", O.ular, {}), ("V", "Van", O.van, dict(dy=40, s=1.15)), ("W", "Wau", O.wau, dict(dy=-43)),
    ("X", "Xilofon", O.xilofon, {}), ("Y", "Yo-yo", O.yoyo, dict(dx=20, dy=45, s=0.9)),
    ("Z", "Zirafah", O.zirafah, dict(dx=-40, dy=-50, s=0.95)),
]
# Two letters share a page: (baseline of "Aa", baseline of the word, centre of the drawing)
HALVES = [(420, 570, (640, 580)), (1000, 1150, (640, 1010))]


def huruf(i, first, second):
    def half(pen, k, letter, word, fn, tweak):
        base, word_base, (cx, cy) = HALVES[k]
        pair = letter + letter.lower()
        size = min(230, 230 * 360 / text_width(pair, 230))
        out = hollow(pen, 60, base, pair, size, PALETTE[(2 * i + k) % len(PALETTE)], w=5)
        wsize = min(80, 80 * 380 / text_width(word, 80))
        out += hollow(pen, 64, word_base, word, wsize, PALETTE[(2 * i + k + 3) % len(PALETTE)])
        s = 0.92 * tweak.get("s", 1.0)
        return out + O.place(pen, fn, cx - tweak.get("dx", 0) * s, cy - tweak.get("dy", 0) * s, s)

    def subject(pen):
        out = half(pen, 0, *first)
        out += (f'<line x1="50" y1="748" x2="855" y2="748" stroke="{INK}" stroke-width="{pen.sw(2.4)}" '
                f'stroke-dasharray="{pen.sw(12)} {pen.sw(10)}" stroke-linecap="round"/>')
        return out + half(pen, 1, *second)
    return page(f"Huruf {first[0]} dan {second[0]}", subject, backdrop("#fff8e1"), ref=(-100, 150, 1110))


# ---------------------------------------------------------------- nombor

NUMBERS = [
    (1, "satu", O.gajah), (2, "dua", O.ikan), (3, "tiga", O.epal), (4, "empat", O.bola),
    (5, "lima", O.belon), (6, "enam", O.bunga), (7, "tujuh", O.bintang), (8, "lapan", O.oren),
    (9, "sembilan", O.siput), (10, "sepuluh", O.kereta),
]
SIZE = {O.gajah: 0.9, O.kereta: 1.1}  # objects whose box is not the usual 320 x 320
ROWS = {1: [1], 2: [2], 3: [3], 4: [2, 2], 5: [3, 2], 6: [3, 3], 7: [4, 3], 8: [4, 4], 9: [3, 3, 3], 10: [4, 3, 3]}
BALLOONS = ["#e53935", "#1e88e5", "#43a047", "#fdd835", "#8e24aa"]


def nombor(n, word, fn):
    color = PALETTE[(n + 1) % len(PALETTE)]

    def subject(pen):
        num = str(n)
        size = min(400, 400 * 380 / text_width(num, 400))
        out = hollow(pen, 70, 600, num, size, color, w=5)
        x0 = 70 + text_width(num, size) + 40
        wsize = min(120, 120 * (850 - x0) / text_width(word, 120))
        out += hollow(pen, x0, 590, word, wsize, PALETTE[(n + 4) % len(PALETTE)])
        rows = ROWS[n]
        top, bottom, left, right = 660, 1240, 50, 855
        cell_h = (bottom - top) / len(rows)
        cell_w = (right - left) / max(rows)
        s = min(cell_w, cell_h) / 360 * 0.95 * SIZE.get(fn, 1.0)
        k = 0
        for r, cols in enumerate(rows):
            y = top + cell_h * (r + 0.5)
            x_start = W / 2 - cell_w * cols / 2
            for c in range(cols):
                x = x_start + cell_w * (c + 0.5)
                if fn is O.belon:
                    color_k = BALLOONS[k % len(BALLOONS)]
                    out += O.place(pen, lambda p, c=color_k: O.belon(p, c), x, y - 20 * s, s)
                else:
                    out += O.place(pen, fn, x, y, s)
                k += 1
        return out
    return page(f"Nombor {n}", subject, backdrop("#e3f2fd"))


# ---------------------------------------------------------------- bentuk

SHAPES = [
    ("Bulatan", lambda r: f"M{-150 * r},0 A{150 * r},{150 * r} 0 1 0 {150 * r},0 A{150 * r},{150 * r} 0 1 0 {-150 * r},0 Z",
     0, O.donat, "#e53935"),
    ("Segi Tiga", lambda r: f"M0,{-165 * r} L{175 * r},{130 * r} L{-175 * r},{130 * r} Z", 40, O.khemah, "#43a047"),
    ("Segi Empat Sama", lambda r: f"M{-140 * r},{-140 * r} H{140 * r} V{140 * r} H{-140 * r} Z", 0, O.kotak_hadiah,
     "#1e88e5"),
    ("Segi Empat Tepat", lambda r: f"M{-180 * r},{-110 * r} H{180 * r} V{110 * r} H{-180 * r} Z", 0, O.buku, "#fb8c00"),
    ("Bujur", lambda r: f"M{-115 * r},0 A{115 * r},{160 * r} 0 1 0 {115 * r},0 A{115 * r},{160 * r} 0 1 0 {-115 * r},0 Z",
     0, O.telur, "#8e24aa"),
    ("Bintang", lambda r: star_d(0, 10 * r, 175 * r, 78 * r), 24, O.bintang_laut, "#fdd835"),
    ("Hati", lambda r: O.hati_d(1.15 * r), -10, O.belon_hati, "#ec407a"),
]


OBJECT_AT = {"Hati": (830, 1.1)}


def bentuk(i, name, shape_d, face_dy, fn, color):
    def subject(pen):
        out = f'<g transform="translate(275,425)">'
        out += pen.path(shape_d(1.0), fill=color, w=5.5)
        out += face(pen, {}, cx=0, cy=face_dy - 14, gap=30) + "</g>"
        for x in (640, 790):
            out += (f'<g transform="translate({x},525)"><path d="{shape_d(0.36)}" fill="none" stroke="{INK}" '
                    f'stroke-width="{pen.sw(3)}" stroke-dasharray="{pen.sw(9)} {pen.sw(8)}" stroke-linecap="round"/></g>')
        cy, s = OBJECT_AT.get(name, (900, 1.2))
        out += O.place(pen, fn, 452, cy, s)
        wsize = min(84, 84 * 760 / text_width(name, 84))
        out += hollow(pen, W / 2, 1230, name, wsize, PALETTE[(i + 2) % len(PALETTE)], anchor="middle")
        return out
    return page(name, subject, backdrop("#f3e5f5"))


PAGES = ([huruf(i, WORDS[2 * i], WORDS[2 * i + 1]) for i in range(len(WORDS) // 2)]
         + [nombor(*n) for n in NUMBERS]
         + [bentuk(i, *s) for i, s in enumerate(SHAPES)])
