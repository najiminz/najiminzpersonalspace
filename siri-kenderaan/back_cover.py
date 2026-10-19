"""Back cover ("Kulit Belakang") for the Siri Kenderaan coloring book.

Follows the layout of the publisher's "Mari Membaca" back cover: wooden title
sign, a description card with four feature tiles, two children coloring
together, and a publisher panel with contact details and an ISBN barcode.
The ISBN and barcode are placeholders until a real ISBN is assigned.
"""
import math

import vehicles as V
from cover import NAVY, OUTLINE, butterfly, ell, flower, p, vehicle
from draw import Pen, blob_d

W, H = 905, 1280
SKIN = "#ffd9b8"
FONT = 'font-family="Fredoka"'


def text(x, y, s, size, fill=NAVY, weight=600, anchor="middle", extra=""):
    return (f'<text x="{x}" y="{y}" {FONT} font-weight="{weight}" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}" {extra}>{s}</text>')


# ---------------------------------------------------------------- background

def background():
    out = '<rect width="905" height="1280" fill="url(#bsky)"/>'
    for x, y, s in ((20, 40, 1.2), (330, 10, 0.9), (640, 60, 0.8)):
        out += (f'<g transform="translate({x},{y}) scale({s})">'
                + p(blob_d(100, 50, 95, 40, 9, int(x + y) + 3, flat_bottom=True), "#ffffff", stroke="#cfe8f7", w=3)
                + "</g>")
    # distant trees
    for cx, cy, r, c in ((60, 260, 90, "#5cab3c"), (220, 330, 80, "#4f9f33"), (720, 300, 90, "#5cab3c"),
                         (600, 360, 70, "#66b84a")):
        out += p(blob_d(cx, cy, r, r * 0.8, 10, cx), c, stroke="#3d7f27", w=3)
    # house on the left
    out += p("M-20,330 L150,330 L150,620 L-20,620 Z", "#f6e3c4", stroke="#8a5a2f", w=3.5)
    out += p("M-30,340 L60,250 L170,250 L190,350 Z", "#d9552f", stroke="#8a2f1a", w=3.5)
    for y in (275, 300, 325):
        out += p(f"M{-10},{y + 10} L{180},{y + 10}", "none", stroke="#a63a1e", w=2)
    out += p("M20,420 L120,420 L120,540 L20,540 Z", "#8fd3f4", stroke="#8a5a2f", w=4)
    out += p("M70,420 L70,540 M20,480 L120,480", "none", stroke="#8a5a2f", w=3)
    out += '<rect x="10" y="540" width="120" height="16" rx="4" fill="#c98b4f" stroke="#8a5a2f" stroke-width="3"/>'
    # big tree on the right
    out += p("M800,1100 Q820,760 780,520 Q770,440 740,380 L790,370 Q820,430 840,500 Q860,380 905,330 L905,1100 Z",
             "#a8743f")
    out += p("M840,620 Q846,700 840,780 M820,860 Q826,930 820,1000", "none", stroke="#6d4421", w=3)
    for cx, cy, rx, ry, c in ((760, 60, 170, 110, "#4caf50"), (880, 180, 140, 120, "#3f9a2e"),
                              (640, 20, 140, 80, "#5cbf4a"), (820, 300, 110, 80, "#43a047")):
        out += p(blob_d(cx, cy, rx, ry, 12, cx + cy), c, stroke="#2e7d32", w=3.5)
    # fence + hedges
    for x in range(640, 905, 46):
        out += p(f"M{x},900 L{x},680 L{x + 10},668 L{x + 20},680 L{x + 20},900 Z", "#d9a066", stroke="#8a5a2f", w=3)
    out += '<rect x="630" y="720" width="290" height="14" rx="4" fill="#c98b4f" stroke="#8a5a2f" stroke-width="3"/>'
    out += '<rect x="630" y="800" width="290" height="14" rx="4" fill="#c98b4f" stroke="#8a5a2f" stroke-width="3"/>'
    out += p("M-20,700 L240,700 L240,780 L-20,780 Z", "#c98b4f", stroke="#8a5a2f", w=3)
    out += '<rect x="20" y="660" width="50" height="140" rx="4" fill="#d9a066" stroke="#8a5a2f" stroke-width="3"/>'
    out += p(blob_d(100, 760, 140, 60, 10, 5, flat_bottom=True), "#4caf50", stroke="#2e7d32", w=3)
    out += p(blob_d(790, 830, 150, 80, 10, 6, flat_bottom=True), "#4caf50", stroke="#2e7d32", w=3)
    for x, y in ((40, 740), (110, 720), (170, 750), (720, 780), (800, 760), (860, 800), (700, 830), (830, 840)):
        out += flower(x, y, 0.9)
    out += p("M-20,880 Q200,860 450,872 Q700,860 940,880 L940,1300 L-20,1300 Z", "url(#bgrass)", stroke="#4e9a2c", w=3)
    return out


