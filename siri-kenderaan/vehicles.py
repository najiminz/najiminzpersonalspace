"""The 30 vehicles. Each function draws in local coordinates and returns (svg, length).

Road vehicles: x runs from the front bumper (left) to the back, y=0 is the road.
Aircraft, boats and the submarine use y=0 as their centre/water line instead.
"""
import math

from draw import (DW, GLASS, INK, LW, arch, cross_d, mirror, spoked_wheel, star_d, wheel, wheel_well)

BUMPER = "#b0bec5"
LIGHT = "#fff59d"
TAIL = "#e53935"


def lightbar(pen, x, y, w, colors):
    out = pen.rect(x, y, w, 28, fill=colors[0], rx=11)
    seg = w / len(colors)
    for i, c in enumerate(colors[1:], 1):
        if pen.colored:
            out += pen.rect(x + seg * i, y + 2, seg - (2 if i == len(colors) - 1 else 0), 24, fill=c, rx=0, sw=0)
        out += pen.line(x + seg * i, y, x + seg * i, y + 28)
    return out + pen.rect(x, y, w, 28, fill="none", rx=11)


# ---------------------------------------------------------------- emergency & cars

def van_body():
    r, R, yb = 62, 76, -40
    return (f"M18,{yb} " + arch(130, r, R, yb) + arch(615, r, R, yb) +
            f"L745,{yb} Q758,{yb} 758,-58 L758,-340 Q758,-362 736,-362 L248,-362 Q230,-362 222,-348 "
            f"L128,-222 Q120,-210 104,-208 L32,-196 Q8,-192 6,-166 L4,-80 Q4,{yb} 18,{yb} Z")


def van_cab(pen):
    out = pen.path("M210,-62 L210,-226 L244,-346 L356,-346 L356,-62 Z", fill="none", w=DW + 0.6)
    out += pen.path("M224,-232 L254,-330 L342,-330 L342,-232 Z", fill=GLASS, w=DW + 0.6)
    out += pen.line(262, -320, 236, -248, sw=2) + pen.line(285, -318, 262, -254, sw=2)
    out += pen.rect(318, -208, 26, 10, fill="#bbb", rx=5, sw=DW)
    out += pen.rect(8, -186, 38, 26, fill=LIGHT, rx=8, sw=DW + 0.6)
    out += pen.rect(-4, -88, 64, 38, fill=BUMPER, rx=10)
    out += pen.rect(732, -82, 34, 32, fill=BUMPER, rx=8)
    out += pen.rect(746, -236, 14, 48, fill=TAIL, rx=4, sw=DW)
    out += pen.line(198, -262, 182, -268, sw=LW)
    out += pen.rect(164, -298, 22, 52, fill="#fff", rx=8, sw=DW + 0.6)
    return out


def ambulans(pen):
    body = van_body()
    out = lightbar(pen, 240, -394, 176, ["#e53935", "#ffffff", "#1e63c9"])
    out += pen.rect(268, -366, 120, 6, fill="#999", sw=DW)
    out += pen.rect(696, -380, 40, 20, fill="#1e63c9", rx=6, sw=DW + 0.6)
    out += pen.path(body, fill="#ffffff")
    out += pen.clipped(body, pen.fillrect(-10, -182, 780, 50, "#e53935", sw=DW + 0.6))
    out += van_cab(pen)
    out += pen.path("M372,-62 L372,-346 L530,-346 L530,-62", fill="none", w=DW + 0.6)
    out += pen.rect(386, -330, 130, 92, fill=GLASS, rx=8, sw=DW + 0.6)
    out += pen.rect(384, -214, 26, 10, fill="#bbb", rx=5, sw=DW)
    out += pen.path(cross_d(650, -268, 50, 17), fill="#e53935")
    out += pen.text(650, -143, "AMBULANS", 36, fill_color="#ffffff")
    out += pen.text(455, -143, "999", 34, fill_color="#ffffff")
    out += pen.circle(28, -112, 9, fill="#ffcc80", sw=DW)
    out += wheel(pen, 130, 62) + wheel(pen, 615, 62)
    return out, 760


def van_aiskrim(pen):
    body = van_body()
    # giant ice cream on the roof
    out = pen.path("M470,-362 L500,-452 L530,-362 Z", fill="#e0a96d", w=DW + 0.8)
    out += pen.line(482, -398, 512, -420, sw=1.8) + pen.line(488, -380, 522, -404, sw=1.8)
    out += pen.line(518, -398, 492, -420, sw=1.8)
    out += pen.circle(500, -470, 34, fill="#f48fb1")
    out += pen.circle(500, -515, 24, fill="#a5d6a7")
    out += pen.circle(508, -543, 9, fill="#e53935", sw=DW)
    out += pen.path(body, fill="#fce4ec")
    out += pen.clipped(body, pen.fillrect(-10, -182, 780, 50, "#f06292", sw=DW + 0.6))
    out += van_cab(pen)
    # serving hatch with striped awning
    out += pen.rect(380, -330, 170, 112, fill=GLASS, rx=6, sw=DW + 0.6)
    out += pen.rect(372, -222, 186, 14, fill="#ffffff", rx=4, sw=DW)
    aw = "M368,-352 L562,-352 L562,-326 " + "".join(
        f"Q{562 - 24.25 * i - 12.1:.1f},{-306} {562 - 24.25 * (i + 1):.1f},-326 " for i in range(8)) + "Z"
    out += pen.path(aw, fill="#ffffff", w=DW + 0.6)
    if pen.colored:
        for i in range(0, 8, 2):
            out += pen.rect(368 + 24.25 * i + 1, -350, 22, 23, fill="#f06292", sw=0)
    for i in range(1, 8):
        out += pen.line(368 + 24.25 * i, -352, 368 + 24.25 * i, -326, sw=1.8)
    out += pen.path(aw, fill="none", w=DW + 0.6)
    # popsicle + cone pictures on the back panel
    out += pen.rect(600, -312, 44, 74, fill="#ffb74d", rx=20, sw=DW + 0.6)
    out += pen.rect(615, -240, 14, 34, fill="#e0a96d", rx=4, sw=DW)
    out += pen.path("M676,-262 L696,-206 L716,-262 Z", fill="#e0a96d", w=DW + 0.6)
    out += pen.circle(696, -276, 24, fill="#f48fb1", sw=DW + 0.6)
    out += pen.text(650, -143, "AISKRIM", 38, fill_color="#ffffff", spacing=2)
    out += pen.text(465, -143, "SEDAP!", 30, fill_color="#ffffff")
    out += wheel(pen, 130, 62) + wheel(pen, 615, 62)
    return out, 760


