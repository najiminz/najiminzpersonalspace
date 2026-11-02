"""Shared drawing helpers for the Siri Kenderaan pages.

Every page is drawn twice with the same code: once as black-and-white line art
and once in color for the small reference picture. Pen.f() decides the fill.
"""
import math
import random

# Page is designed on a 905 x 1280 canvas (same proportions as A4 and the template)
W, H = 905, 1280
INK = "#1b1b1b"
LW = 4.2  # main outline
DW = 2.6  # detail lines

FRAME = (18, 150, 869, 1112)  # x, y, w, h of the big drawing frame
SIDEWALK_Y = 1000
ROAD_Y = 1032
GROUND = 1172  # where the tyres touch the road

GLASS = "#8fd3f4"


class Pen:
    """Holds the drawing mode: line art (all white) or the colored reference."""

    weight = 1.0  # global line-weight multiplier (a book can set Pen.weight for thicker lines)

    def __init__(self, colored, prefix):
        self.colored = colored
        self.p = prefix
        self.k = 1.0  # stroke compensation when a vehicle is drawn scaled
        self.n = 0

    def uid(self, name):
        self.n += 1
        return f"{self.p}-{name}-{self.n}"

    def f(self, color):
        if color == "none":
            return "none"
        return color if self.colored else "#ffffff"

    def sw(self, w):
        return round(w * self.k * self.weight, 2)

    def path(self, d, fill="#fff", w=LW, extra=""):
        return (f'<path d="{d}" fill="{self.f(fill)}" stroke="{INK}" stroke-width="{self.sw(w)}" '
                f'stroke-linejoin="round" stroke-linecap="round" {extra}/>')

    def rect(self, x, y, w, h, fill="#fff", rx=0, sw=LW):
        return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{self.f(fill)}" '
                f'stroke="{INK}" stroke-width="{self.sw(sw)}" stroke-linejoin="round"/>')

    def circle(self, cx, cy, r, fill="#fff", sw=LW):
        return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{self.f(fill)}" '
                f'stroke="{INK}" stroke-width="{self.sw(sw)}"/>')

    def ellipse(self, cx, cy, rx, ry, fill="#fff", sw=LW, rot=0):
        return (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" transform="rotate({rot} {cx} {cy})" '
                f'fill="{self.f(fill)}" stroke="{INK}" stroke-width="{self.sw(sw)}"/>')

    def line(self, x1, y1, x2, y2, sw=DW):
        return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{INK}" '
                f'stroke-width="{self.sw(sw)}" stroke-linecap="round"/>')

    def tube(self, d, width, fill="#fff"):
        """A thick bar with an outline (bicycle frames, booms, poles)."""
        return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{width + self.sw(2 * 3.4):.2f}" '
                f'stroke-linejoin="round" stroke-linecap="round"/>'
                f'<path d="{d}" fill="none" stroke="{self.f(fill)}" stroke-width="{width}" '
                f'stroke-linejoin="round" stroke-linecap="round"/>')

    def text(self, x, y, s, size, fill_line=INK, fill_color=INK, anchor="middle", weight=700, spacing=1,
             extra=""):
        fill = fill_color if self.colored else fill_line
        return (f'<text x="{x}" y="{y}" font-family="Fredoka" font-weight="{weight}" font-size="{size}" '
                f'text-anchor="{anchor}" letter-spacing="{spacing}" fill="{fill}" {extra}>{s}</text>')

    def clipped(self, d, inner):
        """Draw `inner` clipped to the outline `d` (stripes on a body etc.)."""
        cid = self.uid("clip")
        return f'<clipPath id="{cid}"><path d="{d}"/></clipPath><g clip-path="url(#{cid})">{inner}</g>'

    def fillrect(self, x, y, w, h, color, sw=DW):
        """Plain band (used inside clipped groups)."""
        return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{self.f(color)}" stroke="{INK}" '
                f'stroke-width="{self.sw(sw)}"/>')


# ---------------------------------------------------------------- nature

CLOUD = ("M10,48 A10,10 0 0 1 8,30 A14,14 0 0 1 28,16 A20,20 0 0 1 62,10 "
         "A16,16 0 0 1 86,24 A12.5,12.5 0 0 1 92,48 Z")