# ---------------------------------------------------------------- top: publisher mark, sign, card

def wordmark(x, y, size=40, tagline=True):
    out = (f'<text x="{x}" y="{y}" font-family="Liberation Sans, Arial, sans-serif" font-weight="700" '
           f'font-style="italic" font-size="{size}" fill="#1a3a8f" letter-spacing="-1">FSK'
           f'<tspan fill="#e53935">X</tspan>pert</text>')
    if tagline:
        out += (f'<text x="{x + 2}" y="{y + size * 0.42:.0f}" font-family="Liberation Sans, Arial, sans-serif" '
                f'font-weight="700" font-size="{size * 0.3:.0f}" fill="#1a3a8f">Pendidikan • Inovasi • Komuniti</text>')
    return out


def sign(series="Siri Kenderaan"):
    board = "M232,96 Q450,82 672,96 L664,176 Q450,188 240,176 Z"
    out = ""
    rnd = [(214, 100, -30), (230, 74, -60), (290, 80, 20), (612, 80, -20), (672, 74, 60), (690, 100, 30),
           (220, 170, 200), (686, 170, -20), (420, 76, 0), (500, 78, 10)]
    for x, y, rot in rnd:
        out += ell(x, y, 18, 9, "#66bb55", stroke="#2e7d32", w=2, rot=rot)
    out += p(board, "url(#bwood)", stroke="#6b3e1a", w=5)
    for d in ("M260,116 Q380,110 460,114", "M480,160 Q580,154 650,160"):
        out += p(d, "none", stroke="#b5733a", w=2.5)
    out += text(452, 155, 'Buku <tspan fill="#ffd54f">Mewarna</tspan>', 54, fill="#ffffff", weight=700,
                extra=f'stroke="{OUTLINE}" stroke-width="8" stroke-linejoin="round" paint-order="stroke"')
    out += f'<rect x="322" y="176" width="260" height="44" rx="22" fill="#ec407a" stroke="#ffffff" stroke-width="4"/>'
    out += text(452, 207, series, 26, fill="#ffffff", weight=700)
    return out


def icon_crayon(cx, cy):
    g = (f'<g transform="rotate(-40 {cx} {cy})">'
         + p(f"M{cx - 40},{cy - 11} L{cx + 22},{cy - 11} L{cx + 44},{cy} L{cx + 22},{cy + 11} L{cx - 40},{cy + 11} Z",
             "#ec407a", stroke=NAVY, w=3)
         + p(f"M{cx + 22},{cy - 11} L{cx + 22},{cy + 11} M{cx - 26},{cy - 11} L{cx - 26},{cy + 11}", "none", stroke=NAVY, w=2.5)
         + "</g>")
    return g + p(f"M{cx - 40},{cy + 30} Q{cx - 20},{cy + 14} {cx},{cy + 30} Q{cx + 20},{cy + 46} {cx + 40},{cy + 28}",
                 "none", stroke="#ec407a", w=4)


