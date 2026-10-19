"""Siri Kenderaan - 4 coloring pages (A4, 300 DPI) following the "Ambulans" template.

Builds one SVG per page (line art + a small colored reference picture in the
top-right box), then render.mjs turns them into 2480x3508 PNGs and this script
tags them with 300 DPI and bundles a print-ready PDF.

    python3 generate.py svg      # write build/*.html
    node render.mjs              # screenshot to build/*.png
    python3 generate.py finish   # set 300 DPI + make the PDF
"""
import base64
import math
import os
import random
import sys

from PIL import Image, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, "build")
OUT = os.path.join(HERE, "output")
FONT_BOLD = os.path.join(HERE, "fonts", "Fredoka-Bold.ttf")
FONT_SEMI = os.path.join(HERE, "fonts", "Fredoka-SemiBold.ttf")

# Page is designed on a 905 x 1280 canvas (same proportions as A4 and the template)
W, H = 905, 1280
PX_W, PX_H = 2480, 3508  # A4 @ 300 DPI

INK = "#1b1b1b"
LW = 4.2  # main outline
DW = 2.6  # detail lines

FRAME = (18, 150, 869, 1112)  # x, y, w, h of the big drawing frame
SIDEWALK_Y = 1000
ROAD_Y = 1032
GROUND = 1172  # where the tyres touch the road


class Pen:
    """Holds the drawing mode: line art (all white) or the colored reference."""

    def __init__(self, colored, prefix):
        self.colored = colored
        self.p = prefix

    def f(self, color):
        return color if self.colored else "#ffffff"

    def shape(self, tag, fill="#fff", w=LW, extra=""):
        return f'<{tag} fill="{self.f(fill)}" stroke="{INK}" stroke-width="{w}" {extra}/>'

    def path(self, d, fill="#fff", w=LW, extra=""):
        return f'<path d="{d}" fill="{self.f(fill)}" stroke="{INK}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round" {extra}/>'

    def rect(self, x, y, w, h, fill="#fff", rx=0, sw=LW):
        return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{self.f(fill)}" '
                f'stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"/>')

    def circle(self, cx, cy, r, fill="#fff", sw=LW):
        return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{self.f(fill)}" stroke="{INK}" stroke-width="{sw}"/>'

    def line(self, x1, y1, x2, y2, sw=DW):
        return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{INK}" '
                f'stroke-width="{sw}" stroke-linecap="round"/>')

    def text(self, x, y, s, size, fill_line=INK, fill_color=INK, anchor="middle", weight=700, spacing=1):
        fill = fill_color if self.colored else fill_line
        return (f'<text x="{x}" y="{y}" font-family="Fredoka" font-weight="{weight}" font-size="{size}" '
                f'text-anchor="{anchor}" letter-spacing="{spacing}" fill="{fill}">{s}</text>')


# ---------------------------------------------------------------- shapes

CLOUD = ("M10,48 A10,10 0 0 1 8,30 A14,14 0 0 1 28,16 A20,20 0 0 1 62,10 "
         "A16,16 0 0 1 86,24 A12.5,12.5 0 0 1 92,48 Z")


def cloud(pen, x, y, w, h):
    return (f'<g transform="translate({x},{y}) scale({w / 100},{h / 50})">'
            f'<path d="{CLOUD}" fill="#fff" stroke="{INK}" stroke-width="{LW}" '
            f'vector-effect="non-scaling-stroke" stroke-linejoin="round"/></g>')


def blob_d(cx, cy, rx, ry, n, seed, flat_bottom=False):
    """Bumpy outline (tree crowns, bushes): arcs bulging outward between points on an ellipse."""
    rnd = random.Random(seed)
    pts = []
    for k in range(n):
        a = 2 * math.pi * k / n + math.pi / 2
        j = 1 + rnd.uniform(-0.07, 0.07)
        px, py = cx + rx * j * math.cos(a), cy + ry * j * math.sin(a)
        if flat_bottom and py > cy:
            py = cy + ry * 0.35
        pts.append((px, py))
    d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f} "
    for i in range(n):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % n]
        chord = math.hypot(x2 - x1, y2 - y1)
        if flat_bottom and y1 > cy and y2 > cy:
            d += f"L{x2:.1f},{y2:.1f} "
        else:
            r = chord * 0.62
            d += f"A{r:.1f},{r:.1f} 0 0 1 {x2:.1f},{y2:.1f} "
    return d + "Z"


