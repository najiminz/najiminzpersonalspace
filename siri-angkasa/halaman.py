"""The 30 pages of Siri 7: Angkasa Lepas, drawn straight in page coordinates.

Same page template, thick lines and recurring cast as the other series. The
children wear space suits (outfit="angkasawan"). Planets, the sun and stars
get the cast's friendly face.
"""
import math
import random

from characters import HEAD_SCALE, NECK, face, kid
from draw import DW, GLASS, INK, LW, W, blob_d, cloud, star_d
from subjects import jalur_gemilang, small_house, tufts

NAVY = "#1a237e"


def circle_d(cx, cy, r):
    return f"M{cx - r},{cy} A{r},{r} 0 1 0 {cx + r},{cy} A{r},{r} 0 1 0 {cx - r},{cy} Z"


def scaled(pen, s, cx, cy, fn):
    """Draw fn(pen) (in local coords around 0,0) at (cx, cy) scaled by s with even line weight."""
    k0 = pen.k
    pen.k = k0 / s
    svg = fn(pen)
    pen.k = k0
    return f'<g transform="translate({cx:.1f},{cy:.1f}) scale({s})">{svg}</g>'


def cute(pen, cx, cy, s=1.0):
    return scaled(pen, s, cx, cy, lambda p: face(p, {}, cx=0, cy=-14, gap=26))


def astro(pen, who, x, y, s, rot=0, **kw):
    svg = kid(pen, who, x, y, s, outfit="angkasawan", **kw)
    return f'<g transform="rotate({rot} {x} {y - 160 * s})">{svg}</g>' if rot else svg


# ---------------------------------------------------------------- backgrounds

def sparkle(pen, x, y, r):
    return pen.path(f"M{x},{y - r} Q{x},{y} {x + r},{y} Q{x},{y} {x},{y + r} Q{x},{y} {x - r},{y} Q{x},{y} {x},{y - r} Z",
                    fill="#fff59d", w=1.8)


def starfield(pen, seed=1, n=30, y1=1250):
    rnd = random.Random(seed)
    out = ""
    for i in range(n):
        x, y = rnd.uniform(40, 870), rnd.uniform(170, y1)
        kind = i % 3
        if kind == 0:
            out += pen.path(star_d(x, y, 13, 6), fill="#fff59d", w=1.8)
        elif kind == 1:
            out += sparkle(pen, x, y, 12)
        else:
            out += pen.circle(x, y, 4, fill="#ffffff", sw=1.4)
    return out


def ringed(pen, cx, cy, r, color="#ce93d8"):
    out = pen.ellipse(cx, cy, r * 1.9, r * 0.5, fill="none", sw=DW, rot=-15)
    out += pen.circle(cx, cy, r, fill=color, sw=DW)
    return out + pen.path(f"M{cx - r * 1.8:.0f},{cy + r * 0.62:.0f} Q{cx},{cy + r * 0.1:.0f} {cx + r * 1.75:.0f},"
                          f"{cy - r * 0.55:.0f}", fill="none", w=DW)


def space(pen, seed=1, extras=True, color="#1a237e"):
    out = f'<rect width="{W}" height="1280" fill="{color}"/>' if pen.colored else ""
    out += starfield(pen, seed)
    if extras:
        out += ringed(pen, 110, 300, 26)
        out += pen.circle(470, 230, 18, fill="#80cbc4", sw=DW) + pen.path("M456,226 Q470,220 484,228", fill="none", w=1.4)
    return out


def night(pen, ground_y=1040, seed=3):
    out = f'<rect width="{W}" height="{ground_y}" fill="#283593"/>' if pen.colored else ""
    out += starfield(pen, seed, n=18, y1=ground_y - 120)
    out += pen.path(f"M18,{ground_y} Q160,{ground_y - 110} 330,{ground_y - 40} Q520,{ground_y - 140} 700,{ground_y - 50} "
                    f"Q800,{ground_y - 90} 887,{ground_y - 40} L887,1280 L18,1280 Z", fill="#2e7d32")
    out += pen.path(f"M18,{ground_y + 20} Q300,{ground_y - 20} 600,{ground_y + 10} Q760,{ground_y + 24} 887,{ground_y}",
                    fill="none", w=DW)
    return out + tufts(pen, 14, ground_y + 2, ground_y + 40, y1=1250)


def day(pen, ground_y=1060, seed=5):
    out = f'<rect width="{W}" height="{ground_y}" fill="#bfe7fb"/>' if pen.colored else ""
    out += cloud(pen, 46, 196, 210, 84) + cloud(pen, 280, 300, 130, 52)
    out += f'<rect y="{ground_y}" width="{W}" height="300" fill="#c5e1a5"/>' if pen.colored else ""
    out += pen.line(18, ground_y, 887, ground_y, sw=LW)
    return out + tufts(pen, 14, seed, ground_y + 30, y1=1250)


def crater(pen, x, y, rx, ry, fill="#9e9e9e"):
    out = pen.ellipse(x, y, rx, ry, fill=fill, sw=DW)
    return out + pen.path(f"M{x - rx * 0.8:.0f},{y - ry * 0.1:.0f} Q{x},{y - ry * 0.9:.0f} {x + rx * 0.8:.0f},"
                          f"{y - ry * 0.1:.0f}", fill="none", w=1.4)


def moon_ground(pen, y=1060, seed=2):
    d = (f"M18,{y} Q140,{y - 40} 260,{y - 10} Q420,{y + 20} 560,{y - 20} Q720,{y - 50} 887,{y - 10} "
         f"L887,1280 L18,1280 Z")
    out = pen.path(d, fill="#cfd8dc")
    rnd = random.Random(seed)
    inner = ""
    for _ in range(9):
        x, yy = rnd.uniform(60, 840), rnd.uniform(y + 40, 1240)
        r = rnd.uniform(22, 48)
        inner += crater(pen, round(x), round(yy), round(r), round(r * 0.35), fill="#b0bec5")
    for _ in range(10):
        inner += pen.circle(round(rnd.uniform(40, 860)), round(rnd.uniform(y + 20, 1250)), 5, fill="#b0bec5", sw=1.4)
    return out + pen.clipped(d, inner)


def rock(pen, x, y, r, seed, fill="#a1887f"):
    return pen.path(blob_d(x, y, r, r * 0.7, 7, seed, flat_bottom=True), fill=fill, w=DW)


def mars_ground(pen, y=1040, seed=4):
    sky = f'<rect width="{W}" height="{y}" fill="#ffccbc"/>' if pen.colored else ""
    d = f"M18,{y} Q200,{y - 60} 380,{y - 10} Q600,{y + 30} 887,{y - 30} L887,1280 L18,1280 Z"
    hills = pen.path(f"M18,{y - 20} L150,{y - 180} L260,{y - 90} L400,{y - 220} L560,{y - 70} L700,{y - 160} "
                     f"L887,{y - 60} L887,{y} L18,{y} Z", fill="#ffab91")
    out = sky + hills + pen.path(d, fill="#e57350")
    rnd = random.Random(seed)
    for _ in range(9):
        out += rock(pen, round(rnd.uniform(60, 840)), round(rnd.uniform(y + 40, 1240)), round(rnd.uniform(16, 34)),
                    rnd.randint(1, 99), fill="#bf5b3c")
    for yy in (y + 60, y + 150):
        out += pen.path(f"M60,{yy} Q300,{yy - 20} 500,{yy + 10} Q700,{yy + 26} 860,{yy}", fill="none", w=1.6)
    return out