def cloud(pen, x, y, w, h, fill="#ffffff"):
    return (f'<g transform="translate({x},{y}) scale({w / 100},{h / 50})">'
            f'<path d="{CLOUD}" fill="{fill if pen.colored else "#fff"}" stroke="{INK}" stroke-width="{LW}" '
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


def tree(pen, cx, top, w, h, seed, base=SIDEWALK_Y):
    crown_cy = top + h * 0.42
    branches = (f"M{cx - 7},{crown_cy + h * 0.2} L{cx - 7},{crown_cy + h * 0.15} L{cx - 30},{crown_cy - h * 0.02} "
                f"M{cx + 7},{crown_cy + h * 0.2} L{cx + 7},{crown_cy + h * 0.08} L{cx + 32},{crown_cy - h * 0.06}")
    out = pen.path(blob_d(cx, crown_cy, w / 2, h * 0.42, 11, seed), fill="#5cb84a")
    out += pen.path(f"M{cx - 9},{base} L{cx - 7},{crown_cy + h * 0.2} L{cx + 7},{crown_cy + h * 0.2} "
                    f"L{cx + 9},{base} Z", fill="#8a5a2f", w=DW + 0.6)
    out += f'<path d="{branches}" fill="none" stroke="{INK}" stroke-width="{DW}" stroke-linecap="round"/>'
    return out


def palm(pen, x, base, h, lean=30, seed=1):
    """Coconut tree."""
    tx, ty = x + lean, base - h
    out = pen.path(f"M{x - 13},{base} Q{x - 10 + lean * 0.2},{base - h * 0.5} {tx - 7},{ty} "
                   f"L{tx + 7},{ty} Q{x + 12 + lean * 0.2},{base - h * 0.5} {x + 13},{base} Z", fill="#9c6b3c")
    for i in range(1, 6):
        y = base - h * i / 6
        xx = x + lean * (i / 6) ** 1.6
        out += pen.line(xx - 9, y, xx + 9, y + 4, sw=1.8)
    for ang in (-160, -120, -60, -20, 200):
        a = math.radians(ang)
        ex, ey = tx + 120 * math.cos(a), ty + 70 * math.sin(a) + 40
        mx, my = tx + 70 * math.cos(a), ty + 55 * math.sin(a) - 25
        nx, ny = -(ey - ty), ex - tx
        nl = math.hypot(nx, ny) or 1
        ox, oy = nx / nl * 18, ny / nl * 18
        out += pen.path(f"M{tx},{ty} Q{mx + ox:.1f},{my + oy:.1f} {ex:.1f},{ey:.1f} "
                        f"Q{mx - ox:.1f},{my - oy:.1f} {tx},{ty} Z", fill="#4caf50", w=DW + 0.6)
    out += pen.circle(tx - 8, ty + 10, 9, fill="#7a5230", sw=DW)
    out += pen.circle(tx + 9, ty + 12, 9, fill="#7a5230", sw=DW)
    return out


def bush(pen, cx, base, w, h, seed, fill="#4caf50"):
    return pen.path(blob_d(cx, base - h * 0.45, w / 2, h * 0.55, 9, seed, flat_bottom=True), fill=fill)


def sun(pen, cx, cy, r):
    out = ""
    for k in range(12):
        a = 2 * math.pi * k / 12
        out += pen.line(cx + (r + 10) * math.cos(a), cy + (r + 10) * math.sin(a),
                        cx + (r + 30) * math.cos(a), cy + (r + 30) * math.sin(a), sw=LW)
    return out + pen.circle(cx, cy, r, fill="#ffd54f")


def bird(pen, x, y, s=1.0):
    return (f'<path d="M{x - 16 * s},{y} Q{x - 8 * s},{y - 10 * s} {x},{y} Q{x + 8 * s},{y - 10 * s} {x + 16 * s},{y}" '
            f'fill="none" stroke="{INK}" stroke-width="{DW + 0.4}" stroke-linecap="round" stroke-linejoin="round"/>')


def hills(pen, base, specs, fill="#9ccc65"):
    """specs: (cx, half_width, height)."""
    out = ""
    for cx, hw, h in specs:
        out += pen.path(f"M{cx - hw},{base} Q{cx - hw * 0.5},{base - h} {cx},{base - h} "
                        f"Q{cx + hw * 0.5},{base - h} {cx + hw},{base} Z", fill=fill)
    return out


def windows(pen, x, y, cols, rows, ww, wh, gx, gy, fill=GLASS, sw=DW):
    out = ""
    for r in range(rows):
        for c in range(cols):
            out += pen.rect(x + c * (ww + gx), y + r * (wh + gy), ww, wh, fill=fill, sw=sw)
    return out


def cross_d(cx, cy, a, t):
    return (f"M{cx - t},{cy - a} h{2 * t} v{a - t} h{a - t} v{2 * t} h{-(a - t)} v{a - t} h{-2 * t} "
            f"v{-(a - t)} h{-(a - t)} v{-2 * t} h{a - t} Z")


def star_d(cx, cy, r1, r2, n=5):
    pts = []
    for k in range(2 * n):
        r = r1 if k % 2 == 0 else r2
        a = math.pi * k / n - math.pi / 2
        pts.append(f"{cx + r * math.cos(a):.1f},{cy + r * math.sin(a):.1f}")
    return "M" + " L".join(pts) + " Z"


def cone(pen, x, base, s=1.0):
    """Traffic cone."""
    out = pen.path(f"M{x - 14 * s},{base - 6 * s} L{x - 5 * s},{base - 52 * s} L{x + 5 * s},{base - 52 * s} "
                   f"L{x + 14 * s},{base - 6 * s} Z", fill="#ff7043", w=DW + 0.6)
    out += pen.line(x - 10 * s, base - 22 * s, x + 10 * s, base - 22 * s, sw=DW)
    out += pen.line(x - 8 * s, base - 34 * s, x + 8 * s, base - 34 * s, sw=DW)
    return out + pen.rect(x - 22 * s, base - 8 * s, 44 * s, 8 * s, fill="#ff7043", rx=2, sw=DW)


# ---------------------------------------------------------------- vehicle parts

def wheel(pen, cx, r, cy=None, rim="#cfd8dc"):
    cy = -r if cy is None else cy
    out = pen.circle(cx, cy, r, fill="#3a3a3a")
    out += pen.circle(cx, cy, r * 0.6, fill=rim, sw=DW + 0.6)
    out += pen.circle(cx, cy, r * 0.2, fill="#9ea7ad", sw=DW)
    for k in range(5):
        a = 2 * math.pi * k / 5 - math.pi / 2
        out += pen.circle(cx + r * 0.4 * math.cos(a), cy + r * 0.4 * math.sin(a), r * 0.055, fill="#555", sw=1.8)
    return out


def spoked_wheel(pen, cx, r, cy=None, spokes=12, tyre=9, rim="#cfd8dc"):
    """Thin bicycle-style wheel."""
    cy = -r if cy is None else cy
    out = pen.circle(cx, cy, r, fill="#3a3a3a")
    out += pen.circle(cx, cy, r - tyre, fill="#ffffff", sw=DW)
    for k in range(spokes):
        a = 2 * math.pi * k / spokes
        out += pen.line(cx, cy, cx + (r - tyre) * math.cos(a), cy + (r - tyre) * math.sin(a), sw=1.6)
    return out + pen.circle(cx, cy, r * 0.12, fill=rim, sw=DW)


def wheel_well(pen, cx, r, R, yb=0, fill="#4a4a4a"):
    """Dark half-round opening above a wheel, so the wheel sits inside the body."""
    return pen.path(f"M{cx - R},{yb} L{cx - R},{-r} A{R},{R} 0 0 1 {cx + R},{-r} L{cx + R},{yb} Z", fill=fill, w=DW + 0.6)


def arch(cx, r, R, yb):
    """Body outline segment that jumps over a wheel (arc concentric with the wheel)."""
    dx = math.sqrt(R * R - (r + yb) ** 2)
    return f"L{cx - dx:.1f},{yb} A{R},{R} 0 1 1 {cx + dx:.1f},{yb} "


def mirror(pen, x, y):
    """Side mirror on an arm, arm attached at (x, y)."""
    return pen.line(x, y, x - 18, y - 8, sw=LW) + pen.rect(x - 38, y - 44, 20, 54, fill="#fff", rx=8, sw=DW + 0.6)
