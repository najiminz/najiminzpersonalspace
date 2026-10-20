"""Object library for Siri 10: ABC, Nombor dan Bentuk.

Every object is drawn centred on (0, 0) inside roughly a 320 x 320 box, so the
same drawing can be used big on a letter page or small in a counting grid.
place(pen, fn, cx, cy, s) puts it on the page and keeps the line weight even.
"""
import math
import random

import vehicles as V
from characters import face, kid
from draw import DW, GLASS, INK, LW, blob_d, star_d


def place(pen, fn, cx, cy, s=1.0):
    k0 = pen.k
    pen.k = k0 / s
    svg = fn(pen)
    pen.k = k0
    return f'<g transform="translate({cx:.1f},{cy:.1f}) scale({s})">{svg}</g>'


def cute_face(pen, cx=0, cy=0, gap=26):
    """The cast's face, reused on suns, stars and shapes."""
    return face(pen, {}, cx=cx, cy=cy - 14, gap=gap)


def leaf(pen, x, y, l, ang, fill="#66bb6a"):
    d = f"M0,0 Q{l * 0.45},{-l * 0.35} {l},0 Q{l * 0.45},{l * 0.35} 0,0 Z"
    return (f'<g transform="translate({x},{y}) rotate({ang})">' + pen.path(d, fill=fill)
            + pen.line(4, 0, l - 8, 0, sw=DW - 0.6) + "</g>")


# ---------------------------------------------------------------- A - Z

def ayam(pen):
    out = ""
    for d in ("M80,-60 Q120,-170 170,-120", "M90,-50 Q160,-150 190,-70", "M96,-40 Q170,-90 180,-10"):
        out += pen.path(d, fill="none", w=LW + 6)
        out += pen.path(d, fill="none", w=LW + 1)
    body = "M-110,10 Q-120,-80 -40,-90 Q40,-100 90,-60 Q150,-30 140,30 Q120,90 40,100 Q-40,110 -80,80 Q-114,56 -110,10 Z"
    out += pen.path(body, fill="#fff3e0")
    out += pen.path("M-20,-10 Q40,-40 80,0 Q50,40 -10,30 Q-30,10 -20,-10 Z", fill="#ffe0b2")
    out += pen.path("M0,0 Q30,-6 60,10 M4,16 Q30,12 52,24", fill="none", w=DW - 0.4)
    for x in (-30, 20):
        out += pen.line(x, 100, x, 150, sw=LW)
        out += pen.path(f"M{x - 20},160 L{x},150 L{x + 20},160 M{x},150 L{x},166", fill="none", w=LW)
    out += pen.circle(-90, -110, 52, fill="#fff3e0")
    out += pen.path("M-128,-150 Q-124,-190 -104,-162 Q-92,-202 -76,-162 Q-58,-192 -56,-146 Z", fill="#e53935")
    out += pen.path("M-138,-118 L-176,-104 L-136,-92 Z", fill="#ffb300")
    out += pen.path(blob_d(-124, -74, 13, 18, 6, 3), fill="#e53935", w=DW)
    out += pen.circle(-100, -118, 9, fill=INK, sw=1) + f'<circle cx="-97" cy="-121" r="3" fill="#fff"/>'
    return out


def bola(pen):
    r = 150
    out = pen.circle(0, 0, r, fill="#ffffff")
    inner = ""
    pent = lambda cx, cy, rr, a0=-90: "M" + " L".join(
        f"{cx + rr * math.cos(math.radians(a0 + 72 * k)):.1f},{cy + rr * math.sin(math.radians(a0 + 72 * k)):.1f}"
        for k in range(5)) + " Z"
    inner += pen.path(pent(0, 0, 46), fill="#212121")
    for k in range(5):
        a = math.radians(-90 + 72 * k)
        inner += pen.line(46 * math.cos(a), 46 * math.sin(a), 96 * math.cos(a), 96 * math.sin(a))
        b = math.radians(-54 + 72 * k)
        inner += pen.path(pent(150 * math.cos(b), 150 * math.sin(b), 50, -54 + 72 * k + 180), fill="#212121")
    out += pen.clipped(f"M{-r},0 A{r},{r} 0 1 0 {r},0 A{r},{r} 0 1 0 {-r},0 Z", inner)
    return out + pen.circle(0, 0, r, fill="none")