# ---------------------------------------------------------------- planets

def planet(pen, cx, cy, r, color, inner="", with_face=True, face_s=None):
    d = circle_d(cx, cy, r)
    out = pen.circle(cx, cy, r, fill=color) + pen.clipped(d, inner) + pen.circle(cx, cy, r, fill="none")
    if with_face:
        out += cute(pen, cx, cy + r * 0.12, face_s or r / 110)
    return out


def craters(pen, cx, cy, r, seed, n=9, fill="#9e9e9e", skip_face=True):
    rnd = random.Random(seed)
    out = ""
    for _ in range(n):
        a, d = rnd.uniform(0, 2 * math.pi), rnd.uniform(0.3, 0.95) * r
        x, y = cx + d * math.cos(a), cy + d * math.sin(a)
        if skip_face and abs(x - cx) < r * 0.5 and abs(y - cy - r * 0.05) < r * 0.4:
            continue
        rr = rnd.uniform(0.07, 0.16) * r
        out += crater(pen, round(x), round(y), round(rr), round(rr * 0.8), fill=fill)
    return out


def bands(pen, cx, cy, r, colors, wavy=10, n=9):
    out = ""
    for i in range(n):
        y0 = cy - r + 2 * r * i / n
        h = 2 * r / n
        c = colors[i % len(colors)]
        d = (f"M{cx - r - 10},{y0:.0f} " + "".join(f"q{r / 4:.0f},{wavy if k % 2 else -wavy} {r / 2:.0f},0 "
                                                   for k in range(5)) +
             f"L{cx + r + 10},{y0 + h:.0f} L{cx - r - 10},{y0 + h:.0f} Z")
        out += pen.path(d, fill=c, w=1.8)
    return out


def earth_inner(pen, cx, cy, r):
    out = ""
    for x, y, rx, ry, sd in ((-0.55, -0.35, 0.32, 0.28, 3), (0.5, -0.45, 0.35, 0.22, 4), (-0.35, 0.55, 0.3, 0.25, 5),
                             (0.6, 0.45, 0.28, 0.3, 6), (0.0, -0.8, 0.22, 0.12, 7)):
        out += pen.path(blob_d(cx + x * r, cy + y * r, rx * r, ry * r, 8, sd), fill="#66bb6a", w=DW)
    out += pen.path(f"M{cx - r},{cy + r * 0.05:.0f} Q{cx - r * 0.5:.0f},{cy - r * 0.08:.0f} {cx},{cy + r * 0.02:.0f}",
                    fill="none", w=1.6)
    return out + pen.ellipse(cx, cy - r * 0.97, r * 0.45, r * 0.12, fill="#ffffff", sw=DW)


def mini_planet(pen, kind, cx, cy, r):
    if kind == "utarid":
        return planet(pen, cx, cy, r, "#bdbdbd", craters(pen, cx, cy, r, 1, 6, skip_face=False), with_face=False)
    if kind == "zuhrah":
        return planet(pen, cx, cy, r, "#ffcc80", bands(pen, cx, cy, r, ["#ffcc80", "#ffe0b2"], 4, 5), with_face=False)
    if kind == "bumi":
        return planet(pen, cx, cy, r, "#42a5f5", earth_inner(pen, cx, cy, r), with_face=False)
    if kind == "marikh":
        return planet(pen, cx, cy, r, "#e57350", craters(pen, cx, cy, r, 2, 5, "#bf5b3c", False), with_face=False)
    if kind == "musytari":
        inner = bands(pen, cx, cy, r, ["#ffcc80", "#d7a86e", "#fff3e0"], 5, 7)
        inner += pen.ellipse(cx + r * 0.3, cy + r * 0.3, r * 0.22, r * 0.13, fill="#e57373", sw=1.6)
        return planet(pen, cx, cy, r, "#ffcc80", inner, with_face=False)
    if kind == "zuhal":
        out = pen.ellipse(cx, cy, r * 2.0, r * 0.5, fill="none", sw=DW, rot=-12)
        out += planet(pen, cx, cy, r, "#ffe082", bands(pen, cx, cy, r, ["#ffe082", "#ffecb3"], 4, 5), with_face=False)
        return out + pen.path(f"M{cx - r * 1.95:.0f},{cy + r * 0.45:.0f} Q{cx},{cy + r * 0.25:.0f} {cx + r * 1.95:.0f},"
                              f"{cy - r * 0.38:.0f}", fill="none", w=DW)
    if kind == "uranus":
        out = pen.ellipse(cx, cy, r * 0.4, r * 1.6, fill="none", sw=DW, rot=10)
        return out + planet(pen, cx, cy, r, "#80deea", with_face=False)
    return planet(pen, cx, cy, r, "#5c6bc0", pen.ellipse(cx + r * 0.2, cy, r * 0.25, r * 0.14, fill="#283593", sw=1.4),
                  with_face=False)


def sun_disc(pen, cx, cy, r, rays=16, face_s=None):
    out = ""
    for k in range(rays):
        a = 2 * math.pi * k / rays
        long = 1.45 if k % 2 == 0 else 1.25
        b, c = a - math.pi / rays * 0.7, a + math.pi / rays * 0.7
        out += pen.path(f"M{cx + r * 0.95 * math.cos(b):.1f},{cy + r * 0.95 * math.sin(b):.1f} "
                        f"L{cx + r * long * math.cos(a):.1f},{cy + r * long * math.sin(a):.1f} "
                        f"L{cx + r * 0.95 * math.cos(c):.1f},{cy + r * 0.95 * math.sin(c):.1f} Z",
                        fill="#ffb300" if k % 2 == 0 else "#ffd54f")
    out += pen.circle(cx, cy, r, fill="#fdd835")
    out += pen.circle(cx, cy, r * 0.82, fill="none", sw=1.8)
    return out + cute(pen, cx, cy + r * 0.1, face_s or r / 100)


# ---------------------------------------------------------------- machines

def porthole(pen, x, y, r):
    return pen.circle(x, y, r + 6, fill="#b0bec5", sw=DW) + pen.circle(x, y, r, fill=GLASS, sw=DW)