def tree(pen, cx, top, w, h, seed):
    crown_cy = top + h * 0.42
    trunk = (f"M{cx - 9},{SIDEWALK_Y} L{cx - 7},{crown_cy + h * 0.15} L{cx - 30},{crown_cy - h * 0.02} "
             f"M{cx + 8},{SIDEWALK_Y} L{cx + 7},{crown_cy + h * 0.08} L{cx + 32},{crown_cy - h * 0.06}")
    out = pen.path(blob_d(cx, crown_cy, w / 2, h * 0.42, 11, seed), fill="#5cb84a")
    out += pen.path(f"M{cx - 9},{SIDEWALK_Y} L{cx - 7},{crown_cy + h * 0.2} L{cx + 7},{crown_cy + h * 0.2} "
                    f"L{cx + 9},{SIDEWALK_Y} Z", fill="#8a5a2f", w=DW + 0.6)
    out += f'<path d="{trunk}" fill="none" stroke="{INK}" stroke-width="{DW}" stroke-linecap="round"/>'
    return out


def bush(pen, cx, base, w, h, seed, fill="#4caf50"):
    return pen.path(blob_d(cx, base - h * 0.45, w / 2, h * 0.55, 9, seed, flat_bottom=True), fill=fill)


def windows(pen, x, y, cols, rows, ww, wh, gx, gy, fill="#8fd3f4", sw=DW):
    out = ""
    for r in range(rows):
        for c in range(cols):
            out += pen.rect(x + c * (ww + gx), y + r * (wh + gy), ww, wh, fill=fill, sw=sw)
    return out


def skyline(pen):
    out = pen.rect(140, 405, 72, 600, fill="#cfd8e6")
    out += windows(pen, 155, 430, 2, 6, 14, 16, 14, 26)
    out += pen.rect(238, 470, 52, 540, fill="#e3d6f0")
    out += pen.rect(286, 540, 66, 470, fill="#cfe3d6")
    out += windows(pen, 298, 560, 3, 5, 10, 13, 8, 20)
    return out


def ground(pen):
    x, y, w, h = FRAME
    out = pen.rect(x - 5, SIDEWALK_Y, w + 10, ROAD_Y - SIDEWALK_Y, fill="#d8d8d8")
    for sx in range(40, 900, 95):
        out += pen.line(sx, SIDEWALK_Y, sx - 10, ROAD_Y)
    out += pen.rect(x - 5, ROAD_Y, w + 10, 260, fill="#8e98a4")
    for dx in range(-30, 900, 160):
        out += pen.rect(dx, 1222, 82, 11, fill="#ffffff", rx=3, sw=DW)
    return out


def foreground(pen):
    return bush(pen, 850, 1268, 150, 80, 7, fill="#66bb55") + bush(pen, 35, 1268, 120, 60, 9, fill="#66bb55")


def wheel(pen, cx, r):
    cy = -r
    out = pen.circle(cx, cy, r, fill="#3a3a3a")
    out += pen.circle(cx, cy, r * 0.6, fill="#cfd8dc", sw=DW + 0.6)
    out += pen.circle(cx, cy, r * 0.2, fill="#9ea7ad", sw=DW)
    for k in range(5):
        a = 2 * math.pi * k / 5 - math.pi / 2
        out += pen.circle(round(cx + r * 0.4 * math.cos(a), 1), round(cy + r * 0.4 * math.sin(a), 1),
                          r * 0.055, fill="#555", sw=1.8)
    return out


def arch(cx, r, R, yb):
    """Body outline segment that jumps over a wheel (arc concentric with the wheel)."""
    dx = math.sqrt(R * R - (r + yb) ** 2)
    return f"L{cx - dx:.1f},{yb} A{R},{R} 0 1 1 {cx + dx:.1f},{yb} "


def clip(pen, name, d):
    cid = f"{pen.p}-{name}"
    return f'<clipPath id="{cid}"><path d="{d}"/></clipPath>', cid