def cawan(pen):
    out = pen.ellipse(0, 120, 170, 34, fill="#90caf9")
    out += pen.ellipse(0, 114, 100, 16, fill="#bbdefb", sw=DW)
    out += pen.tube("M96,-30 Q170,-34 158,22 Q148,66 76,56", 18, "#ffffff")
    out += pen.path("M-110,-60 L110,-60 Q104,90 0,110 Q-104,90 -110,-60 Z", fill="#ffffff")
    out += pen.ellipse(0, -60, 110, 24, fill="#8d6e63")
    out += pen.path("M-104,0 Q0,24 104,0", fill="none", w=DW)
    for x in (-60, 0, 60):
        out += pen.circle(x, 34, 12, fill="#f48fb1", sw=DW - 0.4)
    for x in (-40, 0, 40):
        out += pen.path(f"M{x},-100 Q{x - 16},-130 {x},-150 Q{x + 16},-170 {x},-196", fill="none", w=DW)
    return out


def durian(pen):
    pts = []
    n = 40
    for k in range(n):
        a = 2 * math.pi * k / n
        r = 1.0 if k % 2 == 0 else 1.14
        pts.append(f"{120 * r * math.cos(a):.1f},{20 + 140 * r * math.sin(a):.1f}")
    body = "M" + " L".join(pts) + " Z"
    out = pen.path(body, fill="#9ccc65")
    inner = ""
    for row in range(-5, 7):
        for col in range(-4, 5):
            x = col * 34 + (17 if row % 2 else 0)
            y = 20 + row * 28
            inner += pen.path(f"M{x - 9},{y + 6} L{x},{y - 8} L{x + 9},{y + 6}", fill="none", w=DW - 0.6)
    out += pen.clipped(body, inner)
    out += pen.rect(-12, -170, 24, 44, fill="#8d6e63", rx=6)
    return out


def epal(pen):
    body = "M0,-90 C60,-140 150,-100 140,0 C130,100 60,150 0,124 C-60,150 -130,100 -140,0 C-150,-100 -60,-140 0,-90 Z"
    out = pen.tube("M0,-90 Q4,-130 16,-158", 14, "#8d6e63")
    out += pen.path(body, fill="#e53935")
    out += pen.path("M-96,-40 Q-104,10 -84,50", fill="none", w=DW)
    out += leaf(pen, 18, -146, 90, -24)
    return out


def feri(pen):
    out = pen.rect(40, -190, 40, 70, fill="#e53935", rx=4)
    out += pen.rect(-110, -130, 200, 62, fill="#ffffff", rx=6)
    for x in range(-96, 80, 36):
        out += pen.rect(x, -116, 24, 24, fill=GLASS, rx=5, sw=DW)
    out += pen.rect(-150, -70, 300, 72, fill="#ffffff", rx=6)
    for x in range(-136, 140, 40):
        out += pen.circle(x + 14, -34, 12, fill=GLASS, sw=DW)
    out += pen.path("M-180,0 L180,0 L150,80 L-150,80 Z", fill="#1e88e5")
    out += pen.text(0, 54, "FERI", 44, fill_color="#ffffff", spacing=4)
    out += pen.path("M-200,100 " + "".join("q25,-20 50,0 " for _ in range(8)), fill="none", w=DW + 0.6)
    out += pen.path("M-170,140 " + "".join("q25,-20 50,0 " for _ in range(7)), fill="none", w=DW)
    return out


def gajah(pen):
    out = ""
    for x in (-40, 10, 70, 120):
        out += pen.rect(x - 20, 60, 46, 90, fill="#b0bec5", rx=14)
    out += pen.path("M150,0 Q180,20 172,60", fill="none", w=LW)
    out += pen.ellipse(40, 30, 130, 90, fill="#b0bec5")
    out += pen.ellipse(-80, -40, 80, 76, fill="#b0bec5")
    out += pen.tube("M-140,-10 Q-170,60 -150,110 Q-140,130 -120,120", 34, "#b0bec5")
    out += pen.path("M-60,-90 Q30,-110 40,-20 Q40,50 -40,40 Q-30,-20 -60,-90 Z", fill="#90a4ae")
    out += pen.path("M-30,-60 Q10,-60 14,-20", fill="none", w=DW - 0.4)
    out += pen.circle(-110, -54, 9, fill=INK, sw=1) + '<circle cx="-107" cy="-57" r="3" fill="#fff"/>'
    out += pen.path("M-128,0 Q-118,20 -98,24 L-108,8 Z", fill="#ffffff", w=DW)
    return out