def rocket(pen, cx, base, h=700, flame=False, label=True):
    w = h * 0.24
    top = base - h
    out = ""
    if flame:
        out += pen.path(f"M{cx - w * 0.4},{base} Q{cx - w * 0.6},{base + h * 0.25} {cx},{base + h * 0.42} "
                        f"Q{cx + w * 0.6},{base + h * 0.25} {cx + w * 0.4},{base} Z", fill="#ff7043")
        out += pen.path(f"M{cx - w * 0.22},{base} Q{cx - w * 0.3},{base + h * 0.16} {cx},{base + h * 0.28} "
                        f"Q{cx + w * 0.3},{base + h * 0.16} {cx + w * 0.22},{base} Z", fill="#fdd835")
    for s in (-1, 1):
        out += pen.path(f"M{cx + s * w * 0.5},{base - h * 0.32} Q{cx + s * w * 1.15},{base - h * 0.12} "
                        f"{cx + s * w * 1.1},{base + h * 0.02} L{cx + s * w * 0.5},{base - h * 0.06} Z", fill="#e53935")
    out += pen.rect(cx - w * 0.36, base - h * 0.06, w * 0.72, h * 0.07, fill="#78909c", rx=6)
    body = (f"M{cx - w * 0.5},{base - h * 0.04} L{cx - w * 0.5},{top + h * 0.36} "
            f"Q{cx - w * 0.5},{top + h * 0.1} {cx},{top} Q{cx + w * 0.5},{top + h * 0.1} {cx + w * 0.5},{top + h * 0.36} "
            f"L{cx + w * 0.5},{base - h * 0.04} Z")
    out += pen.path(body, fill="#eceff1")
    stripes = (pen.fillrect(cx - w, top, w * 2, h * 0.17, "#e53935") +
               pen.fillrect(cx - w, base - h * 0.2, w * 2, h * 0.05, "#1e88e5") +
               pen.fillrect(cx - w, base - h * 0.13, w * 2, h * 0.05, "#fdd835"))
    out += pen.clipped(body, stripes) + pen.path(body, fill="none")
    for k, yy in enumerate((0.3, 0.45)):
        out += porthole(pen, cx, top + h * yy, w * 0.18)
    for k in range(1, 4):
        out += pen.line(cx - w * 0.5, top + h * (0.58 + k * 0.06), cx + w * 0.5, top + h * (0.58 + k * 0.06), sw=1.4)
    for x in (cx - w * 0.36, cx + w * 0.36):
        for k in range(8):
            out += pen.circle(x, top + h * (0.2 + k * 0.08), 3, fill="#b0bec5", sw=1.0)
    if label:
        out += pen.text(cx, top + h * 0.72, "MALAYSIA", w * 0.17, fill_color=NAVY, spacing=1,
                        extra=f'transform="rotate(-90 {cx} {top + h * 0.72})" dominant-baseline="middle"')
    return out


def cloud_puffs(pen, cx, cy, w, h, seed):
    return pen.path(blob_d(cx, cy, w, h, 11, seed, flat_bottom=True), fill="#eceff1")


def solar_panel(pen, x, y, w, h, cols=4, rows=3, fill="#3949ab"):
    out = pen.rect(x, y, w, h, fill=fill, rx=3)
    for i in range(1, cols):
        out += pen.line(x + w * i / cols, y, x + w * i / cols, y + h, sw=1.6)
    for j in range(1, rows):
        out += pen.line(x, y + h * j / rows, x + w, y + h * j / rows, sw=1.6)
    return out


def earth_arc(pen, cy=1500, r=520):
    d = circle_d(452, cy, r)
    out = pen.circle(452, cy, r, fill="#42a5f5")
    inner = ""
    for x, y, rx, ry, sd in ((150, cy - r + 120, 140, 70, 1), (560, cy - r + 70, 170, 60, 2), (820, cy - r + 160, 90, 80, 3),
                             (330, cy - r + 230, 110, 60, 4)):
        inner += pen.path(blob_d(x, y, rx, ry, 9, sd), fill="#66bb6a", w=DW)
    for x, y in ((260, cy - r + 50), (700, cy - r + 130)):
        inner += pen.path(f"M{x - 60},{y} q30,-20 60,0 q30,20 60,0", fill="none", w=DW)
    return out + pen.clipped(d, inner) + pen.circle(452, cy, r, fill="none")


def glasses(pen, x, y, s, look_y=-258):
    """Eclipse glasses over the cast's eyes (drawn in the same shrunken head space as the face)."""
    def draw(p):
        k0 = p.k
        p.k = k0 / HEAD_SCALE
        g = (p.rect(-46, look_y - 18, 40, 34, fill="#424242", rx=9) + p.rect(6, look_y - 18, 40, 34, fill="#424242", rx=9)
             + p.line(-6, look_y - 6, 6, look_y - 6, sw=DW))
        p.k = k0
        return f'<g transform="translate(0,{NECK}) scale({HEAD_SCALE}) translate(0,{-NECK})">{g}</g>'
    return scaled(pen, s, x, y, draw)


# ---------------------------------------------------------------- pages 1-11: sistem suria

ORDER = ["utarid", "zuhrah", "bumi", "marikh", "musytari", "zuhal", "uranus", "neptun"]


def s_sistem_suria(pen):
    out = ""
    for k in range(8):
        rx = 250 + k * 86
        out += (f'<ellipse cx="-40" cy="790" rx="{rx}" ry="{rx * 0.62:.0f}" fill="none" stroke="{INK}" '
                f'stroke-width="{pen.sw(1.6)}" stroke-dasharray="{pen.sw(8)} {pen.sw(8)}"/>')
    out += sun_disc(pen, -40, 790, 190, face_s=1.2)
    sizes = [16, 22, 24, 19, 52, 40, 30, 28]
    angles = [-28, 18, -12, 30, -20, 14, -8, 24]
    for k, kind in enumerate(ORDER):
        rx = 250 + k * 86
        a = math.radians(angles[k])
        out += mini_planet(pen, kind, -40 + rx * math.cos(a), 790 + rx * 0.62 * math.sin(a), sizes[k])
    out += astro(pen, "ravi", 760, 1230, 0.42, rot=12, la=(-80, -200), ra=(70, -112))
    return out


def s_matahari(pen):
    out = sun_disc(pen, 452, 790, 220, rays=18, face_s=2.2)
    for x, y, r in ((380, 690, 14), (540, 860, 10), (560, 700, 8)):
        out += pen.circle(x, y, r, fill="#ffb300", sw=1.6)
    out += mini_planet(pen, "utarid", 130, 1160, 34) + mini_planet(pen, "zuhrah", 790, 1180, 44)
    return out


