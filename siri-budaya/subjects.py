"""The 30 Siri Budaya Malaysia illustrations and their backgrounds.

Everything here is drawn straight in page coordinates (905 x 1280 canvas, the
same frame as the template). Each subject returns (svg, 905) so the shared
template places it without moving it.
"""
import math
import random

from characters import kid, kid_hands
from draw import (DW, GLASS, INK, LW, W, bird, blob_d, bush, cloud, palm, star_d, sun)

GY = 1150  # where the children stand
HZ = 940   # horizon / back of the floor


def mirror(svg, cx):
    return f'<g transform="translate({2 * cx},0) scale(-1,1)">{svg}</g>'


def rot(svg, deg, cx, cy):
    return f'<g transform="rotate({deg} {cx} {cy})">{svg}</g>'


def fill_rect(pen, x, y, w, h, color):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}"/>' if pen.colored else ""


def tufts(pen, n, seed, y0=1000, y1=1250, x0=40, x1=860):
    rnd = random.Random(seed)
    out = ""
    for _ in range(n):
        x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
        out += pen.path(f"M{x - 9:.0f},{y:.0f} L{x - 4:.0f},{y - 15:.0f} L{x:.0f},{y:.0f} L{x + 5:.0f},{y - 17:.0f} "
                        f"L{x + 10:.0f},{y:.0f}", fill="none", w=DW)
    return out


def small_flower(pen, cx, cy, r=12, fill="#f06292"):
    out = ""
    for k in range(5):
        a = 2 * math.pi * k / 5 - math.pi / 2
        out += pen.circle(cx + r * 0.9 * math.cos(a), cy + r * 0.9 * math.sin(a), r * 0.62, fill=fill, sw=DW - 0.4)
    return out + pen.circle(cx, cy, r * 0.45, fill="#fdd835", sw=DW - 0.6)


def bunting(pen, x0, y0, x1, y1, n, colors=("#e53935", "#fdd835", "#1e88e5", "#43a047")):
    sag = 40
    out = pen.path(f"M{x0},{y0} Q{(x0 + x1) / 2},{(y0 + y1) / 2 + sag * 2} {x1},{y1}", fill="none", w=DW)
    for i in range(n):
        t = (i + 0.5) / n
        x = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * (x0 + x1) / 2 + t * t * x1
        y = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * ((y0 + y1) / 2 + sag * 2) + t * t * y1
        out += pen.path(f"M{x - 16:.1f},{y:.1f} L{x + 16:.1f},{y:.1f} L{x:.1f},{y + 34:.1f} Z",
                        fill=colors[i % len(colors)], w=DW)
    return out


# ---------------------------------------------------------------- backgrounds

def small_tree(pen, x, base, h, seed):
    out = pen.rect(x - 6, base - h * 0.45, 12, h * 0.45, fill="#8a5a2f", sw=DW)
    return out + pen.path(blob_d(x, base - h * 0.68, h * 0.34, h * 0.32, 9, seed), fill="#66bb6a", w=DW + 0.4)


def small_house(pen, x, base, w=120):
    """Distant kampung house on stilts."""
    h = w * 0.55
    out = ""
    for k in range(5):
        px = x - w * 0.42 + k * w * 0.21
        out += pen.line(px, base, px, base - h * 0.35, sw=DW)
    out += pen.rect(x - w * 0.45, base - h * 0.35 - h * 0.6, w * 0.9, h * 0.6, fill="#d7a86e", sw=DW)
    for k in range(1, 8):
        px = x - w * 0.45 + k * w * 0.9 / 8
        out += pen.line(px, base - h * 0.95, px, base - h * 0.35, sw=1.2)
    out += pen.rect(x - w * 0.3, base - h * 0.82, w * 0.18, h * 0.3, fill=GLASS, sw=1.8)
    out += pen.rect(x + w * 0.1, base - h * 0.82, w * 0.18, h * 0.3, fill=GLASS, sw=1.8)
    out += pen.path(f"M{x - w * 0.6},{base - h * 0.92} L{x - w * 0.25},{base - h * 1.5} L{x + w * 0.25},{base - h * 1.5} "
                    f"L{x + w * 0.6},{base - h * 0.92} Z", fill="#8d4f2a", w=DW)
    return out + pen.path(f"M{x - w * 0.25},{base - h * 1.5} L{x},{base - h * 1.75} L{x + w * 0.25},{base - h * 1.5}",
                          fill="#a1887f", w=DW)


def fence(pen, x0, x1, base, h=46):
    out = pen.rect(x0, base - h * 0.75, x1 - x0, 8, fill="#d7a86e", sw=1.8)
    out += pen.rect(x0, base - h * 0.35, x1 - x0, 8, fill="#d7a86e", sw=1.8)
    for x in range(int(x0) + 6, int(x1), 34):
        out += pen.path(f"M{x},{base} L{x},{base - h} L{x + 7},{base - h - 9} L{x + 14},{base - h} L{x + 14},{base} Z",
                        fill="#e8b47a", w=1.8)
    return out


def pebbles(pen, cx, cy, seed):
    rnd = random.Random(seed)
    out = ""
    for _ in range(4):
        out += pen.ellipse(round(cx + rnd.uniform(-34, 34)), round(cy + rnd.uniform(-8, 8)), rnd.choice((10, 13, 16)),
                           rnd.choice((6, 8)), fill="#bdbdbd", sw=1.8)
    return out


def outdoor(pen, horizon=HZ, hills=True, sunny=True, n_tufts=18, ground="#c5e1a5", clouds=True, scenery=True):
    out = fill_rect(pen, 0, 0, W, horizon, "#bfe7fb")
    out += fill_rect(pen, 0, horizon, W, 400, ground)
    if clouds:
        out += cloud(pen, 46, 196, 210, 84) + cloud(pen, 280, 286, 130, 52)
        out += bird(pen, 420, 330) + bird(pen, 456, 356, 0.8)
        if sunny:
            out += sun(pen, 470, 210, 34)
    if hills:
        out += pen.path(f"M18,{horizon} Q120,{horizon - 150} 260,{horizon - 70} Q420,{horizon - 170} 600,{horizon - 80} "
                        f"Q760,{horizon - 150} 887,{horizon - 60} L887,{horizon} Z", fill="#c5e1a5")
        if scenery:
            out += small_house(pen, 330, horizon - 92, 104) + small_house(pen, 690, horizon - 86, 96)
        out += pen.path(f"M18,{horizon} Q170,{horizon - 90} 330,{horizon - 20} Q520,{horizon - 110} 700,{horizon - 30} "
                        f"Q800,{horizon - 70} 887,{horizon - 20} L887,{horizon} Z", fill="#aed581")
    if scenery:
        out += fence(pen, 18, 887, horizon)
        for i, (x, h) in enumerate(((150, 90), (760, 100))):
            out += small_tree(pen, x, horizon, h, 50 + i)
        out += palm(pen, 50, horizon, 380, lean=26, seed=3) + palm(pen, 862, horizon, 330, lean=-22, seed=4)
        out += bush(pen, 230, horizon + 6, 120, 50, 11, fill="#66bb6a") + bush(pen, 610, horizon + 6, 110, 46, 12,
                                                                              fill="#66bb6a")
    out += pen.line(18, horizon, 887, horizon, sw=LW)
    out += tufts(pen, n_tufts, horizon, horizon + 40)
    if scenery:
        for x, y, c in ((60, horizon + 120, "#f06292"), (845, horizon + 150, "#ffb300"), (110, horizon + 250, "#ba68c8"),
                        (800, horizon + 270, "#f06292"), (300, horizon + 300, "#ffb300"), (620, horizon + 290, "#ba68c8"),
                        (40, horizon + 200, "#ffb300"), (870, horizon + 230, "#ba68c8")):
            if y < 1262:
                out += pen.line(x, y + 8, x, y + 30, sw=DW) + small_flower(pen, x, y, 12, c)
                out += pen.path(f"M{x},{y + 24} Q{x + 14},{y + 14} {x + 18},{y + 20} Q{x + 10},{y + 28} {x},{y + 24} Z",
                                fill="#66bb6a", w=1.4)
        out += pebbles(pen, 200, horizon + 200, 1) + pebbles(pen, 700, horizon + 220, 2)
    return out


def lamp(pen, x=400, top=150):
    out = pen.line(x, top, x, top + 110, sw=DW)
    out += pen.path(f"M{x - 60},{top + 170} Q{x - 54},{top + 110} {x},{top + 106} Q{x + 54},{top + 110} {x + 60},{top + 170} Z",
                    fill="#ffb74d")
    out += pen.path(f"M{x - 60},{top + 170} " + "".join(f"q7.5,10 15,0 " for _ in range(8)), fill="none", w=1.6)
    out += pen.path(f"M{x - 30},{top + 150} Q{x},{top + 132} {x + 30},{top + 150}", fill="none", w=1.6)
    return out + pen.circle(x, top + 180, 14, fill="#fff59d", sw=DW)


def shelf(pen, x0=610, x1=860, y=690):
    out = pen.rect(x0, y, x1 - x0, 14, fill="#a1887f", rx=3)
    for x in (x0 + 20, x1 - 30):
        out += pen.path(f"M{x},{y + 14} L{x},{y + 40} L{x + 14},{y + 14}", fill="#a1887f", w=DW)
    colors = ["#e53935", "#1e88e5", "#43a047", "#fdd835"]
    for k, c in enumerate(colors):
        out += pen.rect(x0 + 16 + k * 22, y - 70 + (k % 2) * 8, 20, 70 - (k % 2) * 8, fill=c, rx=2, sw=1.8)
    vx = x0 + 150
    out += pen.path(f"M{vx - 18},{y} Q{vx - 30},{y - 40} {vx - 10},{y - 60} L{vx + 10},{y - 60} Q{vx + 30},{y - 40} {vx + 18},{y} Z",
                    fill="#4fc3f7", w=1.8)
    for dx, dy, c in ((-18, -96, "#f06292"), (14, -104, "#ffb300"), (0, -120, "#e53935")):
        out += pen.line(vx, y - 60, vx + dx, y + dy + 10, sw=1.6) + small_flower(pen, vx + dx, y + dy, 11, c)
    out += pen.rect(x1 - 52, y - 40, 34, 40, fill="#ffcc80", rx=4, sw=1.8)
    return out + pen.ellipse(x1 - 35, y - 40, 17, 5, fill="#ffcc80", sw=1.6)


def tikar(pen, floor):
    mat = f"M150,{floor + 40} L755,{floor + 40} L830,{floor + 250} L75,{floor + 250} Z"
    out = pen.path(mat, fill="#e6c27a")
    inner = "".join(pen.line(x, floor, x + 300, floor + 300, sw=1.2) + pen.line(x + 300, floor, x, floor + 300, sw=1.2)
                    for x in range(-200, 1000, 32))
    out += pen.clipped(mat, inner)
    out += pen.path(f"M170,{floor + 56} L738,{floor + 56} L806,{floor + 236} L100,{floor + 236} Z", fill="none", w=DW)
    return out + pen.path(mat, fill="none")


def batik_band(pen, y=158):
    out = pen.rect(-10, y, 925, 40, fill="#ffcc80", sw=DW)
    for x in range(10, 900, 60):
        out += small_flower(pen, x + 30, y + 20, 11, "#e57373")
        out += pen.path(f"M{x},{y + 20} q8,-12 16,0 q8,12 16,0", fill="none", w=1.4)
    return out