# ---------------------------------------------------------------- vehicles
# Drawn in local coords: x from the front bumper (left) to the back, y=0 on the road.

def ambulans(pen):
    r, R, yb = 62, 76, -40
    body = (f"M18,{yb} " + arch(130, r, R, yb) + arch(615, r, R, yb) +
            f"L745,{yb} Q758,{yb} 758,-58 L758,-340 Q758,-362 736,-362 L248,-362 Q230,-362 222,-348 "
            f"L128,-222 Q120,-210 104,-208 L32,-196 Q8,-192 6,-166 L4,-80 Q4,{yb} 18,{yb} Z")
    defs, cid = clip(pen, "amb", body)
    out = defs
    out += pen.rect(240, -394, 176, 34, fill="#e53935", rx=12)
    out += pen.line(298, -394, 298, -360) + pen.line(358, -394, 358, -360)
    out += pen.rect(268, -362, 120, 6, fill="#999", sw=DW)
    out += pen.rect(696, -380, 40, 20, fill="#1e63c9", rx=6, sw=DW + 0.6)
    out += pen.path(body, fill="#ffffff")
    out += (f'<g clip-path="url(#{cid})"><rect x="-10" y="-182" width="780" height="50" '
            f'fill="{pen.f("#e53935")}" stroke="{INK}" stroke-width="{DW + 0.6}"/></g>')
    # cab door + window
    out += pen.path("M210,-62 L210,-226 L244,-346 L356,-346 L356,-62 Z", fill="none", w=DW + 0.6)
    out += pen.path("M224,-232 L254,-330 L342,-330 L342,-232 Z", fill="#8fd3f4", w=DW + 0.6)
    out += pen.line(262, -320, 236, -248, sw=2) + pen.line(285, -318, 262, -254, sw=2)
    out += pen.rect(318, -208, 26, 10, fill="#bbb", rx=5, sw=DW)
    # sliding door + window
    out += pen.path("M372,-62 L372,-346 L530,-346 L530,-62", fill="none", w=DW + 0.6)
    out += pen.rect(386, -330, 130, 92, fill="#8fd3f4", rx=8, sw=DW + 0.6)
    out += pen.rect(384, -214, 26, 10, fill="#bbb", rx=5, sw=DW)
    # red cross on the back panel
    cx, cy, a, t = 650, -268, 50, 17
    cross = (f"M{cx - t},{cy - a} h{2 * t} v{a - t} h{a - t} v{2 * t} h{-(a - t)} v{a - t} h{-2 * t} "
             f"v{-(a - t)} h{-(a - t)} v{-2 * t} h{a - t} Z")
    out += pen.path(cross, fill="#e53935")
    out += pen.text(650, -143, "AMBULANS", 36, fill_color="#ffffff")
    out += pen.text(455, -143, "999", 34, fill_color="#ffffff")
    # lights, bumpers, mirror
    out += pen.rect(8, -186, 38, 26, fill="#fff59d", rx=8, sw=DW + 0.6)
    out += pen.circle(28, -112, 9, fill="#ffcc80", sw=DW)
    out += pen.rect(-4, -88, 64, 38, fill="#b0bec5", rx=10)
    out += pen.rect(732, -82, 34, 32, fill="#b0bec5", rx=8)
    out += pen.rect(746, -236, 14, 48, fill="#e53935", rx=4, sw=DW)
    out += pen.line(198, -262, 182, -268, sw=LW)
    out += pen.rect(164, -298, 22, 52, fill="#fff", rx=8, sw=DW + 0.6)
    out += wheel(pen, 130, r) + wheel(pen, 615, r)
    return out, 760