def planet_page(kind, r=230, extra=None, face=True):
    color = {"utarid": "#bdbdbd", "zuhrah": "#ffcc80", "bumi": "#42a5f5", "bulan": "#e0e0e0", "marikh": "#e57350",
             "musytari": "#ffcc80", "uranus": "#80deea", "neptun": "#5c6bc0"}[kind]

    def subject(pen):
        cx, cy = 452, 790
        inner = ""
        if kind in ("utarid", "bulan"):
            inner = craters(pen, cx, cy, r, 11 if kind == "utarid" else 12, 14, "#bdbdbd" if kind == "bulan" else "#9e9e9e")
        elif kind == "zuhrah":
            inner = bands(pen, cx, cy, r, ["#ffcc80", "#ffe0b2", "#ffb74d"], 14, 9)
        elif kind == "bumi":
            inner = earth_inner(pen, cx, cy, r)
        elif kind == "marikh":
            inner = craters(pen, cx, cy, r, 13, 12, "#bf5b3c")
            inner += pen.ellipse(cx, cy - r * 0.95, r * 0.4, r * 0.12, fill="#ffffff", sw=DW)
            inner += pen.path(f"M{cx - r},{cy + r * 0.55:.0f} Q{cx},{cy + r * 0.4:.0f} {cx + r},{cy + r * 0.6:.0f}",
                              fill="none", w=1.8)
        elif kind == "musytari":
            inner = bands(pen, cx, cy, r, ["#ffcc80", "#d7a86e", "#fff3e0", "#ffab91"], 12, 11)
            inner += pen.ellipse(cx + r * 0.42, cy + r * 0.48, r * 0.22, r * 0.12, fill="#e57373", sw=DW)
            inner += pen.ellipse(cx + r * 0.42, cy + r * 0.48, r * 0.12, r * 0.06, fill="#ef9a9a", sw=1.4)
        elif kind == "uranus":
            inner = bands(pen, cx, cy, r, ["#80deea", "#b2ebf2"], 4, 7)
        elif kind == "neptun":
            inner = bands(pen, cx, cy, r, ["#5c6bc0", "#7986cb"], 8, 7)
            inner += pen.ellipse(cx - r * 0.45, cy + r * 0.45, r * 0.18, r * 0.1, fill="#283593", sw=DW)
            for k in range(4):
                inner += pen.path(f"M{cx - r * 0.2 + k * 30},{cy - r * 0.55 + k * 18} q40,-10 80,0", fill="none", w=1.8)
        out = ""
        if kind == "uranus":
            out += pen.ellipse(cx, cy, r * 0.32, r * 1.55, fill="none", sw=DW + 2, rot=8)
        out += planet(pen, cx, cy, r, color, inner, with_face=face, face_s=r / 105)
        if extra:
            out += extra(pen)
        return out
    return subject


def s_zuhal(pen):
    cx, cy, r = 452, 800, 190
    ring = (f"M{-r * 2.25},0 A{r * 2.25},{r * 0.62} 0 1 0 {r * 2.25},0 A{r * 2.25},{r * 0.62} 0 1 0 {-r * 2.25},0 Z "
            f"M{-r * 1.35},0 A{r * 1.35},{r * 0.34} 0 1 1 {r * 1.35},0 A{r * 1.35},{r * 0.34} 0 1 1 {-r * 1.35},0 Z")
    rings = (f'<path d="{ring}" fill="{pen.f("#ffe0b2")}" fill-rule="evenodd" stroke="{INK}" stroke-width="{pen.sw(LW)}"/>'
             + "".join(f'<ellipse cx="0" cy="0" rx="{r * f:.0f}" ry="{r * f * 0.27:.0f}" fill="none" stroke="{INK}" '
                       f'stroke-width="{pen.sw(1.6)}"/>' for f in (1.6, 1.85, 2.05)))
    cid = pen.uid("ring")
    hide = (f'<clipPath id="{cid}"><path clip-rule="evenodd" d="M-2000,-2000 H2000 V2000 H-2000 Z '
            f'M{-r},0 A{r},{r} 0 0 1 {r},0 Z"/></clipPath>')
    body = planet(pen, 0, 0, r, "#ffe082", bands(pen, 0, 0, r, ["#ffe082", "#ffecb3", "#ffca28"], 10, 9), with_face=False)
    out = f'<g transform="translate({cx},{cy}) rotate(-14)">{rings}{body}{hide}<g clip-path="url(#{cid})">{rings}</g></g>'
    out += cute(pen, cx, cy + 20, 1.8)
    for x, y, rr in ((130, 520, 22), (790, 520, 16), (180, 1160, 18), (760, 1130, 26)):
        out += pen.circle(x, y, rr, fill="#e0e0e0", sw=DW) + crater(pen, x - rr * 0.3, y - rr * 0.2, rr * 0.3, rr * 0.22)
    return out


def moons(cx_list):
    def draw(pen):
        out = ""
        for x, y, r in cx_list:
            out += pen.circle(x, y, r, fill="#e0e0e0", sw=DW) + crater(pen, round(x - r * 0.3), round(y - r * 0.2),
                                                                       round(r * 0.3), round(r * 0.22))
        return out
    return draw


def lumpy(pen, x, y, r, seed, fill="#a1887f", face_s=None):
    d = blob_d(x, y, r, r * 0.8, 9, seed)
    out = pen.path(d, fill=fill) + pen.clipped(d, craters(pen, x, y, r, seed, 5, "#8d6e63", False))
    out += pen.path(d, fill="none")
    return out + (cute(pen, x, y + r * 0.1, face_s) if face_s else "")


def small_rocket(pen, x, y, s, rot):
    return f'<g transform="rotate({rot} {x} {y})">{scaled(pen, s, x, y, lambda p: rocket(p, 0, 350, 700, flame=True, label=False))}</g>'


def satellite(pen, cx, cy, s=1.0):
    def draw(p):
        out = p.tube("M-120,0 L120,0", 10, "#9e9e9e")
        for x in (-330, 130):
            out += solar_panel(p, x, -70, 200, 140, 5, 3)
        out += p.rect(-90, -90, 180, 180, fill="#ffca28", rx=10)
        for k in range(1, 4):
            out += p.path(f"M{-90 + k * 45},-90 L{-90 + k * 45 - 10},90", fill="none", w=1.4)
        out += p.path("M-20,-90 L-30,-170 M20,-90 L30,-170", fill="none", w=DW)
        out += p.path("M-80,-230 Q0,-150 80,-230 Q0,-200 -80,-230 Z", fill="#eceff1")
        out += p.line(0, -205, 0, -250, sw=DW) + p.circle(0, -254, 8, fill="#e53935", sw=DW)
        out += p.circle(0, 0, 40, fill=GLASS, sw=DW) + p.circle(0, 0, 18, fill="#1e88e5", sw=1.6)
        out += p.line(0, 90, 0, 150, sw=DW) + p.circle(0, 156, 10, fill="#e53935", sw=DW)
        return out
    return scaled(pen, s, cx, cy, draw)


def tail(pen, x0, y0, x1, y1, width, color, n=4):
    out = ""
    for k in range(n):
        off = (k - (n - 1) / 2) * width * 0.6
        out += pen.tube(f"M{x0},{y0 + off} Q{(x0 + x1) / 2 + off},{(y0 + y1) / 2 - 60} {x1},{y1 + off * 2}",
                        width * (1 - k * 0.12), color)
    return out


# ---------------------------------------------------------------- pages 12-18: langit

def s_bintang(pen):
    out = pen.path(star_d(560, 640, 230, 100), fill="#fdd835") + cute(pen, 560, 680, 2.0)
    for x, y, r, c in ((160, 520, 70, "#ffb74d"), (780, 1000, 60, "#f48fb1"), (380, 1110, 54, "#80deea")):
        out += pen.path(star_d(x, y, r, r * 0.45), fill=c) + cute(pen, x, y + r * 0.2, r / 115)
    out += pen.path("M60,980 L230,880", fill="none", w=1.8) + pen.path("M60,1000 L230,900", fill="none", w=1.8)
    out += pen.path(star_d(250, 870, 36, 16), fill="#fff59d")
    moon = "M820,420 A90,90 0 1 0 870,560 A70,70 0 1 1 820,420 Z"
    out += pen.path(moon, fill="#fff59d")
    out += astro(pen, "aisyah", 600, 1240, 0.55, la=(-80, -220), ra=(70, -112))
    return out