def icon_brain(cx, cy):
    out = p(blob_d(cx, cy, 40, 32, 9, 11), "#e3f2fd", stroke=NAVY, w=3)
    out += p(f"M{cx},{cy - 30} Q{cx - 6},{cy} {cx},{cy + 30}", "none", stroke=NAVY, w=3)
    for s in (-1, 1):
        out += p(f"M{cx + s * 8},{cy - 14} Q{cx + s * 24},{cy - 18} {cx + s * 28},{cy - 4} "
                 f"M{cx + s * 10},{cy + 10} Q{cx + s * 22},{cy + 6} {cx + s * 30},{cy + 16}", "none", stroke=NAVY, w=2.5)
    return out


def icon_car(cx, cy):
    return vehicle(V.kereta, cx - 50, cy + 26, 0.16, colored=False, prefix="ic")


def icon_smile(cx, cy):
    return (f'<circle cx="{cx}" cy="{cy}" r="34" fill="none" stroke="{NAVY}" stroke-width="3.5"/>'
            f'<circle cx="{cx - 12}" cy="{cy - 8}" r="4" fill="{NAVY}"/><circle cx="{cx + 12}" cy="{cy - 8}" r="4" fill="{NAVY}"/>'
            + p(f"M{cx - 16},{cy + 8} Q{cx},{cy + 24} {cx + 16},{cy + 8}", "none", stroke=NAVY, w=3.5))


BLURB = ["Buku ini direka khas untuk membantu",
         "kanak-kanak prasekolah dan awal tahun",
         "sekolah rendah mengenal 30 jenis kenderaan",
         "di darat, laut dan udara sambil mewarna."]
TILES = [("#f8bbd0", icon_crayon, ["Melatih", "kemahiran", "motor halus"]),
         ("#bbdefb", icon_brain, ["Merangsang", "kreativiti &amp;", "imaginasi"]),
         ("#fff59d", icon_car, ["Mengenal", "30 jenis", "kenderaan"]),
         ("#c5e1a5", icon_smile, ["Ilustrasi", "menarik dan", "mesra kanak-kanak"])]
TAGLINE = "Mewarna, Meneroka, Membangun Masa Depan"
BOOKS = ["Mewarna", "Melukis", "Meneroka", "Berkarya", "Berakhlak"]


def card(lines=BLURB, tiles=TILES, tagline=TAGLINE):
    out = (f'<rect x="132" y="232" width="642" height="420" rx="26" fill="#fffaf0" fill-opacity="0.96" '
           f'stroke="#f3d9a4" stroke-width="3"/>'
           f'<rect x="146" y="246" width="614" height="392" rx="20" fill="none" stroke="#e7c27a" stroke-width="2.5" '
           f'stroke-dasharray="9 7"/>')
    for i, line in enumerate(lines):
        out += text(176, 296 + i * 34, line, 23, fill="#263238", weight=400, anchor="start")
    for i, (bg, icon, label) in enumerate(tiles):
        x = 160 + i * 150
        out += f'<rect x="{x}" y="440" width="136" height="146" rx="16" fill="{bg}"/>'
        out += icon(x + 68, 482)
        for j, line in enumerate(label):
            out += text(x + 68, 538 + j * 17, line, 15 if len(line.replace("&amp;", "&")) < 16 else 13.5, fill="#263238", weight=500)
    out += (f'<rect x="196" y="598" width="514" height="40" rx="20" fill="#ffffff" stroke="#ce93d8" stroke-width="2.5" '
            f'stroke-dasharray="8 6"/>')
    out += text(453, 625, tagline, 19, fill="#6a1b9a", weight=600,
                extra='font-style="italic"')
    return out


# ---------------------------------------------------------------- characters

