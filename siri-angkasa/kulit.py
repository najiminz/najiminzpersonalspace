"""Front and back covers for Siri 7: Angkasa Lepas.

Same full-color cartoon style as the other series covers (FSKXpert logo,
bubbly title, wooden sign, page-count badge), set in space with the cast in
space suits standing on the moon.
"""
import back_cover as BC
import cover as C
import covers as BUDAYA  # shared FSKXpert badge and back-cover children
import halaman as H
from draw import Pen

PAGES = 30


def front_background(pen):
    out = ('<defs><linearGradient id="space" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0d1442"/>'
           '<stop offset="0.6" stop-color="#283593"/><stop offset="1" stop-color="#5c6bc0"/></linearGradient></defs>'
           '<rect width="905" height="1280" fill="url(#space)"/>')
    out += H.starfield(pen, 41, n=40, y1=1000)
    out += H.mini_planet(pen, "zuhal", 760, 640, 64)
    out += H.mini_planet(pen, "marikh", 100, 640, 40)
    out += H.mini_planet(pen, "bumi", 430, 700, 34)
    out += H.small_rocket(pen, 820, 860, 0.24, 25)
    out += H.tail(pen, 160, 470, 30, 560, 14, "#b3e5fc", 3) + pen.circle(166, 466, 18, fill="#e1f5fe", sw=2.5)
    return out + H.moon_ground(pen, 1000, 7)


def front_cover_svg(px_w=2480, px_h=3508):
    pen = Pen(True, "fc")
    out = [BUDAYA.svg_open(px_w, px_h), C.defs(), front_background(pen)]
    cast = [("amir", 98, dict(ra=(70, -300))), ("aisyah", 275, {}), ("mei", 452, {}),
            ("ravi", 629, dict(la=(-80, -220))), ("lina", 806, dict(ra=(90, -280)))]
    for who, x, kw in cast:
        out.append(H.astro(pen, who, x, 1230, 0.74, **kw))
    out.append(BUDAYA.logo_badge())
    out.append(C.ribbon("SIRI 7", y=124))
    out.append(C.bubbly("ANGKASA", base_y=320, max_w=700, font_size=190))
    out.append(C.bubbly("LEPAS", base_y=452, max_w=440, font_size=120,
                        colors=["1e88e5", "e8402f", "fdd835", "43a047", "8e24aa"]))
    out.append(f'<g transform="translate(0,128)">{C.sign()}{C.badge(str(PAGES))}</g>')
    out.append("</svg>")
    return "\n".join(out)


# ---------------------------------------------------------------- back

def icon_planet(cx, cy):
    pen = Pen(True, "ip")
    pen.weight = 0.6
    return H.mini_planet(pen, "zuhal", cx, cy, 18)


def icon_rocket(cx, cy):
    pen = Pen(True, "ir")
    pen.weight = 0.2
    return H.small_rocket(pen, cx, cy - 6, 0.08, 30)


BLURB = ["Buku ini direka khas untuk membantu",
         "kanak-kanak prasekolah dan awal tahun",
         "sekolah rendah mengenal Matahari, planet,",
         "bintang dan penerokaan angkasa lepas."]
TILES = [("#f8bbd0", BC.icon_crayon, ["Melatih", "kemahiran", "motor halus"]),
         ("#bbdefb", icon_planet, ["Mengenal", "sistem", "suria"]),
         ("#fff59d", icon_rocket, ["Meneroka", "dunia", "angkasa"]),
         ("#c5e1a5", BC.icon_smile, ["Ilustrasi", "menarik dan", "mesra kanak-kanak"])]


def book_art(pen):
    return H.mini_planet(pen, "zuhal", 486, 958, 16) + H.mini_planet(pen, "marikh", 430, 966, 9)


def back_cover_svg(px_w=2480, px_h=3508):
    return BC.back_cover_svg(px_w, px_h, series="Siri Angkasa Lepas", lines=BLURB, tiles=TILES,
                             tagline="Mewarna, Meneroka, Menggapai Bintang",
                             books=["Mewarna", "Angkasa", "Planet", "Bintang", "Berakhlak"],
                             kids=lambda: BUDAYA.back_kids(book_art))