def con_star(pen, x, y, r=14):
    return pen.path(star_d(x, y, r, r * 0.45), fill="#fff59d", w=DW)


def constellation(pen, pts, links):
    out = ""
    for a, b in links:
        out += (f'<line x1="{pts[a][0]}" y1="{pts[a][1]}" x2="{pts[b][0]}" y2="{pts[b][1]}" stroke="{INK}" '
                f'stroke-width="{pen.sw(2)}" stroke-dasharray="{pen.sw(8)} {pen.sw(6)}"/>')
    return out + "".join(con_star(pen, x, y, 18 if i == 0 else 14) for i, (x, y) in enumerate(pts))


def s_buruj(pen):
    biduk = [(90, 230), (170, 250), (250, 240), (320, 280), (330, 360), (440, 370), (450, 290)]
    out = constellation(pen, biduk, [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 3)])
    pari = [(740, 470), (740, 640), (660, 560), (820, 560), (770, 600)]
    out += constellation(pen, pari, [(0, 1), (2, 3)])
    belantik = [(240, 500), (420, 520), (290, 640), (330, 650), (370, 660), (220, 800), (440, 790)]
    out += constellation(pen, belantik, [(0, 2), (1, 4), (2, 3), (3, 4), (2, 5), (4, 6)])
    out += pen.path("M600,780 A60,60 0 1 0 640,880 A46,46 0 1 1 600,780 Z", fill="#fff59d")
    out += small_house(pen, 760, 1000, 130)
    out += kid(pen, "mei", 250, 1200, 0.85, la=(-90, -300), ra=(60, -112))
    out += kid(pen, "ravi", 470, 1210, 0.85, la=(-60, -112), ra=(90, -300))
    return out


def s_komet(pen):
    out = tail(pen, 640, 560, 70, 1150, 60, "#b3e5fc")
    for x, y in ((300, 900), (200, 1020), (450, 780), (130, 1100)):
        out += sparkle(pen, x, y, 14)
    out += pen.path(blob_d(650, 560, 110, 100, 10, 8), fill="#e1f5fe") + cute(pen, 650, 575, 1.3)
    out += mini_planet(pen, "musytari", 160, 470, 70) + mini_planet(pen, "marikh", 780, 1080, 50)
    return out


def meteor(pen, x, y, r, seed):
    out = pen.path(f"M{x + r * 0.5},{y - r * 0.6} L{x + r * 4},{y - r * 4.2}", fill="none", w=DW + 6)
    out += pen.path(f"M{x + r * 0.8},{y} L{x + r * 4.5},{y - r * 3.4}", fill="none", w=DW)
    out += pen.path(f"M{x},{y - r * 0.8} L{x + r * 3.2},{y - r * 4.6}", fill="none", w=DW)
    return out + lumpy(pen, x, y, r, seed, "#ff8a65")


def s_meteor(pen):
    out = ""
    for x, y, r, sd in ((120, 470, 26, 1), (330, 560, 34, 2), (560, 680, 30, 3), (200, 760, 22, 4), (720, 860, 26, 5),
                        (430, 400, 20, 6)):
        out += meteor(pen, x, y, r, sd)
    out += small_house(pen, 760, 1010, 150)
    out += kid(pen, "amir", 230, 1210, 0.95, la=(-60, -112), ra=(100, -290))
    out += kid(pen, "aisyah", 480, 1220, 0.9, la=(-60, -112), ra=(60, -112))
    return out


def s_asteroid(pen):
    out = ""
    for x, y, r, sd in ((140, 470, 46, 1), (330, 410, 30, 2), (780, 520, 40, 3), (110, 1050, 54, 4), (780, 1120, 60, 5),
                        (560, 1180, 34, 6), (300, 1170, 28, 7)):
        out += lumpy(pen, x, y, r, sd)
    out += lumpy(pen, 452, 780, 210, 9, "#bcaaa4", face_s=1.8)
    out += f'<path d="M100,700 Q200,560 300,620" fill="none" stroke="{INK}" stroke-width="{pen.sw(2)}" ' \
           f'stroke-dasharray="{pen.sw(6)} {pen.sw(8)}"/>'
    out += small_rocket(pen, 330, 600, 0.22, 60)
    return out


def s_galaksi(pen):
    cx, cy = 452, 780
    out = ""
    for arm in range(3):
        pts = []
        for k in range(40):
            t = k / 39
            a = arm * 2 * math.pi / 3 + t * 3.4
            r = 70 + t * 330
            pts.append((cx + r * math.cos(a), cy + r * 0.72 * math.sin(a)))
        for k in range(0, 39, 3):
            w = 70 * (1 - k / 45)
            seg = pts[k:k + 4]
            d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in seg)
            out += pen.tube(d, w, "#b39ddb")
    out += pen.ellipse(cx, cy, 110, 80, fill="#fff59d") + pen.ellipse(cx, cy, 60, 44, fill="#ffffff", sw=DW)
    rnd = random.Random(11)
    for _ in range(26):
        a, r = rnd.uniform(0, 2 * math.pi), rnd.uniform(130, 380)
        out += pen.circle(cx + r * math.cos(a), cy + r * 0.72 * math.sin(a), 5, fill="#ffffff", sw=1.4)
    for x, y in ((140, 1150), (780, 460)):
        out += pen.ellipse(x, y, 60, 26, fill="#f8bbd0", rot=-20) + pen.ellipse(x, y, 20, 10, fill="#fff59d", sw=1.6, rot=-20)
    out += astro(pen, "lina", 760, 1240, 0.45, rot=-10, la=(-90, -220), ra=(70, -112))
    return out


def s_gerhana(pen):
    cx, cy = 452, 560
    out = ""
    for k in range(24):
        a = 2 * math.pi * k / 24
        l = 1.55 if k % 2 == 0 else 1.32
        out += pen.path(f"M{cx + 150 * math.cos(a - 0.12):.0f},{cy + 150 * math.sin(a - 0.12):.0f} "
                        f"Q{cx + 190 * math.cos(a + 0.1):.0f},{cy + 190 * math.sin(a + 0.1):.0f} "
                        f"{cx + 150 * l * math.cos(a):.0f},{cy + 150 * l * math.sin(a):.0f} "
                        f"Q{cx + 170 * math.cos(a - 0.15):.0f},{cy + 170 * math.sin(a - 0.15):.0f} "
                        f"{cx + 150 * math.cos(a + 0.12):.0f},{cy + 150 * math.sin(a + 0.12):.0f} Z", fill="#ffb300", w=DW)
    out += pen.circle(cx, cy, 168, fill="#fdd835") + pen.circle(cx, cy, 150, fill="#455a64")
    out += scaled(pen, 1.4, cx, cy + 20, lambda p: p.path("M-40,-14 Q-26,-4 -12,-14 M12,-14 Q26,-4 40,-14", fill="none", w=DW)
                  + p.path("M-14,18 Q0,26 14,18", fill="none", w=DW))
    for x, w, s in ((190, "mei", 0.85), (450, "amir", 0.9), (700, "ravi", 0.85)):
        out += kid(pen, w, x, 1220, s, la=(-60, -112), ra=(64, -112))
        out += glasses(pen, x, 1220, s)
    return out