def kereta_polis(pen):
    r, R, yb = 58, 72, -38
    body = (f"M22,{yb} " + arch(140, r, R, yb) + arch(595, r, R, yb) +
            f"L715,{yb} Q738,{yb} 738,-62 L738,-128 Q738,-150 715,-152 L612,-160 L536,-256 "
            f"Q526,-268 506,-268 L318,-268 Q298,-268 286,-256 L206,-172 L42,-156 Q10,-150 6,-118 "
            f"L4,-70 Q4,{yb} 22,{yb} Z")
    defs, cid = clip(pen, "pol", body)
    out = defs
    out += pen.rect(342, -278, 132, 12, fill="#888", sw=DW)
    out += pen.rect(322, -304, 172, 28, fill="#e53935", rx=11)
    out += (f'<rect x="408" y="-304" width="86" height="28" rx="11" fill="{pen.f("#1e63c9")}" '
            f'stroke="{INK}" stroke-width="{LW}"/>')
    out += pen.rect(408, -304, 20, 28, fill="#1e63c9", sw=0.01)
    out += pen.line(408, -304, 408, -276, sw=LW)
    out += pen.path(body, fill="#ffffff")
    # dark-blue lower half + yellow/red stripe (PDRM style)
    out += (f'<g clip-path="url(#{cid})">'
            f'<rect x="-10" y="-120" width="760" height="90" fill="{pen.f("#163b8c")}" stroke="{INK}" stroke-width="{DW + 0.6}"/>'
            f'<rect x="-10" y="-146" width="760" height="22" fill="{pen.f("#fbc02d")}" stroke="{INK}" stroke-width="{DW + 0.6}"/>'
            f'</g>')
    out += pen.path("M234,-170 L296,-246 L406,-246 L406,-170 Z", fill="#8fd3f4", w=DW + 0.6)
    out += pen.path("M424,-170 L424,-246 L512,-246 L572,-170 Z", fill="#8fd3f4", w=DW + 0.6)
    out += pen.line(300, -236, 272, -200, sw=2) + pen.line(322, -236, 296, -204, sw=2)
    out += pen.line(222, -166, 222, -50) + pen.line(415, -258, 415, -50) + pen.line(590, -164, 590, -131)
    out += pen.rect(380, -112, 24, 9, fill="#ccc", rx=4, sw=DW)
    out += pen.rect(556, -112, 24, 9, fill="#ccc", rx=4, sw=DW)
    out += pen.text(400, -55, "POLIS", 44, fill_color="#ffffff", spacing=3)
    out += pen.path("M10,-140 L46,-146 L50,-126 L12,-122 Z", fill="#fff59d", w=DW + 0.6)
    out += pen.rect(-4, -80, 46, 32, fill="#b0bec5", rx=10)
    out += pen.rect(712, -80, 34, 30, fill="#b0bec5", rx=8)
    out += pen.rect(724, -148, 14, 26, fill="#e53935", rx=4, sw=DW)
    out += pen.line(214, -176, 204, -184, sw=LW)
    out += pen.rect(180, -204, 28, 24, fill="#fff", rx=8, sw=DW + 0.6)
    out += wheel(pen, 140, r) + wheel(pen, 595, r)
    return out, 740