def harimau(pen):
    out = pen.ellipse(0, 130, 110, 60, fill="#ff9800")
    for x in (-50, 50):
        out += pen.ellipse(x, 176, 34, 18, fill="#ff9800")
    for x in (-60, -20, 20, 60):
        out += pen.path(f"M{x},84 Q{x + 6},110 {x},134", fill="none", w=DW + 0.6)
    for s in (-1, 1):
        out += pen.circle(s * 92, -80, 32, fill="#ff9800")
        out += pen.circle(s * 92, -80, 16, fill="#ffffff", sw=DW)
    out += pen.ellipse(0, 0, 128, 106, fill="#ff9800")
    for s in (-1, 1):
        out += pen.path(f"M{s * 126},-10 L{s * 96},-4 L{s * 124},6 M{s * 120},30 L{s * 90},28 L{s * 114},44",
                        fill="none", w=DW + 0.6)
    out += pen.path("M-20,-104 L-14,-76 L-6,-104 M6,-104 L14,-76 L20,-104 M-44,-96 L-34,-74", fill="none", w=DW + 0.6)
    out += pen.ellipse(0, 40, 64, 46, fill="#ffffff")
    out += face(pen, {}, cx=0, cy=-6, gap=40)
    out += pen.path("M-14,22 L14,22 L0,36 Z", fill="#5d4037", w=DW)
    for s in (-1, 1):
        for y in (46, 58):
            out += pen.circle(s * 30, y, 3, fill=INK, sw=1)
    return out


def ikan(pen):
    out = pen.path("M-10,-80 Q30,-130 80,-90 Q40,-80 30,-50 Z", fill="#ffb300")
    body = "M-160,0 Q-60,-110 80,-34 L160,-100 L140,0 L160,100 L80,34 Q-60,110 -160,0 Z"
    out += pen.path(body, fill="#ff7043")
    inner = ""
    for row in (-1, 0, 1):
        for x in range(-40, 80, 30):
            inner += pen.path(f"M{x},{row * 30 - 14} Q{x + 18},{row * 30} {x},{row * 30 + 14}", fill="none", w=DW - 0.6)
    out += pen.clipped(body, inner) + pen.path(body, fill="none")
    out += pen.path("M-80,-50 Q-60,0 -80,50", fill="none", w=DW)
    out += pen.circle(-118, -14, 16, fill="#ffffff", sw=DW) + pen.circle(-114, -14, 7, fill=INK, sw=1)
    for x, y, r in ((-190, -60, 10), (-210, -100, 7), (-196, -134, 5)):
        out += pen.circle(x, y, r, fill="#e1f5fe", sw=DW - 0.6)
    return out


def jam(pen):
    out = ""
    for s in (-1, 1):
        out += pen.path(f"M{s * 60},-120 A50,50 0 0 1 {s * 140},-56", fill="#fdd835")
        out += pen.line(s * 96, 120, s * 120, 160, sw=LW + 2)
    out += pen.circle(0, 10, 140, fill="#e53935")
    out += pen.circle(0, 10, 112, fill="#ffffff", sw=DW + 0.6)
    for n, (x, y) in (("12", (0, -62)), ("3", (82, 26)), ("6", (0, 108)), ("9", (-82, 26))):
        out += pen.text(x, y, n, 34, fill_color=INK)
    out += pen.line(0, 10, 0, -50, sw=LW + 1) + pen.line(0, 10, 46, 30, sw=LW + 1)
    out += pen.circle(0, 10, 8, fill=INK, sw=1)
    out += pen.rect(-14, -170, 28, 28, fill="#fdd835", rx=6)
    return out


