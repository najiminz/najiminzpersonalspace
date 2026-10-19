"""The recurring cast of Siri Budaya Malaysia.

All children share one body, one face and one line style so they look like the
same family of characters on every page. Only hair/headwear, skin tone and
outfit change.

kid(pen, who, x, y, s, la, ra, outfit, sit) draws a child standing (or sitting)
with feet at page point (x, y). la / ra are the left / right hand positions in
the child's own coordinates (feet at 0,0, up is negative y, unscaled).
"""
from draw import DW, INK, LW, blob_d

CAST = {
    "amir": dict(skin="#f2c39b", hair="amir", outfit="tshirt", top="#42a5f5", bottom="#1e3f8f"),
    "aisyah": dict(skin="#ffd8b8", hair="tudung", outfit="kurung", top="#f48fb1", bottom="#f06292",
                   tudung="#ce93d8"),
    "mei": dict(skin="#ffe1c4", hair="mei", outfit="samfu", top="#e53935", bottom="#212121"),
    "ravi": dict(skin="#c98a5e", hair="ravi", outfit="kurta", top="#ffb300", bottom="#fff8e1"),
    "lina": dict(skin="#f0c39a", hair="lina", outfit="kaamatan", top="#212121", bottom="#212121"),
}

SIT = 92  # how far the upper body drops when sitting


def solid(d, color=INK):
    return f'<path d="{d}" fill="{color}"/>'


def face(pen, look, cx=0, cy=-262, gap=24, small=False):
    out = ""
    for ex in (-gap, gap):
        out += f'<ellipse cx="{cx + ex}" cy="{cy}" rx="{8.5 if small else 9.5}" ry="{11.5 if small else 12.5}" fill="{INK}"/>'
        out += f'<circle cx="{cx + ex + 3}" cy="{cy - 5}" r="3.6" fill="#fff"/>'
        out += pen.path(f"M{cx + ex - 11},{cy - 25} Q{cx + ex},{cy - 32} {cx + ex + 11},{cy - 25}", fill="none", w=DW)
        if pen.colored:
            out += f'<circle cx="{cx + ex * 1.62}" cy="{cy + 22}" r="10" fill="#ff9e9e" opacity="0.7"/>'
    out += pen.path(f"M{cx - 4},{cy + 12} Q{cx},{cy + 16} {cx + 4},{cy + 12}", fill="none", w=DW - 0.4)
    out += pen.path(f"M{cx - 17},{cy + 26} Q{cx},{cy + 46} {cx + 17},{cy + 26} Q{cx},{cy + 32} {cx - 17},{cy + 26} Z",
                    fill="#e57373", w=DW)
    return out


def legs(pen, look, outfit, sit):
    if sit:
        lap = "M-86,-8 Q-96,-60 -48,-70 L48,-70 Q96,-60 86,-8 Q0,8 -86,-8 Z"
        color = look["top"] if outfit == "kurung" else look["bottom"]
        out = pen.path(lap, fill=color)
        out += pen.path("M-30,-40 Q0,-22 30,-40", fill="none", w=DW)
        out += pen.ellipse(-58, -16, 24, 12, fill="#5d4037", sw=DW + 0.6)
        out += pen.ellipse(58, -16, 24, 12, fill="#5d4037", sw=DW + 0.6)
        return out
    out = ""
    if outfit in ("tshirt",):
        for x in (-38, 6):
            out += pen.rect(x, -76, 32, 66, fill=look["skin"], rx=6)
    elif outfit not in ("kurung", "kaamatan"):
        for x in (-40, 4):
            out += pen.rect(x, -116, 36, 106, fill=look["bottom"], rx=6)
    for x in (-24, 24):
        out += pen.ellipse(x, -9, 27, 13, fill="#5d4037", sw=LW)
    return out