def wall_picture(pen, x=640, y=440, w=170, h=110):
    out = pen.rect(x - 10, y - 10, w + 20, h + 20, fill="#8d6e63", rx=6)
    out += pen.rect(x, y, w, h, fill="#bfe7fb", sw=DW)
    out += pen.path(f"M{x},{y + h * 0.75} Q{x + w * 0.3},{y + h * 0.45} {x + w * 0.55},{y + h * 0.7} "
                    f"Q{x + w * 0.8},{y + h * 0.5} {x + w},{y + h * 0.65} L{x + w},{y + h} L{x},{y + h} Z",
                    fill="#9ccc65", w=DW)
    return out + pen.circle(x + w * 0.75, y + h * 0.28, 16, fill="#fdd835", sw=DW)


def potted_plant(pen, x, base):
    out = ""
    for ang, l in ((-150, 90), (-120, 110), (-90, 120), (-60, 110), (-30, 90)):
        a = math.radians(ang)
        out += pen.path(f"M{x},{base - 60} Q{x + l * 0.6 * math.cos(a) - 14},{base - 60 + l * 0.6 * math.sin(a)} "
                        f"{x + l * math.cos(a):.0f},{base - 60 + l * math.sin(a):.0f} "
                        f"Q{x + l * 0.6 * math.cos(a) + 14},{base - 60 + l * 0.6 * math.sin(a)} {x},{base - 60} Z",
                        fill="#66bb6a", w=DW)
    return out + pen.path(f"M{x - 40},{base - 66} L{x + 40},{base - 66} L{x + 30},{base} L{x - 30},{base} Z",
                          fill="#d7764a")


def indoor(pen, floor=HZ, window=True, picture=True, plant=True, with_lamp=True, rug=True, with_shelf=None):
    out = fill_rect(pen, 0, 0, W, floor, "#fff3e0")
    out += fill_rect(pen, 0, floor, W, 400, "#e0b07a")
    out += pen.rect(-10, floor - 150, 925, 150, fill="#ffe0b2", sw=DW)
    out += pen.rect(-10, floor - 162, 925, 16, fill="#bc8a5f", sw=DW)
    for x in range(60, 900, 110):
        out += pen.rect(x, floor - 126, 70, 102, fill="none", rx=6, sw=1.8)
    out += pen.line(18, floor, 887, floor, sw=LW)
    for y in (floor + 70, floor + 170):
        out += pen.line(18, y, 887, y, sw=DW - 0.4)
    for x in range(120, 900, 180):
        out += pen.line(x, floor, x - 30, floor + 70, sw=1.6) + pen.line(x + 60, floor + 70, x + 40, floor + 170, sw=1.6)
    if window:
        out += pen.rect(70, 300, 190, 230, fill=GLASS, rx=8)
        out += pen.line(165, 300, 165, 530, sw=DW + 0.6) + pen.line(70, 415, 260, 415, sw=DW + 0.6)
        out += pen.path("M72,410 Q120,360 165,390 Q210,350 258,404 L258,413 L72,413 Z", fill="#aed581", w=1.8)
        out += pen.path("M215,413 L222,330 M222,330 Q190,322 180,340 M222,330 Q250,316 258,336 M222,330 Q214,306 232,300",
                        fill="none", w=1.8)
        out += cloud(pen, 82, 316, 70, 28)
        for side, d in ((-1, "M60,290 Q100,420 70,540 L50,540 L50,290 Z"), (1, "M270,290 Q230,420 260,540 L280,540 L280,290 Z")):
            out += pen.path(d, fill="#ef9a9a")
            cx = 66 if side < 0 else 264
            out += pen.clipped(d, "".join(pen.circle(cx + (k % 2) * 10 - 5, 310 + k * 34, 5, fill="#ffffff", sw=1.2)
                                          for k in range(7)))
        out += pen.rect(44, 280, 242, 14, fill="#8d6e63", rx=5)
    out += batik_band(pen)
    if with_lamp:
        out += lamp(pen)
    if picture:
        out += wall_picture(pen)
    if picture if with_shelf is None else with_shelf:
        out += shelf(pen)
    if rug:
        out += tikar(pen, floor)
    if plant:
        out += potted_plant(pen, 845, floor + 40)
    return out


def night(pen, horizon=HZ):
    out = fill_rect(pen, 0, 0, W, horizon, "#283593")
    out += fill_rect(pen, 0, horizon, W, 400, "#9fa8da")
    out += pen.path("M110,200 A56,56 0 1 0 170,282 A44,44 0 1 1 110,200 Z", fill="#fff59d")
    for x, y, r in ((260, 220, 14), (400, 300, 10), (60, 360, 10), (330, 420, 12), (210, 470, 9), (480, 200, 10),
                    (70, 520, 8), (520, 380, 8)):
        out += pen.path(star_d(x, y, r, r * 0.45), fill="#fff59d", w=DW - 0.4)
    for x in (60, 820):
        out += pen.rect(x - 40, horizon - 70, 80, 70, fill="#5c6bc0", sw=DW)
        out += pen.path(f"M{x - 52},{horizon - 66} L{x},{horizon - 120} L{x + 52},{horizon - 66} Z", fill="#3949ab", w=DW)
        out += pen.rect(x - 12, horizon - 50, 24, 28, fill="#fff59d", sw=1.8)
    out += pen.line(18, horizon, 887, horizon, sw=LW)
    return out


def table(pen, top=1000):
    out = indoor(pen, floor=top, window=True, plant=False, rug=False)
    out += pen.rect(-10, top, 925, 290, fill="#c8915a")
    out += pen.rect(-10, top, 925, 30, fill="#ffffff", sw=DW)
    for i, x in enumerate(range(-10, 915, 30)):
        if i % 2 == 0:
            out += pen.rect(x, top, 30, 15, fill="#e53935", sw=1.2) + pen.rect(x + 30, top + 15, 30, 15, fill="#e53935", sw=1.2)
    out += pen.path(f"M-10,{top + 30} " + "".join(f"q15,16 30,0 " for _ in range(31)), fill="#ffffff", w=1.8)
    for y in (top + 90, top + 170):
        out += pen.path(f"M18,{y} Q300,{y - 8} 600,{y + 4} Q760,{y + 10} 887,{y}", fill="none", w=DW - 0.6)
    return out


def sea(pen, horizon=900):
    out = fill_rect(pen, 0, 0, W, horizon, "#bfe7fb")
    out += fill_rect(pen, 0, horizon, W, 400, "#4fc3f7")
    out += cloud(pen, 46, 196, 210, 84) + cloud(pen, 280, 286, 130, 52)
    out += pen.path(f"M700,{horizon} Q760,{horizon - 50} 880,{horizon - 30} L887,{horizon} Z", fill="#ffe082")
    out += palm(pen, 800, horizon - 34, 150, lean=-20)
    out += pen.line(18, horizon, 887, horizon, sw=LW)
    out += bird(pen, 470, 330) + bird(pen, 510, 356, 0.8) + bird(pen, 380, 300, 0.9)
    out += sun(pen, 470, 210, 34)
    bx = 300
    out += pen.path(f"M{bx - 50},{horizon - 4} L{bx + 50},{horizon - 4} L{bx + 36},{horizon + 12} L{bx - 36},{horizon + 12} Z",
                    fill="#8d6e63", w=1.8)
    out += pen.line(bx, horizon - 4, bx, horizon - 70, sw=1.8)
    out += pen.path(f"M{bx + 2},{horizon - 66} L{bx + 40},{horizon - 10} L{bx + 2},{horizon - 10} Z", fill="#ffffff", w=1.8)
    for y, off in ((940, 0), (980, 70)):
        for x in range(40 + off, 880, 150):
            out += pen.path(f"M{x},{y} q18,-14 36,0 q18,14 36,0", fill="none", w=DW)
    return out


# ---------------------------------------------------------------- 1-5 permainan tradisional

def wau(pen, cx, cy, s=1.0):
    def side():
        o = pen.path("M0,-205 C80,-232 222,-232 272,-170 C232,-150 202,-112 192,-60 C140,-92 70,-92 0,-60 Z",
                     fill="#e53935")
        o += pen.path("M40,-180 C90,-205 170,-205 220,-172 C186,-150 166,-122 160,-92 C120,-110 70,-110 30,-96 Z",
                      fill="#fdd835", w=DW)
        o += pen.path("M70,-150 C96,-182 150,-176 148,-148 C146,-128 118,-130 120,-148", fill="none", w=DW)
        o += small_flower(pen, 200, -150, 13, "#1e88e5")
        o += pen.path("M48,-118 Q110,-146 150,-112", fill="none", w=DW)
        o += pen.path("M272,-170 L300,-150 L284,-140 Z M192,-60 L214,-36 L198,-30 Z", fill="#1e88e5", w=DW)
        o += pen.path("M60,60 C110,74 150,80 210,60 C200,120 170,160 120,180", fill="none")
        o += pen.path("M95,110 C110,90 140,96 136,116 C132,132 112,126 116,114", fill="none", w=DW)
        return o

    out = pen.path("M-150,-262 Q0,-344 150,-262", fill="none", w=LW + 2)
    out += pen.line(-150, -262, 150, -262, sw=DW - 0.6)
    out += pen.path("M60,40 C120,40 170,20 214,60 C200,140 120,200 0,206 L0,40 Z", fill="#1e88e5")
    out += mirror(pen.path("M60,40 C120,40 170,20 214,60 C200,140 120,200 0,206 L0,40 Z", fill="#1e88e5"), 0)
    out += pen.path("M-150,70 C-110,150 110,150 150,70 L120,84 C90,128 -90,128 -120,84 Z", fill="#ffffff")
    out += side() + mirror(side(), 0)
    out += pen.path("M-28,-62 L28,-62 L40,44 L-40,44 Z", fill="#43a047")
    out += small_flower(pen, 0, -10, 16, "#fdd835")
    out += pen.ellipse(0, -236, 24, 30, fill="#fdd835", sw=LW)
    out += pen.line(0, -266, 0, 206, sw=DW)
    return f'<g transform="translate({cx},{cy}) scale({s})">{out}</g>'


def s_wau(pen):
    out = wau(pen, 450, 640, 1.0)
    out += pen.path("M450,700 Q330,820 214,814", fill="none", w=DW)
    out += kid(pen, "amir", 170, GY, 0.95, la=(-60, -112), ra=(46, -316))
    out += kid(pen, "aisyah", 740, GY, 0.9, la=(-96, -300), ra=(96, -300))
    return out, W