def kucing(pen):
    out = pen.tube("M80,120 Q170,110 160,30 Q154,0 130,6", 22, "#ffb74d")
    out += pen.ellipse(0, 90, 100, 84, fill="#ffb74d")
    out += pen.ellipse(0, 110, 54, 52, fill="#fff3e0", sw=DW)
    for x in (-44, 44):
        out += pen.ellipse(x, 166, 30, 16, fill="#ffb74d")
    for s in (-1, 1):
        out += pen.path(f"M{s * 80},-80 L{s * 90},-170 L{s * 20},-130 Z", fill="#ffb74d")
        out += pen.path(f"M{s * 72},-96 L{s * 80},-148 L{s * 36},-124 Z", fill="#f8bbd0", w=DW)
    out += pen.circle(0, -60, 96, fill="#ffb74d")
    for x in (-24, 0, 24):
        out += pen.path(f"M{x},-156 Q{x + 4},-140 {x},-124", fill="none", w=DW + 0.6)
    out += face(pen, {}, cx=0, cy=-64, gap=34)
    for s in (-1, 1):
        for dy in (-6, 8):
            out += pen.line(s * 44, -30 + dy, s * 110, -38 + dy * 2, sw=DW - 0.4)
    return out


def lebah(pen):
    out = pen.ellipse(-10, -96, 60, 40, fill="#e1f5fe", rot=-20)
    out += pen.ellipse(60, -96, 60, 40, fill="#e1f5fe", rot=20)
    body = "M-80,0 A110,76 0 1 0 140,0 A110,76 0 1 0 -80,0 Z"
    out += pen.path("M140,0 L180,10 L140,20 Z", fill="#424242")
    out += pen.path(body, fill="#fdd835")
    out += pen.clipped(body, "".join(pen.fillrect(x, -90, 34, 180, "#424242", sw=DW) for x in (-10, 54, 118)))
    out += pen.path(body, fill="none")
    out += pen.circle(-110, -6, 62, fill="#fdd835")
    out += face(pen, {}, cx=-112, cy=-6, gap=22)
    for s in (-1, 1):
        out += pen.path(f"M{-110 + s * 20},-62 Q{-110 + s * 34},-110 {-110 + s * 54},-118", fill="none", w=DW + 0.6)
        out += pen.circle(-110 + s * 56, -120, 10, fill="#424242", sw=DW)
    return out


def matahari(pen):
    out = ""
    for k in range(12):
        a = math.radians(k * 30)
        b, c = math.radians(k * 30 - 9), math.radians(k * 30 + 9)
        out += pen.path(f"M{115 * math.cos(b):.1f},{115 * math.sin(b):.1f} L{165 * math.cos(a):.1f},{165 * math.sin(a):.1f} "
                        f"L{115 * math.cos(c):.1f},{115 * math.sin(c):.1f} Z", fill="#ffb300")
    out += pen.circle(0, 0, 112, fill="#fdd835")
    return out + cute_face(pen, 0, 10, gap=34)


def nanas(pen):
    out = ""
    for ang, l in ((-150, 120), (-120, 140), (-90, 150), (-60, 140), (-30, 120)):
        a = math.radians(ang)
        ex, ey = l * math.cos(a), -80 + l * math.sin(a)
        nx, ny = -math.sin(a) * 22, math.cos(a) * 22
        out += pen.path(f"M{-nx:.0f},{-80 - ny:.0f} L{ex:.0f},{ey:.0f} L{nx:.0f},{-80 + ny:.0f} Z", fill="#43a047")
    body = "M-100,40 A100,130 0 1 0 100,40 A100,130 0 1 0 -100,40 Z"
    out += pen.path(body, fill="#ffb300")
    grid = "".join(pen.line(x, -120, x + 260, 200, sw=DW - 0.4) + pen.line(x + 260, -120, x, 200, sw=DW - 0.4)
                   for x in range(-360, 200, 46))
    out += pen.clipped(body, grid) + pen.path(body, fill="none")
    return out