def eyes(cx, cy, gap=30):
    out = ""
    for ex in (-gap, gap):
        out += ell(cx + ex, cy, 13, 17, "#3b2314", stroke="none")
        out += f'<circle cx="{cx + ex + 5}" cy="{cy - 6}" r="5.5" fill="#fff"/><circle cx="{cx + ex - 4}" cy="{cy + 6}" r="2.5" fill="#fff"/>'
        out += ell(cx + ex * 1.55, cy + 26, 14, 8, "#ff8a80", stroke="none", extra='opacity="0.6"')
    return out


def boy(cx=320):
    out = ""
    # legs (crossed, sitting)
    out += p(f"M{cx - 100},990 Q{cx - 110},940 {cx - 50},930 L{cx + 60},940 Q{cx + 90},960 {cx + 70},1000 "
             f"L{cx - 80},1010 Z", "#3f7fcf", stroke=OUTLINE, w=3.5)
    out += ell(cx - 104, 1004, 36, 19, "#212121", stroke=OUTLINE, w=3, rot=8)
    out += p(f"M{cx - 136},1010 Q{cx - 104},1026 {cx - 70},1014", "none", stroke="#ffffff", w=4)
    # body
    out += p(f"M{cx - 80},950 Q{cx - 90},860 {cx - 40},840 L{cx + 40},840 Q{cx + 90},860 {cx + 80},950 Z", "#e53935",
             stroke=OUTLINE, w=3.5)
    out += p(f"M{cx - 20},842 Q{cx},860 {cx + 20},842", "none", stroke="#b71c1c", w=3)
    # head
    out += ell(cx - 84, 760, 16, 20, SKIN, stroke=OUTLINE, w=3)
    out += ell(cx + 84, 760, 16, 20, SKIN, stroke=OUTLINE, w=3)
    out += f'<circle cx="{cx}" cy="752" r="86" fill="{SKIN}" stroke="{OUTLINE}" stroke-width="3.5"/>'
    hair = (f"M{cx - 88},752 Q{cx - 100},690 {cx - 60},672 L{cx - 70},640 L{cx - 30},660 L{cx - 20},622 L{cx + 8},656 "
            f"L{cx + 30},626 L{cx + 40},664 L{cx + 80},650 L{cx + 70},684 Q{cx + 100},700 {cx + 88},752 "
            f"Q{cx + 70},700 {cx + 30},700 Q{cx + 10},720 {cx - 20},700 Q{cx - 50},720 {cx - 60},700 "
            f"Q{cx - 80},720 {cx - 88},752 Z")
    out += p(hair, "url(#hair)", stroke=OUTLINE, w=3.5)
    out += eyes(cx, 762)
    out += p(f"M{cx - 50},734 Q{cx - 30},726 {cx - 14},734 M{cx + 14},734 Q{cx + 30},726 {cx + 50},734", "none", w=3)
    out += p(f"M{cx - 24},796 Q{cx},826 {cx + 24},796 Q{cx},806 {cx - 24},796 Z", "#9c2b1f", stroke=OUTLINE, w=2.5)
    out += p(f"M{cx - 4},778 Q{cx},784 {cx + 4},778", "none", w=2.5)
    return out