def sedan(pen, lower, stripe, label, roof, label_size=44):
    r, R, yb = 58, 72, -38
    body = (f"M22,{yb} " + arch(140, r, R, yb) + arch(595, r, R, yb) +
            f"L715,{yb} Q738,{yb} 738,-62 L738,-128 Q738,-150 715,-152 L612,-160 L536,-256 "
            f"Q526,-268 506,-268 L318,-268 Q298,-268 286,-256 L206,-172 L42,-156 Q10,-150 6,-118 "
            f"L4,-70 Q4,{yb} 22,{yb} Z")
    out = ""
    if roof == "police":
        out += pen.rect(342, -278, 132, 12, fill="#888", sw=DW)
        out += lightbar(pen, 322, -304, 172, ["#e53935", "#1e63c9"])
    elif roof == "taxi":
        out += pen.rect(352, -312, 112, 46, fill="#fdd835", rx=10)
        out += pen.text(408, -279, "TEKSI", 26, fill_color=INK)
    out += pen.path(body, fill="#ffffff")
    out += pen.clipped(body, pen.fillrect(-10, -120, 760, 90, lower, sw=DW + 0.6) +
                       pen.fillrect(-10, -146, 760, 22, stripe, sw=DW + 0.6))
    out += pen.path("M234,-170 L296,-246 L406,-246 L406,-170 Z", fill=GLASS, w=DW + 0.6)
    out += pen.path("M424,-170 L424,-246 L512,-246 L572,-170 Z", fill=GLASS, w=DW + 0.6)
    out += pen.line(300, -236, 272, -200, sw=2) + pen.line(322, -236, 296, -204, sw=2)
    out += pen.line(222, -166, 222, -50) + pen.line(415, -258, 415, -50) + pen.line(590, -164, 590, -131)
    out += pen.rect(380, -112, 24, 9, fill="#ccc", rx=4, sw=DW)
    out += pen.rect(556, -112, 24, 9, fill="#ccc", rx=4, sw=DW)
    out += pen.text(400, -55, label, label_size, fill_color="#ffffff", spacing=3)
    out += pen.path("M10,-140 L46,-146 L50,-126 L12,-122 Z", fill=LIGHT, w=DW + 0.6)
    out += pen.rect(-4, -80, 46, 32, fill=BUMPER, rx=10)
    out += pen.rect(712, -80, 34, 30, fill=BUMPER, rx=8)
    out += pen.rect(724, -148, 14, 26, fill=TAIL, rx=4, sw=DW)
    out += pen.line(214, -176, 204, -184, sw=LW)
    out += pen.rect(180, -204, 28, 24, fill="#fff", rx=8, sw=DW + 0.6)
    out += wheel(pen, 140, r) + wheel(pen, 595, r)
    return out, 740


def kereta_polis(pen):
    return sedan(pen, "#163b8c", "#fbc02d", "POLIS", "police")


def teksi(pen):
    return sedan(pen, "#e53935", "#fdd835", "TEKSI", "taxi")


def kereta(pen):
    r, R, yb = 56, 70, -38
    body = (f"M20,{yb} " + arch(120, r, R, yb) + arch(510, r, R, yb) +
            f"L610,{yb} Q632,{yb} 632,-62 L632,-150 Q632,-172 618,-184 L566,-266 Q554,-284 530,-284 "
            f"L290,-284 Q266,-284 252,-268 L184,-184 L48,-164 Q12,-156 6,-122 L4,-70 Q4,{yb} 20,{yb} Z")
    out = pen.rect(300, -296, 220, 12, fill="#888", rx=5, sw=DW)
    out += pen.path(body, fill="#ff8a3d")
    out += pen.clipped(body, pen.fillrect(-10, -112, 660, 16, "#ffffff", sw=DW))
    out += pen.path("M208,-184 L272,-264 L392,-264 L392,-184 Z", fill=GLASS, w=DW + 0.6)
    out += pen.path("M408,-184 L408,-264 L538,-264 L590,-184 Z", fill=GLASS, w=DW + 0.6)
    out += pen.line(278, -254, 248, -212, sw=2) + pen.line(300, -254, 272, -216, sw=2)
    out += pen.line(198, -180, 198, -48) + pen.line(400, -276, 400, -48) + pen.line(592, -180, 592, -128)
    out += pen.rect(360, -160, 26, 10, fill="#ddd", rx=5, sw=DW)
    out += pen.rect(552, -160, 26, 10, fill="#ddd", rx=5, sw=DW)
    out += pen.path("M10,-146 L50,-152 L54,-130 L12,-126 Z", fill=LIGHT, w=DW + 0.6)
    out += pen.rect(-4, -82, 46, 34, fill=BUMPER, rx=10)
    out += pen.rect(608, -82, 32, 32, fill=BUMPER, rx=8)
    out += pen.rect(618, -176, 14, 30, fill=TAIL, rx=4, sw=DW)
    out += pen.line(192, -186, 182, -194, sw=LW)
    out += pen.rect(156, -214, 28, 24, fill="#fff", rx=8, sw=DW + 0.6)
    out += wheel(pen, 120, r) + wheel(pen, 510, r)
    return out, 640


def kereta_lumba(pen):
    out = pen.tube("M716,-110 L716,-262", 14, "#555")
    out += pen.rect(680, -300, 120, 30, fill="#e53935", rx=6)
    out += pen.rect(792, -320, 18, 110, fill="#ffffff", rx=6)
    body = ("M14,-56 L10,-84 Q12,-98 40,-102 L250,-134 Q300,-186 362,-190 L420,-190 Q440,-232 476,-232 "
            "L520,-228 Q560,-214 600,-180 L720,-136 Q748,-120 748,-92 L748,-56 Z")
    out += pen.path(body, fill="#e53935")
    out += pen.clipped(body, pen.fillrect(0, -118, 760, 22, "#ffffff", sw=DW) +
                       pen.fillrect(0, -96, 760, 40, "#212121", sw=DW))
    out += pen.path("M300,-150 Q340,-150 380,-130 L560,-130 Q600,-140 620,-170", fill="none", w=DW)
    out += pen.circle(386, -212, 32, fill="#fdd835")
    out += pen.path("M356,-222 Q380,-236 412,-220 L410,-204 L356,-206 Z", fill="#37474f", w=DW)
    out += pen.circle(548, -168, 30, fill="#ffffff", sw=DW + 0.6)
    out += pen.text(548, -155, "8", 36, fill_color=INK)
    out += pen.rect(-26, -66, 140, 18, fill="#ffffff", rx=6)
    out += pen.rect(-30, -104, 16, 58, fill="#e53935", rx=6)
    out += wheel(pen, 150, 62, rim="#ffffff") + wheel(pen, 630, 72, rim="#ffffff")
    out += pen.text(460, -64, "LUMBA", 26, fill_color="#ffffff", fill_line=INK)
    return f'<g transform="translate(30,0)">{out}</g>', 840


def jip(pen):
    r, R, yb = 70, 84, -52
    body = (f"M22,{yb} " + arch(135, r, R, yb) + arch(530, r, R, yb) +
            f"L640,{yb} Q656,{yb} 656,-74 L656,-300 Q656,-320 636,-320 L272,-320 L236,-212 "
            f"L44,-204 Q12,-200 10,-170 L8,-84 Q8,{yb} 22,{yb} Z")
    out = pen.rect(290, -342, 340, 12, fill="#5d4037", rx=4, sw=DW)
    for x in (310, 460, 610):
        out += pen.line(x, -330, x, -320, sw=DW)
    out += pen.circle(676, -200, 56, fill="#3a3a3a")
    out += pen.circle(676, -200, 30, fill="#cfd8dc", sw=DW)
    out += pen.path(body, fill="#7cb342")
    out += pen.clipped(body, pen.fillrect(-10, -160, 680, 22, "#33691e", sw=DW))
    out += pen.path("M282,-300 L388,-300 L388,-222 L256,-222 Z", fill=GLASS, w=DW + 0.6)
    out += pen.rect(404, -300, 112, 78, fill=GLASS, rx=4, sw=DW + 0.6)
    out += pen.rect(532, -300, 108, 78, fill=GLASS, rx=4, sw=DW + 0.6)
    out += pen.line(250, -212, 250, -60) + pen.line(396, -312, 396, -60)
    out += pen.rect(354, -196, 26, 10, fill="#ddd", rx=5, sw=DW)
    out += pen.text(320, -76, "4X4", 34, fill_color="#ffffff")
    out += pen.rect(12, -186, 32, 26, fill=LIGHT, rx=8, sw=DW + 0.6)
    out += pen.path("M-10,-60 L-10,-160 L14,-160 M-10,-110 L14,-110", fill="none", w=LW + 2)
    out += pen.rect(-14, -96, 60, 40, fill="#616161", rx=8)
    out += pen.line(244, -224, 232, -232, sw=LW)
    out += pen.rect(206, -264, 26, 50, fill="#fff", rx=8, sw=DW + 0.6)
    out += wheel(pen, 135, r) + wheel(pen, 530, r)
    return f'<g transform="translate(16,0)">{out}</g>', 750


