"""Front and back covers for Siri 8: Budaya Malaysia.

Same full-color cartoon style and layout as the Siri Kenderaan covers, with
the recurring cast (Amir, Aisyah, Mei, Ravi, Lina) in traditional clothes and
the FSKXpert logo on the front.
"""
import math

import back_cover as BC
import cover as C
from characters import kid, kid_hands
from draw import Pen, blob_d, palm
from subjects import big_hibiscus, rumah_melayu, wau

W, H = 905, 1280


def svg_open(px_w, px_h):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{px_w}" height="{px_h}" viewBox="0 0 {W} {H}" '
            f'preserveAspectRatio="none">')


# ---------------------------------------------------------------- front

def front_background():
    out = '<rect width="905" height="1280" fill="url(#sky)"/>'
    for k in range(14):
        a = 2 * math.pi * k / 14
        out += (f'<path d="M{805 + 70 * math.cos(a - 0.09):.1f},{120 + 70 * math.sin(a - 0.09):.1f} '
                f'L{805 + 112 * math.cos(a):.1f},{120 + 112 * math.sin(a):.1f} '
                f'L{805 + 70 * math.cos(a + 0.09):.1f},{120 + 70 * math.sin(a + 0.09):.1f} Z" fill="#ffd54f"/>')
    out += '<circle cx="805" cy="120" r="62" fill="url(#sun)" stroke="#f9a825" stroke-width="4"/>'
    for x, y, s in ((560, 180, 0.7), (40, 640, 0.6), (700, 620, 0.55)):
        out += (f'<g transform="translate({x},{y}) scale({s})">'
                + C.p(blob_d(90, 40, 85, 34, 9, int(x + y), flat_bottom=True), "#ffffff", stroke="#9fd3ef", w=3)
                + "</g>")
    out += C.p("M-20,900 Q160,780 360,860 Q560,790 760,850 Q860,820 940,860 L940,1000 L-20,1000 Z", "url(#hill1)",
               stroke="#4e9a2c", w=3)
    out += C.p("M-20,960 Q200,900 450,940 Q700,900 940,950 L940,1300 L-20,1300 Z", "url(#grass)", stroke="#4e9a2c",
               w=3)
    return out


def logo_badge():
    return ('<rect x="22" y="20" width="248" height="84" rx="18" fill="#ffffff" fill-opacity="0.92" '
            'stroke="#1a3a8f" stroke-width="2.5"/>' + BC.wordmark(38, 66, 42))


def front_cover_svg(px_w=2480, px_h=3508):
    pen = Pen(True, "fc")
    out = [svg_open(px_w, px_h), C.defs(), front_background()]
    out.append(f'<g transform="translate(372,452) scale(0.56)">{rumah_melayu(pen)}</g>')
    out.append(palm(pen, 60, 1000, 380, lean=28) + palm(pen, 860, 990, 300, lean=-24))
    out.append(wau(pen, 150, 800, 0.34))
    amir_hand = (60, -330)
    out.append(C.p(f"M150,824 Q{110 + 60},900 {110 + amir_hand[0] * 0.95:.0f},{1130 + amir_hand[1] * 0.95:.0f}",
                   "none", stroke="#424242", w=2))
    cast = [("amir", 110, dict(outfit="bajumelayu", ra=amir_hand)),
            ("aisyah", 280, {}),
            ("mei", 450, dict(la=(-84, -170), ra=(84, -170))),
            ("ravi", 620, {}),
            ("lina", 780, dict(la=(-90, -220), ra=(90, -220)))]
    for who, x, kw in cast:
        out.append(kid(pen, who, x, 1130, 0.95, **kw))
    for x, y, r in ((40, 1180, 60), (865, 1190, 64), (200, 1235, 42), (700, 1240, 44)):
        out.append(big_hibiscus(pen, x, y, r, 12))
    for x, y, s in ((330, 1200, 1.0), (450, 1240, 0.9), (560, 1196, 1.0), (120, 1110, 0.8), (780, 1120, 0.8)):
        out.append(C.flower(x, y, s))
    out.append(C.butterfly(860, 760, 0.9, "#ec407a", "#f8bbd0", rot=12))
    out.append(logo_badge())
    out.append(C.ribbon("SIRI 8", y=124))
    out.append(C.bubbly("BUDAYA", base_y=320, max_w=680, font_size=190))
    out.append(C.bubbly("MALAYSIA", base_y=452, max_w=600, font_size=112,
                        colors=["1e88e5", "e8402f", "fdd835", "43a047", "ff9800", "8e24aa", "00acc1", "ec407a"]))
    out.append(f'<g transform="translate(0,128)">{C.sign()}{C.badge()}</g>')
    out.append("</svg>")
    return "\n".join(out)