def girl(cx=580):
    out = ""
    out += p(f"M{cx - 70},1000 Q{cx - 90},950 {cx - 40},940 L{cx + 70},945 Q{cx + 110},960 {cx + 100},1005 "
             f"L{cx - 60},1015 Z", "#6a2c70", stroke=OUTLINE, w=3.5)
    out += p(f"M{cx + 90},1015 Q{cx + 120},985 {cx + 150},1000 Q{cx + 150},1022 {cx + 100},1025 Z", "#f48fb1",
             stroke=OUTLINE, w=3)
    out += p(f"M{cx - 86},960 Q{cx - 96},880 {cx - 50},850 L{cx + 50},850 Q{cx + 96},880 {cx + 86},960 Z", "#9575cd",
             stroke=OUTLINE, w=3.5)
    hijab = (f"M{cx - 100},900 Q{cx - 120},780 {cx - 90},720 Q{cx - 60},650 {cx},648 Q{cx + 60},650 {cx + 90},720 "
             f"Q{cx + 120},780 {cx + 104},900 Q{cx + 60},870 {cx},874 Q{cx - 60},870 {cx - 100},900 Z")
    out += p(hijab, "url(#hijab)", stroke=OUTLINE, w=3.5)
    out += p(f"M{cx - 70},880 Q{cx},840 {cx + 74},882", "none", stroke="#c2185b", w=2.5)
    out += ell(cx, 768, 66, 72, SKIN, stroke=OUTLINE, w=3)
    out += p(f"M{cx - 66},748 Q{cx - 50},690 {cx},692 Q{cx + 50},690 {cx + 66},748 Q{cx + 40},712 {cx},712 "
             f"Q{cx - 40},712 {cx - 66},748 Z", "url(#hijab)", stroke=OUTLINE, w=3)
    out += eyes(cx, 772, gap=26)
    out += p(f"M{cx - 42},748 Q{cx - 26},740 {cx - 12},748 M{cx + 12},748 Q{cx + 26},740 {cx + 42},748", "none", w=3)
    out += p(f"M{cx - 20},804 Q{cx},830 {cx + 20},804 Q{cx},812 {cx - 20},804 Z", "#9c2b1f", stroke=OUTLINE, w=2.5)
    return out


def held_book():
    out = p("M352,850 L606,836 L622,1000 L360,1014 Z", "url(#redbook)", stroke=OUTLINE, w=4)
    out += p("M352,850 L340,860 L348,1022 L360,1014 Z", "#b71c1c", stroke=OUTLINE, w=3.5)
    out += p("M606,836 L616,830 L632,994 L622,1000", "#fafafa", stroke=OUTLINE, w=3)
    out += (f'<g transform="rotate(-3 486 925)">'
            + text(486, 878, "Buku", 30, fill="#ffd54f", weight=700,
                   extra=f'stroke="{OUTLINE}" stroke-width="5" paint-order="stroke"')
            + text(486, 908, "Mewarna", 30, fill="#ffffff", weight=700,
                   extra=f'stroke="{OUTLINE}" stroke-width="5" paint-order="stroke"')
            + f'<rect x="400" y="926" width="172" height="70" rx="8" fill="#bfe7fb" stroke="{OUTLINE}" stroke-width="2.5"/>'
            + f'<rect x="400" y="976" width="172" height="20" fill="#8e98a4"/>'
            + vehicle(V.bas_sekolah, 434, 990, 0.13, prefix="hb")
            + "</g>")
    for x, y in ((356, 930), (612, 916)):
        out += ell(x, y, 22, 18, SKIN, stroke=OUTLINE, w=3)
    out += ell(320, 960, 22, 16, SKIN, stroke=OUTLINE, w=3, rot=-30)
    return out


def book_stack(x=-10, y=820, labels=BOOKS):
    out = ""
    books = zip(("#ec407a", "#1e88e5", "#fb8c00", "#43a047", "#8e24aa"), labels)
    for i, (c, label) in enumerate(books):
        by = y + i * 42
        dx = (i % 2) * 8
        out += p(f"M{x + dx},{by} L{x + dx + 220},{by} Q{x + dx + 232},{by} {x + dx + 232},{by + 12} L{x + dx + 232},{by + 30} "
                 f"Q{x + dx + 232},{by + 42} {x + dx + 220},{by + 42} L{x + dx},{by + 42} Z", c, stroke=OUTLINE, w=3)
        out += f'<rect x="{x + dx + 196}" y="{by + 5}" width="30" height="32" rx="4" fill="#fffde7"/>'
        out += p(f"M{x + dx + 30},{by + 6} L{x + dx + 30},{by + 36}", "none", stroke="#ffffff", w=2)
        out += text(x + dx + 110, by + 29, label, 22, fill="#ffffff", weight=600)
    return out