def bas_sekolah(pen):
    r, R, yb = 62, 78, -42
    body = (f"M20,{yb} " + arch(165, r, R, yb) + arch(640, r, R, yb) +
            f"L780,{yb} Q798,{yb} 798,-62 L798,-405 Q798,-426 777,-426 L40,-426 Q16,-426 13,-402 "
            f"L4,-262 L4,-72 Q4,{yb} 20,{yb} Z")
    defs, cid = clip(pen, "bas", body)
    out = defs
    out += pen.rect(46, -442, 46, 18, fill="#ff7043", rx=6, sw=DW + 0.6)
    out += pen.rect(712, -442, 46, 18, fill="#ff7043", rx=6, sw=DW + 0.6)
    out += pen.path(body, fill="#ffc928")
    out += (f'<g clip-path="url(#{cid})">'
            f'<rect x="-10" y="-262" width="820" height="22" fill="{pen.f("#222")}" stroke="{INK}" stroke-width="{DW}"/>'
            f'<rect x="-10" y="-112" width="820" height="16" fill="{pen.f("#222")}" stroke="{INK}" stroke-width="{DW}"/>'
            f'</g>')
    out += pen.path("M22,-398 L124,-398 L124,-282 L15,-282 Z", fill="#8fd3f4", w=DW + 0.6)
    out += pen.line(60, -386, 36, -300, sw=2) + pen.line(84, -386, 62, -304, sw=2)
    # door
    out += pen.rect(246, -410, 88, 366, fill="#ffc928", rx=4, sw=DW + 0.8)
    out += pen.line(290, -410, 290, -44, sw=DW)
    out += pen.rect(254, -398, 28, 150, fill="#8fd3f4", rx=5, sw=DW)
    out += pen.rect(298, -398, 28, 150, fill="#8fd3f4", rx=5, sw=DW)
    out += pen.rect(254, -230, 28, 120, fill="#8fd3f4", rx=5, sw=DW)
    out += pen.rect(298, -230, 28, 120, fill="#8fd3f4", rx=5, sw=DW)
    # passenger windows
    ww = (785 - 352 - 3 * 14) / 4
    for i in range(4):
        x = 352 + i * (ww + 14)
        out += pen.rect(round(x, 1), -398, round(ww, 1), 116, fill="#8fd3f4", rx=8, sw=DW + 0.6)
        out += pen.line(round(x + ww / 2, 1), -398, round(x + ww / 2, 1), -282, sw=2)
    out += pen.text(568, -166, "BAS SEKOLAH", 44, fill_color="#222", spacing=2)
    out += pen.rect(6, -134, 34, 26, fill="#fff59d", rx=7, sw=DW + 0.6)
    out += pen.rect(-6, -86, 56, 42, fill="#9e9e9e", rx=10)
    out += pen.rect(772, -86, 34, 42, fill="#9e9e9e", rx=8)
    out += pen.rect(784, -200, 14, 44, fill="#e53935", rx=4, sw=DW)
    out += pen.line(14, -340, -6, -350, sw=LW)
    out += pen.rect(-24, -380, 18, 58, fill="#fff", rx=8, sw=DW + 0.6)
    out += wheel(pen, 165, r) + wheel(pen, 640, r)
    return out, 800


def jentera_bomba(pen):
    r, R, yb = 64, 78, -44
    cab = (f"M18,{yb} " + arch(150, r, R, yb) +
           f"L244,{yb} L244,-386 L42,-386 Q18,-386 15,-362 L6,-232 L4,-76 Q4,{yb} 18,{yb} Z")
    body = (f"M240,{yb} " + arch(650, r, R, yb) +
            f"L780,{yb} Q795,{yb} 795,-62 L795,-312 L240,-312 Z")
    defs, cid = clip(pen, "bomba", body)
    defs2, cid2 = clip(pen, "bomba-cab", cab)
    out = defs + defs2
    # ladder on the roof
    out += pen.rect(300, -374, 14, 64, fill="#9e9e9e", sw=DW)
    out += pen.rect(744, -374, 14, 64, fill="#9e9e9e", sw=DW)
    out += pen.rect(150, -406, 650, 34, fill="#cfd8dc", rx=4)
    for x in range(178, 800, 30):
        out += pen.line(x, -406, x, -372, sw=DW)
    out += pen.rect(44, -414, 160, 28, fill="#1e63c9", rx=10)
    out += pen.line(97, -414, 97, -386) + pen.line(151, -414, 151, -386)
    out += pen.path(body, fill="#e53935")
    out += f'<g clip-path="url(#{cid})"><rect x="230" y="-152" width="580" height="24" fill="{pen.f("#ffd54f")}" stroke="{INK}" stroke-width="{DW + 0.6}"/></g>'
    for x0, x1 in ((256, 420), (436, 600), (616, 782)):
        out += pen.rect(x0, -296, x1 - x0, 132, fill="#cfd8dc", rx=6, sw=DW + 0.6)
        for y in range(-276, -180, 18):
            out += pen.line(x0 + 8, y, x1 - 8, y, sw=1.8)
        out += pen.rect((x0 + x1) / 2 - 22, -182, 44, 9, fill="#888", rx=4, sw=DW)
    out += pen.text(408, -64, "BOMBA", 54, fill_color="#ffffff", spacing=3)
    out += pen.path(cab, fill="#e53935")
    out += f'<g clip-path="url(#{cid2})"><rect x="-10" y="-152" width="260" height="24" fill="{pen.f("#ffd54f")}" stroke="{INK}" stroke-width="{DW + 0.6}"/></g>'
    out += pen.path("M22,-366 L106,-366 L106,-250 L14,-250 Z", fill="#8fd3f4", w=DW + 0.6)
    out += pen.line(58, -354, 36, -270, sw=2) + pen.line(80, -354, 60, -274, sw=2)
    out += pen.rect(116, -376, 118, 222, fill="none", rx=6, sw=DW + 0.6)
    out += pen.rect(126, -366, 98, 112, fill="#8fd3f4", rx=6, sw=DW + 0.6)
    out += pen.rect(198, -230, 24, 9, fill="#ccc", rx=4, sw=DW)
    out += pen.text(175, -176, "994", 30, fill_color="#ffffff")
    out += pen.rect(6, -146, 34, 26, fill="#fff59d", rx=7, sw=DW + 0.6)
    out += pen.rect(-6, -92, 56, 46, fill="#b0bec5", rx=10)
    out += pen.rect(780, -88, 26, 42, fill="#b0bec5", rx=8)
    out += pen.rect(784, -240, 12, 40, fill="#ffb300", rx=4, sw=DW)
    out += pen.line(14, -320, -6, -330, sw=LW)
    out += pen.rect(-24, -360, 18, 58, fill="#fff", rx=8, sw=DW + 0.6)
    out += wheel(pen, 150, r) + wheel(pen, 650, r)
    return out, 800