def oren(pen):
    out = pen.circle(-30, 20, 130, fill="#ff9800")
    for x, y in ((-90, -30), (-40, -60), (10, -10), (-70, 50), (-10, 70), (30, 30), (-110, 30)):
        out += pen.circle(x, y, 3.5, fill=INK, sw=1)
    out += pen.tube("M-30,-110 L-24,-140", 12, "#8d6e63") + leaf(pen, -24, -136, 80, -30)
    out += pen.path("M60,150 A100,100 0 0 1 180,40 L120,130 Z", fill="#ffb74d")
    out += pen.path("M60,150 A100,100 0 0 1 180,40", fill="none", w=LW)
    for k in range(1, 4):
        a = math.radians(-90 - 22 * k)
        out += pen.line(120, 130, 120 + 90 * math.cos(a + math.pi / 2.6), 130 + 90 * math.sin(a + math.pi / 2.6),
                        sw=DW - 0.4)
    return out


def payung(pen):
    out = kid(pen, "aisyah", -80, 170, 0.85, la=(-64, -112), ra=(125, -250))
    out += pen.tube("M26,-40 L26,-150", 10, "#8d6e63")
    canopy = "M-180,-150 Q-170,-300 26,-320 Q222,-300 232,-150 " + "".join(
        f"Q{232 - 41 * i - 20.5:.1f},-176 {232 - 41 * (i + 1):.1f},-150 " for i in range(10)) + "Z"
    out += pen.path(canopy, fill="#ab47bc")
    for x in (-98, -16, 68, 150):
        out += pen.path(f"M26,-318 Q{(26 + x) / 2},-260 {x},-152", fill="none", w=DW)
    out += pen.circle(26, -326, 10, fill="#ab47bc", sw=DW)
    for x, y in ((-230, -200), (270, -230), (-250, 10), (270, -30), (-200, -360), (220, -400)):
        out += pen.path(f"M{x},{y} Q{x - 12},{y + 20} {x},{y + 28} Q{x + 12},{y + 20} {x},{y} Z", fill="#81d4fa", w=DW)
    return out


def rehal(pen):
    """Wooden X-shaped Quran stand with the Quran open on it (drawn around 0,0, about 340 wide)."""
    out = pen.tube("M-140,140 L120,-40 M140,140 L-120,-40", 26, "#e53935")
    out += pen.path("M0,-30 L-170,-80 L-170,-170 L0,-120 Z", fill="#ffffff")
    out += pen.path("M0,-30 L170,-80 L170,-170 L0,-120 Z", fill="#ffffff")
    for k in range(4):
        out += pen.line(-150, -150 + k * 18 + 6, -20, -110 + k * 18 + 6, sw=1.4)
        out += pen.line(20, -110 + k * 18 + 6, 150, -150 + k * 18 + 6, sw=1.4)
    out += pen.path("M0,-30 L-170,-80 L-170,-60 L0,-10 L170,-60 L170,-80 Z", fill="#1e88e5")
    return out


QARI = dict(top="#43a047", bottom="#5d4037")


def qari(pen):
    """A young qari: Amir in a kopiah, sitting cross-legged and reciting from the Quran on a rehal."""
    la, ra = (40, -150), (110, -170)
    out = kid(pen, "amir", -70, 190, 1.1, la=la, ra=ra, sit=True, headwear="kopiah", hands=False, colors=QARI,
              outfit="kurta")
    k0 = pen.k
    pen.k = k0 / 0.62
    out += f'<g transform="translate(95,95) scale(0.62)">{rehal(pen)}</g>'
    pen.k = k0
    from characters import kid_hands
    out += kid_hands(pen, "amir", -70, 190, 1.1, la=la, ra=ra, sit=True)
    for x, y in ((-200, -130), (-220, -60)):
        out += pen.path(f"M{x},{y} q14,-16 28,0 q14,16 28,0", fill="none", w=DW)
    return out


def rama_rama(pen):
    out = ""
    for s in (-1, 1):
        out += pen.path(f"M0,-20 C{s * 60},-170 {s * 190},-170 {s * 170},-60 C{s * 160},0 {s * 60},10 0,0 Z", fill="#ab47bc")
        out += pen.path(f"M0,10 C{s * 70},10 {s * 160},40 {s * 140},120 C{s * 120},170 {s * 40},120 0,30 Z", fill="#ffb74d")
        out += pen.circle(s * 110, -80, 26, fill="#fdd835", sw=DW)
        out += pen.circle(s * 90, 70, 18, fill="#81d4fa", sw=DW)
    out += pen.ellipse(0, 10, 16, 90, fill="#5d4037")
    out += pen.circle(0, -90, 22, fill="#5d4037")
    out += pen.path("M-8,-108 Q-30,-160 -54,-166 M8,-108 Q30,-160 54,-166", fill="none", w=DW + 0.6)
    out += pen.circle(-56, -168, 7, fill="#5d4037", sw=DW) + pen.circle(56, -168, 7, fill="#5d4037", sw=DW)
    return out