def cat(cx=770, cy=990):
    out = p(f"M{cx + 80},{cy + 10} Q{cx + 130},{cy - 10} {cx + 110},{cy - 50} Q{cx + 100},{cy - 70} {cx + 84},{cy - 56} "
            f"Q{cx + 100},{cy - 30} {cx + 70},{cy}", "#ffb74d", stroke=OUTLINE, w=3)
    out += ell(cx + 20, cy - 4, 90, 44, "#ffb74d", stroke=OUTLINE, w=3.5)
    for k in range(4):
        x = cx + k * 26
        out += p(f"M{x},{cy - 46} Q{x + 6},{cy - 30} {x},{cy - 18}", "none", stroke="#e65100", w=3)
    out += p(f"M{cx - 92},{cy - 50} L{cx - 84},{cy - 104} L{cx - 50},{cy - 74} Z M{cx - 20},{cy - 70} L{cx - 4},{cy - 108} "
             f"L{cx + 20},{cy - 56} Z", "#ffb74d", stroke=OUTLINE, w=3)
    out += p(f"M{cx - 82},{cy - 64} L{cx - 80},{cy - 90} L{cx - 62},{cy - 74} Z", "#ffccbc", stroke="none")
    out += ell(cx - 50, cy - 30, 62, 50, "#ffb74d", stroke=OUTLINE, w=3.5)
    out += ell(cx - 50, cy - 12, 34, 22, "#fff3e0", stroke="none")
    for ex in (-74, -26):
        out += p(f"M{cx + ex - 10},{cy - 36} Q{cx + ex},{cy - 28} {cx + ex + 10},{cy - 36}", "none", w=3)
    out += ell(cx - 50, cy - 18, 6, 4, "#f06292", stroke="none")
    out += p(f"M{cx - 58},{cy - 10} Q{cx - 50},{cy - 4} {cx - 42},{cy - 10}", "none", w=2.5)
    for s in (-1, 1):
        out += p(f"M{cx - 50 + s * 20},{cy - 16} L{cx - 50 + s * 52},{cy - 22} M{cx - 50 + s * 20},{cy - 10} "
                 f"L{cx - 50 + s * 52},{cy - 6}", "none", w=1.8)
    out += ell(cx - 30, cy + 30, 24, 12, "#fff3e0", stroke=OUTLINE, w=3)
    return out


# ---------------------------------------------------------------- bottom panel

def barcode(x, y):
    out = f'<rect x="{x}" y="{y}" width="220" height="118" rx="8" fill="#ffffff" stroke="#9e9e9e" stroke-width="2"/>'
    out += text(x + 110, y + 22, "ISBN 978-967-XXXXXXX-X", 13, fill="#212121", weight=500)
    widths = [1, 1, 3, 2, 1, 1, 2, 3, 1, 2, 1, 1, 3, 1, 2, 2, 1, 3, 1, 1, 2, 1, 1, 2, 3, 1, 1, 2, 1, 3, 2, 1, 1, 1,
              2, 1, 3, 1, 2, 1, 1, 2, 1, 1, 3, 2, 1, 1, 2, 1]
    bx = x + 18
    for i, wdt in enumerate(widths):
        if i % 2 == 0:
            tall = 66 if i in (0, 2, 24, 26, len(widths) - 4, len(widths) - 2) else 58
            out += f'<rect x="{bx:.1f}" y="{y + 30}" width="{wdt * 1.6:.1f}" height="{tall}" fill="#111"/>'
        bx += wdt * 1.6 + 0.9
    out += text(x + 110, y + 110, "9 789667 XXXXXX", 15, fill="#212121", weight=500)
    return out