# ---------------------------------------------------------------- two & three wheelers

def motosikal(pen):
    out = spoked_wheel(pen, 395, 64, tyre=16, spokes=10)
    out += pen.tube("M290,-120 L395,-64", 14, "#757575")
    out += pen.tube("M384,-78 L404,-206", 10, "#bdbdbd")
    for y in (-110, -130, -150, -170):
        out += pen.line(380 + (y + 78) * -0.16, y, 402 + (y + 78) * -0.16, y, sw=1.6)
    out += pen.tube("M236,-100 L330,-100 Q360,-100 382,-116 L466,-132", 18, "#cfd8dc")
    out += pen.path("M330,-122 Q396,-164 474,-124 L466,-112 Q396,-150 338,-110 Z", fill="#e53935", w=DW + 0.6)
    out += pen.path("M270,-212 L442,-220 Q454,-200 442,-180 L340,-160 L290,-160 Z", fill="#e53935")
    out += pen.path("M262,-232 Q280,-258 330,-252 L442,-238 Q462,-234 454,-216 L262,-208 Z", fill="#5d4037")
    out += pen.rect(450, -236, 22, 16, fill=TAIL, rx=4, sw=DW)
    out += pen.rect(198, -172, 108, 82, fill="#9e9e9e", rx=16)
    for y in (-152, -134, -116):
        out += pen.line(206, y, 298, y, sw=1.8)
    out += pen.tube("M156,-246 L226,-136 L300,-112", 12, "#424242")
    tank = "M160,-250 Q180,-294 250,-286 Q292,-280 288,-240 L270,-210 L190,-208 Q158,-214 160,-250 Z"
    out += pen.path(tank, fill="#e53935")
    out += pen.clipped(tank, pen.fillrect(150, -262, 150, 16, "#ffffff", sw=DW))
    out += pen.rect(280, -110, 34, 10, fill="#424242", rx=4, sw=DW)
    out += pen.tube("M152,-262 L85,-64", 16, "#cfd8dc")
    out += spoked_wheel(pen, 85, 64, tyre=16, spokes=10)
    out += pen.path("M22,-100 Q85,-152 148,-100 L138,-91 Q85,-137 32,-91 Z", fill="#e53935", w=DW + 0.6)
    out += pen.circle(126, -240, 26, fill="#9e9e9e")
    out += pen.circle(120, -240, 16, fill=LIGHT, sw=DW)
    out += pen.tube("M146,-282 L178,-302 L220,-294", 10, "#424242")
    out += pen.rect(206, -302, 26, 14, fill="#424242", rx=6, sw=DW)
    out += pen.line(176, -300, 166, -346, sw=LW)
    out += pen.ellipse(164, -354, 18, 11, fill="#ffffff", sw=DW + 0.6)
    return out, 480


def basikal(pen):
    out = spoked_wheel(pen, 345, 78) + spoked_wheel(pen, 75, 78)
    out += pen.path("M215,-108 L345,-90 M215,-56 L345,-66", fill="none", w=DW)
    out += pen.circle(345, -78, 14, fill="#9e9e9e", sw=DW)
    out += pen.tube("M345,-78 L215,-82 L255,-235 Z M215,-82 L106,-206 L118,-238 L255,-235", 13, "#29b6f6")
    out += pen.tube("M110,-215 L75,-78", 11, "#bdbdbd")
    out += pen.tube("M255,-235 L262,-266", 9, "#9e9e9e")
    out += pen.path("M232,-272 Q260,-286 304,-274 Q302,-260 272,-262 L242,-262 Z", fill="#5d4037")
    out += pen.tube("M118,-238 L112,-276 L150,-282", 9, "#616161")
    out += pen.rect(144, -288, 34, 14, fill="#5d4037", rx=6, sw=DW)
    out += pen.path("M14,-332 L120,-332 L110,-276 L26,-276 Z", fill="#ffcc80")
    for x in (40, 66, 92):
        out += pen.line(x, -330, x + 2, -278, sw=1.6)
    out += pen.line(20, -304, 116, -304, sw=1.6)
    out += pen.circle(215, -82, 26, fill="#9e9e9e")
    out += pen.tube("M215,-82 L242,-36", 8, "#616161")
    out += pen.rect(228, -40, 34, 10, fill="#424242", rx=4, sw=DW)
    out += pen.circle(104, -194, 9, fill=LIGHT, sw=DW)
    return out, 420


def beca(pen):
    out = spoked_wheel(pen, 470, 72)
    out += pen.tube("M120,-72 L252,-112 L380,-92 L470,-72", 13, "#455a64")
    out += pen.tube("M380,-92 L404,-262", 11, "#455a64")
    out += pen.path("M384,-284 Q412,-296 452,-284 Q450,-270 424,-272 L394,-272 Z", fill="#5d4037")
    out += pen.tube("M246,-232 L290,-300 L326,-300", 10, "#455a64")
    out += pen.circle(380, -92, 22, fill="#9e9e9e")
    out += pen.tube("M380,-92 L404,-46", 8, "#616161")
    hood = "M50,-270 C40,-420 120,-480 262,-462 L256,-270 Z"
    out += pen.path(hood, fill="#ffca28")
    out += pen.clipped(hood, pen.path("M110,-270 C104,-390 160,-440 262,-432", fill="none", w=DW) +
                       pen.path("M180,-270 C176,-370 210,-405 262,-402", fill="none", w=DW))
    for i in range(7):
        t = i / 6
        x = 50 + (262 - 50) * t ** 0.7 - 20 * math.sin(t * math.pi)
        y = -270 - 190 * math.sin(t * math.pi / 2) ** 0.8
        out += pen.circle(x, y, 9, fill="#e91e63", sw=DW)
    out += pen.path("M24,-112 Q12,-150 46,-162 L72,-262 Q78,-282 98,-282 L236,-282 Q256,-282 256,-262 "
                    "L260,-112 Z", fill="#e53935")
    out += pen.rect(70, -212, 170, 30, fill="#ffffff", rx=10, sw=DW + 0.6)
    out += pen.path(star_d(160, -246, 18, 8), fill="#fdd835", w=DW)
    out += pen.rect(-14, -124, 92, 16, fill="#8d6e63", rx=5)
    out += spoked_wheel(pen, 130, 72)
    return out, 560


# ---------------------------------------------------------------- buses