# ---------------------------------------------------------------- pages 19-30: penerokaan

def gantry(pen, x0, x1, top, base):
    out = pen.rect(x0, top, x1 - x0, base - top, fill="none", sw=DW)
    for y in range(int(top), int(base), 60):
        out += pen.line(x0, y, x1, y + 60, sw=1.6) + pen.line(x1, y, x0, y + 60, sw=1.6) + pen.line(x0, y, x1, y, sw=1.8)
    return out + pen.rect(x0 - 10, top - 20, x1 - x0 + 20, 20, fill="#e53935", rx=3)


def s_roket(pen):
    out = gantry(pen, 120, 210, 330, 1150)
    for y in (520, 760):
        out += pen.tube(f"M210,{y} L360,{y}", 12, "#9e9e9e")
    out += pen.rect(250, 1150, 410, 40, fill="#90a4ae", rx=4)
    out += rocket(pen, 452, 1150, 780)
    for x, y, w, h, sd in ((300, 1170, 120, 40, 1), (600, 1170, 130, 44, 2)):
        out += cloud_puffs(pen, x, y, w, h, sd)
    out += pen.rect(640, 1120, 230, 18, fill="#bdbdbd", sw=DW)
    for x in range(650, 870, 30):
        out += pen.line(x, 1060, x, 1138, sw=DW)
    out += pen.line(640, 1070, 870, 1070, sw=DW)
    out += kid(pen, "amir", 760, 1240, 0.55, la=(-60, -112), ra=(70, -260))
    return out


def s_pelancaran(pen):
    out = gantry(pen, 90, 170, 420, 1150)
    for x, y, w, h, sd in ((200, 1150, 190, 90, 3), (452, 1170, 260, 110, 4), (720, 1150, 190, 90, 5),
                           (320, 1060, 140, 70, 6), (600, 1060, 140, 70, 7)):
        out += cloud_puffs(pen, x, y, w, h, sd)
    out = out + f'<g transform="rotate(4 452 700)">{rocket(pen, 452, 900, 640, flame=True)}</g>'
    for x, y, w, h, sd in ((330, 1210, 150, 60, 8), (600, 1220, 170, 60, 9)):
        out += cloud_puffs(pen, x, y, w, h, sd)
    for x in (120, 780):
        out += pen.path(f"M{x - 30},{560} q15,-10 30,0 q15,10 30,0", fill="none", w=DW)
    return out


def s_angkasawan(pen):
    out = earth_arc(pen, 1560, 560)
    out += pen.path("M40,520 Q220,560 330,700", fill="none", w=DW + 3)
    out += pen.rect(-20, 440, 120, 120, fill="#cfd8dc", rx=12) + porthole(pen, 40, 500, 24)
    out += astro(pen, "amir", 470, 1080, 1.35, rot=-12, la=(-110, -210), ra=(110, -260))
    out += mini_planet(pen, "marikh", 790, 470, 40)
    return out


def s_satelit(pen):
    out = earth_arc(pen, 1560, 560)
    out += satellite(pen, 452, 700, 1.15)
    for k in range(3):
        out += pen.path(f"M{560 + k * 40},{880 + k * 30} q20,-24 0,-48", fill="none", w=DW)
    out += pen.path("M110,420 A60,60 0 1 0 150,520 A46,46 0 1 1 110,420 Z", fill="#fff59d")
    return out


def s_stesen(pen):
    out = earth_arc(pen, 1600, 560)
    out += pen.rect(60, 690, 785, 36, fill="#b0bec5")
    for x in range(60, 845, 36):
        out += pen.line(x, 690, x + 36, 726, sw=1.4)
    for x in (80, 220, 560, 700):
        out += solar_panel(pen, x, 460, 120, 220, 3, 6, "#3949ab") + pen.line(x + 60, 680, x + 60, 690, sw=DW)
        out += solar_panel(pen, x, 736, 120, 220, 3, 6, "#3949ab") + pen.line(x + 60, 726, x + 60, 736, sw=DW)
    out += pen.rect(360, 620, 180, 170, fill="#eceff1", rx=20)
    for k in range(3):
        out += porthole(pen, 400 + k * 50, 660, 12)
    out += pen.rect(420, 790, 60, 150, fill="#eceff1", rx=16) + pen.rect(410, 540, 80, 80, fill="#eceff1", rx=14)
    out += pen.text(450, 760, "ISS", 28, fill_color=NAVY)
    out += astro(pen, "lina", 700, 1180, 0.5, rot=14, la=(-90, -220), ra=(70, -112))
    return out


def s_kapal_angkasa(pen):
    def shuttle(p):
        out = p.path("M-300,40 L-120,40 L-60,140 L80,140 L120,40 Z", fill="#cfd8dc")
        out += p.path("M-330,-60 Q-280,-80 -200,-80 L240,-80 L330,-40 L330,40 L-330,40 Z", fill="#eceff1")
        out += p.path("M240,-80 Q330,-80 360,-20 Q330,20 240,40 Z", fill="#eceff1")
        out += p.path("M280,-62 L320,-50 L330,-30 L290,-36 Z", fill=GLASS, w=DW)
        out += p.path("M-330,-60 L-380,-180 L-280,-180 L-220,-80 Z", fill="#eceff1")
        out += p.path("M-330,-40 L-360,-30 L-360,30 L-330,40 Z", fill="#90a4ae")
        for y in (-20, 20):
            out += p.path(f"M-360,{y - 12} L-420,{y - 22} L-420,{y + 22} L-360,{y + 12} Z", fill="#78909c")
            out += p.path(f"M-420,{y - 16} Q-500,{y} -420,{y + 16} Z", fill="#ff7043")
        out += p.rect(-200, -110, 380, 30, fill="#ffffff", sw=DW) + p.text(-10, 0, "MALAYSIA", 36, fill_color=NAVY)
        out += p.rect(-200, 40, 380, 10, fill="#424242", sw=1.4)
        for x in range(-180, 200, 50):
            out += p.line(x, -80, x, -60, sw=1.4)
        return out
    out = earth_arc(pen, 1560, 520)
    out += f'<g transform="rotate(-10 452 760)">{scaled(pen, 1.0, 470, 760, shuttle)}</g>'
    out += mini_planet(pen, "zuhal", 160, 480, 40)
    return out