# ---------------------------------------------------------------- back

def icon_wau(cx, cy):
    return wau(Pen(False, "iw"), cx, cy + 4, 0.15)


def icon_heart(cx, cy):
    return (C.p(f"M{cx},{cy + 28} C{cx - 50},{cy - 4} {cx - 30},{cy - 44} {cx},{cy - 20} "
                f"C{cx + 30},{cy - 44} {cx + 50},{cy - 4} {cx},{cy + 28} Z", "#ef5350", stroke=C.NAVY, w=3)
            + C.p(f"M{cx + 26},{cy - 34} C{cx + 14},{cy - 46} {cx + 22},{cy - 58} {cx + 32},{cy - 48} "
                  f"C{cx + 42},{cy - 58} {cx + 50},{cy - 46} {cx + 38},{cy - 34} L{cx + 32},{cy - 28} Z",
                  "#f48fb1", stroke=C.NAVY, w=2.5))


BLURB = ["Buku ini direka khas untuk membantu",
         "kanak-kanak prasekolah dan awal tahun",
         "sekolah rendah mengenal 30 warisan budaya",
         "Malaysia yang kaya sambil mewarna."]
TILES = [("#f8bbd0", BC.icon_crayon, ["Melatih", "kemahiran", "motor halus"]),
         ("#fff59d", icon_wau, ["Mengenal", "30 warisan", "budaya"]),
         ("#bbdefb", icon_heart, ["Menyemai", "semangat", "perpaduan"]),
         ("#c5e1a5", BC.icon_smile, ["Ilustrasi", "menarik dan", "mesra kanak-kanak"])]


def held_book(pen, art=None):
    out = C.p("M352,850 L606,836 L622,1000 L360,1014 Z", "url(#redbook)", stroke=C.OUTLINE, w=4)
    out += C.p("M352,850 L340,860 L348,1022 L360,1014 Z", "#b71c1c", stroke=C.OUTLINE, w=3.5)
    out += C.p("M606,836 L616,830 L632,994 L622,1000", "#fafafa", stroke=C.OUTLINE, w=3)
    out += (f'<g transform="rotate(-3 486 925)">'
            + BC.text(486, 878, "Buku", 30, fill="#ffd54f", weight=700,
                      extra=f'stroke="{C.OUTLINE}" stroke-width="5" paint-order="stroke"')
            + BC.text(486, 908, "Mewarna", 30, fill="#ffffff", weight=700,
                      extra=f'stroke="{C.OUTLINE}" stroke-width="5" paint-order="stroke"')
            + f'<rect x="400" y="922" width="172" height="74" rx="8" fill="#bfe7fb" stroke="{C.OUTLINE}" stroke-width="2.5"/>'
            + (art(pen) if art else wau(pen, 486, 958, 0.11)) + "</g>")
    return out


def back_kids(art=None):
    pen = Pen(True, "bk")
    la_a, ra_a = (-60, -116), (40, -150)
    la_b, ra_b = (-40, -150), (60, -116)
    out = kid(pen, "aisyah", 580, 1010, 1.05, la=la_b, ra=ra_b, sit=True, hands=False)
    out += kid(pen, "amir", 330, 1010, 1.05, la=la_a, ra=ra_a, sit=True, hands=False)
    out += held_book(pen, art)
    out += kid_hands(pen, "amir", 330, 1010, 1.05, la=(-60, -116), ra=(30, -100), sit=True)
    out += kid_hands(pen, "aisyah", 580, 1010, 1.05, la=(-30, -110), ra=(60, -116), sit=True)
    return out


def back_cover_svg(px_w=2480, px_h=3508):
    return BC.back_cover_svg(px_w, px_h, series="Siri Budaya Malaysia", lines=BLURB, tiles=TILES,
                             tagline="Mewarna, Mengenal, Menghargai Budaya Kita",
                             books=["Mewarna", "Budaya", "Warisan", "Perpaduan", "Berakhlak"], kids=back_kids)