def bus(pen, color, label, label_color, doors, lower=None, sign=None):
    r, R, yb = 62, 78, -42
    body = (f"M20,{yb} " + arch(165, r, R, yb) + arch(640, r, R, yb) +
            f"L780,{yb} Q798,{yb} 798,-62 L798,-405 Q798,-426 777,-426 L40,-426 Q16,-426 13,-402 "
            f"L4,-262 L4,-72 Q4,{yb} 20,{yb} Z")
    out = pen.rect(46, -442, 46, 18, fill="#ff7043", rx=6, sw=DW + 0.6)
    out += pen.rect(712, -442, 46, 18, fill="#ff7043", rx=6, sw=DW + 0.6)
    out += pen.path(body, fill=color)
    bands = pen.fillrect(-10, -262, 820, 22, "#222", sw=DW)
    if lower:
        bands += pen.fillrect(-10, -240, 820, 200, lower, sw=DW)
    else:
        bands += pen.fillrect(-10, -112, 820, 16, "#222", sw=DW)
    out += pen.clipped(body, bands)
    out += pen.path("M22,-398 L124,-398 L124,-282 L15,-282 Z", fill=GLASS, w=DW + 0.6)
    out += pen.line(60, -386, 36, -300, sw=2) + pen.line(84, -386, 62, -304, sw=2)
    if sign:
        out += pen.rect(140, -416, 100, 30, fill="#212121", rx=4, sw=DW)
        out += pen.text(190, -393, sign, 22, fill_line=INK, fill_color="#ffb300")
    spans, start = [], 140 if not sign else 250
    for a, b in doors:
        out += pen.rect(a, -410, b - a, 366, fill=color, rx=4, sw=DW + 0.8)
        m = (a + b) / 2
        out += pen.line(m, -410, m, -44, sw=DW)
        for x in (a + 8, m + 8):
            out += pen.rect(x, -398, m - a - 16, 150, fill=GLASS, rx=5, sw=DW)
            out += pen.rect(x, -230, m - a - 16, 120, fill=GLASS, rx=5, sw=DW)
        if a > start + 60:
            spans.append((start, a - 14))
        start = b + 18
    spans.append((start, 785))
    for a, b in spans:
        n = max(1, round((b - a) / 112))
        ww = (b - a - (n - 1) * 14) / n
        for i in range(n):
            x = a + i * (ww + 14)
            out += pen.rect(x, -398, ww, 116, fill=GLASS, rx=8, sw=DW + 0.6)
            out += pen.line(x + ww / 2, -398, x + ww / 2, -282, sw=2)
    out += label
    out += pen.rect(6, -134, 34, 26, fill=LIGHT, rx=7, sw=DW + 0.6)
    out += pen.rect(-6, -86, 56, 42, fill="#9e9e9e", rx=10)
    out += pen.rect(772, -86, 34, 42, fill="#9e9e9e", rx=8)
    out += pen.rect(784, -200, 14, 44, fill=TAIL, rx=4, sw=DW)
    out += pen.line(14, -340, -6, -350, sw=LW)
    out += pen.rect(-24, -380, 18, 58, fill="#fff", rx=8, sw=DW + 0.6)
    out += wheel(pen, 165, r) + wheel(pen, 640, r)
    return out, 800


def bas_sekolah(pen):
    label = pen.text(568, -166, "BAS SEKOLAH", 44, fill_color="#222", spacing=2)
    return bus(pen, "#ffc928", label, "#222", [(246, 334)])


def bas_bandar(pen):
    label = pen.text(675, -150, "BANDAR", 40, fill_color="#ffffff", spacing=2)
    label += pen.text(402, -150, "10", 46, fill_color="#ffffff")
    return bus(pen, "#e8f5e9", label, "#fff", [(246, 334), (470, 558)], lower="#2e7d32", sign="10")


# ---------------------------------------------------------------- trucks

def truck_cab(pen, color, stripe=None, light=None, label=None):
    r, R, yb = 58, 72, -40
    cab = (f"M18,{yb} " + arch(120, r, R, yb) +
           f"L234,{yb} L234,-340 L52,-340 Q24,-340 20,-314 L8,-200 L4,-80 Q4,{yb} 18,{yb} Z")
    out = ""
    if light:
        out += lightbar(pen, 70, -368, 130, light)
    out += pen.path(cab, fill=color)
    if stripe:
        out += pen.clipped(cab, pen.fillrect(-10, -178, 260, 22, stripe, sw=DW + 0.6))
    out += pen.path("M30,-318 L88,-318 L88,-222 L17,-222 Z", fill=GLASS, w=DW + 0.6)
    out += pen.line(56, -306, 36, -238, sw=2)
    out += pen.rect(96, -330, 128, 188, fill="none", rx=6, sw=DW + 0.6)
    out += pen.rect(106, -318, 108, 96, fill=GLASS, rx=6, sw=DW + 0.6)
    out += pen.rect(186, -206, 26, 10, fill="#ddd", rx=5, sw=DW)
    if label:
        out += label
    out += pen.rect(6, -160, 32, 24, fill=LIGHT, rx=7, sw=DW + 0.6)
    out += pen.rect(-6, -92, 58, 46, fill=BUMPER, rx=10)
    out += mirror(pen, 16, -270)
    out += wheel(pen, 120, r)
    return out


def chassis(pen, x0=222, x1=800):
    return pen.rect(x0, -114, x1 - x0, 38, fill="#616161", rx=6)


def rear_wheels(pen, xs=(590, 712), r=58):
    return "".join(wheel(pen, x, r) for x in xs)


def lori(pen):
    out = chassis(pen)
    box = "M244,-122 L244,-404 Q244,-414 254,-414 L790,-414 Q800,-414 800,-404 L800,-122 Z"
    out += pen.path(box, fill="#eceff1")
    out += pen.clipped(box, pen.fillrect(230, -200, 580, 30, "#1e88e5", sw=DW))
    for x in range(310, 790, 66):
        out += pen.line(x, -404, x, -330, sw=1.6)
    out += pen.rect(290, -356, 80, 64, fill="#d7a86e", rx=4, sw=DW + 0.6)
    out += pen.line(330, -356, 330, -292, sw=DW) + pen.line(290, -330, 370, -330, sw=DW)
    out += pen.text(570, -300, "KARGO", 64, fill_color="#1e88e5", spacing=4)
    out += pen.text(522, -142, "PENGHANTARAN PANTAS", 24, fill_color=INK)
    out += pen.rect(790, -110, 14, 26, fill=TAIL, rx=4, sw=DW)
    out += rear_wheels(pen)
    out += truck_cab(pen, "#1e88e5", stripe="#ffffff")
    return out, 806


def lori_sampah(pen):
    out = chassis(pen)
    body = "M244,-122 L244,-392 Q244,-410 262,-410 L690,-410 Q770,-410 792,-330 L806,-122 Z"
    out += pen.path(body, fill="#43a047")
    out += pen.clipped(body, pen.fillrect(230, -200, 600, 26, "#ffffff", sw=DW))
    out += pen.path("M704,-404 L736,-122", fill="none", w=DW + 0.6)
    for x in (330, 420, 510, 600):
        out += pen.line(x, -404, x, -360, sw=1.8)
    # little bin icon
    out += pen.path("M300,-330 L380,-330 L372,-226 L308,-226 Z", fill="#ffffff", w=DW + 0.6)
    out += pen.rect(294, -344, 92, 14, fill="#ffffff", rx=5, sw=DW + 0.6)
    out += pen.line(326, -312, 330, -244, sw=DW) + pen.line(354, -312, 350, -244, sw=DW)
    out += pen.text(540, -296, "JAGA", 48, fill_color="#ffffff", spacing=3)
    out += pen.text(540, -240, "KEBERSIHAN", 38, fill_color="#ffffff", spacing=2)
    out += pen.tube("M770,-300 L830,-200 L830,-130", 12, "#9e9e9e")
    out += pen.rect(812, -200, 40, 70, fill="#ffb300", rx=6, sw=DW + 0.6)
    out += rear_wheels(pen)
    out += truck_cab(pen, "#ffffff", stripe="#43a047")
    return out, 850


def lori_tangki(pen):
    out = chassis(pen)
    out += pen.rect(300, -132, 120, 40, fill="#9e9e9e", rx=4, sw=DW + 0.6)
    for x in (330, 480, 630):
        out += pen.rect(x, -400, 50, 24, fill="#9e9e9e", rx=8, sw=DW + 0.6)
    out += pen.line(300, -430, 720, -430, sw=DW + 0.6)
    for x in range(300, 721, 70):
        out += pen.line(x, -430, x, -385, sw=DW)
    tank = "M350,-386 L700,-386 Q800,-386 800,-260 Q800,-130 700,-130 L350,-130 Q244,-130 244,-260 Q244,-386 350,-386 Z"
    out += pen.path(tank, fill="#eceff1")
    out += pen.clipped(tank, pen.fillrect(230, -230, 580, 34, "#e53935", sw=DW))
    for x in (400, 560):
        out += pen.line(x, -386, x, -130, sw=1.8)
    out += pen.text(482, -270, "MINYAK", 56, fill_color="#e53935", spacing=4)
    out += pen.path("M690,-312 L730,-272 L690,-232 L650,-272 Z", fill="#ff9800", w=DW + 0.6)
    out += pen.path("M690,-296 Q704,-276 690,-252 Q676,-276 690,-296 Z", fill="#e53935", w=DW)
    out += pen.tube("M780,-386 L780,-130 M806,-386 L806,-130", 6, "#9e9e9e")
    for y in range(-360, -140, 40):
        out += pen.line(780, y, 806, y, sw=DW)
    out += rear_wheels(pen)
    out += truck_cab(pen, "#e53935", stripe="#ffffff")
    return out, 812