def siput(pen):
    out = pen.path("M-170,110 Q-180,60 -120,60 L120,60 Q190,60 180,110 Q190,140 -170,130 Z", fill="#c5e1a5")
    out += pen.tube("M-140,70 L-160,-40 M-110,70 L-120,-50", 10, "#c5e1a5")
    out += pen.circle(-160, -46, 12, fill="#ffffff", sw=DW) + pen.circle(-120, -56, 12, fill="#ffffff", sw=DW)
    pts = []
    for k in range(120):
        t = k / 119 * 3.2 * math.pi
        r = 130 * (1 - t / (3.6 * math.pi))
        pts.append(f"{30 + r * math.cos(t + math.pi):.1f},{-30 + r * math.sin(t + math.pi):.1f}")
    out += pen.circle(30, -30, 130, fill="#ffb74d")
    out += pen.path("M" + " L".join(pts), fill="none", w=DW + 0.6)
    return out


def tembikai(pen):
    whole = "M-180,-20 A120,100 0 1 0 60,-20 A120,100 0 1 0 -180,-20 Z"
    out = pen.path(whole, fill="#43a047")
    out += pen.clipped(whole, "".join(pen.path(f"M{x},-130 Q{x + 30},-20 {x},90", fill="none", w=DW + 1)
                                      for x in range(-160, 70, 40)))
    out += pen.path(whole, fill="none")
    out += pen.path("M-40,120 A140,140 0 0 1 220,120 Z", fill="#43a047")
    out += pen.path("M-22,120 A122,122 0 0 1 202,120 Z", fill="#ffffff", w=DW)
    out += pen.path("M-6,120 A106,106 0 0 1 186,120 Z", fill="#ef5350", w=DW)
    for x, y in ((40, 80), (90, 50), (140, 80), (70, 100), (115, 98), (90, 20)):
        out += pen.ellipse(x, y, 6, 10, fill="#212121", sw=1.4)
    return out


def ular(pen):
    body = "M150,140 C40,160 -160,140 -150,60 C-140,-10 140,30 140,-40 C140,-110 -40,-120 -80,-110"
    out = pen.tube(body, 50, "#7cb342")
    for x, y in ((-140, 70), (-100, 40), (-40, 30), (20, 30), (80, 10), (130, -30), (110, -80), (50, -104)):
        out += pen.circle(x, y, 7, fill="#fdd835", sw=1.6)
    out += pen.ellipse(-110, -112, 56, 40, fill="#7cb342")
    out += pen.circle(-118, -126, 8, fill=INK, sw=1) + pen.circle(-90, -126, 8, fill=INK, sw=1)
    out += pen.path("M-164,-104 L-200,-100 L-212,-112 M-200,-100 L-212,-90", fill="none", w=DW + 0.4)
    return out


def van(pen):
    k0 = pen.k
    pen.k = k0 / 0.42
    svg, length = V.van_aiskrim(pen)
    pen.k = k0
    return f'<g transform="translate({-length * 0.21:.0f},120) scale(0.42)">{svg}</g>'


def wau(pen):
    from subjects import wau as budaya_wau
    return budaya_wau(pen, 0, 0, 0.62)


def xilofon(pen):
    colors = ["#e53935", "#ff9800", "#fdd835", "#43a047", "#1e88e5", "#3949ab", "#8e24aa"]
    out = pen.path("M-190,-40 L190,-10 L190,40 L-190,90 Z", fill="#8d6e63")
    for i, c in enumerate(colors):
        x = -160 + i * 50
        h = 190 - i * 18
        out += pen.rect(x, -h / 2 + 20, 38, h, fill=c, rx=8)
        for y in (-h / 2 + 34, h / 2 + 6):
            out += pen.circle(x + 19, y, 4, fill="#bdbdbd", sw=1.4)
    for s, ang in ((-1, -30), (1, 30)):
        out += f'<g transform="rotate({ang} {s * 60} -150)">'
        out += pen.tube(f"M{s * 60},-150 L{s * 60},-20", 10, "#d7a86e")
        out += pen.circle(s * 60, -160, 20, fill="#e53935") + "</g>"
    return out


