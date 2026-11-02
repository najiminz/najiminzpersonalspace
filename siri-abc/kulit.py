"""Front and back covers for Siri 10: ABC, Nombor dan Bentuk.

Same full-color cartoon style as the other series covers: FSKXpert logo,
bubbly title, wooden sign, the recurring cast holding letter and number
blocks, and an open book with a coloured and an uncoloured page.
"""
import back_cover as BC
import cover as C
import covers as BUDAYA  # the Siri Budaya covers: shared background, logo and back-cover children
import objek as O
from characters import kid, kid_hands
from draw import INK, Pen, star_d

PAGES = 30


def block(pen, x, y, label, color, size=74):
    """A toy block with a letter or number on the front."""
    d = size * 0.3
    out = C.p(f"M{x},{y} L{x + d},{y - d} L{x + size + d},{y - d} L{x + size},{y} Z", color, stroke=C.NAVY, w=3)
    out += C.p(f"M{x + size},{y} L{x + size + d},{y - d} L{x + size + d},{y + size - d} L{x + size},{y + size} Z",
               color, stroke=C.NAVY, w=3, extra='opacity="0.85"')
    out += f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="6" fill="{color}" stroke="{C.NAVY}" stroke-width="3"/>'
    out += (f'<text x="{x + size / 2}" y="{y + size * 0.76}" text-anchor="middle" font-family="Fredoka" '
            f'font-weight="700" font-size="{size * 0.72:.0f}" fill="#ffffff" stroke="{C.NAVY}" stroke-width="3" '
            f'paint-order="stroke">{label}</text>')
    return out


def floating_shapes():
    out = C.p(star_d(70, 700, 34, 15), "#fdd835", stroke=C.NAVY, w=3)
    out += C.p(O.hati_d(0.22), "#ec407a", stroke=C.NAVY, w=3,
               extra='transform="translate(840,720)"')
    out += f'<circle cx="300" cy="700" r="22" fill="#42a5f5" stroke="{C.NAVY}" stroke-width="3"/>'
    out += C.p("M620,676 L646,720 L594,720 Z", "#66bb6a", stroke=C.NAVY, w=3)
    return out


def open_book():
    out = C.p("M50,1012 Q250,990 452,1006 Q660,990 860,1012 L872,1250 Q660,1232 452,1250 Q250,1232 36,1250 Z",
              "#1e63c9", stroke=C.NAVY, w=4)
    out += C.p("M66,1000 Q260,982 452,996 L452,1232 Q260,1216 56,1234 Z", "#ffffff", stroke="#9e9e9e", w=3)
    out += C.p("M452,996 Q650,982 842,1000 L852,1234 Q650,1216 452,1232 Z", "#ffffff", stroke="#9e9e9e", w=3)
    out += C.p("M452,996 L452,1232", "none", stroke="#bdbdbd", w=3)
    out += (f'<text x="100" y="1060" font-family="Fredoka" font-weight="700" font-size="40" fill="#e8402f">Aa</text>'
            f'<text x="176" y="1058" font-family="Fredoka" font-weight="600" font-size="30" fill="{C.NAVY}">Ayam</text>'
            f'<text x="486" y="1060" font-family="Fredoka" font-weight="700" font-size="40" fill="#1e88e5">Bb</text>'
            f'<text x="560" y="1058" font-family="Fredoka" font-weight="600" font-size="30" fill="{C.NAVY}">Bola</text>')
    out += O.place(Pen(True, "obA"), O.ayam, 260, 1150, 0.42)
    out += O.place(Pen(False, "obB"), O.bola, 650, 1146, 0.4)
    out += (f'<g transform="rotate(-24 790 1130)">'
            + C.p("M720,1120 L830,1120 L856,1130 L830,1140 L720,1140 Z", "#43a047", stroke=C.NAVY, w=2.5)
            + '<rect x="734" y="1120" width="14" height="20" fill="#fff" opacity="0.6"/></g>')
    return out