# ---------------------------------------------------------------- buildings

def hospital(pen):
    out = pen.rect(384, 520, 120, 490, fill="#e8f1fb")
    out += windows(pen, 400, 545, 3, 5, 22, 28, 12, 26)
    out += pen.rect(780, 520, 92, 490, fill="#e8f1fb")
    out += windows(pen, 794, 545, 2, 5, 24, 28, 14, 26)
    out += pen.rect(500, 480, 284, 530, fill="#ffffff")
    out += pen.rect(540, 418, 204, 122, fill="#ffffff")
    cx, cy, a, t = 642, 456, 30, 10
    out += pen.path(f"M{cx - t},{cy - a} h{2 * t} v{a - t} h{a - t} v{2 * t} h{-(a - t)} v{a - t} h{-2 * t} "
                    f"v{-(a - t)} h{-(a - t)} v{-2 * t} h{a - t} Z", fill="#e53935")
    out += pen.text(642, 526, "HOSPITAL", 36, spacing=2)
    out += windows(pen, 516, 560, 6, 1, 36, 52, 9, 0)
    out += pen.rect(510, 626, 264, 22, fill="#cfd8dc")
    out += windows(pen, 534, 662, 4, 2, 44, 60, 14, 16, fill="#b3e5fc")
    return out


def balai_polis(pen):
    out = pen.line(420, 1000, 420, 410, sw=LW)
    out += pen.circle(420, 404, 7, fill="#ffd54f", sw=DW)
    out += pen.rect(424, 418, 96, 58, fill="#ffffff", sw=DW + 0.6)
    stripe = 58 / 7
    if pen.colored:
        for i in range(0, 7, 2):
            out += f'<rect x="424" y="{418 + i * stripe:.1f}" width="96" height="{stripe:.1f}" fill="#e53935"/>'
    for i in range(1, 7):
        y = round(418 + i * stripe, 1)
        out += pen.line(424 if y > 418 + 29 else 466, y, 520, y, sw=1.6)
    out += pen.rect(424, 418, 96, 58, fill="none", sw=DW + 0.6)
    out += pen.rect(424, 418, 42, 29, fill="#163b8c", sw=DW)
    out += pen.circle(440, 432, 7, fill="#ffd54f", sw=1.6)
    out += pen.rect(452, 525, 410, 485, fill="#e3f2fd")
    out += pen.rect(440, 505, 434, 26, fill="#163b8c")
    out += pen.rect(500, 548, 314, 64, fill="#163b8c", rx=8)
    out += pen.text(657, 595, "BALAI POLIS", 40, fill_color="#ffffff", spacing=2)
    out += windows(pen, 472, 636, 6, 3, 46, 50, 22, 22)
    return out