def trak_tunda(pen):
    out = chassis(pen, 222, 760)
    out += pen.tube("M450,-262 L700,-400", 26, "#fdd835")
    out += pen.tube("M500,-262 L620,-350", 12, "#9e9e9e")
    out += pen.line(700, -400, 700, -230, sw=DW + 0.6)
    out += pen.path("M700,-230 L700,-206 Q700,-186 718,-186 Q734,-186 734,-204", fill="none", w=LW + 1)
    out += pen.circle(700, -400, 14, fill="#9e9e9e", sw=DW + 0.6)
    out += pen.rect(244, -270, 300, 156, fill="#fdd835", rx=8)
    for x in (340, 440):
        out += pen.line(x, -270, x, -114, sw=DW)
    out += pen.rect(258, -250, 70, 14, fill="#ddd", rx=4, sw=DW)
    out += pen.text(394, -144, "TUNDA 24 JAM", 26, fill_color=INK)
    out += pen.tube("M700,-110 L820,-110 L840,-70", 18, "#757575")
    out += pen.rect(816, -84, 46, 20, fill="#424242", rx=6, sw=DW)
    out += rear_wheels(pen, (640,))
    out += truck_cab(pen, "#fb8c00", stripe="#212121", light=["#ffb300", "#ffb300", "#ffb300"])
    return out, 862


def treler(pen):
    r, R, yb = 54, 68, -40
    out = pen.rect(220, -116, 200, 36, fill="#616161", rx=6)
    out += pen.rect(240, -152, 660, 26, fill="#757575", rx=4)
    box = "M260,-152 L260,-440 L896,-440 L896,-152 Z"
    out += pen.path(box, fill="#ef6c00")
    for x in range(286, 896, 26):
        out += pen.line(x, -428, x, -164, sw=1.4)
    out += pen.rect(300, -350, 300, 96, fill="#ef6c00", rx=6, sw=DW + 0.6)
    out += pen.text(450, -284, "KONTENA", 52, fill_color="#ffffff", spacing=3)
    out += pen.line(868, -420, 868, -170, sw=DW + 0.6) + pen.line(884, -420, 884, -170, sw=DW + 0.6)
    out += pen.tube("M380,-126 L380,-30", 10, "#757575") + pen.rect(364, -34, 32, 12, fill="#424242", sw=DW)
    out += wheel(pen, 300, r) + wheel(pen, 740, r) + wheel(pen, 852, r)
    cab = (f"M18,{yb} " + arch(110, r, R, yb) +
           f"L224,{yb} L224,-386 L48,-386 Q22,-386 18,-360 L8,-220 L4,-80 Q4,{yb} 18,{yb} Z")
    out += pen.path("M58,-386 Q80,-450 224,-452 L224,-386 Z", fill="#ffffff")
    out += pen.path(cab, fill="#ffffff")
    out += pen.clipped(cab, pen.fillrect(-10, -200, 250, 40, "#1565c0", sw=DW + 0.6))
    out += pen.path("M30,-362 L90,-362 L90,-262 L16,-262 Z", fill=GLASS, w=DW + 0.6)
    out += pen.rect(98, -372, 118, 210, fill="none", rx=6, sw=DW + 0.6)
    out += pen.rect(108, -362, 98, 100, fill=GLASS, rx=6, sw=DW + 0.6)
    out += pen.rect(182, -236, 24, 10, fill="#ddd", rx=5, sw=DW)
    out += pen.tube("M232,-380 L232,-500", 12, "#9e9e9e")
    out += pen.rect(6, -150, 32, 24, fill=LIGHT, rx=7, sw=DW + 0.6)
    out += pen.rect(-6, -92, 58, 46, fill=BUMPER, rx=10)
    out += mirror(pen, 16, -300)
    out += wheel(pen, 110, r)
    return out, 900


# ---------------------------------------------------------------- construction & farm

def tracks(pen, x0, x1):
    out = pen.rect(x0, -150, x1 - x0, 150, fill="#424242", rx=75)
    out += pen.rect(x0 + 15, -135, x1 - x0 - 30, 120, fill="#9e9e9e", rx=60, sw=DW + 0.6)
    n = 5
    for i in range(n):
        cx = x0 + 75 + (x1 - x0 - 150) * i / (n - 1)
        out += pen.circle(cx, -75, 36, fill="#bdbdbd", sw=DW + 0.6)
        out += pen.circle(cx, -75, 12, fill="#757575", sw=DW)
    for x in range(x0 + 70, x1 - 60, 28):
        out += pen.line(x, -150, x, -137, sw=DW) + pen.line(x, -13, x, 0, sw=DW)
    return out


def jentolak(pen):
    out = pen.tube("M250,-318 L250,-410", 16, "#424242")
    out += tracks(pen, 100, 620)
    out += pen.path("M150,-150 L150,-302 Q150,-320 168,-320 L370,-320 L370,-150 Z", fill="#fbc02d")
    for y in (-290, -270, -250):
        out += pen.line(230, y, 350, y, sw=1.8)
    out += pen.path("M370,-150 L370,-480 Q370,-496 386,-496 L590,-496 Q606,-496 606,-480 L606,-150 Z",
                    fill="#fbc02d")
    out += pen.rect(358, -516, 262, 22, fill="#f9a825", rx=6)
    out += pen.rect(392, -470, 90, 140, fill=GLASS, rx=6, sw=DW + 0.6)
    out += pen.rect(496, -470, 90, 140, fill=GLASS, rx=6, sw=DW + 0.6)
    out += pen.rect(546, -300, 26, 10, fill="#ddd", rx=4, sw=DW)
    out += pen.tube("M606,-120 L668,-150 L676,-34", 18, "#616161")
    out += pen.tube("M40,-128 L190,-100", 26, "#fbc02d")
    out += pen.tube("M52,-240 L170,-270", 12, "#9e9e9e")
    blade = "M-14,-318 Q44,-170 -4,-16 L66,-16 Q104,-170 50,-318 Z"
    out += pen.path(blade, fill="#fbc02d")
    out += pen.path("M18,-310 Q74,-170 30,-22", fill="none", w=DW)
    out += pen.rect(-12, -22, 82, 18, fill="#757575", rx=4, sw=DW + 0.6)
    return f'<g transform="translate(30,0)">{out}</g>', 712


def jengkaut(pen):
    out = tracks(pen, 160, 650)
    out += pen.rect(200, -176, 420, 24, fill="#616161", rx=6)
    out += pen.path("M340,-176 L340,-332 Q340,-348 356,-348 L640,-348 Q668,-348 668,-320 L668,-176 Z", fill="#fbc02d")
    out += pen.rect(600, -330, 68, 154, fill="#616161", rx=8)
    for y in (-310, -290, -270):
        out += pen.line(420, y, 560, y, sw=1.8)
    out += pen.path("M196,-176 L196,-472 Q196,-492 216,-492 L326,-492 Q346,-492 346,-472 L346,-176 Z", fill="#fbc02d")
    out += pen.path("M212,-472 L330,-472 L330,-300 L212,-300 Z", fill=GLASS, w=DW + 0.6)
    out += pen.line(240, -460, 222, -400, sw=2)
    out += pen.tube("M400,-290 Q350,-560 190,-650", 46, "#fbc02d")
    out += pen.tube("M360,-250 L292,-470", 14, "#9e9e9e")
    out += pen.tube("M190,-650 L60,-350", 34, "#fbc02d")
    out += pen.tube("M176,-600 L90,-430", 12, "#9e9e9e")
    out += pen.circle(190, -650, 16, fill="#757575", sw=DW + 0.6)
    out += pen.circle(400, -290, 16, fill="#757575", sw=DW + 0.6)
    out += pen.path("M60,-360 L-30,-330 L-46,-230 L-6,-210 L74,-276 Z", fill="#fbc02d")
    for i in range(4):
        x = -42 + i * 12
        out += pen.path(f"M{x},{-230 + i * 6} L{x - 12},{-206 + i * 6} L{x + 4},{-214 + i * 6}", fill="#757575", w=DW)
    out += pen.circle(60, -350, 12, fill="#757575", sw=DW)
    return f'<g transform="translate(70,0)">{out}</g>', 740