def panel():
    out = f'<rect x="40" y="1060" width="825" height="196" rx="22" fill="#ffffff" fill-opacity="0.97" stroke="#e0e0e0" stroke-width="2"/>'
    out += wordmark(70, 1110, 46)
    for i, line in enumerate(["Fakulti Sains Kemanusiaan", "Universiti Pendidikan Sultan Idris",
                              "Tanjong Malim, Perak."]):
        out += text(72, 1152 + i * 20, line, 15, fill="#263238", weight=400, anchor="start")
    out += f'<circle cx="82" cy="1226" r="11" fill="#1a3a8f"/>'
    out += p("M71,1226 L93,1226 M82,1215 Q76,1226 82,1237 Q88,1226 82,1215", "none", stroke="#ffffff", w=1.6)
    out += text(100, 1232, "fskxpert.upsi.my", 17, fill="#263238", weight=500, anchor="start")
    out += (f'<text x="470" y="1128" text-anchor="middle" font-family="Liberation Serif, serif" font-size="26" '
            f'fill="#1a3a8f">UNIVERSITI</text>'
            f'<text x="470" y="1156" text-anchor="middle" font-family="Liberation Serif, serif" font-size="26" '
            f'fill="#1a3a8f">PENDIDIKAN</text>'
            f'<text x="470" y="1184" text-anchor="middle" font-family="Liberation Serif, serif" font-size="26" '
            f'fill="#1a3a8f">SULTAN IDRIS</text>'
            f'<text x="470" y="1210" text-anchor="middle" font-family="Liberation Serif, serif" font-size="12.5" '
            f'fill="#1a3a8f">SULTAN IDRIS EDUCATION UNIVERSITY</text>')
    out += f'<rect x="604" y="1072" width="248" height="62" rx="12" fill="#ffffff" stroke="#1a3a8f" stroke-width="2.5"/>'
    out += text(728, 1096, "Prof. Madya Dr. Kamarul Ismail", 14.5, fill="#1a3a8f", weight=600)
    out += f'<circle cx="634" cy="1116" r="12" fill="#25d366"/>'
    out += p("M628,1112 Q630,1122 640,1122", "none", stroke="#ffffff", w=2.4)
    out += text(654, 1124, "01126247763", 22, fill="#1a3a8f", weight=700, anchor="start")
    out += barcode(626, 1138)
    return out


def defs():
    return ("<defs>"
            '<linearGradient id="bsky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5ec2f0"/>'
            '<stop offset="0.5" stop-color="#b8e6fb"/><stop offset="1" stop-color="#e3f6ff"/></linearGradient>'
            '<linearGradient id="bgrass" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8fd36b"/>'
            '<stop offset="1" stop-color="#4c9c30"/></linearGradient>'
            '<linearGradient id="bwood" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d9954f"/>'
            '<stop offset="1" stop-color="#9c5a2a"/></linearGradient>'
            '<linearGradient id="hair" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8a5a34"/>'
            '<stop offset="1" stop-color="#5a3519"/></linearGradient>'
            '<linearGradient id="hijab" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f48fb1"/>'
            '<stop offset="1" stop-color="#e05592"/></linearGradient>'
            '<linearGradient id="redbook" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ef5350"/>'
            '<stop offset="1" stop-color="#c62828"/></linearGradient>'
            "</defs>")


def children():
    return girl() + boy() + held_book()


def back_cover_svg(px_w=2480, px_h=3508, series="Siri Kenderaan", lines=BLURB, tiles=TILES, tagline=TAGLINE,
                   books=BOOKS, kids=children):
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{px_w}" height="{px_h}" viewBox="0 0 {W} {H}" '
           f'preserveAspectRatio="none">', defs(), background()]
    out.append(wordmark(36, 58, 40))
    out.append(card(lines, tiles, tagline))
    out.append(sign(series))
    out.append(butterfly(110, 640, 0.9, "#ff9800", "#fdd835", rot=-12))
    out.append(book_stack(labels=books))
    out.append(kids())
    out.append(cat())
    for x, y, s in ((30, 1060, 1.2), (250, 1050, 1.0), (680, 1052, 1.1), (880, 1056, 1.2), (20, 1265, 1.0),
                    (440, 1270, 1.0), (890, 1268, 1.0)):
        out.append(flower(x, y, s, petal="#ffe082" if x % 3 else "#ffffff", center="#ff9800"))
    out.append(panel())
    out.append("</svg>")
    return "\n".join(out)