def s_gasing(pen):
    g = pen.path("M-30,-40 C-210,-60 -210,-160 -70,-176 L70,-176 C210,-160 210,-60 30,-40 Z", fill="#ff7043")
    g += pen.path("M-188,-110 Q0,-70 188,-110", fill="none", w=DW + 0.6)
    g += pen.path("M-150,-150 Q0,-124 150,-150", fill="none", w=DW)
    g += pen.path("M-160,-84 Q0,-50 160,-84", fill="none", w=DW)
    g += pen.path("M-30,-40 L-8,-4 L0,0 L8,-4 L30,-40 Z", fill="#9e9e9e")
    g += pen.rect(-36, -236, 72, 64, fill="#8d6e63", rx=12)
    g += pen.ellipse(0, -236, 36, 12, fill="#a1887f", sw=DW + 0.6)
    for x in (-120, -60, 0, 60, 120):
        g += pen.circle(x, -126 + abs(x) * 0.12, 8, fill="#fdd835", sw=DW - 0.4)
    body = "M-30,-40 C-210,-60 -210,-160 -70,-176 L70,-176 C210,-160 210,-60 30,-40 Z"
    band = ""
    for x in range(-180, 180, 30):
        yb = -92 + abs(x) * 0.06
        band += pen.path(f"M{x},{yb + 6} L{x + 15},{yb - 12} L{x + 30},{yb + 6} Z", fill="#1e88e5", w=1.6)
    for x in range(-130, 140, 26):
        band += pen.path(f"M{x - 8},-160 Q{x},-172 {x + 8},-160", fill="none", w=1.6)
    g += pen.clipped(body, band)
    for k in range(-2, 3):
        g += pen.line(k * 12, -228, k * 12, -180, sw=1.4)
    out = f'<g transform="translate(470,1110) scale(1.15)">{g}</g>'
    for r, a0, a1 in ((270, 200, 250), (290, -70, -20), (250, 290, 330)):
        x0, y0 = 470 + r * math.cos(math.radians(a0)), 990 + r * 0.38 * math.sin(math.radians(a0))
        x1, y1 = 470 + r * math.cos(math.radians(a1)), 990 + r * 0.38 * math.sin(math.radians(a1))
        out += pen.path(f"M{x0:.0f},{y0:.0f} A{r},{r * 0.38:.0f} 0 0 1 {x1:.0f},{y1:.0f}", fill="none", w=DW)
    out += pen.path(blob_d(450, 1120, 40, 14, 7, 2, flat_bottom=True), fill="#d7ccc8", w=DW)
    out += pen.path(blob_d(500, 1124, 30, 12, 7, 3, flat_bottom=True), fill="#d7ccc8", w=DW)
    out += kid(pen, "amir", 150, GY, 0.95, la=(-60, -112), ra=(70, -180))
    out += pen.path("M216,980 Q260,1000 240,1030 Q220,1060 270,1070 Q320,1080 300,1110", fill="none", w=DW + 0.6)
    out += kid(pen, "mei", 770, GY, 0.9, la=(-96, -300), ra=(96, -300))
    return out, W


def s_congkak(pen):
    board = "M110,962 Q110,896 200,896 L706,896 Q796,896 796,962 Q796,1034 706,1042 L200,1042 Q110,1034 110,962 Z"
    out = kid(pen, "aisyah", 300, 1000, 1.15, la=(-50, -150), ra=(60, -116), sit=True, hands=False)
    out += kid(pen, "mei", 610, 1000, 1.15, la=(-60, -116), ra=(50, -150), sit=True, hands=False)
    out += pen.path("M110,962 L110,1000 Q110,1072 200,1080 L706,1080 Q796,1072 796,1000 L796,962", fill="#8d6e63")
    out += pen.path(board, fill="#bc8a5f")
    out += pen.ellipse(166, 968, 36, 50, fill="#8d6e63") + pen.ellipse(740, 968, 36, 50, fill="#8d6e63")
    rnd = random.Random(4)
    for row, y in enumerate((934, 1004)):
        for i in range(7):
            x = 238 + i * 72
            out += pen.ellipse(x, y, 27, 19, fill="#8d6e63", sw=DW + 0.6)
            for _ in range(rnd.randint(1, 3)):
                out += pen.circle(x + rnd.uniform(-10, 10), y + rnd.uniform(-5, 6), 6, fill="#fff8e1", sw=1.6)
    rim = "M110,1000 Q110,1072 200,1080 L706,1080 Q796,1072 796,1000 L796,1040 L110,1040 Z"
    carve = ""
    for x in range(150, 770, 48):
        carve += pen.path(f"M{x},1062 q12,-14 24,0 q12,14 24,0", fill="none", w=1.6)
        carve += pen.circle(x + 24, 1062, 4, fill="#fdd835", sw=1.2)
    out += carve
    for cx in (166, 740):
        for k in range(8):
            a = math.radians(k * 45)
            out += pen.ellipse(round(cx + 46 * math.cos(a)), round(968 + 60 * math.sin(a)), 8, 5, fill="#a5d6a7", sw=1.2,
                               rot=round(k * 45))
    for x, y in ((156, 954), (176, 976), (160, 990), (730, 950), (750, 975)):
        out += pen.circle(x, y, 7, fill="#fff8e1", sw=1.6)
    out += kid_hands(pen, "aisyah", 300, 1000, 1.15, la=(-50, -150), ra=(60, -116), sit=True)
    out += kid_hands(pen, "mei", 610, 1000, 1.15, la=(-60, -116), ra=(50, -150), sit=True)
    return out, W


def rattan_ball(pen, cx, cy, r):
    inner = ""
    for k in range(6):
        a = 2 * math.pi * k / 6
        inner += pen.circle(cx + r * 0.62 * math.cos(a), cy + r * 0.62 * math.sin(a), r * 0.24, fill="#ffffff", sw=DW)
    inner += pen.circle(cx, cy, r * 0.24, fill="#ffffff", sw=DW)
    for k in range(6):
        a = 2 * math.pi * k / 6 + math.pi / 6
        inner += pen.line(cx + r * 0.3 * math.cos(a), cy + r * 0.3 * math.sin(a), cx + r * math.cos(a), cy + r * math.sin(a),
                          sw=1.6)
    return pen.circle(cx, cy, r, fill="#ffca28") + pen.clipped(
        f"M{cx - r},{cy} A{r},{r} 0 1 0 {cx + r},{cy} A{r},{r} 0 1 0 {cx - r},{cy} Z", inner) + pen.circle(
        cx, cy, r, fill="none")


def s_sepak_takraw(pen):
    court = "M90,1060 L815,1060 L870,1240 L35,1240 Z"
    out = pen.path(court, fill="#ffcc80")
    out += pen.path("M452,1060 L452,1240 M110,1120 L795,1120", fill="none", w=DW)
    out += pen.ellipse(452, 1180, 80, 30, fill="none", sw=DW)
    for x, c in ((360, "#e53935"), (545, "#1e88e5")):
        out += pen.path(f"M{x},880 L{x + (40 if x > 400 else -40)},894 L{x},908 Z", fill=c, w=1.8)
    out += pen.tube("M360,1150 L360,880 M545,1150 L545,880", 12, "#9e9e9e")
    net = "M360,900 L545,900 L545,990 L360,990 Z"
    out += pen.path(net, fill="none", w=DW)
    out += pen.clipped(net, "".join(pen.line(x, 890, x - 40, 1000, sw=1.6) + pen.line(x - 40, 890, x, 1000, sw=1.6)
                                    for x in range(360, 600, 22)))
    out += pen.rect(354, 892, 198, 14, fill="#ffffff", rx=4, sw=DW)
    out += rattan_ball(pen, 452, 600, 84)
    for x0 in (90, 680):
        out += pen.rect(x0, 1250, 120, 4, fill="#ffffff", sw=0.1)
    for d in ("M360,560 Q330,600 360,640", "M330,540 Q290,600 330,660", "M544,560 Q574,600 544,640"):
        out += pen.path(d, fill="none", w=DW)
    out += kid(pen, "amir", 180, GY, 1.05, la=(-86, -300), ra=(86, -300))
    out += kid(pen, "ravi", 730, GY, 1.05, la=(-86, -300), ra=(86, -300), outfit="tshirt")
    return out, W


def seremban_bag(pen, x, y, s=1.0, c="#f06292"):
    d = (f"M{x - 20 * s},{y} Q{x - 24 * s},{y - 26 * s} {x},{y - 30 * s} Q{x + 24 * s},{y - 26 * s} {x + 20 * s},{y} "
         f"Q{x},{y + 8 * s} {x - 20 * s},{y} Z")
    return pen.path(d, fill=c, w=DW + 0.6) + pen.path(f"M{x - 8 * s},{y - 22 * s} L{x},{y - 30 * s} L{x + 8 * s},{y - 22 * s}",
                                                     fill="none", w=DW - 0.6)


def s_batu_seremban(pen):
    mat = "M140,1020 L770,1020 L840,1200 L70,1200 Z"
    out = pen.path(mat, fill="#e6c27a")
    out += pen.clipped(mat, "".join(pen.line(x, 1000, x + 200, 1220, sw=1.6) + pen.line(x + 200, 1000, x, 1220, sw=1.6)
                                    for x in range(-100, 1000, 46)))
    out += pen.path(mat, fill="none")
    out += kid(pen, "aisyah", 450, 1080, 1.35, la=(-70, -110), ra=(84, -270), sit=True)
    out += seremban_bag(pen, 575, 640, 1.2, "#42a5f5")
    out += pen.path("M560,700 Q556,730 566,750 M590,700 Q596,724 588,744", fill="none", w=DW)
    for i, (x, y, c) in enumerate(((290, 1150, "#f06292"), (360, 1172, "#fdd835"), (540, 1168, "#66bb6a"),
                                   (610, 1146, "#ff7043"))):
        out += seremban_bag(pen, x, y, 1.15, c)
    return out, W


# ---------------------------------------------------------------- 6-8 seni persembahan

def s_silat(pen):
    out = pen.path("M120,1070 L780,1070 L860,1210 L40,1210 Z", fill="#ffe0b2")
    out += pen.path("M170,1090 L730,1090 L790,1190 L110,1190 Z", fill="none", w=DW)
    out += kid(pen, "amir", 450, 1150, 1.6, outfit="silat", la=(-150, -230), ra=(70, -130))
    for x in (120, 790):
        out += pen.tube(f"M{x},1070 L{x},780", 10, "#8d6e63")
        out += pen.path(f"M{x},780 L{x + (60 if x < 400 else -60)},800 L{x},826 Z", fill="#fdd835", w=DW)
    out += pen.ellipse(130, 1150, 54, 20, fill="#a1887f")
    out += pen.path("M76,1150 L84,1220 Q130,1236 176,1220 L184,1150", fill="#8d6e63")
    for x in (96, 130, 164):
        out += pen.line(x, 1156, x, 1226, sw=1.6)
    out += pen.ellipse(130, 1150, 54, 20, fill="#f5e6c8")
    out += pen.tube("M720,1210 L720,1010 L860,1010 L860,1210", 10, "#8d6e63")
    out += pen.line(790, 1010, 790, 1050, sw=DW)
    out += pen.circle(790, 1110, 58, fill="#fdd835") + pen.circle(790, 1110, 20, fill="#ffb300", sw=DW)
    return out, W


def bunga_manggar(pen, x, top, base=1150):
    out = pen.tube(f"M{x},{base} L{x},{top + 40}", 12, "#8d6e63")
    for k in range(9):
        a = math.radians(-160 + k * 17.5)
        ex, ey = x + 110 * math.cos(a), top + 40 + 110 * math.sin(a) + 60
        out += pen.path(f"M{x},{top + 40} Q{(x + ex) / 2:.0f},{top - 10 + 60 * (k % 2):.0f} {ex:.0f},{ey:.0f}",
                        fill="none", w=DW + 0.6)
        out += pen.circle(ex, ey, 7, fill=["#e53935", "#fdd835", "#43a047"][k % 3], sw=DW - 0.6)
    return out


def kompang(pen, cx, cy, r):
    out = pen.circle(cx, cy, r, fill="#8d6e63")
    out += pen.circle(cx, cy, r * 0.82, fill="#f5e6c8", sw=DW + 0.6)
    for k in range(16):
        a = 2 * math.pi * k / 16
        out += pen.circle(cx + r * 0.91 * math.cos(a), cy + r * 0.91 * math.sin(a), 3.5, fill="#fdd835", sw=1.4)
    return out