def yoyo(pen):
    out = kid(pen, "mei", -90, 170, 0.85, la=(-64, -112), ra=(100, -200))
    out += pen.path("M-4,0 Q60,40 110,120", fill="none", w=DW)
    out += pen.circle(120, 130, 70, fill="#e53935")
    out += pen.circle(120, 130, 42, fill="#fdd835", sw=DW)
    out += pen.circle(120, 130, 12, fill="#ffffff", sw=DW)
    for k in range(6):
        a = math.radians(k * 60)
        out += pen.line(120 + 46 * math.cos(a), 130 + 46 * math.sin(a), 120 + 64 * math.cos(a), 130 + 64 * math.sin(a),
                        sw=DW - 0.4)
    return out


def zirafah(pen):
    out = ""
    for x in (-60, -20, 50, 90):
        out += pen.rect(x - 14, 60, 28, 120, fill="#ffca28", rx=10)
    out += pen.path("M110,10 Q150,40 140,100", fill="none", w=LW)
    body = "M-90,30 A100,60 0 1 0 110,30 A100,60 0 1 0 -90,30 Z"
    neck = "M-90,10 L-130,-170 L-80,-180 L-40,0 Z"
    out += pen.path(neck, fill="#ffca28") + pen.path(body, fill="#ffca28")
    spots = "".join(pen.path(blob_d(x, y, 18, 14, 6, int(x * y) % 97), fill="#a1662f", w=DW)
                    for x, y in ((-60, 20), (-10, 0), (40, 20), (80, 50), (0, 60), (-110, -40), (-118, -110),
                                 (-90, -80)))
    out += pen.clipped(body, spots) + pen.clipped(neck, spots) + pen.path(body, fill="none") + pen.path(neck, fill="none")
    out += pen.ellipse(-130, -200, 56, 40, fill="#ffca28", rot=-10)
    out += pen.ellipse(-168, -190, 26, 20, fill="#ffe0b2", sw=DW, rot=-10)
    for x in (-130, -106):
        out += pen.line(x, -236, x - 4, -270, sw=LW) + pen.circle(x - 4, -276, 9, fill="#a1662f", sw=DW)
    out += pen.ellipse(-84, -220, 22, 10, fill="#ffca28", sw=DW, rot=-30)
    out += pen.circle(-138, -208, 7, fill=INK, sw=1)
    return out


# ---------------------------------------------------------------- counting & shapes extras

def belon(pen, color="#e53935"):
    out = pen.path("M0,90 Q-20,130 10,170 Q30,200 0,230", fill="none", w=DW)
    out += pen.path("M-10,100 L10,100 L0,86 Z", fill=color, w=DW)
    out += pen.ellipse(0, -10, 80, 100, fill=color)
    return out + pen.path("M-40,-60 Q-50,-30 -40,0", fill="none", w=DW)


def bunga(pen):
    out = pen.tube("M0,40 Q-10,140 0,200", 12, "#7cb342")
    out += leaf(pen, -2, 140, 70, 200) + leaf(pen, 0, 160, 70, -30)
    for k in range(8):
        a = 2 * math.pi * k / 8
        out += pen.circle(64 * math.cos(a), 64 * math.sin(a), 44, fill="#f06292")
    return out + pen.circle(0, 0, 52, fill="#fdd835") + cute_face(pen, 0, 4, gap=18)


def bintang(pen):
    return pen.path(star_d(0, 0, 160, 70), fill="#fdd835") + cute_face(pen, 0, 20, gap=26)


def kereta(pen):
    k0 = pen.k
    pen.k = k0 / 0.5
    svg, length = V.kereta(pen)
    pen.k = k0
    return f'<g transform="translate({-length * 0.25:.0f},80) scale(0.5)">{svg}</g>'