def sekolah(pen):
    out = pen.line(860, 1000, 860, 450, sw=LW)
    out += pen.path("M864,458 L864,510 L815,500 L815,468 Z", fill="#e53935", w=DW + 0.6)
    out += pen.rect(380, 572, 470, 438, fill="#fff3e0")
    out += pen.path("M370,580 L392,548 L838,548 L860,580 Z", fill="#ef6c00")
    out += pen.path("M500,560 L625,456 L750,560 Z", fill="#ef6c00")
    out += pen.circle(625, 520, 24, fill="#ffffff", sw=DW + 0.6)
    out += pen.line(625, 520, 625, 504, sw=DW) + pen.line(625, 520, 637, 524, sw=DW)
    out += pen.rect(520, 592, 210, 56, fill="#ffffff", rx=8)
    out += pen.text(625, 634, "SEKOLAH", 38, spacing=2)
    out += windows(pen, 396, 600, 2, 4, 40, 44, 16, 22)
    out += windows(pen, 744, 600, 2, 4, 40, 44, 12, 22)
    out += windows(pen, 532, 672, 4, 2, 38, 44, 12, 22)
    return out


def balai_bomba(pen):
    out = pen.rect(398, 440, 86, 570, fill="#ffccbc")
    out += pen.path("M388,446 L441,404 L494,446 Z", fill="#c62828")
    out += windows(pen, 420, 465, 1, 4, 42, 40, 0, 28)
    out += pen.rect(484, 520, 386, 490, fill="#ffe0d6")
    out += pen.rect(476, 504, 402, 24, fill="#c62828")
    out += pen.rect(510, 544, 334, 60, fill="#c62828", rx=8)
    out += pen.text(677, 588, "BALAI BOMBA", 38, fill_color="#ffffff", spacing=2)
    for x in (500, 626, 752):
        out += pen.path(f"M{x},1010 L{x},690 Q{x},640 {x + 55},640 Q{x + 110},640 {x + 110},690 L{x + 110},1010",
                        fill="#ffccbc", w=DW + 0.8)
        for y in range(700, 1000, 24):
            out += pen.line(x + 8, y, x + 102, y, sw=1.6)
    return out


# ---------------------------------------------------------------- page

PAGES = [
    dict(slug="1-ambulans", num=1, title="Ambulans", vehicle=ambulans, building=hospital,
         trees=[(80, 440, 150, 300), (850, 520, 90, 220)]),
    dict(slug="2-kereta-polis", num=2, title="Kereta Polis", vehicle=kereta_polis, building=balai_polis,
         trees=[(80, 450, 150, 300), (300, 640, 120, 240)]),
    dict(slug="3-bas-sekolah", num=3, title="Bas Sekolah", vehicle=bas_sekolah, building=sekolah,
         trees=[(80, 440, 150, 300), (300, 650, 110, 220)]),
    dict(slug="4-jentera-bomba", num=4, title="Jentera Bomba", vehicle=jentera_bomba, building=balai_bomba,
         trees=[(80, 450, 150, 300), (320, 650, 110, 220)]),
]


def scene(page, pen):
    out = ""
    if pen.colored:
        out += f'<rect x="0" y="0" width="{W}" height="{SIDEWALK_Y}" fill="#bfe7fb"/>'
    out += cloud(pen, 50, 195, 330, 150) + cloud(pen, 330, 300, 190, 80)
    out += skyline(pen)
    out += page["building"](pen)
    for i, (cx, top, w, h) in enumerate(page["trees"]):
        out += tree(pen, cx, top, w, h, seed=page["num"] * 10 + i)
    out += bush(pen, 200, SIDEWALK_Y, 170, 70, 3) + bush(pen, 860, SIDEWALK_Y, 120, 60, 4)
    out += ground(pen)
    v, length = page["vehicle"](pen)
    x0 = round((W - length) / 2)
    out += f'<g transform="translate({x0},{GROUND})">{v}</g>'
    out += foreground(pen)
    return out


def fit_title(titles, max_w, start=64):
    size = start
    while size > 30:
        font = ImageFont.truetype(FONT_BOLD, size)
        if all(font.getlength(t) <= max_w for t in titles):
            return size
        size -= 1
    return size