def s_kompang(pen):
    la, ra = (-82, -150), (78, -176)
    out = bunga_manggar(pen, 110, 600) + bunga_manggar(pen, 800, 620)
    out += bunting(pen, 30, 470, 520, 440, 9)
    out += kid(pen, "amir", 450, 1150, 1.5, la=la, ra=ra, outfit="bajumelayu", hands=False)
    out += kompang(pen, 450, 1150 - 150 * 1.5, 104)
    out += kid_hands(pen, "amir", 450, 1150, 1.5, la=la, ra=ra)
    return out, W


def puppet(pen):
    out = pen.line(0, -40, 0, 330, sw=LW)
    out += pen.path("M-36,-330 Q-40,-380 -10,-420 Q0,-460 10,-420 Q40,-380 36,-330 Z", fill="#fdd835")
    out += pen.path("M-46,-300 Q-60,-340 -30,-336 L30,-336 Q60,-340 46,-300 Z", fill="#fdd835")
    out += pen.path("M-30,-300 Q-70,-296 -84,-266 Q-60,-262 -40,-268 Q-40,-232 -12,-226 L28,-226 Q44,-260 30,-300 Z",
                    fill="#8d6e63")
    out += pen.circle(-8, -276, 5, fill="#ffffff", sw=1.6)
    body = "M-40,-224 L40,-224 L54,-120 L70,-20 Q0,6 -70,-20 L-54,-120 Z"
    out += pen.path(body, fill="#e53935")
    for x, y in ((-20, -190), (20, -190), (0, -150), (-28, -100), (28, -100), (0, -60)):
        out += pen.circle(x, y, 8, fill="#ffffff", sw=1.6)
    out += pen.path("M-70,-20 Q-90,40 -60,90 L60,90 Q90,40 70,-20 Q0,6 -70,-20 Z", fill="#1e88e5")
    out += pen.path("M-50,10 L-40,80 M0,14 L0,86 M50,10 L40,80", fill="none", w=DW)
    out += pen.path("M-60,90 L-90,120 L-30,110 Z M60,90 L90,120 L30,110 Z", fill="#8d6e63")
    out += pen.tube("M-38,-214 Q-120,-150 -130,-40", 12, "#8d6e63")
    out += pen.tube("M38,-214 Q120,-180 150,-110", 12, "#8d6e63")
    out += pen.circle(-130, -40, 10, fill="#8d6e63", sw=DW) + pen.circle(150, -110, 10, fill="#8d6e63", sw=DW)
    out += pen.line(-130, -40, -150, 320, sw=DW) + pen.line(150, -110, 170, 320, sw=DW)
    return out


def pohon_beringin(pen):
    leaf = "M0,-300 C80,-220 130,-100 110,10 Q60,60 0,70 Q-60,60 -110,10 C-130,-100 -80,-220 0,-300 Z"
    out = pen.path(leaf, fill="#43a047")
    out += pen.path("M0,60 L0,-240 M0,-60 Q-50,-90 -60,-150 M0,-100 Q50,-130 56,-190 M0,-10 Q60,-30 80,-80 "
                    "M0,10 Q-60,-10 -80,-50", fill="none", w=DW)
    for x, y in ((-60, -150), (56, -190), (80, -80), (-80, -50), (0, -240)):
        out += small_flower(pen, x, y, 10, "#fdd835")
    out += pen.line(0, 70, 0, 330, sw=LW)
    return out


def s_wayang_kulit(pen):
    out = pen.rect(120, 460, 670, 520, fill="#8d6e63", rx=10)
    out += pen.rect(150, 490, 610, 460, fill="#fff8e1")
    scal = "M120,460 " + "".join(f"q{670 / 14 / 2:.1f},-34 {670 / 14:.1f},0 " for _ in range(14))
    out += pen.path(scal + "Z", fill="#e53935")
    out += f'<g transform="translate(290,820) scale(0.9)">{pohon_beringin(pen)}</g>'
    out += f'<g transform="translate(560,820) scale(0.95)">{puppet(pen)}</g>'
    out += pen.rect(100, 980, 710, 130, fill="#c62828")
    for x in range(140, 800, 90):
        out += pen.path(f"M{x},1000 L{x + 30},1045 L{x},1090 L{x - 30},1045 Z", fill="#fdd835", w=DW)
    out += pen.line(455, 400, 455, 420, sw=DW)
    out += pen.path("M430,420 L480,420 L470,450 L440,450 Z", fill="#bdbdbd", w=DW)
    out += pen.path("M455,452 Q445,470 455,484 Q465,470 455,452 Z", fill="#ff9800", w=DW)
    return out, W


# ---------------------------------------------------------------- 9-13 kraf tangan

def big_hibiscus(pen, cx, cy, r, rot_deg=0):
    out = ""
    for k in range(5):
        a = rot_deg + k * 72
        petal = (f"M0,0 C{-r * 0.55:.0f},{-r * 0.3:.0f} {-r * 0.7:.0f},{-r * 0.95:.0f} {-r * 0.2:.0f},{-r:.0f} "
                 f"Q0,{-r * 1.08:.0f} {r * 0.2:.0f},{-r:.0f} C{r * 0.7:.0f},{-r * 0.95:.0f} {r * 0.55:.0f},{-r * 0.3:.0f} 0,0 Z")
        veins = (f"M0,{-r * 0.15:.0f} L0,{-r * 0.8:.0f} M0,{-r * 0.3:.0f} Q{-r * 0.2:.0f},{-r * 0.55:.0f} {-r * 0.3:.0f},{-r * 0.8:.0f} "
                 f"M0,{-r * 0.3:.0f} Q{r * 0.2:.0f},{-r * 0.55:.0f} {r * 0.3:.0f},{-r * 0.8:.0f}")
        out += (f'<g transform="translate({cx},{cy}) rotate({a})">' + pen.path(petal, fill="#e53935")
                + pen.path(veins, fill="none", w=DW - 0.4) + "</g>")
    out += pen.circle(cx, cy, r * 0.16, fill="#b71c1c", sw=DW)
    return out


def s_batik(pen):
    out = pen.tube("M300,1150 L320,980 M760,1150 L740,980", 14, "#8d6e63")
    out += pen.rect(270, 560, 520, 430, fill="#8d6e63", rx=6)
    cloth = "M292,582 L768,582 L768,968 L292,968 Z"
    out += pen.path(cloth, fill="#fff8e1", w=DW)
    motif = big_hibiscus(pen, 450, 740, 110, 10) + big_hibiscus(pen, 660, 880, 70, -20)
    motif += pen.path("M330,920 Q400,860 470,900 Q520,930 560,880", fill="none", w=DW)
    for x, y, a in ((340, 640, -30), (600, 650, 20), (720, 720, 60), (380, 880, 10), (560, 940, -40)):
        motif += rot(pen.path(f"M{x - 40},{y} Q{x},{y - 30} {x + 40},{y} Q{x},{y + 30} {x - 40},{y} Z", fill="#66bb6a") +
                     pen.line(x - 34, y, x + 34, y, sw=DW - 0.6), a, x, y)
    out += pen.clipped(cloth, motif)
    out += kid(pen, "aisyah", 150, GY, 1.05, la=(-60, -112), ra=(118, -250))
    hx, hy = 150 + 118 * 1.05, GY - 250 * 1.05
    out += pen.path(f"M{hx - 4},{hy + 6} L{hx + 40},{hy - 40}", fill="none", w=LW)
    out += pen.path(f"M{hx + 34},{hy - 52} L{hx + 54},{hy - 52} L{hx + 50},{hy - 34} L{hx + 38},{hy - 34} Z",
                    fill="#bdbdbd", w=DW)
    out += pen.path(f"M{hx + 50},{hy - 38} L{hx + 66},{hy - 26}", fill="none", w=DW)
    out += pen.path("M600,1150 L610,1080 L720,1080 L730,1150 Z", fill="#90a4ae")
    for x, c in ((630, "#e53935"), (665, "#1e88e5"), (700, "#fdd835")):
        out += pen.ellipse(x, 1080, 14, 6, fill=c, sw=DW - 0.4)
    return out, W


def s_songket(pen):
    out = pen.tube("M190,1150 L190,520 M710,1150 L710,520", 24, "#8d6e63")
    out += pen.rect(160, 520, 580, 36, fill="#a1887f", rx=8)
    for x in range(222, 690, 16):
        out += pen.line(x, 556, x, 840, sw=1.6)
    out += pen.rect(200, 836, 500, 24, fill="#a1887f", rx=6)
    cloth = "M210,860 L690,860 L690,990 L210,990 Z"
    out += pen.path(cloth, fill="#c62828", w=DW)
    pat = ""
    for x in range(210, 700, 60):
        pat += pen.path(f"M{x},990 L{x + 30},900 L{x + 60},990 Z", fill="#fdd835", w=DW - 0.4)
        pat += pen.path(f"M{x + 30},870 l10,10 -10,10 -10,-10 Z", fill="#fdd835", w=DW - 0.6)
    out += pen.clipped(cloth, pat) + pen.path(cloth, fill="none", w=DW)
    out += pen.rect(170, 990, 560, 36, fill="#a1887f", rx=8)
    out += pen.path("M380,848 Q450,828 520,848 Q450,868 380,848 Z", fill="#ffcc80", w=DW)
    out += pen.rect(300, 1080, 300, 26, fill="#8d6e63", rx=6)
    out += pen.tube("M320,1106 L320,1150 M580,1106 L580,1150", 10, "#8d6e63")
    out += kid(pen, "aisyah", 800, GY, 0.85, la=(-120, -210), ra=(60, -112))
    return out, W


def s_labu_sayong(pen):
    out = pen.ellipse(450, 1100, 250, 44, fill="#e6c27a")
    for k in range(1, 4):
        out += pen.ellipse(450, 1100, 250 * k / 4, 44 * k / 4, fill="none", sw=DW - 0.8)
    pot = ("M420,700 L420,760 Q290,780 270,900 Q256,1050 450,1090 Q644,1050 630,900 Q610,780 480,760 L480,700 Z")
    out += pen.path(pot, fill="#5d4037")
    out += pen.path("M396,640 Q450,620 504,640 L486,700 L414,700 Z", fill="#5d4037")
    out += pen.ellipse(450, 640, 54, 16, fill="#4e342e")
    out += pen.path("M430,620 Q430,580 450,574 Q470,580 470,620 Z", fill="#8d6e63")
    deco = ""
    for x in range(260, 650, 30):
        deco += pen.path(f"M{x},850 L{x + 15},880 L{x + 30},850", fill="none", w=DW)
    deco += pen.path("M270,900 Q450,930 630,900 M276,960 Q450,990 624,960", fill="none", w=DW)
    for x in (330, 450, 570):
        deco += small_flower(pen, x, 1015, 16, "#ffcc80")
        deco += pen.path(f"M{x - 50},1020 Q{x - 30},1000 {x - 22},1018", fill="none", w=DW - 0.6)
    deco += pen.path("M430,770 L430,700 M470,770 L470,700", fill="none", w=DW - 0.6)
    out += pen.clipped(pot, deco) + pen.path(pot, fill="none")
    out += pen.path("M150,1100 L160,1010 L240,1010 L250,1100 Z", fill="#5d4037")
    out += pen.ellipse(200, 1010, 40, 10, fill="#4e342e")
    out += pen.path("M162,1050 L238,1050", fill="none", w=DW - 0.6)
    k0 = pen.k
    pen.k = k0 / 0.42
    small = pen.path(pot, fill="#795548") + pen.path("M396,640 Q450,620 504,640 L486,700 L414,700 Z", fill="#795548")
    small += pen.ellipse(450, 640, 54, 16, fill="#4e342e")
    small += pen.clipped(pot, "".join(pen.path(f"M{x},850 L{x + 15},880 L{x + 30},850", fill="none", w=DW)
                                      for x in range(260, 650, 30)))
    pen.k = k0
    out += f'<g transform="translate(720,1092) scale(0.42) translate(-450,-1090)">{small}</g>'
    out += pen.path("M690,1100 L696,1060 L744,1060 L750,1100 Z", fill="#5d4037")
    return out, W