def lori_simen(pen):
    out = chassis(pen)
    out += pen.rect(244, -340, 34, 214, fill="#90a4ae", rx=14)
    out += pen.tube("M310,-160 L310,-118 M710,-204 L730,-118", 14, "#757575")
    drum = ("M282,-214 Q270,-338 392,-380 L626,-440 Q770,-470 790,-342 Q800,-246 690,-206 L400,-150 "
            "Q290,-136 282,-214 Z")
    out += pen.path(drum, fill="#eceff1")
    spiral = "".join(pen.tube(f"M{x},-470 Q{x + 60},-300 {x - 30},-130", 30, "#ff9800") for x in (350, 470, 590, 710))
    out += pen.clipped(drum, spiral)
    out += pen.path(drum, fill="none")
    out += pen.path("M770,-250 L852,-186 L840,-170 L756,-232 Z", fill="#ff9800", w=DW + 0.6)
    out += pen.tube("M786,-118 L806,-330", 6, "#9e9e9e") + pen.tube("M806,-118 L826,-300", 6, "#9e9e9e")
    out += pen.text(520, -260, "SIMEN", 50, fill_color="#e65100", spacing=3,
                    extra='transform="rotate(-11 520 -260)"')
    out += rear_wheels(pen)
    out += truck_cab(pen, "#1e88e5", stripe="#ff9800")
    return out, 852


def kren(pen):
    out = chassis(pen)
    out += pen.rect(236, -230, 564, 116, fill="#fbc02d", rx=8)
    for x in (300, 420, 690):
        out += pen.rect(x, -210, 80, 60, fill="#e0e0e0", rx=4, sw=DW)
    out += pen.tube("M262,-120 L250,-20 M786,-120 L800,-20", 16, "#757575")
    out += pen.rect(226, -24, 48, 14, fill="#424242", sw=DW) + pen.rect(776, -24, 48, 14, fill="#424242", sw=DW)
    out += pen.rect(540, -320, 250, 90, fill="#fbc02d", rx=10)
    out += pen.path("M556,-300 L640,-300 L640,-238 L556,-238 Z", fill=GLASS, w=DW + 0.6)
    out += pen.line(140, -760, 140, -520, sw=DW + 0.6)
    out += pen.rect(124, -540, 32, 40, fill="#e53935", rx=6, sw=DW + 0.6)
    out += pen.path("M140,-500 L140,-480 Q140,-462 156,-462 Q170,-462 170,-478", fill="none", w=LW + 1)
    out += pen.tube("M660,-300 Q600,-480 140,-770", 30, "#e53935")
    out += pen.tube("M700,-300 L440,-550", 44, "#fbc02d")
    out += pen.tube("M640,-240 L560,-420", 16, "#9e9e9e")
    out += pen.circle(720, -290, 18, fill="#757575", sw=DW + 0.6)
    out += pen.text(410, -150, "KREN", 40, fill_color=INK, spacing=4)
    out += rear_wheels(pen, (540, 660))
    out += truck_cab(pen, "#e53935", stripe="#fbc02d", light=["#ffb300", "#ffb300"])
    return out, 830


def penggelek_jalan(pen):
    out = pen.tube("M300,-320 L300,-570 M572,-320 L572,-570", 14, "#424242")
    out += pen.rect(270, -598, 330, 32, fill="#fbc02d", rx=10)
    out += pen.rect(410, -630, 50, 28, fill="#ff9800", rx=8, sw=DW + 0.6)
    out += pen.rect(380, -400, 90, 72, fill="#5d4037", rx=10)
    out += pen.tube("M332,-360 L352,-430", 8, "#424242")
    out += pen.ellipse(352, -436, 30, 10, fill="#424242", sw=DW, rot=-15)
    out += pen.path("M240,-110 L240,-302 Q240,-322 260,-322 L560,-322 Q610,-322 610,-276 L610,-110 Z", fill="#fbc02d")
    for x in range(530, 600, 16):
        out += pen.line(x, -300, x, -220, sw=1.8)
    out += pen.circle(140, -124, 124, fill="#9e9e9e")
    out += pen.circle(140, -124, 98, fill="#bdbdbd", sw=DW + 0.6)
    out += pen.circle(140, -124, 30, fill="#757575", sw=DW + 0.6)
    out += pen.path("M6,-124 Q6,-268 140,-270 Q274,-268 274,-124 L250,-124 Q250,-244 140,-246 Q30,-244 30,-124 Z",
                    fill="#fbc02d")
    out += pen.rect(26, -136, 228, 24, fill="#fbc02d", rx=6, sw=DW + 0.6)
    out += wheel_well(pen, 480, 90, 104, yb=-110)
    out += wheel(pen, 480, 90)
    return out, 620


def traktor(pen):
    out = pen.tube("M222,-282 L222,-390", 16, "#424242")
    out += pen.rect(212, -404, 20, 16, fill="#424242", rx=4, sw=DW)
    out += pen.rect(60, -160, 300, 56, fill="#616161", rx=8)
    out += pen.path("M30,-150 L30,-252 Q30,-272 52,-274 L330,-286 L330,-150 Z", fill="#43a047")
    for x in (46, 60, 74):
        out += pen.line(x, -258, x, -164, sw=1.8)
    out += pen.circle(100, -236, 14, fill=LIGHT, sw=DW)
    out += pen.path("M320,-292 L344,-520 L572,-520 L572,-292 Z", fill=GLASS)
    out += pen.line(450, -520, 450, -292, sw=DW + 0.6)
    out += pen.rect(306, -552, 286, 32, fill="#43a047", rx=10)
    out += pen.rect(300, -300, 290, 22, fill="#43a047", rx=6)
    out += pen.tube("M370,-380 L400,-330", 8, "#424242")
    out += pen.rect(470, -380, 60, 60, fill="#5d4037", rx=10, sw=DW + 0.6)
    out += wheel(pen, 100, 74, rim="#fdd835")
    out += wheel(pen, 440, 140, rim="#fdd835")
    for k in range(24):
        a = 2 * math.pi * k / 24
        out += pen.line(440 + 108 * math.cos(a), -140 + 108 * math.sin(a),
                        440 + 136 * math.cos(a + 0.08), -140 + 136 * math.sin(a + 0.08), sw=DW)
    out += pen.path("M272,-140 A168,168 0 0 1 608,-140 L588,-140 A148,148 0 0 0 292,-140 Z", fill="#43a047")
    out += pen.text(180, -190, "LADANG", 32, fill_color="#ffffff")
    return out, 610


# ---------------------------------------------------------------- rail, air, sea