def donat(pen):
    out = pen.circle(0, 0, 150, fill="#d7a86e")
    icing = "M-130,0 " + "".join(
        f"A20,20 0 0 1 {130 * math.cos(math.radians(180 + (k + 1) * 30)):.1f},{130 * math.sin(math.radians(180 + (k + 1) * 30)):.1f} "
        for k in range(12)) + "Z"
    out += pen.path(icing, fill="#f48fb1")
    rnd = random.Random(2)
    for _ in range(18):
        a, r = rnd.uniform(0, 2 * math.pi), rnd.uniform(70, 115)
        x, y = r * math.cos(a), r * math.sin(a)
        out += pen.rect(x - 9, y - 3.5, 18, 7, fill=rnd.choice(["#fdd835", "#42a5f5", "#ffffff", "#66bb6a"]), rx=3.5,
                        sw=1.4)
    return out + pen.circle(0, 0, 48, fill="#ffffff")


def khemah(pen):
    out = pen.path("M-190,140 L0,-170 L190,140 Z", fill="#ff7043")
    out += pen.path("M0,-170 L-60,140 L60,140 Z", fill="#ffe0b2")
    out += pen.path("M0,-170 L0,140", fill="none", w=DW)
    out += pen.line(0, -170, 0, -220, sw=LW) + pen.path("M0,-220 L50,-206 L0,-192 Z", fill="#fdd835", w=DW)
    return out + pen.line(-220, 140, 220, 140, sw=LW)


def kotak_hadiah(pen):
    out = pen.rect(-150, -110, 300, 260, fill="#42a5f5", rx=6)
    out += pen.rect(-26, -110, 52, 260, fill="#e53935", sw=DW + 0.6)
    out += pen.rect(-170, -150, 340, 56, fill="#64b5f6", rx=8)
    out += pen.rect(-26, -150, 52, 56, fill="#e53935", sw=DW + 0.6)
    for s in (-1, 1):
        out += pen.path(f"M0,-150 C{s * 40},-230 {s * 120},-210 {s * 90},-160 C{s * 70},-140 {s * 30},-150 0,-150 Z",
                        fill="#e53935")
    return out + pen.circle(0, -152, 16, fill="#c62828")


def buku(pen):
    out = pen.rect(-130, -170, 260, 340, fill="#43a047", rx=10)
    out += pen.rect(-130, -170, 36, 340, fill="#2e7d32", rx=6, sw=DW + 0.6)
    out += pen.rect(-70, -110, 170, 80, fill="#ffffff", rx=8, sw=DW + 0.6)
    out += pen.text(15, -56, "ABC", 46, fill_color="#e53935")
    out += pen.path(star_d(15, 60, 40, 18), fill="#fdd835", w=DW)
    return out


def telur(pen):
    out = pen.path("M-200,90 Q-190,30 -110,30 L110,30 Q190,30 200,90 Q170,150 0,150 Q-170,150 -200,90 Z", fill="#d7a86e")
    for x in range(-180, 200, 36):
        out += pen.path(f"M{x},50 Q{x + 20},90 {x + 6},140", fill="none", w=DW - 0.4)
    out += pen.ellipse(0, -40, 110, 145, fill="#fff8e1")
    for x, y in ((-30, -100), (40, -60), (-20, 20), (50, 30)):
        out += pen.circle(x, y, 9, fill="#ffcc80", sw=1.6)
    return out


def bintang_laut(pen):
    out = pen.path(star_d(0, 0, 165, 72), fill="#ff7043")
    for k in range(5):
        a = math.radians(-90 + 72 * k)
        for r in (40, 75, 110):
            out += pen.circle(r * math.cos(a), r * math.sin(a), 7, fill="#ffffff", sw=1.6)
    return out + cute_face(pen, 0, 8, gap=20)


def hati_d(r=1.0):
    return (f"M0,{130 * r} C{-200 * r},{10 * r} {-140 * r},{-150 * r} 0,{-70 * r} "
            f"C{140 * r},{-150 * r} {200 * r},{10 * r} 0,{130 * r} Z")


def belon_hati(pen):
    out = pen.path("M0,130 Q-20,170 10,200 Q30,230 0,260", fill="none", w=DW)
    out += pen.path(hati_d(1.0), fill="#e53935")
    return out + pen.path("M-90,-70 Q-104,-40 -90,-10", fill="none", w=DW)