def wavy_blade(x0, x1, y, w0, luk=5):
    top, bot = [], []
    n = 60
    for i in range(n + 1):
        t = i / n
        x = x0 + (x1 - x0) * t
        c = y + 12 * math.sin(t * luk * math.pi)
        half = w0 * (1 - t ** 1.6) / 2
        top.append((x, c - half))
        bot.append((x, c + half))
    pts = top + bot[::-1]
    return "M" + " L".join(f"{px:.1f},{py:.1f}" for px, py in pts) + " Z"


def s_keris(pen):
    out = pen.rect(130, 1060, 640, 40, fill="#8d6e63", rx=8)
    for x in (250, 650):
        out += pen.rect(x - 16, 760, 32, 300, fill="#a1887f", rx=6)
        out += pen.path(f"M{x - 40},760 L{x - 20},800 L{x + 20},800 L{x + 40},760", fill="#a1887f")
        out += pen.path(f"M{x - 40},920 L{x - 20},950 L{x + 20},950 L{x + 40},920", fill="#a1887f")
    # sheath on the lower rest
    out += pen.path("M140,912 Q150,880 230,884 L320,890 Q340,906 320,922 L230,930 Q150,936 140,912 Z", fill="#d7a86e")
    out += pen.path("M320,898 L800,906 Q816,912 800,918 L320,916 Z", fill="#d7a86e")
    out += pen.path("M180,906 Q240,896 300,906", fill="none", w=DW - 0.6)
    # keris on the upper rest
    out += pen.path(wavy_blade(270, 820, 770, 46), fill="#cfd8dc")
    out += pen.path(wavy_blade(280, 800, 770, 4), fill="none", w=DW - 0.6)
    out += pen.path("M250,748 L290,744 L300,770 L290,796 L250,792 Q236,770 250,748 Z", fill="#fdd835")
    out += pen.rect(232, 752, 20, 36, fill="#c62828", rx=4, sw=DW)
    out += pen.path("M232,760 Q180,730 140,750 Q110,770 128,800 Q150,812 170,796 Q196,790 232,786 Z", fill="#8d6e63")
    out += pen.path("M150,764 Q164,758 170,770 M180,780 Q200,772 214,780", fill="none", w=DW - 0.6)
    out += pen.circle(146, 776, 5, fill=INK, sw=1)
    cloth = "M90,1104 L810,1104 L800,1170 L100,1170 Z"
    out += pen.path(cloth, fill="#8e24aa")
    out += pen.clipped(cloth, "".join(pen.path(f"M{x},1137 l14,-16 14,16 -14,16 Z", fill="#fdd835", w=1.6)
                                      for x in range(100, 800, 44)))
    out += pen.path(cloth, fill="none")
    for x in range(110, 800, 18):
        out += pen.line(x, 1170, x, 1186, sw=1.6)
    return out, W


def s_sape(pen):
    body = ("M396,1110 Q360,1060 364,900 L370,560 Q372,520 400,500 L500,500 Q528,520 530,560 L536,900 "
            "Q540,1060 504,1110 Z")
    out = pen.path(body, fill="#fff8e1")
    deco = ""
    for cy in (640, 820, 980):
        deco += pen.path(f"M450,{cy - 60} C510,{cy - 60} 520,{cy} 480,{cy + 10} C450,{cy + 18} 440,{cy - 10} 460,{cy - 20}",
                         fill="#e53935", w=DW)
        deco += pen.path(f"M450,{cy - 60} C390,{cy - 60} 380,{cy} 420,{cy + 10} C450,{cy + 18} 460,{cy - 10} 440,{cy - 20}",
                         fill="#1e88e5", w=DW)
        deco += pen.path(f"M390,{cy + 50} Q450,{cy + 20} 510,{cy + 50}", fill="none", w=DW)
    out += pen.clipped(body, deco) + pen.path(body, fill="none")
    out += pen.path("M400,500 Q380,430 420,380 Q450,350 480,380 Q520,430 500,500 Z", fill="#8d6e63")
    out += pen.path("M420,380 Q400,330 440,300 Q470,290 470,320 Q450,320 450,340 Q470,350 480,380",
                    fill="#8d6e63")
    for x in (430, 450, 470):
        out += pen.line(x, 500, x, 1080, sw=1.6)
    for y in range(520, 760, 40):
        out += pen.rect(410, y, 80, 8, fill="#a1887f", rx=3, sw=1.6)
    for x, y in ((430, 470), (470, 470), (450, 440)):
        out += pen.circle(x, y, 7, fill="#fdd835", sw=1.6)
    out += pen.rect(380, 1080, 140, 22, fill="#8d6e63", rx=6, sw=DW)
    out += kid(pen, "ravi", 180, GY, 0.95, outfit="tshirt", la=(-60, -112), ra=(120, -200))
    out += kid(pen, "amir", 730, GY, 0.95, la=(-110, -210), ra=(60, -112))
    return out, W


# ---------------------------------------------------------------- 14-15 pakaian

def festive_backdrop(pen):
    out = ""
    for x, y, sc in ((120, 330, 0.9), (240, 400, 0.75), (360, 330, 0.9)):
        out += pen.line(x, 150, x, y - 92 * sc, sw=DW) + ketupat(pen, x, y, sc)
    return out + pelita(pen, 110, 760) + pelita(pen, 800, 790)


def s_baju_melayu(pen):
    out = festive_backdrop(pen) + kid(pen, "amir", 450, 1150, 1.85, outfit="bajumelayu", la=(-70, -112), ra=(70, -112))
    out += small_flower(pen, 120, 1080, 22) + small_flower(pen, 790, 1080, 22, "#fdd835")
    return out, W


def s_baju_kurung(pen):
    out = festive_backdrop(pen) + kid(pen, "aisyah", 450, 1150, 1.85, la=(-70, -112), ra=(70, -112))
    out += small_flower(pen, 120, 1080, 22, "#ba68c8") + small_flower(pen, 790, 1080, 22, "#fdd835")
    return out, W


# ---------------------------------------------------------------- 16-18 seni bina & perahu

def rumah_melayu(pen):
    out = ""
    for x in (180, 300, 420, 540, 660, 760):
        out += pen.rect(x, 870, 22, 140, fill="#8d6e63", sw=DW + 0.6)
        out += pen.rect(x - 8, 1000, 38, 16, fill="#9e9e9e", rx=3, sw=DW)
    out += pen.rect(150, 860, 650, 22, fill="#8d6e63", rx=4)
    out += pen.rect(170, 700, 610, 162, fill="#f5deb3")
    for x in range(190, 780, 24):
        out += pen.line(x, 704, x, 858, sw=1.4)
    for x in (210, 640):
        out += pen.rect(x, 730, 100, 110, fill="#8d6e63")
        out += pen.line(x + 50, 730, x + 50, 840, sw=DW)
        out += pen.rect(x, 704, 100, 22, fill="#ffffff", sw=DW)
        for k in range(5):
            out += pen.circle(x + 10 + k * 20, 715, 5, fill="#fdd835", sw=1.4)
    out += pen.rect(420, 726, 110, 136, fill="#8d6e63")
    out += pen.path("M110,710 L300,540 L650,540 L840,710 Z", fill="#8d4f2a")
    out += pen.path("M300,540 L475,420 L650,540 Z", fill="#ffe0b2")
    for k in range(9):
        a = math.radians(200 + k * 17.5)
        out += pen.line(475, 540, 475 + 150 * math.cos(a) * 1.2, 540 + 100 * math.sin(a), sw=DW - 0.4)
    out += pen.path("M300,540 L475,420 L650,540", fill="none", w=LW + 1)
    out += pen.path("M455,430 L495,380 M495,430 L455,380", fill="none", w=LW + 2)
    out += pen.path("M430,862 L400,1010 M520,862 L550,1010", fill="none", w=LW)
    for i in range(5):
        y = 890 + i * 26
        out += pen.line(426 - i * 6, y, 524 + i * 6, y, sw=DW + 0.6)
    return out


def s_rumah_melayu(pen):
    out = palm(pen, 80, 1000, 440, lean=24) + rumah_melayu(pen)
    out += kid(pen, "amir", 640, GY, 0.75, la=(-60, -112), ra=(70, -300))
    out += kid(pen, "aisyah", 280, GY, 0.72)
    return out, W


def hornbill(pen, x, y, s=1.0):
    g = pen.path("M-60,0 Q-20,-40 40,-20 Q80,-10 110,10 Q60,20 0,30 Q-40,30 -60,0 Z", fill="#212121")
    g += pen.path("M-20,-20 Q-80,-120 -170,-110 Q-110,-60 -40,0 Z", fill="#ffffff")
    g += pen.path("M20,-20 Q60,-110 150,-120 Q110,-60 50,-4 Z", fill="#ffffff")
    g += pen.path("M100,4 Q140,-30 160,-10 Q150,14 110,16 Z", fill="#212121")
    g += pen.path("M150,-12 Q210,-30 240,4 Q200,4 156,8 Z", fill="#fdd835")
    g += pen.path("M150,-14 Q190,-40 220,-20 Q190,-24 156,-10 Z", fill="#e53935")
    g += pen.circle(146, -2, 4, fill="#ffffff", sw=1.4)
    g += pen.path("M-60,0 L-120,20 L-110,34 L-56,18 Z", fill="#ffffff")
    return f'<g transform="translate({x},{y}) scale({s})">{g}</g>'


def s_rumah_panjang(pen):
    out = hornbill(pen, 190, 470, 0.9)
    for x in range(70, 860, 70):
        out += pen.rect(x, 860, 18, 180, fill="#8d6e63", sw=DW)
    out += pen.rect(40, 840, 830, 24, fill="#a1887f", rx=4)
    out += pen.rect(60, 690, 790, 150, fill="#d7a86e")
    for i, x in enumerate(range(90, 840, 110)):
        out += pen.rect(x, 730, 60, 108, fill="#8d6e63", rx=4, sw=DW + 0.6)
        out += pen.circle(x + 48, 784, 4, fill="#fdd835", sw=1.4)
        out += pen.path(f"M{x + 68},740 L{x + 100},740 L{x + 100},780 L{x + 68},780 Z", fill="#8d6e63", w=DW)
    out += pen.path("M20,700 L120,590 L790,590 L890,700 Z", fill="#8d4f2a")
    for x in range(140, 790, 50):
        out += pen.line(x, 594, x - 30, 696, sw=1.6)
    out += pen.rect(40, 820, 830, 10, fill="#a1887f", sw=DW)
    for x in range(60, 870, 30):
        out += pen.line(x, 800, x, 820, sw=DW - 0.4)
    out += pen.line(40, 800, 870, 800, sw=DW)
    log = "M330,1120 L380,850 L410,856 L364,1126 Z"
    out += pen.path(log, fill="#a1887f")
    for i in range(6):
        y = 1080 - i * 45
        x = 352 + (1120 - y) * 0.18
        out += pen.path(f"M{x - 4},{y} L{x + 22},{y - 6}", fill="none", w=DW)
    out += kid(pen, "amir", 600, GY, 0.8, la=(-60, -112), ra=(70, -300))
    return out, W