def torso(pen, look, outfit):
    top, bottom = look["top"], look["bottom"]
    out = ""
    if outfit == "tshirt":
        out += pen.path("M-50,-114 L50,-114 L46,-66 L6,-66 L0,-88 L-6,-66 L-46,-66 Z", fill=bottom)
        out += pen.path("M-44,-202 Q-58,-196 -56,-150 L-52,-108 L52,-108 L56,-150 Q58,-196 44,-202 Z", fill=top)
        out += pen.path("M-16,-202 Q0,-188 16,-202", fill="none", w=DW)
    elif outfit in ("bajumelayu", "silat"):
        out += pen.path("M-46,-202 Q-60,-196 -58,-150 L-56,-100 L56,-100 L58,-150 Q60,-196 46,-202 Z", fill=top)
        out += pen.rect(-12, -206, 24, 14, fill=top, rx=3, sw=DW)
        out += pen.line(0, -192, 0, -140, sw=DW)
        for y in (-180, -164, -148):
            out += pen.circle(0, y, 3.4, fill="#fdd835", sw=1.6)
        samp = "M-60,-128 L60,-128 L66,-58 L-66,-58 Z"
        sc = "#fdd835" if outfit == "bajumelayu" else "#c62828"
        out += pen.path(samp, fill=sc)
        out += pen.clipped(samp, "".join(pen.path(f"M{x},-128 L{x + 40},-58", fill="none", w=1.6)
                                         for x in range(-100, 80, 20)))
        out += pen.path(samp, fill="none")
        out += pen.rect(-62, -134, 124, 12, fill=sc, rx=4, sw=DW)
    elif outfit == "kurung":
        out += pen.path("M-58,-112 L58,-112 L70,-16 L-70,-16 Z", fill=bottom)
        for x, y in ((-40, -40), (-6, -70), (30, -36), (44, -84), (-30, -92), (6, -30)):
            out += pen.circle(x, y, 6, fill="#ffffff", sw=1.6)
        out += pen.path("M-46,-202 Q-62,-192 -62,-150 L-70,-74 L70,-74 L62,-150 Q62,-192 46,-202 Z", fill=top)
        for x, y in ((-34, -120), (30, -150), (-20, -96), (36, -100)):
            out += pen.circle(x, y, 7, fill="#fff59d", sw=1.6)
    elif outfit == "samfu":
        out += pen.path("M-46,-202 Q-60,-196 -58,-150 L-56,-100 L56,-100 L58,-150 Q60,-196 46,-202 Z", fill=top)
        out += pen.rect(-16, -210, 32, 14, fill=top, rx=4, sw=DW)
        out += pen.path("M-4,-196 Q20,-180 44,-176", fill="none", w=DW)
        for x, y in ((10, -189), (26, -181)):
            out += pen.path(f"M{x - 8},{y} L{x + 8},{y}", fill="none", w=LW)
        out += pen.path("M-56,-108 L56,-108", fill="none", w=DW)
    elif outfit == "kurta":
        out += pen.path("M-46,-202 Q-60,-196 -58,-150 L-60,-62 L60,-62 L58,-150 Q60,-196 46,-202 Z", fill=top)
        out += pen.rect(-8, -204, 16, 64, fill="#fff8e1", rx=3, sw=DW)
        for y in (-190, -172, -154):
            out += pen.circle(0, y, 3, fill="#8d6e63", sw=1.4)
        out += pen.path("M-60,-80 L-40,-80 M40,-80 L60,-80", fill="none", w=DW)
        out += pen.path("M-58,-74 L58,-74", fill="none", w=DW)
    elif outfit == "kaamatan":
        out += pen.path("M-60,-112 L60,-112 L68,-16 L-68,-16 Z", fill=bottom)
        for y in (-80, -50):
            out += pen.rect(-66, y, 132, 12, fill="#fdd835", sw=DW)
        out += pen.path("M-46,-202 Q-60,-196 -58,-150 L-56,-106 L56,-106 L58,-150 Q60,-196 46,-202 Z", fill=top)
        out += pen.path("M-30,-202 L-2,-150 L30,-202", fill="none", w=DW)
        out += pen.path("M-50,-196 L50,-118 L44,-108 L-56,-184 Z", fill="#e53935", w=DW)
        out += pen.rect(-62, -118, 124, 16, fill="#bdbdbd", rx=4, sw=DW)
        for x in range(-52, 60, 16):
            out += pen.circle(x, -110, 5, fill="#eeeeee", sw=1.4)
    return out


def hand(pen, look, pos):
    return pen.circle(pos[0], pos[1], 15, fill=look["skin"], sw=LW)


def arm(pen, look, outfit, side, hand):
    sx = -46 if side < 0 else 46
    hx, hy = hand
    sleeve = look["top"]
    out = ""
    if outfit == "tshirt":
        mx, my = sx + (hx - sx) * 0.32, -190 + (hy + 190) * 0.32
        out += pen.tube(f"M{sx},-190 L{hx},{hy}", 22, look["skin"])
        out += pen.tube(f"M{sx},-190 L{mx:.1f},{my:.1f}", 30, sleeve)
    else:
        out += pen.tube(f"M{sx},-190 L{hx},{hy}", 26, sleeve)
    return out


def hair_back(pen, look):
    h = look["hair"]
    if h == "ravi":
        return pen.path(blob_d(0, -300, 74, 52, 13, 21), fill="#3e2723")
    if h == "mei":
        out = pen.circle(-48, -334, 22, fill="#212121") + pen.circle(48, -334, 22, fill="#212121")
        return out + pen.path("M-72,-262 Q-76,-350 0,-348 Q76,-350 72,-262 Q74,-226 56,-212 L-56,-212 "
                              "Q-74,-226 -72,-262 Z", fill="#212121")
    if h == "lina":
        return pen.circle(0, -344, 32, fill="#212121")
    if h == "tudung":
        return pen.path("M-82,-256 Q-86,-352 0,-354 Q86,-352 82,-256 L96,-150 Q0,-128 -96,-150 Z",
                        fill=look["tudung"])
    return ""