def front_cover_svg(px_w=2480, px_h=3508):
    pen = Pen(True, "fc")
    out = [BUDAYA.svg_open(px_w, px_h), C.defs(), BUDAYA.front_background(), floating_shapes()]
    cast = [("amir", 115, "A", "#e53935"), ("aisyah", 283, "B", "#1e88e5"), ("mei", 451, "C", "#43a047"),
            ("ravi", 619, "1", "#fb8c00"), ("lina", 787, "2", "#8e24aa")]
    la, ra = (-44, -150), (44, -150)
    for who, x, label, color in cast:
        out.append(kid(pen, who, x, 1080, 0.85, la=la, ra=ra, arms_front=True, hands=False))
        out.append(block(pen, x - 36, 1080 - 192 * 0.85, label, color))
        out.append(kid_hands(pen, who, x, 1080, 0.85, la=la, ra=ra))
    out.append(open_book())
    for x, y, s in ((24, 1110, 0.9), (884, 1112, 0.9), (20, 1262, 0.8), (888, 1262, 0.8)):
        out.append(C.flower(x, y, s))
    out.append(BUDAYA.logo_badge())
    out.append(C.ribbon("SIRI 10", y=124))
    out.append(C.bubbly("ABC 123", base_y=338, max_w=760, font_size=210))
    out.append(f'<rect x="222" y="368" width="460" height="48" rx="24" fill="#8e24aa" stroke="#ffffff" stroke-width="4"/>'
               f'<text x="452" y="402" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="28" '
               f'letter-spacing="1" fill="#ffffff">Huruf • Nombor • Bentuk</text>')
    out.append(f'<g transform="translate(0,96)">{C.sign()}{C.badge(str(PAGES))}</g>')
    out.append("</svg>")
    return "\n".join(out)


# ---------------------------------------------------------------- back

def icon_abc(cx, cy):
    out = ""
    for i, (ch, c) in enumerate((("A", "#e53935"), ("B", "#1e88e5"), ("C", "#43a047"))):
        out += (f'<text x="{cx - 34 + i * 34}" y="{cy + 16}" text-anchor="middle" font-family="Fredoka" '
                f'font-weight="700" font-size="40" fill="{c}" stroke="{C.NAVY}" stroke-width="2">{ch}</text>')
    return out


def icon_123(cx, cy):
    out = ""
    for i, (ch, c) in enumerate((("1", "#fb8c00"), ("2", "#8e24aa"), ("3", "#00acc1"))):
        out += (f'<text x="{cx - 30 + i * 30}" y="{cy + 16}" text-anchor="middle" font-family="Fredoka" '
                f'font-weight="700" font-size="42" fill="{c}" stroke="{C.NAVY}" stroke-width="2">{ch}</text>')
    return out


def icon_shapes(cx, cy):
    return (f'<circle cx="{cx - 28}" cy="{cy - 12}" r="17" fill="#e53935" stroke="{C.NAVY}" stroke-width="2.5"/>'
            + C.p(f"M{cx + 26},{cy - 32} L{cx + 46},{cy + 2} L{cx + 6},{cy + 2} Z", "#fdd835", stroke=C.NAVY, w=2.5)
            + f'<rect x="{cx - 14}" y="{cy + 8}" width="30" height="30" fill="#42a5f5" stroke="{C.NAVY}" stroke-width="2.5"/>')


BLURB = ["Buku ini direka khas untuk membantu",
         "kanak-kanak prasekolah mengenal huruf A-Z,",
         "nombor 1 hingga 10 dan bentuk asas",
         "sambil berseronok mewarna."]
TILES = [("#f8bbd0", BC.icon_crayon, ["Melatih", "kemahiran", "motor halus"]),
         ("#bbdefb", icon_abc, ["Mengenal", "huruf", "A hingga Z"]),
         ("#fff59d", icon_123, ["Belajar", "mengira", "1 hingga 10"]),
         ("#c5e1a5", icon_shapes, ["Mengenal", "7 bentuk", "asas"])]


def book_art(pen):
    return (f'<text x="486" y="980" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="44" '
            f'fill="#e53935" stroke="{INK}" stroke-width="2.5">A<tspan fill="#1e88e5">B</tspan>'
            f'<tspan fill="#43a047">C</tspan></text>')


def back_cover_svg(px_w=2480, px_h=3508):
    return BC.back_cover_svg(px_w, px_h, series="Huruf, Nombor dan Bentuk", lines=BLURB, tiles=TILES,
                             tagline="Mewarna, Membaca, Mengira dengan Ceria",
                             books=["Mewarna", "Membaca", "Mengira", "Menulis", "Berakhlak"],
                             kids=lambda: BUDAYA.back_kids(book_art))