def page_svg(page, title_size):
    fx, fy, fw, fh = FRAME
    line_pen, color_pen = Pen(False, "l"), Pen(True, "c")
    ref = (556, 30, 326, 352)  # colored reference box
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{PX_W}" height="{PX_H}" '
         f'viewBox="0 0 {W} {H}" preserveAspectRatio="none">']
    s.append(f'<defs><clipPath id="frame"><rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" rx="22"/></clipPath>'
             f'<clipPath id="refclip"><rect x="{ref[0]}" y="{ref[1]}" width="{ref[2]}" height="{ref[3]}" rx="16"/></clipPath></defs>')
    s.append(f'<rect width="{W}" height="{H}" fill="#fff"/>')
    s.append(f'<g clip-path="url(#frame)">{scene(page, line_pen)}</g>')
    s.append(f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" rx="22" fill="none" stroke="{INK}" stroke-width="4.5"/>')
    # colored reference picture
    s.append(f'<rect x="{ref[0]}" y="{ref[1]}" width="{ref[2]}" height="{ref[3]}" rx="16" fill="#fff"/>')
    s.append(f'<g clip-path="url(#refclip)"><svg x="{ref[0]}" y="{ref[1]}" width="{ref[2]}" height="{ref[3]}" '
             f'viewBox="22 400 862 862" preserveAspectRatio="xMidYMid slice">{scene(page, color_pen)}</svg></g>')
    s.append(f'<rect x="{ref[0]}" y="{ref[1]}" width="{ref[2]}" height="{ref[3]}" rx="16" fill="none" stroke="{INK}" stroke-width="4.5"/>')
    # title pill + number badge
    s.append(f'<rect x="110" y="24" width="{ref[0] - 110 - 18}" height="112" rx="24" fill="#fde3c8" stroke="{INK}" stroke-width="4.5"/>')
    s.append(f'<text x="168" y="{80 + title_size * 0.36:.1f}" font-family="Fredoka" font-weight="700" '
             f'font-size="{title_size}" fill="{INK}">{page["title"]}</text>')
    s.append(f'<circle cx="86" cy="82" r="68" fill="#fff" stroke="{INK}" stroke-width="4.5"/>')
    s.append('<circle cx="86" cy="82" r="56" fill="#e8402f"/>')
    s.append(f'<text x="86" y="111" text-anchor="middle" font-family="Fredoka" font-weight="700" '
             f'font-size="84" fill="#fff">{page["num"]}</text>')
    s.append("</svg>")
    return "\n".join(s)


def font_face(name, weight, path):
    data = base64.b64encode(open(path, "rb").read()).decode()
    return (f"@font-face{{font-family:'{name}';font-weight:{weight};"
            f"src:url(data:font/ttf;base64,{data}) format('truetype');}}")


def build_svg():
    os.makedirs(BUILD, exist_ok=True)
    os.makedirs(OUT, exist_ok=True)
    title_size = fit_title([p["title"] for p in PAGES], 556 - 18 - 168 - 26)
    css = font_face("Fredoka", 700, FONT_BOLD) + font_face("Fredoka", 600, FONT_SEMI)
    for page in PAGES:
        svg = page_svg(page, title_size)
        with open(os.path.join(OUT, f"{page['slug']}.svg"), "w") as fh:
            fh.write(svg.replace("<svg ", f"<svg ", 1).replace("<defs>", f"<defs><style>{css}</style>", 1))
        html = (f"<!doctype html><html><head><meta charset='utf-8'><style>{css}"
                f"html,body{{margin:0;padding:0;background:#fff}}svg{{display:block}}</style></head>"
                f"<body>{svg}</body></html>")
        with open(os.path.join(BUILD, f"{page['slug']}.html"), "w") as fh:
            fh.write(html)
    print("title size", title_size)


def finish():
    images = []
    for page in PAGES:
        src = os.path.join(BUILD, f"{page['slug']}.png")
        im = Image.open(src).convert("RGB")
        assert im.size == (PX_W, PX_H), im.size
        im.save(os.path.join(OUT, f"{page['slug']}.png"), dpi=(300, 300), optimize=True)
        images.append(im)
    images[0].save(os.path.join(OUT, "siri-kenderaan-A4-300dpi.pdf"), save_all=True,
                   append_images=images[1:], resolution=300.0)
    print("done")


if __name__ == "__main__":
    {"svg": build_svg, "finish": finish}[sys.argv[1]]()