def s_perahu(pen):
    out = pen.tube("M440,880 L440,470", 12, "#8d6e63")
    out += pen.path("M446,480 Q620,560 700,820 L446,820 Z", fill="#ffffff")
    out += pen.path("M446,560 Q560,620 610,720", fill="none", w=DW)
    out += pen.path("M434,500 Q300,600 250,820 L434,820 Z", fill="#ffe082")
    for d in ("M446,480 Q620,560 700,820 L446,820 Z", "M434,500 Q300,600 250,820 L434,820 Z"):
        out += pen.clipped(d, "".join(pen.line(200, y, 720, y, sw=1.6) for y in range(560, 820, 52)))
    hull = "M90,760 Q120,860 200,900 L700,900 Q800,860 830,740 Q760,820 650,830 L250,830 Q150,830 90,760 Z"
    out += pen.path(hull, fill="#1e88e5")
    deco = ""
    for x in range(220, 700, 60):
        deco += pen.path(f"M{x},850 l14,14 -14,14 -14,-14 Z", fill="#fdd835", w=DW - 0.4)
    deco += pen.path("M150,850 Q450,880 760,840", fill="none", w=DW)
    deco += pen.rect(80, 868, 760, 40, fill="#e53935", sw=DW)
    out += pen.clipped(hull, deco) + pen.path(hull, fill="none")
    out += pen.path("M90,760 Q60,660 100,620 Q130,600 140,640 Q110,650 120,700 Q130,740 150,790 Z", fill="#e53935")
    out += pen.path("M830,740 Q860,650 830,610 Q810,600 800,630 Q820,650 812,700 Q800,740 790,790 Z",
                    fill="#e53935")
    out += pen.circle(118, 650, 6, fill="#fdd835", sw=1.4) + pen.circle(818, 640, 6, fill="#fdd835", sw=1.4)
    waves = "M18,930 " + "".join("q30,-24 60,0 " for _ in range(15)) + "L887,1262 L18,1262 Z"
    out += pen.path(waves, fill="#29b6f6")
    for y, off in ((1020, 0), (1100, 70), (1180, 30)):
        for x in range(60 + off, 860, 160):
            out += pen.path(f"M{x},{y} q18,-14 36,0 q18,14 36,0", fill="none", w=DW)
    for fx, fy, c, flip in ((170, 1150, "#ff7043", 1), (700, 1190, "#fdd835", -1), (440, 1225, "#ab47bc", 1)):
        body = (f"M{fx - 64 * flip},{fy} Q{fx},{fy - 42} {fx + 42 * flip},{fy} Q{fx},{fy + 42} {fx - 64 * flip},{fy} Z "
                f"M{fx + 38 * flip},{fy} L{fx + 76 * flip},{fy - 26} L{fx + 76 * flip},{fy + 26} Z")
        out += pen.path(body, fill=c, w=DW)
        out += pen.path(f"M{fx - 20 * flip},{fy - 28} Q{fx - 10 * flip},{fy} {fx - 20 * flip},{fy + 28}", fill="none", w=1.6)
        for k in range(3):
            out += pen.path(f"M{fx + (k * 14 - 6) * flip},{fy - 12} Q{fx + (k * 14 + 2) * flip},{fy} {fx + (k * 14 - 6) * flip},"
                            f"{fy + 12}", fill="none", w=1.4)
        out += pen.circle(fx - 40 * flip, fy - 8, 5, fill=INK, sw=1)
    for x, y, r in ((200, 1130, 6), (210, 1105, 4), (760, 1160, 6), (770, 1138, 4)):
        out += pen.circle(x, y, r, fill="#e1f5fe", sw=1.4)
    return out, W


# ---------------------------------------------------------------- 19-23 perayaan

def ketupat(pen, cx, cy, s=1.0):
    d = f"M{cx},{cy - 50 * s} L{cx + 50 * s},{cy} L{cx},{cy + 50 * s} L{cx - 50 * s},{cy} Z"
    grid = ""
    for k in range(-3, 4):
        o = k * 14 * s
        grid += pen.line(cx - 60 * s + o, cy - 60 * s - o, cx + 60 * s + o, cy + 60 * s - o, sw=1.6)
        grid += pen.line(cx - 60 * s - o, cy + 60 * s - o, cx + 60 * s - o, cy - 60 * s - o, sw=1.6)
    out = pen.path(d, fill="#aed581") + pen.clipped(d, grid) + pen.path(d, fill="none")
    out += pen.path(f"M{cx - 6 * s},{cy - 50 * s} Q{cx - 20 * s},{cy - 80 * s} {cx - 30 * s},{cy - 96 * s} "
                    f"M{cx + 6 * s},{cy - 50 * s} Q{cx + 12 * s},{cy - 80 * s} {cx + 26 * s},{cy - 92 * s}",
                    fill="none", w=DW)
    return out


def pelita(pen, x, top, base=GY):
    out = pen.tube(f"M{x},{base} L{x},{top + 40}", 16, "#aed581")
    for y in range(int(top) + 100, base, 90):
        out += pen.line(x - 8, y, x + 8, y, sw=DW)
    out += pen.path(f"M{x - 22},{top + 40} L{x + 22},{top + 40} L{x + 16},{top + 4} L{x - 16},{top + 4} Z", fill="#bdbdbd")
    out += pen.line(x, top + 4, x, top - 8, sw=DW)
    out += pen.path(f"M{x},{top - 50} Q{x - 18},{top - 20} {x},{top - 8} Q{x + 18},{top - 20} {x},{top - 50} Z",
                    fill="#ff9800", w=DW)
    return out


def s_hari_raya(pen):
    out = ""
    for x, y, s in ((120, 330, 1.0), (240, 400, 0.85), (380, 330, 1.0)):
        out += pen.line(x, 150, x, y - 92 * s, sw=DW)
        out += ketupat(pen, x, y, s)
    out += pelita(pen, 90, 720) + pelita(pen, 820, 760)
    la_a, ra_a = (-60, -112), (110, -150)
    la_b, ra_b = (-110, -150), (60, -112)
    out += kid(pen, "amir", 330, GY, 1.3, outfit="bajumelayu", la=la_a, ra=ra_a, arms_front=True)
    out += kid(pen, "aisyah", 590, GY, 1.3, la=la_b, ra=ra_b, arms_front=True)
    return out, W


def lantern(pen, x, y, s=1.0):
    body = f"M{x - 60 * s},{y} Q{x - 64 * s},{y - 70 * s} {x},{y - 72 * s} Q{x + 64 * s},{y - 70 * s} {x + 60 * s},{y} " \
           f"Q{x + 64 * s},{y + 70 * s} {x},{y + 72 * s} Q{x - 64 * s},{y + 70 * s} {x - 60 * s},{y} Z"
    out = pen.path(body, fill="#e53935")
    for k in (-0.6, -0.25, 0.25, 0.6):
        out += pen.path(f"M{x + k * 60 * s},{y - 66 * s} Q{x + k * 100 * s},{y} {x + k * 60 * s},{y + 66 * s}",
                        fill="none", w=DW - 0.4)
    out += pen.rect(x - 30 * s, y - 84 * s, 60 * s, 16 * s, fill="#fdd835", rx=3, sw=DW)
    out += pen.rect(x - 30 * s, y + 68 * s, 60 * s, 16 * s, fill="#fdd835", rx=3, sw=DW)
    for k in (-14, 0, 14):
        out += pen.line(x + k * s, y + 84 * s, x + k * s, y + 130 * s, sw=DW)
    return out


def s_tahun_baru_cina(pen):
    out = pen.line(40, 190, 500, 170, sw=DW)
    for x, y, s in ((120, 300, 0.9), (290, 290, 1.0), (450, 280, 0.8)):
        out += pen.line(x, 186 - (x - 40) * 0.04, x, y - 84 * s, sw=DW)
        out += lantern(pen, x, y, s)
    la, ra = (-30, -170), (30, -170)
    out += kid(pen, "mei", 380, GY, 1.45, la=la, ra=ra, arms_front=True, hands=False)
    hx, hy = 380, GY - 182 * 1.45
    out += pen.rect(hx - 36, hy - 50, 72, 100, fill="#e53935", rx=6)
    out += pen.circle(hx, hy - 10, 16, fill="#fdd835", sw=DW)
    out += kid_hands(pen, "mei", 380, GY, 1.45, la=la, ra=ra)
    out += pen.rect(600, 1000, 260, 26, fill="#8d6e63", rx=6)
    out += pen.tube("M620,1026 L620,1150 M840,1026 L840,1150", 12, "#8d6e63")
    out += pen.path("M630,1000 Q730,1060 830,1000 Z", fill="#ffffff")
    for x, y in ((670, 970), (720, 960), (770, 970), (695, 925), (745, 925)):
        out += pen.circle(x, y, 28, fill="#ff9800")
        out += pen.path(f"M{x},{y - 28} Q{x + 14},{y - 44} {x + 26},{y - 36} Q{x + 14},{y - 26} {x},{y - 28} Z",
                        fill="#43a047", w=DW - 0.4)
    return out, W


def diya(pen, x, y, s=1.0):
    out = pen.path(f"M{x - 34 * s},{y} Q{x},{y + 36 * s} {x + 34 * s},{y} L{x + 50 * s},{y - 10 * s} Q{x},{y - 6 * s} "
                   f"{x - 34 * s},{y} Z", fill="#ff7043", w=DW + 0.4)
    out += pen.path(f"M{x + 34 * s},{y - 14 * s} Q{x + 22 * s},{y - 40 * s} {x + 34 * s},{y - 58 * s} "
                    f"Q{x + 48 * s},{y - 40 * s} {x + 34 * s},{y - 14 * s} Z", fill="#fdd835", w=DW)
    return out


def s_deepavali(pen):
    out = ""
    for i in range(10):
        x = 40 + i * 48
        y = 180 + 30 * math.sin(i / 9 * math.pi)
        out += pen.circle(x, y, 18, fill="#ff9800" if i % 2 else "#fdd835", sw=DW)
    out += pen.line(22, 180, 500, 180, sw=DW - 0.6)
    la, ra = (-70, -112), (90, -170)
    out += kid(pen, "ravi", 450, 960, 1.25, la=la, ra=ra)
    cx, cy = 450, 1110
    out += pen.ellipse(cx, cy, 340, 120, fill="#fff59d")
    for k in range(16):
        a = 2 * math.pi * k / 16
        px, py = cx + 250 * math.cos(a), cy + 86 * math.sin(a)
        out += pen.ellipse(round(px), round(py), 42, 18, fill="#f06292" if k % 2 else "#4fc3f7", sw=DW,
                           rot=round(math.degrees(math.atan2(86 * math.sin(a), 250 * math.cos(a)))))
    out += pen.ellipse(cx, cy, 190, 64, fill="#ba68c8", sw=DW)
    for k in range(8):
        a = 2 * math.pi * k / 8
        out += pen.ellipse(round(cx + 120 * math.cos(a)), round(cy + 40 * math.sin(a)), 30, 13, fill="#ffb74d",
                           sw=DW, rot=round(math.degrees(math.atan2(40 * math.sin(a), 120 * math.cos(a)))))
    out += pen.ellipse(cx, cy, 60, 22, fill="#e53935", sw=DW)
    for x, y in ((120, 1060), (780, 1060), (170, 1190), (730, 1190), (450, 1238)):
        out += diya(pen, x, y, 1.0)
    out += diya(pen, 450 + 90 * 1.25, 960 - 186 * 1.25, 0.9)
    return out, W