def kereta_api(pen):
    out = ""
    for x0, x1 in ((40, 230), (290, 470), (540, 720), (820, 1000)):
        out += pen.rect(x0, -84, x1 - x0, 30, fill="#424242", rx=6)
        for cx in (x0 + 40, x1 - 40):
            out += wheel(pen, cx, 32, rim="#9e9e9e")
    out += pen.rect(474, -120, 44, 22, fill="#616161", rx=4)
    car = "M512,-90 L512,-326 Q512,-344 530,-344 L1040,-344 L1040,-90 Z"
    out += pen.path(car, fill="#ffffff")
    out += pen.clipped(car, pen.fillrect(500, -200, 560, 26, "#1565c0", sw=DW) +
                       pen.fillrect(500, -130, 560, 40, "#1565c0", sw=DW))
    out += pen.rect(530, -320, 60, 230, fill="none", rx=4, sw=DW + 0.6)
    out += pen.rect(540, -306, 40, 90, fill=GLASS, rx=4, sw=DW)
    for x in range(610, 1040, 96):
        out += pen.rect(x, -306, 76, 84, fill=GLASS, rx=10, sw=DW + 0.6)
    loco = "M40,-90 L8,-140 L12,-252 Q24,-330 124,-348 L478,-348 L478,-90 Z"
    out += pen.rect(200, -370, 240, 24, fill="#9e9e9e", rx=6)
    for x in range(220, 430, 22):
        out += pen.line(x, -366, x, -350, sw=1.6)
    out += pen.path(loco, fill="#1565c0")
    out += pen.clipped(loco, pen.fillrect(0, -204, 490, 30, "#fdd835", sw=DW) +
                       pen.fillrect(0, -130, 490, 40, "#212121", sw=DW))
    out += pen.path("M24,-248 Q38,-312 112,-322 L112,-226 L22,-226 Z", fill=GLASS, w=DW + 0.6)
    out += pen.rect(132, -326, 66, 236, fill="none", rx=4, sw=DW + 0.6)
    out += pen.rect(142, -312, 46, 80, fill=GLASS, rx=4, sw=DW)
    for x in (226, 316, 406):
        out += pen.rect(x, -310, 60, 76, fill=GLASS, rx=8, sw=DW + 0.6)
    out += pen.text(330, -150, "EKSPRES", 34, fill_color="#ffffff", spacing=2)
    out += pen.circle(28, -160, 14, fill=LIGHT, sw=DW + 0.6)
    out += pen.rect(-6, -116, 30, 30, fill="#9e9e9e", rx=6, sw=DW + 0.6)
    return out, 1040


def kapal_terbang(pen):
    out = pen.path("M640,-50 L734,-212 L800,-212 L820,-54 Z", fill="#1565c0")
    out += pen.path(star_d(770, -140, 26, 11), fill="#fdd835", w=DW)
    body = ("M34,-50 C10,-48 -6,-22 -4,6 C-2,34 22,54 72,56 L640,52 Q706,48 766,8 L824,-40 L824,-58 "
            "L720,-58 Z")
    out += pen.path(body, fill="#ffffff")
    out += pen.clipped(body, pen.fillrect(-10, 12, 840, 14, "#1565c0", sw=DW) +
                       pen.fillrect(-10, 26, 840, 40, "#cfd8dc", sw=DW))
    out += pen.path("M18,-26 Q30,-40 58,-40 L64,-20 L20,-14 Z", fill=GLASS, w=DW + 0.6)
    out += pen.rect(104, -36, 26, 56, fill="none", rx=6, sw=DW + 0.6)
    for x in range(160, 630, 28):
        out += pen.circle(x, -14, 7, fill=GLASS, sw=2)
    out += pen.path("M700,4 L796,-4 L846,30 L820,36 Z", fill="#1565c0", w=DW + 0.6)
    out += pen.path("M300,22 L480,24 L640,136 L598,144 Z", fill="#e0e0e0")
    out += pen.rect(330, 48, 150, 58, fill="#bdbdbd", rx=29)
    out += pen.ellipse(336, 77, 10, 26, fill="#616161", sw=DW)
    out += pen.line(400, 24, 404, 48, sw=DW + 0.6)
    return out, 850


def helikopter(pen):
    out = pen.path("M330,-62 L700,-42 L700,-10 L330,42 Z", fill="#e53935")
    out += pen.text(510, -6, "PENYELAMAT", 24, fill_color="#ffffff")
    out += pen.path("M668,-42 L704,-144 L740,-144 L720,0 Z", fill="#e53935")
    out += pen.tube("M716,-140 L716,-24", 10, "#9e9e9e") + pen.tube("M658,-82 L774,-82", 10, "#9e9e9e")
    out += pen.circle(716, -82, 9, fill="#616161", sw=DW)
    body = "M70,-100 Q0,-95 0,-10 Q2,80 90,92 L300,95 Q340,92 345,50 L345,-55 Q342,-100 290,-100 Z"
    out += pen.rect(160, -138, 32, 40, fill="#9e9e9e", rx=4)
    out += pen.path(body, fill="#e53935")
    out += pen.clipped(body, pen.fillrect(-10, 30, 360, 22, "#ffffff", sw=DW))
    out += pen.path("M12,-20 Q14,-84 80,-88 L112,-88 L112,10 L10,10 Z", fill=GLASS, w=DW + 0.6)
    out += pen.rect(128, -90, 110, 170, fill="none", rx=8, sw=DW + 0.6)
    out += pen.rect(140, -78, 86, 68, fill=GLASS, rx=10, sw=DW + 0.6)
    out += pen.rect(256, -78, 70, 60, fill=GLASS, rx=10, sw=DW + 0.6)
    out += pen.tube("M90,92 L80,140 M262,95 L272,140", 10, "#9e9e9e")
    out += pen.tube("M16,140 L330,140 Q352,140 354,124", 12, "#9e9e9e")
    out += pen.rect(-220, -160, 790, 16, fill="#9e9e9e", rx=8)
    out += pen.circle(176, -152, 16, fill="#616161", sw=DW + 0.6)
    return f'<g transform="translate(220,0)">{out}</g>', 1000


def belon_udara(pen):
    env = ("M0,0 C180,0 262,120 252,232 C242,330 124,400 72,462 L-72,462 C-124,400 -242,330 -252,232 "
           "C-262,120 -180,0 0,0 Z")
    xs = [-3, -2, -1, 0, 1, 2, 3]
    colors = ["#e53935", "#fdd835", "#43a047", "#1e88e5", "#fb8c00", "#8e24aa"]

    def gore(k):
        return f"C{k * 78},20 {k * 92},300 {k * 24},462"

    inner = ""
    if pen.colored:
        for i in range(6):
            a, b = xs[i], xs[i + 1]
            inner += (f'<path d="M0,0 {gore(a)} L{b * 24},462 C{b * 92},300 {b * 78},20 0,0 Z" '
                      f'fill="{colors[i]}"/>')
    for k in xs[1:-1]:
        inner += f'<path d="M0,0 {gore(k)}" fill="none" stroke="{INK}" stroke-width="{pen.sw(DW + 0.6)}"/>'
    inner += pen.path("M-262,230 Q0,280 262,230", fill="none", w=DW + 0.6)
    inner += pen.path("M-240,320 Q0,370 240,320", fill="none", w=DW + 0.6)
    out = pen.path(env, fill="#ffffff") + pen.clipped(env, inner) + pen.path(env, fill="none")
    out += pen.path("M-72,462 L-54,500 L54,500 L72,462 Z", fill="#8d6e63")
    out += pen.line(-50, 500, -46, 560, sw=DW + 0.4) + pen.line(50, 500, 46, 560, sw=DW + 0.4)
    out += pen.line(-16, 500, -16, 560, sw=DW) + pen.line(16, 500, 16, 560, sw=DW)
    out += pen.path("M-14,528 Q0,500 14,528 Q0,544 -14,528 Z", fill="#ff9800", w=DW)
    out += pen.rect(-60, 560, 120, 80, fill="#c8a165", rx=8)
    for x in (-30, 0, 30):
        out += pen.line(x, 560, x, 640, sw=1.8)
    out += pen.line(-60, 590, 60, 590, sw=1.8) + pen.line(-60, 615, 60, 615, sw=1.8)
    out += pen.rect(-66, 554, 132, 14, fill="#8d6e63", rx=6, sw=DW + 0.6)
    return out, 0