def hair_front(pen, look):
    h = look["hair"]
    if h == "amir":
        return pen.path("M-66,-262 Q-72,-342 0,-340 Q72,-342 66,-262 Q60,-300 32,-302 L20,-288 L6,-304 L-8,-288 "
                        "L-24,-304 L-40,-290 Q-60,-294 -66,-262 Z", fill="#4e342e")
    if h == "ravi":
        out = ""
        for x in (-40, -14, 12, 38):
            out += pen.path(f"M{x - 14},-300 Q{x},-322 {x + 14},-300 Q{x},-306 {x - 14},-300 Z", fill="#3e2723", w=DW)
        return out
    if h in ("mei", "lina"):
        out = pen.path("M-64,-270 Q-66,-338 0,-338 Q66,-338 64,-270 L44,-296 L-44,-296 Z" if h == "mei" else
                       "M-66,-258 Q-70,-342 0,-340 Q70,-342 66,-258 Q60,-300 0,-306 Q-60,-300 -66,-258 Z",
                       fill="#212121")
        if h == "lina":
            out += pen.line(0, -338, 0, -308, sw=DW)
        if h == "lina":
            out += pen.path("M-64,-292 Q0,-322 64,-292 L64,-280 Q0,-310 -64,-280 Z", fill="#e53935", w=DW)
            for k in range(-3, 4):
                out += pen.circle(k * 17, -300 + abs(k) * 2.5, 4, fill="#fdd835", sw=1.4)
            for k in range(4):
                out += pen.circle(26 + 9 * k, -356 + 4 * k, 7, fill="#fdd835", sw=1.6)
        return out
    if h == "tudung":
        return pen.path("M-62,-250 Q-64,-336 0,-338 Q64,-336 62,-250 Q54,-312 0,-314 Q-54,-312 -62,-250 Z",
                        fill=look["tudung"])
    return ""


def hat(pen, kind):
    if kind == "songkok":
        return pen.path("M-50,-318 L-46,-356 Q0,-366 46,-356 L50,-318 Q0,-326 -50,-318 Z", fill="#212121")
    if kind == "tanjak":
        out = pen.path("M-66,-300 Q-60,-344 -10,-350 L30,-404 L40,-350 Q66,-338 66,-300 Q0,-316 -66,-300 Z",
                       fill="#c62828")
        return out + pen.path("M-50,-318 Q0,-336 50,-318 M20,-350 L30,-396", fill="none", w=DW)
    return ""


def kid(pen, who, x, y, s=1.0, la=(-64, -112), ra=(64, -112), outfit=None, sit=False, headwear=None,
        arms_front=False, hands=True):
    look = dict(CAST[who])
    outfit = outfit or look["outfit"]
    if outfit in ("bajumelayu", "silat"):
        look["top"] = {"bajumelayu": "#26a69a", "silat": "#212121"}[outfit]
        look["bottom"] = look["top"]
    k0 = pen.k
    pen.k = k0 / s
    up = f'<g transform="translate(0,{SIT})">' if sit else "<g>"
    body = legs(pen, look, outfit, sit)
    arms = arm(pen, look, outfit, -1, la) + arm(pen, look, outfit, 1, ra)
    upper = "" if arms_front else arms
    upper += torso(pen, look, outfit) if not (sit and outfit in ("kurung", "kaamatan")) else _sit_top(pen, look, outfit)
    upper += hair_back(pen, look)
    if look["hair"] == "tudung":
        upper += pen.ellipse(0, -258, 52, 58, fill=look["skin"])
        upper += face(pen, look, cy=-256, gap=20, small=True)
    else:
        if look["hair"] != "mei":
            upper += pen.circle(-64, -258, 13, fill=look["skin"], sw=DW + 0.6)
            upper += pen.circle(64, -258, 13, fill=look["skin"], sw=DW + 0.6)
        upper += pen.circle(0, -262, 64, fill=look["skin"])
        upper += face(pen, look)
    upper += hair_front(pen, look)
    upper += hat(pen, headwear or {"bajumelayu": "songkok", "silat": "tanjak"}.get(outfit))
    upper += (arms if arms_front else "")
    if hands:
        upper += hand(pen, look, la) + hand(pen, look, ra)
    out = f'<g transform="translate({x},{y}) scale({s})">{body}{up}{upper}</g></g>' 
    pen.k = k0
    return out


def kid_hands(pen, who, x, y, s=1.0, la=(-64, -112), ra=(64, -112), sit=False):
    """Just the hands, for drawing on top of something the child is holding."""
    look = CAST[who]
    k0 = pen.k
    pen.k = k0 / s
    out = (f'<g transform="translate({x},{y}) scale({s})"><g transform="translate(0,{SIT if sit else 0})">'
           f'{hand(pen, look, la)}{hand(pen, look, ra)}</g></g>')
    pen.k = k0
    return out


def _sit_top(pen, look, outfit):
    # a sitting girl in a long dress: just the blouse, the skirt becomes the lap
    out = pen.path("M-46,-202 Q-62,-192 -62,-150 L-66,-100 L66,-100 L62,-150 Q62,-192 46,-202 Z", fill=look["top"])
    if outfit == "kurung":
        for x, y in ((-34, -150), (30, -130)):
            out += pen.circle(x, y, 7, fill="#fff59d", sw=1.6)
    return out


def hand_at(x, y, s, local, sit=False):
    """Page position of a hand given in the child's local coordinates."""
    lx, ly = local
    return x + lx * s, y + (ly + (SIT if sit else 0)) * s