def tajau(pen, x, base):
    d = f"M{x - 40},{base - 260} Q{x - 110},{base - 200} {x - 100},{base - 90} Q{x - 90},{base} {x},{base} " \
        f"Q{x + 90},{base} {x + 100},{base - 90} Q{x + 110},{base - 200} {x + 40},{base - 260} Z"
    out = pen.path(d, fill="#8d6e63")
    out += pen.rect(x - 46, base - 290, 92, 32, fill="#795548", rx=6)
    out += pen.clipped(d, pen.path(f"M{x - 120},{base - 170} Q{x - 60},{base - 210} {x},{base - 170} "
                                   f"Q{x + 60},{base - 130} {x + 120},{base - 170}", fill="none", w=DW)
                       + pen.path(f"M{x - 120},{base - 110} Q{x - 60},{base - 150} {x},{base - 110} "
                                  f"Q{x + 60},{base - 70} {x + 120},{base - 110}", fill="none", w=DW))
    for k in (-1, 1):
        out += pen.circle(x + k * 70, base - 230, 12, fill="#fdd835", sw=DW)
    return out


def padi(pen, x, base, h):
    out = pen.path(f"M{x},{base} Q{x + 6},{base - h * 0.6} {x + 20},{base - h}", fill="none", w=DW)
    for k in range(5):
        y = base - h * (0.65 + k * 0.07)
        xx = x + 6 + k * 3
        out += pen.ellipse(round(xx + 8), round(y), 7, 4, fill="#fdd835", sw=1.4, rot=-30)
    return out


def s_kaamatan(pen):
    out = ""
    for x in range(40, 880, 34):
        if 230 < x < 690:
            continue
        out += padi(pen, x, 1150, 150 + (x * 37) % 50)
    out += tajau(pen, 780, 1150)
    out += kid(pen, "lina", 450, 1150, 1.5, la=(-160, -240), ra=(160, -240))
    out += bunting(pen, 30, 470, 520, 440, 9, colors=("#212121", "#fdd835", "#e53935"))
    return out, W


def jalur_gemilang(pen, px, top, w=440, h=280):
    """Jalur Gemilang flying to the right from a pole at x=px: canton at the upper hoist, red stripe on top."""
    stripes = 14

    def band(y0, y1):
        return (f"M{px},{y0:.1f} Q{px + w * 0.25},{y0 + 26:.1f} {px + w * 0.5},{y0:.1f} T{px + w},{y0:.1f} "
                f"L{px + w},{y1:.1f} Q{px + w * 0.75},{y1 - 26:.1f} {px + w * 0.5},{y1:.1f} T{px},{y1:.1f} Z")

    outline = band(top, top + h)
    inner = ""
    for i in range(stripes):
        y = top + h * i / stripes
        inner += (f'<path d="{band(y, y + h / stripes)}" fill="{pen.f("#e53935" if i % 2 == 0 else "#ffffff")}" '
                  f'stroke="{INK}" stroke-width="{pen.sw(1.4)}"/>')
    cw, ch = w * 0.5, h * 8 / 14
    inner += pen.path(f"M{px},{top} Q{px + cw * 0.5},{top + 26} {px + cw},{top} L{px + cw},{top + ch} "
                      f"Q{px + cw * 0.5},{top + ch + 20} {px},{top + ch} Z", fill="#1a237e", w=DW)
    mx, my = px + cw * 0.4, top + ch * 0.54
    # crescent nearer the pole, opening towards the 14-point star
    inner += pen.path(f"M{mx + 10},{my - 52} A54,54 0 1 0 {mx + 10},{my + 52} A44,44 0 1 1 {mx + 10},{my - 52} Z",
                      fill="#fdd835", w=DW)
    inner += pen.path(star_d(mx + 58, my, 34, 16, 14), fill="#fdd835", w=DW)
    return pen.clipped(outline, inner) + pen.path(outline, fill="none")


def s_hari_kebangsaan(pen):
    px = 130
    out = pen.tube(f"M{px},1100 L{px},400", 14, "#9e9e9e")
    out += pen.circle(px, 396, 12, fill="#fdd835", sw=DW)
    out += jalur_gemilang(pen, px + 6, 420)
    out += kid(pen, "amir", 221, GY, 1.3, la=(-70, -112), ra=(-70, -160))
    out += kid(pen, "mei", 500, GY, 1.0, la=(-90, -300), ra=(64, -112))
    out += kid(pen, "ravi", 760, GY, 0.95, la=(-64, -112), ra=(70, -300))
    return out, W


# ---------------------------------------------------------------- 24-29 makanan

def plate(pen, cx, cy, rx, ry):
    out = pen.ellipse(cx, cy, rx, ry, fill="#ffffff")
    n = max(10, int(rx / 18))
    for k in range(n):
        a = 2 * math.pi * k / n
        out += pen.circle(cx + rx * 0.9 * math.cos(a), cy + ry * 0.89 * math.sin(a), max(4, rx / 45), fill="#64b5f6", sw=1.2)
    return out + pen.ellipse(cx, cy, rx * 0.8, ry * 0.78, fill="#ffffff", sw=DW)