def rover(pen, cx, base, s=1.0):
    def draw(p):
        out = p.tube("M-150,-140 L-150,-260", 14, "#9e9e9e")
        out += p.rect(-200, -320, 100, 70, fill="#eceff1", rx=10) + p.circle(-170, -285, 18, fill=GLASS, sw=DW)
        out += p.circle(-130, -285, 12, fill="#424242", sw=DW)
        out += solar_panel(p, -260, -175, 520, 40, 8, 1, "#3949ab")
        out += p.rect(-210, -140, 420, 90, fill="#ffffff", rx=8)
        out += p.rect(-180, -128, 120, 60, fill="#ffca28", rx=4, sw=DW)
        out += p.text(80, -84, "MALAYSIA", 26, fill_color=NAVY)
        out += p.tube("M200,-100 L280,-160 L330,-90", 12, "#9e9e9e") + p.circle(336, -82, 16, fill="#78909c", sw=DW)
        for x in (-160, 0, 160):
            out += p.tube(f"M{x},-52 L{x},-30", 12, "#9e9e9e")
            out += p.circle(x, 0, 52, fill="#616161") + p.circle(x, 0, 30, fill="#bdbdbd", sw=DW)
            for k in range(8):
                a = 2 * math.pi * k / 8
                out += p.line(x + 32 * math.cos(a), 52 * math.sin(a) * 0.6 + 0, x + 50 * math.cos(a), 50 * math.sin(a), sw=1.6)
        return out
    return scaled(pen, s, cx, base - 52 * s, draw)


def s_penjelajah(pen):
    out = pen.circle(140, 360, 26, fill="#e0e0e0", sw=DW) + pen.circle(420, 300, 16, fill="#e0e0e0", sw=DW)
    out += sun_disc(pen, 300, 520, 46, face_s=0.45) + mini_planet(pen, "bumi", 120, 600, 22)
    out += lander(pen, 790, 900, 0.4)
    out += rover(pen, 452, 1130, 1.25)
    out += f'<path d="M80,1180 Q200,1160 300,1150" fill="none" stroke="{INK}" stroke-width="{pen.sw(2)}" ' \
           f'stroke-dasharray="{pen.sw(10)} {pen.sw(8)}"/>'
    return out


def lander(pen, cx, base, s=1.0):
    def draw(p):
        out = ""
        for sx in (-1, 1):
            out += p.tube(f"M{sx * 90},-160 L{sx * 190},-20", 12, "#9e9e9e") + p.ellipse(sx * 196, -10, 36, 12, fill="#bdbdbd")
        out += p.path("M-140,-220 L140,-220 L170,-140 L-170,-140 Z", fill="#ffca28")
        for x in range(-140, 160, 40):
            out += p.line(x, -220, x - 8, -140, sw=1.4)
        out += p.path("M-110,-220 L-80,-330 L80,-330 L110,-220 Z", fill="#eceff1")
        out += p.path("M-40,-310 L40,-310 L50,-260 L-50,-260 Z", fill=GLASS, w=DW)
        out += p.line(0, -330, 0, -380, sw=DW) + p.path("M-30,-380 Q0,-400 30,-380 Z", fill="#eceff1", w=DW)
        out += p.path("M-170,-140 L-120,-40 L-80,-40 L-110,-140", fill="none", w=DW)
        for k in range(4):
            out += p.line(-160 + k * 12, -120 + k * 22, -120 + k * 12, -120 + k * 22, sw=1.6)
        return out
    return scaled(pen, s, cx, base, draw)


def s_mendarat(pen):
    out = pen.circle(160, 420, 70, fill="#42a5f5") + pen.clipped(circle_d(160, 420, 70), earth_inner(pen, 160, 420, 70))
    out += pen.circle(160, 420, 70, fill="none")
    out += lander(pen, 300, 1110, 1.0)
    out += pen.tube("M720,1120 L720,780", 8, "#9e9e9e")
    out += scaled(pen, 0.42, 726, 790, lambda p: jalur_gemilang(p, 0, 0))
    out += astro(pen, "aisyah", 620, 1180, 0.75, la=(130, -230), ra=(130, -170))
    for x, y in ((470, 1220), (510, 1190), (560, 1230)):
        out += pen.ellipse(x, y, 14, 7, fill="#b0bec5", sw=1.6)
    return out


def telescope(pen, x, y, s=1.0, rot=-30):
    def draw(p):
        out = p.tube("M0,0 L-80,200 M0,0 L80,200 M0,0 L0,210", 10, "#8d6e63")
        tube = f'<g transform="rotate({rot})">'
        tube += p.rect(-60, -50, 260, 64, fill="#1e88e5", rx=10) + p.rect(190, -60, 40, 84, fill="#42a5f5", rx=8)
        tube += p.rect(-100, -36, 44, 36, fill="#90a4ae", rx=6) + p.rect(20, -70, 60, 20, fill="#90a4ae", rx=4)
        tube += p.ellipse(232, -18, 8, 40, fill=GLASS, sw=DW) + "</g>"
        return out + tube + p.circle(0, 0, 18, fill="#616161", sw=DW)
    return scaled(pen, s, x, y, draw)


def s_teleskop(pen):
    out = pen.path("M640,360 A90,90 0 1 0 700,500 A70,70 0 1 1 640,360 Z", fill="#fff59d")
    out += mini_planet(pen, "zuhal", 340, 420, 40)
    out += telescope(pen, 520, 870, 1.5, rot=-32)
    out += kid(pen, "mei", 300, 1210, 1.05, la=(110, -260), ra=(150, -230))
    out += small_house(pen, 760, 1050, 140)
    return out


def s_balai_cerap(pen):
    out = ""
    for x, sd in ((120, 1), (790, 2)):
        out += pen.rect(x - 8, 900, 16, 120, fill="#8a5a2f", sw=DW) + pen.path(blob_d(x, 860, 70, 70, 9, sd), fill="#43a047")
    out += pen.rect(250, 760, 400, 270, fill="#eceff1")
    out += pen.path("M230,760 A220,220 0 0 1 670,760 Z", fill="#cfd8dc")
    out += pen.path("M420,545 L480,545 L490,760 L410,760 Z", fill="#455a64")
    out += f'<g transform="rotate(-30 450 640)">' + pen.rect(420, 470, 60, 200, fill="#1e88e5", rx=8) + "</g>"
    for k in range(1, 4):
        out += pen.path(f"M{230 + k * 30},760 A{220 - k * 30},{220 - k * 30} 0 0 1 {670 - k * 30},760", fill="none", w=1.4)
    out += pen.rect(400, 900, 100, 130, fill="#8d6e63", rx=6) + pen.circle(480, 965, 5, fill="#fdd835", sw=1.4)
    for x in (290, 560):
        out += pen.rect(x, 830, 60, 60, fill="#fff59d", sw=DW) + pen.line(x + 30, 830, x + 30, 890, sw=1.6)
    out += pen.rect(300, 780, 300, 36, fill=NAVY, rx=6)
    out += pen.text(450, 806, "BALAI CERAP", 24, fill_color="#ffffff", spacing=2)
    for i in range(4):
        out += pen.rect(380 - i * 14, 1030 + i * 18, 140 + i * 28, 18, fill="#bdbdbd", sw=1.8)
    out += kid(pen, "ravi", 760, 1220, 0.75, la=(-80, -230), ra=(64, -112))
    return out