def kapal(pen):
    out = ""
    for x, y, rx in ((690, -520, 30), (720, -585, 38), (758, -652, 46)):
        out += pen.circle(x, y, rx, fill="#eceff1", sw=DW + 0.6)
    out += pen.path("M600,-300 L620,-470 L704,-470 L704,-290 Z", fill="#e53935")
    out += pen.clipped("M600,-300 L620,-470 L704,-470 L704,-290 Z", pen.fillrect(590, -440, 130, 26, "#fdd835", sw=DW))
    out += pen.line(460, -450, 460, -540, sw=LW)
    out += pen.path("M460,-540 L510,-526 L460,-512 Z", fill="#e53935", w=DW)
    out += pen.rect(214, -300, 470, 124, fill="#ffffff")
    for x in range(240, 670, 50):
        out += pen.rect(x, -270, 30, 26, fill=GLASS, rx=6, sw=DW)
    out += pen.rect(300, -390, 320, 92, fill="#ffffff")
    for x in range(320, 610, 46):
        out += pen.rect(x, -366, 30, 28, fill=GLASS, rx=6, sw=DW)
    out += pen.rect(360, -456, 200, 68, fill="#ffffff")
    out += pen.rect(372, -440, 176, 30, fill=GLASS, rx=6, sw=DW + 0.6)
    out += pen.rect(226, -320, 64, 24, fill="#ff9800", rx=12, sw=DW + 0.6)
    out += pen.rect(636, -320, 44, 24, fill="#ff9800", rx=12, sw=DW + 0.6)
    hull = "M-30,-186 L806,-176 L780,8 L74,8 Z"
    out += pen.path(hull, fill="#1e3f8f")
    out += pen.clipped(hull, pen.fillrect(-40, -46, 860, 60, "#e53935", sw=DW + 0.6) +
                       pen.fillrect(-40, -186, 860, 18, "#ffffff", sw=DW))
    for x in range(160, 760, 62):
        out += pen.circle(x, -112, 13, fill=GLASS, sw=DW + 0.6)
    out += pen.text(110, -62, "SURIA", 34, fill_color="#ffffff", spacing=3)
    # anchor
    out += pen.circle(54, -150, 8, fill="none", sw=DW + 0.6)
    out += pen.line(54, -142, 54, -96, sw=DW + 0.6) + pen.line(42, -128, 66, -128, sw=DW + 0.6)
    out += pen.path("M34,-110 Q38,-90 54,-92 Q70,-90 74,-110", fill="none", w=DW + 0.6)
    for x in range(10, 800, 40):
        out += pen.line(x, -186, x, -210, sw=DW)
    out += pen.line(0, -210, 800, -200, sw=DW)
    return f'<g transform="translate(40,0)">{out}</g>', 860


def kapal_selam(pen):
    out = pen.tube("M300,-240 L300,-330 L250,-330", 12, "#9e9e9e")
    out += pen.rect(232, -344, 22, 28, fill="#9e9e9e", rx=4, sw=DW)
    out += pen.path("M220,-104 L240,-226 Q246,-240 262,-240 L382,-240 Q396,-240 398,-226 L410,-104 Z",
                    fill="#ffca28")
    out += pen.rect(268, -210, 34, 26, fill=GLASS, rx=6, sw=DW)
    out += pen.rect(318, -210, 34, 26, fill=GLASS, rx=6, sw=DW)
    out += pen.path("M396,-180 L450,-168 L446,-156 L398,-160 Z", fill="#fb8c00", w=DW + 0.6)
    out += pen.path("M680,-96 L800,-40 L800,40 L680,96 Z", fill="#ffca28")
    out += pen.path("M760,-60 L790,-150 L820,-150 L808,-40 Z", fill="#fb8c00")
    out += pen.path("M760,60 L790,150 L820,150 L808,40 Z", fill="#fb8c00")
    out += pen.ellipse(830, -30, 14, 34, fill="#9e9e9e", sw=DW + 0.6)
    out += pen.ellipse(830, 30, 14, 34, fill="#9e9e9e", sw=DW + 0.6)
    out += pen.circle(818, 0, 12, fill="#616161", sw=DW)
    hull = "M110,-112 L630,-112 Q720,-112 720,0 Q720,112 630,112 L110,112 Q0,112 0,0 Q0,-112 110,-112 Z"
    out += pen.path(hull, fill="#ffca28")
    out += pen.clipped(hull, pen.fillrect(-10, 50, 740, 20, "#fb8c00", sw=DW))
    for x in range(120, 620, 110):
        out += pen.circle(x, -12, 30, fill="#9e9e9e", sw=LW)
        out += pen.circle(x, -12, 20, fill=GLASS, sw=DW)
    out += pen.circle(26, 0, 10, fill=LIGHT, sw=DW)
    out += pen.path("M60,90 L10,130 L60,126 Z", fill="#fb8c00", w=DW + 0.6)
    return out, 860


def jentera_bomba(pen):
    r, R, yb = 64, 78, -44
    cab = (f"M18,{yb} " + arch(150, r, R, yb) +
           f"L244,{yb} L244,-386 L42,-386 Q18,-386 15,-362 L6,-232 L4,-76 Q4,{yb} 18,{yb} Z")
    body = (f"M240,{yb} " + arch(650, r, R, yb) +
            f"L780,{yb} Q795,{yb} 795,-62 L795,-312 L240,-312 Z")
    out = pen.rect(300, -374, 14, 64, fill="#9e9e9e", sw=DW)
    out += pen.rect(744, -374, 14, 64, fill="#9e9e9e", sw=DW)
    out += pen.rect(150, -406, 650, 34, fill="#cfd8dc", rx=4)
    for x in range(178, 800, 30):
        out += pen.line(x, -406, x, -372, sw=DW)
    out += lightbar(pen, 44, -414, 160, ["#1e63c9", "#e53935", "#1e63c9"])
    out += pen.path(body, fill="#e53935")
    out += pen.clipped(body, pen.fillrect(230, -152, 580, 24, "#ffd54f", sw=DW + 0.6))
    for x0, x1 in ((256, 420), (436, 600), (616, 782)):
        out += pen.rect(x0, -296, x1 - x0, 132, fill="#cfd8dc", rx=6, sw=DW + 0.6)
        for y in range(-276, -180, 18):
            out += pen.line(x0 + 8, y, x1 - 8, y, sw=1.8)
        out += pen.rect((x0 + x1) / 2 - 22, -182, 44, 9, fill="#888", rx=4, sw=DW)
    out += pen.text(408, -64, "BOMBA", 54, fill_color="#ffffff", spacing=3)
    out += pen.path(cab, fill="#e53935")
    out += pen.clipped(cab, pen.fillrect(-10, -152, 260, 24, "#ffd54f", sw=DW + 0.6))
    out += pen.path("M22,-366 L106,-366 L106,-250 L14,-250 Z", fill=GLASS, w=DW + 0.6)
    out += pen.line(58, -354, 36, -270, sw=2) + pen.line(80, -354, 60, -274, sw=2)
    out += pen.rect(116, -376, 118, 222, fill="none", rx=6, sw=DW + 0.6)
    out += pen.rect(126, -366, 98, 112, fill=GLASS, rx=6, sw=DW + 0.6)
    out += pen.rect(198, -230, 24, 9, fill="#ccc", rx=4, sw=DW)
    out += pen.text(175, -176, "994", 30, fill_color="#ffffff")
    out += pen.rect(6, -146, 34, 26, fill=LIGHT, rx=7, sw=DW + 0.6)
    out += pen.rect(-6, -92, 56, 46, fill=BUMPER, rx=10)
    out += pen.rect(780, -88, 26, 42, fill=BUMPER, rx=8)
    out += pen.rect(784, -240, 12, 40, fill="#ffb300", rx=4, sw=DW)
    out += mirror(pen, 14, -320)
    out += wheel(pen, 150, r) + wheel(pen, 650, r)
    return out, 800