def s_nasi_lemak(pen):
    out = plate(pen, 450, 900, 360, 160)
    out += pen.path("M150,900 Q300,760 600,780 Q760,800 760,900 Q600,1010 300,1000 Q170,980 150,900 Z", fill="#7cb342")
    out += pen.path("M180,900 Q450,860 740,880 M300,830 L360,890 M420,800 L460,870 M540,800 L560,870 "
                    "M650,820 L640,880", fill="none", w=DW - 0.6)
    out += pen.path("M300,900 Q300,770 420,760 Q540,770 540,900 Q420,930 300,900 Z", fill="#ffffff")
    for x, y in ((360, 830), (420, 800), (480, 840), (400, 870)):
        out += pen.ellipse(x, y, 10, 6, fill="#ffffff", sw=1.4)
    for x in (590, 680):
        out += pen.ellipse(x, 880, 52, 36, fill="#ffffff")
        out += pen.circle(x, 880, 20, fill="#fdd835", sw=DW)
    for i, x in enumerate((230, 280, 330)):
        out += pen.ellipse(x, 950, 30, 22, fill="#c5e1a5")
        out += pen.ellipse(x, 950, 20, 14, fill="#f1f8e9", sw=DW - 0.6)
    out += pen.path(blob_d(470, 965, 70, 30, 9, 3), fill="#e53935")
    for x, y in ((450, 950), (490, 970), (470, 980)):
        out += pen.ellipse(x, y, 8, 4, fill="#b71c1c", sw=1.4, rot=20)
    for k in range(7):
        x, y = 600 + (k % 4) * 30, 950 + (k // 4) * 24
        out += pen.path(f"M{x},{y} Q{x + 10},{y - 8} {x + 22},{y} Q{x + 10},{y + 6} {x},{y} Z M{x + 22},{y} l6,-5 0,10 Z",
                        fill="#ffcc80", w=1.8)
    for k in range(8):
        out += pen.ellipse(560 + (k % 4) * 26, 1000 + (k // 4) * 16, 9, 6, fill="#d7a86e", sw=1.6)
    out += pen.path("M790,760 L850,760 L842,860 L798,860 Z", fill="#ffcc80")
    out += pen.rect(800, 772, 22, 22, fill="#ffffff", rx=4, sw=1.6) + pen.rect(818, 800, 20, 20, fill="#ffffff", rx=4, sw=1.6)
    out += pen.tube("M830,770 L850,700 L870,700", 8, "#e53935")
    out += f'<g transform="rotate(-30 120 1120)">' + pen.rect(60, 1112, 130, 14, fill="#bdbdbd", rx=7) + \
        pen.ellipse(200, 1119, 30, 20, fill="#bdbdbd") + "</g>"
    return out, W


def skewer(pen, x0, y0, x1, y1, n=4):
    out = pen.line(x0, y0, x1, y1, sw=DW + 0.4)
    for k in range(n):
        t = 0.2 + k * 0.17
        x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        out += pen.rect(x - 15, y - 13, 30, 26, fill="#a1662f", rx=8, sw=DW)
    return out


def s_sate(pen):
    out = ""
    for x in (250, 380, 510):
        out += pen.path(f"M{x},780 Q{x - 30},720 {x},680 Q{x + 30},640 {x},590", fill="none", w=DW + 0.6)
    out += pen.rect(140, 880, 620, 60, fill="#757575", rx=8)
    out += pen.path("M150,890 L750,890", fill="none", w=DW)
    for x in range(170, 740, 40):
        out += pen.path(f"M{x},890 q10,-18 20,0", fill="#ff7043", w=DW - 0.4)
    for i in range(8):
        x = 190 + i * 72
        out += skewer(pen, x, 930, x + 60, 820)
    out += pen.tube("M170,940 L150,1150 M730,940 L750,1150", 14, "#616161")
    out += plate(pen, 330, 1150, 220, 70)
    for i in range(5):
        out += skewer(pen, 190 + i * 40, 1172, 260 + i * 40, 1110, 3)
    out += pen.ellipse(600, 1150, 90, 34, fill="#ffffff")
    out += pen.ellipse(600, 1146, 70, 22, fill="#d4883a", sw=DW)
    for x, y in ((730, 1170), (800, 1180)):
        out += ketupat(pen, x, y, 0.5)
    return out, W


def mug(pen, x, y, s=1.0, foam=False):
    out = pen.path(f"M{x - 34 * s},{y - 60 * s} L{x + 34 * s},{y - 60 * s} L{x + 28 * s},{y + 40 * s} "
                   f"L{x - 28 * s},{y + 40 * s} Z", fill="#cfd8dc")
    out += pen.path(f"M{x + 32 * s},{y - 40 * s} Q{x + 66 * s},{y - 30 * s} {x + 30 * s},{y + 14 * s}", fill="none",
                    w=LW)
    if foam:
        out += pen.path(blob_d(x, y - 62 * s, 36 * s, 10 * s, 7, 2), fill="#fff8e1", w=DW)
    return out


def s_teh_tarik(pen):
    la, ra = (84, -120), (128, -350)
    out = kid(pen, "amir", 330, GY, 1.45, la=la, ra=ra, hands=False, arms_front=True)
    top = (330 + 128 * 1.45, GY - 350 * 1.45)
    low = (330 + 84 * 1.45, GY - 120 * 1.45)
    out += pen.tube(f"M{top[0] + 30},{top[1] - 26} Q{top[0] + 70},{top[1] + 120} {low[0] + 4},{low[1] - 70}", 16,
                    "#d7a86e")
    out += rot(mug(pen, top[0], top[1], 1.0), 40, top[0], top[1])
    out += mug(pen, low[0], low[1], 1.0, foam=True)
    out += kid_hands(pen, "amir", 330, GY, 1.45, la=la, ra=ra)
    out += pen.rect(640, 1000, 230, 24, fill="#8d6e63", rx=6)
    out += pen.tube("M660,1024 L660,1150 M850,1024 L850,1150", 12, "#8d6e63")
    for x in (700, 790):
        out += pen.path(f"M{x - 22},940 L{x + 22},940 L{x + 18},1000 L{x - 18},1000 Z", fill="#d7a86e")
        out += pen.path(blob_d(x, 940, 22, 6, 6, 4), fill="#fff8e1", w=DW - 0.4)
    out += pen.line(340, 150, 340, 196, sw=DW) + pen.line(500, 150, 500, 196, sw=DW)
    out += pen.rect(300, 196, 240, 70, fill="#e53935", rx=10)
    out += pen.text(420, 244, "KEDAI KOPI", 34, fill_color="#ffffff", spacing=2)
    return out, W


def s_kuih_muih(pen):
    out = pen.ellipse(450, 940, 380, 180, fill="#ffcc80")
    out += pen.ellipse(450, 932, 340, 152, fill="#fff3e0", sw=DW)
    for k in range(24):
        a = 2 * math.pi * k / 24
        out += pen.circle(450 + 360 * math.cos(a), 940 + 166 * math.sin(a), 6, fill="#e53935", sw=1.4)
    for x, y in ((230, 900), (275, 870), (270, 925), (315, 900), (250, 960)):
        out += pen.circle(x, y, 26, fill="#7cb342")
        for dx, dy in ((-8, -10), (6, -12), (10, 4), (-6, 8)):
            out += pen.circle(x + dx, y + dy, 2.4, fill="#ffffff", sw=1)
    for i in range(3):
        x = 390 + i * 70
        for k in range(5):
            out += pen.rect(x, 830 + k * 14, 56, 14, fill=["#e53935", "#ffffff"][k % 2], sw=DW - 0.6)
    for x in (600, 670):
        out += pen.rect(x, 850, 58, 34, fill="#43a047", sw=DW)
        out += pen.rect(x, 884, 58, 30, fill="#ffffff", sw=DW)
    for x, y in ((380, 1010), (480, 1030)):
        out += pen.path(f"M{x - 50},{y} Q{x},{y - 70} {x + 50},{y} Z", fill="#ffb74d")
        for k in range(8):
            out += pen.circle(x - 44 + k * 12.5, y - 2, 4.5, fill="#ffb74d", sw=1.4)
    for x, y in ((610, 1000), (690, 990)):
        out += pen.path(f"M{x - 34},{y + 20} L{x},{y - 40} L{x + 34},{y + 20} Z", fill="#7cb342")
        out += pen.path(f"M{x},{y - 40} L{x},{y + 20}", fill="none", w=DW - 0.6)
    return out, W


def s_lemang(pen):
    out = pen.tube("M160,1150 L190,700 M740,1150 L710,700", 16, "#8d6e63")
    out += pen.tube("M150,720 L750,720", 16, "#8d6e63")
    for i in range(6):
        x = 230 + i * 90
        out += pen.path(f"M{x - 24},1110 L{x + 20},700 L{x + 56},704 L{x + 16},1114 Z", fill="#9ccc65")
        for k in (0.3, 0.6):
            y = 1110 - 410 * k
            xx = x - 24 + 44 * k
            out += pen.line(xx, y, xx + 38, y + 2, sw=DW)
        out += pen.path(f"M{x + 20},700 Q{x + 40},650 {x + 66},676 L{x + 56},704 Z", fill="#7cb342", w=DW)
    out += pen.rect(150, 1110, 600, 30, fill="#616161", rx=8)
    for x in range(180, 740, 60):
        out += pen.path(f"M{x},1112 Q{x + 6},1060 {x + 22},1040 Q{x + 22},1076 {x + 36},1060 Q{x + 40},1090 "
                        f"{x + 30},1112 Z", fill="#ff9800", w=DW)
    out += plate(pen, 160, 1190, 120, 42)
    for x in (120, 165, 205):
        out += pen.ellipse(x, 1176, 20, 14, fill="#fff8e1", sw=DW)
        out += pen.path(f"M{x - 20},1176 L{x - 20},1196 Q{x},1206 {x + 20},1196 L{x + 20},1176", fill="#fff8e1", w=DW)
    out += kid(pen, "amir", 820, GY, 0.72, la=(-60, -112), ra=(70, -300))
    return out, W


def s_ketupat(pen):
    la, ra = (-56, -150), (56, -150)
    out = kid(pen, "aisyah", 330, 1080, 1.4, la=la, ra=ra, sit=True, hands=False)
    hx, hy = 330, 1080 + (-150 + 92) * 1.4
    out += ketupat(pen, hx, hy - 6, 0.9)
    out += kid_hands(pen, "aisyah", 330, 1080, 1.4, la=la, ra=ra, sit=True)
    basket = "M560,1010 L800,1010 L770,1160 L590,1160 Z"
    for x, y in ((610, 990), (680, 970), (750, 990), (645, 1000), (715, 1000)):
        out += ketupat(pen, x, y, 0.62)
    out += pen.path(basket, fill="#d7a86e")
    out += pen.clipped(basket, "".join(pen.line(x, 1000, x + 60, 1170, sw=1.6) + pen.line(x + 60, 1000, x, 1170, sw=1.6)
                                       for x in range(540, 820, 26)))
    out += pen.path(basket, fill="none")
    out += pen.rect(550, 1000, 260, 18, fill="#bc8a5f", rx=6)
    return out, W


# ---------------------------------------------------------------- 30 bunga raya

def leaf(pen, x, y, l, ang, fill="#43a047"):
    d = f"M0,0 Q{l * 0.4},{-l * 0.32} {l},0 Q{l * 0.4},{l * 0.32} 0,0 Z"
    teeth = "".join(f"M{l * t:.0f},{-l * 0.2 * math.sin(t * math.pi):.0f} l6,-6" for t in (0.3, 0.5, 0.7))
    return (f'<g transform="translate({x},{y}) rotate({ang})">' + pen.path(d, fill=fill)
            + pen.path(f"M4,0 L{l - 6},0 " + teeth, fill="none", w=DW - 0.6) + "</g>")


def s_bunga_raya(pen):
    out = pen.tube("M450,1150 Q440,980 450,860", 16, "#7cb342")
    out += pen.tube("M450,1000 Q560,940 620,880", 12, "#7cb342")
    out += leaf(pen, 450, 1020, 170, 200) + leaf(pen, 450, 1060, 170, -20) + leaf(pen, 600, 900, 120, -60)
    out += leaf(pen, 446, 920, 140, 210)
    out += pen.path("M620,880 Q610,820 640,790 Q670,820 660,880 Z", fill="#e53935")
    out += pen.path("M620,880 Q640,900 660,880 L652,900 Q640,910 628,900 Z", fill="#7cb342", w=DW)
    out += big_hibiscus(pen, 430, 690, 230, 15)
    out += pen.tube("M430,690 Q470,560 540,500", 14, "#ffcc80")
    for x, y in ((536, 490), (552, 500), (548, 518), (530, 520), (522, 504)):
        out += pen.circle(x, y, 10, fill="#b71c1c", sw=DW - 0.4)
    for k in range(10):
        t = 0.45 + k * 0.05
        x = 430 + (540 - 430) * t
        y = 690 + (500 - 690) * t
        out += pen.circle(x + (8 if k % 2 else -8), y, 4.5, fill="#fdd835", sw=1.4)
    out += f'<g transform="translate(150,520) rotate(-15) scale(1.4)">' \
           f'{pen.ellipse(-14, -10, 16, 20, fill="#ff9800", sw=DW, rot=-25)}{pen.ellipse(14, -10, 16, 20, fill="#ff9800", sw=DW, rot=25)}' \
           f'{pen.ellipse(-10, 12, 10, 12, fill="#fdd835", sw=DW, rot=20)}{pen.ellipse(10, 12, 10, 12, fill="#fdd835", sw=DW, rot=-20)}' \
           f'{pen.ellipse(0, 0, 4, 16, fill="#5d4037", sw=1.4)}</g>'
    out += pen.tube("M720,1150 Q710,1060 716,1000", 12, "#7cb342")
    out += leaf(pen, 716, 1080, 110, -30) + leaf(pen, 714, 1110, 100, 210)
    out += big_hibiscus(pen, 716, 960, 100, 40)
    out += pen.circle(716, 960, 10, fill="#fdd835", sw=DW)
    return out, W


# ---------------------------------------------------------------- page list

def page(title, subject, scene, ref=(22, 330, 900)):
    return (title, subject, lambda pen, sc=scene: (sc(pen), ""), dict(x0=0, y=0, ref=ref))


PAGES = [
    page("Wau Bulan", s_wau, lambda p: outdoor(p, sunny=False), ref=(22, 340, 880)),
    page("Gasing", s_gasing, outdoor),
    page("Congkak", s_congkak, indoor, ref=(40, 520, 760)),
    page("Sepak Takraw", s_sepak_takraw, outdoor),
    page("Batu Seremban", s_batu_seremban, indoor, ref=(60, 500, 760)),
    page("Seni Silat", s_silat, outdoor, ref=(22, 400, 880)),
    page("Kompang", s_kompang, lambda p: outdoor(p, clouds=False), ref=(22, 400, 880)),
    page("Wayang Kulit", s_wayang_kulit, night, ref=(60, 380, 800)),
    page("Batik", s_batik, lambda p: indoor(p, picture=False), ref=(40, 470, 820)),
    page("Songket", s_songket, lambda p: indoor(p, picture=False), ref=(40, 450, 820)),
    page("Labu Sayong", s_labu_sayong, lambda p: table(p, top=1040), ref=(60, 500, 760)),
    page("Keris", s_keris, indoor, ref=(60, 560, 760)),
    page("Sape", s_sape, lambda p: indoor(p, with_lamp=False), ref=(40, 300, 900)),
    page("Baju Melayu", s_baju_melayu, lambda p: outdoor(p, hills=False, n_tufts=4, clouds=False), ref=(60, 380, 820)),
    page("Baju Kurung", s_baju_kurung, lambda p: outdoor(p, hills=False, n_tufts=4, clouds=False), ref=(60, 380, 820)),
    page("Rumah Melayu", s_rumah_melayu, lambda p: outdoor(p, horizon=1010, hills=False), ref=(22, 360, 880)),
    page("Rumah Panjang", s_rumah_panjang, lambda p: outdoor(p, horizon=1030, hills=False), ref=(22, 380, 880)),
    page("Perahu Kolek", s_perahu, sea, ref=(40, 420, 840)),
    page("Hari Raya Aidilfitri", s_hari_raya, lambda p: outdoor(p, hills=False, n_tufts=6, clouds=False),
         ref=(22, 380, 880)),
    page("Tahun Baru Cina", s_tahun_baru_cina, lambda p: indoor(p, window=False, with_lamp=False), ref=(40, 360, 860)),
    page("Deepavali", s_deepavali, lambda p: indoor(p, window=False, with_lamp=False, rug=False), ref=(22, 420, 880)),
    page("Pesta Kaamatan", s_kaamatan, lambda p: outdoor(p, clouds=False), ref=(22, 400, 880)),
    page("Hari Kebangsaan", s_hari_kebangsaan, lambda p: outdoor(p, hills=False), ref=(22, 360, 900)),
    page("Nasi Lemak", s_nasi_lemak, lambda p: table(p, top=860), ref=(60, 560, 760)),
    page("Sate", s_sate, lambda p: outdoor(p, hills=False), ref=(40, 520, 780)),
    page("Teh Tarik", s_teh_tarik, lambda p: indoor(p, picture=False, with_lamp=False, with_shelf=True), ref=(22, 380, 880)),
    page("Kuih-muih", s_kuih_muih, lambda p: table(p, top=860), ref=(60, 560, 760)),
    page("Lemang", s_lemang, outdoor, ref=(40, 560, 760)),
    page("Ketupat", s_ketupat, indoor, ref=(60, 520, 760)),
    page("Bunga Raya", s_bunga_raya, lambda p: outdoor(p, hills=False, n_tufts=8), ref=(60, 380, 820)),
]