def s_planetarium(pen):
    out = pen.path("M18,700 Q452,180 887,700 L887,760 L18,760 Z", fill=NAVY)
    inner = ""
    for k in range(1, 4):
        inner += pen.path(f"M18,{700} Q452,{180 + k * 110} 887,700", fill="none", w=1.4)
    for x, y in ((180, 560), (300, 450), (420, 400), (560, 420), (700, 520), (250, 640), (650, 640)):
        inner += pen.path(star_d(x, y, 16, 7), fill="#fff59d", w=1.8)
    inner += mini_planet(pen, "zuhal", 470, 560, 34) + mini_planet(pen, "bumi", 330, 560, 26)
    out += pen.clipped("M18,700 Q452,180 887,700 L887,760 L18,760 Z", inner)
    out += pen.rect(18, 760, 869, 30, fill="#5d4037")
    out += pen.tube("M452,900 L452,820", 26, "#78909c")
    out += pen.circle(400, 800, 40, fill="#90a4ae") + pen.circle(504, 800, 40, fill="#90a4ae")
    for x in (400, 504):
        for k in range(6):
            a = 2 * math.pi * k / 6
            out += pen.circle(x + 22 * math.cos(a), 800 + 22 * math.sin(a), 5, fill="#fff59d", sw=1.2)
    out += pen.rect(380, 900, 144, 30, fill="#616161", rx=6)
    for x, w in ((120, "amir"), (300, "aisyah"), (620, "mei"), (800, "ravi")):
        out += kid(pen, w, x, 1170, 0.7, la=(-60, -112), ra=(60, -112), sit=True)
        out += pen.rect(x - 70, 1170, 140, 30, fill="#e53935", rx=6) + pen.rect(x - 70, 1000, 20, 200, fill="#e53935", rx=6)
    return out


def s_piring_terbang(pen):
    out = pen.path("M380,640 L240,1140 L660,1140 L520,640 Z", fill="#fff59d", w=DW)
    for k in range(1, 4):
        out += pen.path(f"M{380 - k * 0},{640 + k * 120} L{520},{640 + k * 120}", fill="none", w=1.2)
    out += pen.ellipse(452, 500, 120, 110, fill=GLASS)
    out += pen.circle(452, 520, 54, fill="#9ccc65") + cute(pen, 452, 530, 0.7)
    for s in (-1, 1):
        out += pen.line(452 + s * 20, 470, 452 + s * 40, 410, sw=DW) + pen.circle(452 + s * 40, 406, 10, fill="#e53935", sw=DW)
    out += pen.ellipse(452, 600, 280, 70, fill="#b0bec5")
    out += pen.ellipse(452, 588, 200, 30, fill="#cfd8dc", sw=DW)
    for k in range(7):
        x = 220 + k * 77
        out += pen.circle(x, 616 + (12 if 1 < k < 5 else 0), 12, fill=["#e53935", "#fdd835", "#43a047"][k % 3], sw=DW)
    out += kid(pen, "lina", 180, 1220, 0.8, la=(-90, -300), ra=(60, -112))
    out += kid(pen, "ravi", 720, 1220, 0.8, la=(-60, -112), ra=(90, -300))
    return out


# ---------------------------------------------------------------- page list

def page(title, subject, scene, ref=(22, 330, 900)):
    return (title, lambda pen: (subject(pen), W), lambda pen, sc=scene: (sc(pen), ""), dict(x0=0, y=0, ref=ref))


PAGES = [
    page("Sistem Suria", s_sistem_suria, lambda p: space(p, 1, extras=False), ref=(18, 380, 880)),
    page("Matahari", s_matahari, lambda p: space(p, 2), ref=(80, 400, 760)),
    page("Utarid", planet_page("utarid", extra=lambda p: sun_disc(p, -60, 320, 160, face_s=1.0) +
                               small_rocket(p, 790, 1150, 0.18, 30)), lambda p: space(p, 3, extras=False)),
    page("Zuhrah", planet_page("zuhrah", extra=lambda p: small_rocket(p, 150, 1130, 0.2, -30)), lambda p: space(p, 4)),
    page("Bumi", planet_page("bumi", extra=lambda p: satellite(p, 170, 1100, 0.3) + moons([(780, 1120, 50)])(p)),
         lambda p: space(p, 5)),
    page("Bulan", planet_page("bulan", extra=lambda p: astro(p, "amir", 760, 1240, 0.42, rot=10, la=(-80, -220),
                                                              ra=(70, -112))), lambda p: space(p, 6)),
    page("Marikh", planet_page("marikh", extra=moons([(140, 500, 30), (780, 1110, 22)])), lambda p: space(p, 7)),
    page("Musytari", planet_page("musytari", r=250, extra=moons([(120, 520, 22), (790, 520, 18), (130, 1130, 26),
                                                                  (780, 1150, 20)])), lambda p: space(p, 8)),
    page("Zuhal", s_zuhal, lambda p: space(p, 9, extras=False), ref=(18, 380, 880)),
    page("Uranus", planet_page("uranus", r=200, extra=lambda p: astro(p, "mei", 150, 1240, 0.42, rot=-10,
                                                                          la=(-80, -220), ra=(70, -112))),
         lambda p: space(p, 10)),
    page("Neptun", planet_page("neptun", extra=lambda p: satellite(p, 760, 1120, 0.26)), lambda p: space(p, 11)),
    page("Bintang", s_bintang, lambda p: space(p, 12, extras=False)),
    page("Buruj Bintang", s_buruj, night, ref=(18, 200, 900)),
    page("Komet", s_komet, lambda p: space(p, 14, extras=False)),
    page("Hujan Meteor", s_meteor, lambda p: night(p, 1060, 15)),
    page("Asteroid", s_asteroid, lambda p: space(p, 16, extras=False)),
    page("Galaksi Bima Sakti", s_galaksi, lambda p: space(p, 17, extras=False), ref=(18, 370, 880)),
    page("Gerhana Matahari", s_gerhana, lambda p: day(p, 1060), ref=(18, 340, 900)),
    page("Roket", s_roket, lambda p: day(p, 1150), ref=(40, 330, 860)),
    page("Pelancaran Roket", s_pelancaran, lambda p: day(p, 1150), ref=(40, 300, 880)),
    page("Angkasawan", s_angkasawan, lambda p: space(p, 21), ref=(40, 420, 820)),
    page("Satelit", s_satelit, lambda p: space(p, 22, extras=False), ref=(18, 380, 880)),
    page("Stesen Angkasa", s_stesen, lambda p: space(p, 23, extras=False), ref=(18, 400, 880)),
    page("Kapal Angkasa", s_kapal_angkasa, lambda p: space(p, 24, extras=False), ref=(18, 380, 880)),
    page("Penjelajah Marikh", s_penjelajah, lambda p: mars_ground(p, 1040), ref=(18, 380, 880)),
    page("Mendarat di Bulan", s_mendarat, lambda p: space(p, 26, extras=False) + moon_ground(p, 1080),
         ref=(18, 360, 900)),
    page("Teleskop", s_teleskop, lambda p: night(p, 1080, 27), ref=(18, 340, 900)),
    page("Balai Cerap", s_balai_cerap, lambda p: night(p, 1040, 28), ref=(18, 400, 880)),
    page("Planetarium", s_planetarium, lambda p: f'<rect width="{W}" height="1280" fill="#ede7f6"/>' if p.colored else "",
         ref=(18, 330, 900)),
    page("Piring Terbang", s_piring_terbang, lambda p: night(p, 1100, 30), ref=(18, 340, 900)),
]
