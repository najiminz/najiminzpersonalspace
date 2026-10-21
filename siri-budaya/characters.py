"""The recurring cast of Siri Budaya Malaysia.

All children share one body, one face and one line style so they look like the
same family of characters on every page. Only hair/headwear, skin tone and
outfit change.

kid(pen, who, x, y, s, la, ra, outfit, sit) draws a child standing (or sitting)
with feet at page point (x, y). la / ra are the left / right hand positions in
the child's own coordinates (feet at 0,0, up is negative y, unscaled).
"""
import math

from draw import DW, INK, LW, blob_d

CAST = {
    "amir": dict(skin="#f2c39b", hair="amir", outfit="tshirt", top="#42a5f5", bottom="#1e3f8f"),
    "aisyah": dict(skin="#ffd8b8", lashes=True, hair="tudung", outfit="kurung", top="#f48fb1", bottom="#f06292",
                   tudung="#ce93d8"),
    "mei": dict(skin="#ffe1c4", lashes=True, hair="mei", outfit="samfu", top="#e53935", bottom="#212121"),
    "ravi": dict(skin="#c98a5e", hair="ravi", outfit="kurta", top="#ffb300", bottom="#fff8e1"),
    "lina": dict(skin="#f0c39a", lashes=True, hair="lina", outfit="kaamatan", top="#212121", bottom="#212121"),
}

SIT = 92  # how far the upper body drops when sitting


def solid(d, color=INK):
    return f'<path d="{d}" fill="{color}"/>'


def motif(pen, x, y, r, color):
    """Tiny five-petal flower used as a fabric print."""
    out = ""
    for k in range(5):
        a = math.radians(-90 + 72 * k)
        out += pen.circle(x + r * 0.85 * math.cos(a), y + r * 0.85 * math.sin(a), r * 0.55, fill=color, sw=1.4)
    return out + pen.circle(x, y, r * 0.38, fill="#fdd835", sw=1.2)


def zigzag(pen, x0, x1, y, h=6, step=12):
    d = f"M{x0},{y}" + "".join(f" L{x + step / 2:.1f},{y - h if i % 2 == 0 else y + h} L{x + step:.1f},{y}"
                               for i, x in enumerate(range(int(x0), int(x1) - step + 1, step)))
    return pen.path(d, fill="none", w=1.6)


def face(pen, look, cx=0, cy=-262, gap=24, small=False):
    out = ""
    if look.get("lashes"):
        for ex in (-gap, gap):
            sgn = 1 if ex > 0 else -1
            out += pen.path(f"M{cx + ex + sgn * 8},{cy - 8} L{cx + ex + sgn * 15},{cy - 14}", fill="none", w=DW - 0.4)
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
    elif outfit not in ("kurung", "kaamatan", "jururawat"):
        for x in (-40, 4):
            out += pen.rect(x, -116, 36, 106, fill=look["bottom"], rx=6)
    if outfit not in ("tshirt", "kurung", "kaamatan", "jururawat"):
        for x in (-22, 22):
            out += pen.line(x - 14, -34, x + 14, -34, sw=1.8)
    if outfit == "angkasawan":
        for x in (-22, 22):
            out += pen.rect(x - 22, -46, 44, 30, fill="#b0bec5", rx=6, sw=DW + 0.6)
            out += pen.line(x - 22, -60, x + 22, -60, sw=1.8)
    for x in (-24, 24):
        out += pen.ellipse(x, -9, 27, 13, fill="#5d4037" if outfit != "angkasawan" else "#78909c", sw=LW)
        out += pen.path(f"M{x - 24},-4 Q{x},6 {x + 24},-4", fill="none", w=1.8)
        out += pen.circle(x + (8 if x > 0 else -8), -14, 2.6, fill="#ffffff", sw=1.2)
    return out


def suit(pen, look):
    out = pen.path("M-52,-206 Q-66,-196 -64,-150 L-60,-96 L60,-96 L64,-150 Q66,-196 52,-206 Z", fill="#eceff1")
    out += pen.rect(-30, -154, 60, 34, fill="#90a4ae", rx=7, sw=DW)
    for i, c in enumerate(("#e53935", "#fdd835", "#43a047")):
        out += pen.circle(-16 + i * 16, -143, 5, fill=c, sw=1.4)
    out += pen.rect(-18, -131, 36, 7, fill="#42a5f5", rx=3, sw=1.2)
    out += pen.rect(-64, -114, 128, 16, fill="#ff7043", rx=5, sw=DW)
    out += pen.rect(-12, -116, 24, 20, fill="#cfd8dc", rx=4, sw=1.6)
    # flag patch on the arm side of the chest
    out += pen.rect(38, -154, 20, 13, fill="#ffffff", sw=1.4)
    out += pen.rect(38, -154, 9, 7, fill="#1a237e", sw=1.0)
    return out + pen.path("M-60,-140 L-44,-140 M44,-140 L60,-140", fill="none", w=1.6)


def helmet(pen):
    glass = 'fill="#e3f2fd" fill-opacity="0.22"' if pen.colored else 'fill="none"'
    out = f'<circle cx="0" cy="{HELMET[1]}" r="{HELMET[2]}" {glass} stroke="{INK}" stroke-width="{pen.sw(LW)}"/>'
    out += pen.path("M-68,-330 Q-48,-358 -16,-366", fill="none", w=DW + 1)
    out += pen.path("M-56,-312 Q-48,-324 -36,-330", fill="none", w=DW)
    return out + pen.rect(-70, -178, 140, 22, fill="#b0bec5", rx=11, sw=DW + 0.6)


HELMET = (0, -272, 100)


def in_helmet(pen, svg):
    cx, cy, r = HELMET
    return pen.clipped(f"M{cx - r + 3},{cy} A{r - 3},{r - 3} 0 1 0 {cx + r - 3},{cy} A{r - 3},{r - 3} 0 1 0 "
                       f"{cx - r + 3},{cy} Z", svg)


def backpack(pen):
    out = pen.rect(-78, -232, 156, 130, fill="#cfd8dc", rx=16, sw=DW + 0.6)
    return out + pen.tube("M-60,-232 Q-90,-270 -70,-300", 10, "#90a4ae")


SHIRT = "M-48,-204 Q-62,-196 -60,-150 L-58,-98 L58,-98 L60,-150 Q62,-196 48,-204 Z"
COAT_L = "M-50,-204 Q-66,-196 -64,-150 L-68,-52 L-8,-52 L-8,-150 L-22,-204 Z"


def shirt(pen, top, buttons=True, pockets=True, belt="#5d4037"):
    """Collared long-sleeve shirt tucked into trousers, with a belt."""
    out = pen.path(SHIRT, fill=top)
    out += pen.path("M-22,-206 L0,-180 L22,-206 L14,-212 L0,-196 L-14,-212 Z", fill=top, w=DW)
    if buttons:
        out += pen.line(0, -180, 0, -104, sw=1.6)
        for y in (-166, -146, -126):
            out += pen.circle(0, y, 3, fill="#ffffff", sw=1.2)
    if pockets:
        for x in (-40, 16):
            out += pen.rect(x, -172, 24, 22, fill=top, rx=3, sw=1.6) + pen.line(x, -164, x + 24, -164, sw=1.4)
    if belt:
        out += pen.rect(-60, -108, 120, 12, fill=belt, rx=3, sw=DW) + pen.rect(-9, -110, 18, 16, fill="#fdd835", rx=3, sw=1.4)
    return out


def job_torso(pen, look, outfit):
    top = look["top"]
    if outfit == "seragam":
        return shirt(pen, top)
    if outfit == "askar":
        out = shirt(pen, top)
        inner = "".join(pen.path(blob_d(x, y, 13, 9, 7, x * 7 + y), fill="#33691e", w=1.4)
                        for x, y in ((-36, -186), (24, -190), (-20, -140), (34, -132), (-44, -118), (6, -160)))
        return out + pen.clipped(SHIRT, inner) + pen.path(SHIRT, fill="none")
    if outfit == "kot":
        out = shirt(pen, look.get("shirt", "#bbdefb"), pockets=False, belt=None)
        for side in (1, -1):
            out += f'<g transform="scale({side},1)">' + pen.path(COAT_L, fill="#ffffff")
            out += pen.path("M-22,-204 L-8,-150 L-30,-170 Z", fill="#ffffff", w=1.6)
            out += pen.rect(-56, -110, 30, 24, fill="#ffffff", rx=3, sw=1.6) + "</g>"
        out += pen.line(-44, -112, -44, -132, sw=2.4) + pen.circle(-44, -134, 3, fill="#1e88e5", sw=1.2)
        return out
    if outfit == "chef":
        out = pen.path("M-50,-204 Q-66,-196 -64,-150 L-62,-96 L62,-96 L64,-150 Q66,-196 50,-204 Z", fill="#ffffff")
        out += pen.path("M-30,-204 L30,-204 L30,-96 L-10,-96 Z", fill="none", w=1.6)
        for y in (-176, -150, -124):
            for x in (-12, 16):
                out += pen.circle(x, y, 3.4, fill="#ffffff", sw=1.4)
        out += pen.path("M-26,-206 Q0,-186 26,-206 L14,-180 L0,-170 L-14,-180 Z", fill="#e53935", w=DW)
        return out
    if outfit == "rompi":
        out = shirt(pen, top, pockets=False)
        vest = "M-50,-204 Q-64,-196 -62,-150 L-60,-100 L-10,-100 L-12,-200 Z M50,-204 Q64,-196 62,-150 L60,-100 L10,-100 L12,-200 Z"
        out += pen.path(vest, fill="#ff9800")
        for y in (-170, -128):
            out += pen.rect(-60, y, 48, 10, fill="#e0e0e0", sw=1.4) + pen.rect(12, y, 48, 10, fill="#e0e0e0", sw=1.4)
        return out
    if outfit == "bomba":
        out = shirt(pen, top, buttons=False, pockets=False, belt="#424242")
        out += pen.path("M-4,-200 L-4,-108", fill="none", w=DW)
        for y in (-168, -134):
            out += pen.rect(-60, y, 120, 12, fill="#fdd835", sw=1.6)
        return out
    if outfit == "jururawat":
        out = pen.path("M-58,-112 L58,-112 L70,-16 L-70,-16 Z", fill="#ffffff")
        out += pen.path("M-48,-204 Q-62,-196 -62,-150 L-64,-104 L64,-104 L62,-150 Q62,-196 48,-204 Z", fill="#ffffff")
        out += pen.rect(-60, -112, 120, 10, fill="#90caf9", rx=3, sw=1.6)
        out += pen.path("M-6,-168 h12 v-12 h10 v12 h12 v10 h-12 v12 h-10 v-12 h-12 Z", fill="#e53935", w=1.4)
        return out
    return None


def torso(pen, look, outfit):
    top, bottom = look["top"], look["bottom"]
    out = ""
    if outfit == "angkasawan":
        return suit(pen, look)
    job = job_torso(pen, look, outfit)
    if job is not None:
        return job
    if outfit == "tshirt":
        out += pen.path("M-50,-114 L50,-114 L46,-66 L6,-66 L0,-88 L-6,-66 L-46,-66 Z", fill=bottom)
        out += pen.path("M-44,-202 Q-58,-196 -56,-150 L-52,-108 L52,-108 L56,-150 Q58,-196 44,-202 Z", fill=top)
        out += pen.path("M-16,-202 Q0,-188 16,-202 M-20,-200 Q0,-180 20,-200", fill="none", w=DW)
        out += pen.rect(-40, -176, 26, 24, fill="#ffffff", rx=4, sw=1.8)
        out += pen.path("M-40,-168 L-14,-168", fill="none", w=1.4)
        out += pen.path("M20,-170 l5,10 11,1 -8,7 2,11 -10,-6 -10,6 2,-11 -8,-7 11,-1 Z", fill="#fdd835", w=1.6)
        out += pen.path("M-44,-122 L-38,-122 M38,-122 L44,-122 M-46,-74 L-8,-74 M8,-74 L46,-74", fill="none", w=1.6)
    elif outfit in ("bajumelayu", "silat"):
        out += pen.path("M-46,-202 Q-60,-196 -58,-150 L-56,-100 L56,-100 L58,-150 Q60,-196 46,-202 Z", fill=top)
        out += pen.rect(-12, -206, 24, 14, fill=top, rx=3, sw=DW)
        out += pen.line(0, -192, 0, -140, sw=DW)
        for y in (-180, -164, -148):
            out += pen.circle(0, y, 3.4, fill="#fdd835", sw=1.6)
        out += pen.rect(-42, -172, 24, 18, fill=look["top"], rx=2, sw=1.8)
        samp = "M-60,-128 L60,-128 L66,-58 L-66,-58 Z"
        sc = "#fdd835" if outfit == "bajumelayu" else "#c62828"
        out += pen.path(samp, fill=sc)
        pattern = pen.line(-80, -76, 80, -76, sw=1.6) + zigzag(pen, -78, 80, -68, 5, 10)
        for x in range(-56, 70, 28):
            pattern += pen.path(f"M{x},-118 l10,12 -10,12 -10,-12 Z", fill="#e53935" if outfit == "bajumelayu"
                                else "#fdd835", w=1.4)
        out += pen.clipped(samp, pattern)
        out += pen.path(samp, fill="none")
        out += pen.rect(-62, -134, 124, 12, fill=sc, rx=4, sw=DW)
    elif outfit == "kurung":
        out += pen.path("M-58,-112 L58,-112 L70,-16 L-70,-16 Z", fill=bottom)
        for x, y in ((-40, -40), (-4, -60), (34, -36), (40, -60), (-26, -64)):
            out += motif(pen, x, y, 8, "#ffffff")
        out += pen.rect(-70, -34, 140, 12, fill="#fdd835", sw=1.6)
        out += pen.path("M-46,-202 Q-62,-192 -62,-150 L-70,-74 L70,-74 L62,-150 Q62,-192 46,-202 Z", fill=top)
        for x, y in ((-34, -128), (32, -150), (-18, -98), (38, -104)):
            out += motif(pen, x, y, 9, "#fff59d")
        out += pen.path("M-66,-86 L66,-86", fill="none", w=1.6)
    elif outfit == "samfu":
        out += pen.path("M-46,-202 Q-60,-196 -58,-150 L-56,-100 L56,-100 L58,-150 Q60,-196 46,-202 Z", fill=top)
        out += pen.rect(-16, -210, 32, 14, fill=top, rx=4, sw=DW)
        out += pen.path("M-4,-196 Q20,-180 44,-176", fill="none", w=DW)
        for x, y in ((10, -189), (26, -181)):
            out += pen.path(f"M{x - 8},{y} L{x + 8},{y}", fill="none", w=LW)
        out += pen.path("M-56,-108 L56,-108 M-56,-116 L56,-116", fill="none", w=1.8)
        for x, y in ((-30, -160), (30, -136), (-20, -128)):
            out += motif(pen, x, y, 8, "#ffcdd2")
    elif outfit == "kurta":
        out += pen.path("M-46,-202 Q-60,-196 -58,-150 L-60,-62 L60,-62 L58,-150 Q60,-196 46,-202 Z", fill=top)
        out += pen.rect(-8, -204, 16, 64, fill="#fff8e1", rx=3, sw=DW)
        for y in (-190, -172, -154):
            out += pen.circle(0, y, 3, fill="#8d6e63", sw=1.4)
        out += pen.path("M-60,-80 L-40,-80 M40,-80 L60,-80", fill="none", w=DW)
        out += pen.path("M-58,-74 L58,-74 M-59,-90 L59,-90", fill="none", w=1.8)
        out += zigzag(pen, -56, 58, -82, 4, 10)
        out += pen.path("M-22,-200 Q0,-186 22,-200", fill="none", w=1.6)
    elif outfit == "kaamatan":
        out += pen.path("M-60,-112 L60,-112 L68,-16 L-68,-16 Z", fill=bottom)
        for y in (-80, -50):
            out += pen.rect(-66, y, 132, 12, fill="#fdd835", sw=DW)
            out += zigzag(pen, -62, 64, y + 6, 4, 10)
        out += pen.path("M-46,-202 Q-60,-196 -58,-150 L-56,-106 L56,-106 L58,-150 Q60,-196 46,-202 Z", fill=top)
        out += pen.path("M-30,-202 L-2,-150 L30,-202", fill="none", w=DW)
        out += pen.path("M-50,-196 L50,-118 L44,-108 L-56,-184 Z", fill="#e53935", w=DW)
        out += pen.rect(-62, -118, 124, 16, fill="#bdbdbd", rx=4, sw=DW)
        for x in range(-52, 60, 16):
            out += pen.circle(x, -110, 5, fill="#eeeeee", sw=1.4)
    return out


def hand(pen, look, pos):
    side = 1 if pos[0] > 0 else -1
    skin = look.get("glove", look["skin"])
    out = pen.ellipse(pos[0] - side * 12, pos[1] - 8, 7, 9, fill=skin, sw=DW, rot=side * 30)
    out += pen.circle(pos[0], pos[1], 15 if "glove" not in look else 18, fill=skin, sw=LW)
    return out + pen.path(f"M{pos[0] - 5},{pos[1] + 6} L{pos[0] - 5},{pos[1] + 12} M{pos[0] + 3},{pos[1] + 7} "
                          f"L{pos[0] + 3},{pos[1] + 13}", fill="none", w=1.4)


def arm(pen, look, outfit, side, hand):
    sx = -46 if side < 0 else 46
    hx, hy = hand
    sleeve = {"kot": "#ffffff", "chef": "#ffffff", "jururawat": "#ffffff"}.get(outfit, look["top"])
    out = ""
    if outfit == "tshirt":
        mx, my = sx + (hx - sx) * 0.32, -190 + (hy + 190) * 0.32
        out += pen.tube(f"M{sx},-190 L{hx},{hy}", 22, look["skin"])
        out += pen.tube(f"M{sx},-190 L{mx:.1f},{my:.1f}", 30, sleeve)
    else:
        out += pen.tube(f"M{sx},-190 L{hx},{hy}", 26, sleeve)
        a, b = 0.8, 0.9
        cuff = {"bajumelayu": "#fdd835", "kurta": "#fff8e1", "kaamatan": "#fdd835", "samfu": "#fdd835",
                "angkasawan": "#ff7043", "bomba": "#fdd835", "chef": "#ffffff",
                "kot": "#ffffff", "jururawat": "#90caf9"}.get(outfit, sleeve)
        out += pen.tube(f"M{sx + (hx - sx) * a:.1f},{-190 + (hy + 190) * a:.1f} "
                        f"L{sx + (hx - sx) * b:.1f},{-190 + (hy + 190) * b:.1f}", 26, cuff)
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
        out = pen.path("M-66,-262 Q-72,-342 0,-340 Q72,-342 66,-262 Q60,-300 32,-302 L20,-288 L6,-304 L-8,-288 "
                       "L-24,-304 L-40,-290 Q-60,-294 -66,-262 Z", fill="#4e342e")
        return out + pen.path("M-40,-328 Q-20,-318 -10,-306 M10,-334 Q30,-326 40,-306 M-58,-300 Q-50,-292 -48,-280",
                              fill="none", w=1.6)
    if h == "ravi":
        out = ""
        for x in (-40, -14, 12, 38):
            out += pen.path(f"M{x - 14},-300 Q{x},-322 {x + 14},-300 Q{x},-306 {x - 14},-300 Z", fill="#3e2723", w=DW)
        return out
    if h in ("mei", "lina"):
        out = pen.path("M-64,-270 Q-66,-338 0,-338 Q66,-338 64,-270 L44,-296 L-44,-296 Z" if h == "mei" else
                       "M-66,-258 Q-70,-342 0,-340 Q70,-342 66,-258 Q60,-300 0,-306 Q-60,-300 -66,-258 Z",
                       fill="#212121")
        if h == "mei":
            out += pen.path("M-26,-336 L-22,-298 M0,-338 L0,-298 M26,-336 L22,-298", fill="none", w=1.6)
            out += pen.path("M-56,-338 Q-44,-348 -40,-334 M56,-338 Q44,-348 40,-334", fill="none", w=1.6)
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
        out = pen.path("M-62,-250 Q-64,-336 0,-338 Q64,-336 62,-250 Q54,-312 0,-314 Q-54,-312 -62,-250 Z",
                       fill=look["tudung"])
        out += pen.path("M-70,-196 Q-50,-170 -30,-160 M70,-196 Q50,-170 30,-160", fill="none", w=1.6)
        return out + pen.circle(0, -196, 6, fill="#fdd835", sw=1.6)
    return ""


def hat(pen, kind):
    if kind == "kopiah":
        cap = "M-64,-292 Q-64,-376 0,-378 Q64,-376 64,-292 Q0,-306 -64,-292 Z"
        out = pen.path(cap, fill="#ffffff")
        band = "M-64,-292 Q0,-306 64,-292 L62,-326 Q0,-340 -62,-326 Z"
        out += pen.path(band, fill="#66bb6a", w=DW)
        out += pen.clipped(band, "".join(pen.path(f"M{x},-298 L{x + 11},-332 L{x + 22},-298", fill="#a5d6a7", w=1.4)
                                         for x in range(-72, 70, 22)))
        return out + pen.path(band, fill="none", w=DW)
    if kind == "chef":
        out = pen.path(blob_d(0, -392, 70, 48, 9, 5), fill="#ffffff")
        return out + pen.path("M-56,-296 L-58,-352 Q0,-362 58,-352 L56,-296 Q0,-306 -56,-296 Z", fill="#ffffff")
    if kind in ("polis", "juruterbang", "posmen"):
        color = {"polis": "#1a237e", "juruterbang": "#ffffff", "posmen": "#e53935"}[kind]
        out = pen.path("M-66,-312 Q-74,-376 0,-384 Q74,-376 66,-312 Z", fill=color)
        out += pen.rect(-62, -330, 124, 20, fill="#212121" if kind != "posmen" else "#ffffff", rx=4, sw=DW)
        out += pen.path("M-58,-312 Q0,-292 58,-312 Q0,-300 -58,-312 Z", fill="#212121", w=DW)
        if kind == "juruterbang":
            out += pen.path("M-30,-356 Q-14,-346 0,-352 Q14,-346 30,-356 Q14,-340 0,-344 Q-14,-340 -30,-356 Z",
                            fill="#fdd835", w=1.4)
        return out + pen.path("M0,-372 l9,9 -9,11 -9,-11 Z", fill="#fdd835", w=1.4)
    if kind == "bomba":
        out = pen.ellipse(0, -310, 92, 18, fill="#e53935", sw=DW + 0.6)
        out += pen.path("M-64,-310 Q-66,-388 0,-390 Q66,-388 64,-310 Z", fill="#e53935")
        out += pen.path("M0,-388 L0,-312", fill="none", w=DW)
        return out + pen.path("M-14,-356 L14,-356 L12,-332 L0,-324 L-12,-332 Z", fill="#fdd835", w=1.6)
    if kind == "keselamatan":
        out = pen.ellipse(0, -312, 86, 14, fill="#fdd835", sw=DW + 0.6)
        out += pen.path("M-66,-312 Q-68,-386 0,-388 Q68,-386 66,-312 Z", fill="#fdd835")
        return out + pen.path("M-12,-386 L-12,-314 M12,-386 L12,-314", fill="none", w=DW)
    if kind == "askar":
        out = pen.path("M-70,-300 Q-74,-384 0,-388 Q74,-384 70,-300 Q0,-312 -70,-300 Z", fill="#558b2f")
        return out + "".join(pen.path(blob_d(x, y, 12, 8, 7, x + 3), fill="#33691e", w=1.4)
                             for x, y in ((-34, -352), (20, -364), (40, -326), (-10, -330)))
    if kind == "caping":
        out = pen.path("M-120,-300 L0,-392 L120,-300 Q0,-286 -120,-300 Z", fill="#e6c27a")
        return out + pen.path("M-60,-346 L60,-346 M-90,-322 L90,-322", fill="none", w=1.6)
    if kind == "beret":
        return pen.path("M-70,-314 Q-80,-370 -10,-378 Q60,-384 76,-336 Q40,-316 -70,-314 Z", fill="#e53935") + \
            pen.line(-6, -378, 0, -392, sw=DW)
    if kind == "topi":
        out = pen.path("M-64,-312 Q-66,-380 0,-382 Q66,-380 64,-312 Z", fill="#1e88e5")
        return out + pen.path("M-64,-316 Q-110,-312 -116,-300 Q-70,-298 -40,-310", fill="#1e88e5", w=DW)
    if kind == "jururawat":
        out = pen.path("M-44,-346 L44,-346 L36,-380 L-36,-380 Z", fill="#ffffff")
        return out + pen.path("M-5,-374 h10 v8 h8 v8 h-8 v8 h-10 v-8 h-8 v-8 h8 Z", fill="#e53935", w=1.2)
    if kind == "songkok":
        return pen.path("M-50,-318 L-46,-356 Q0,-366 46,-356 L50,-318 Q0,-326 -50,-318 Z", fill="#212121")
    if kind == "tanjak":
        out = pen.path("M-66,-300 Q-60,-344 -10,-350 L30,-404 L40,-350 Q66,-338 66,-300 Q0,-316 -66,-300 Z",
                       fill="#c62828")
        return out + pen.path("M-50,-318 Q0,-336 50,-318 M20,-350 L30,-396", fill="none", w=DW)
    return ""


def kid(pen, who, x, y, s=1.0, la=(-64, -112), ra=(64, -112), outfit=None, sit=False, headwear=None,
        arms_front=False, hands=True, colors=None):
    look = dict(CAST[who])
    look.update(colors or {})
    outfit = outfit or look["outfit"]
    if outfit in ("bajumelayu", "silat"):
        look["top"] = {"bajumelayu": "#26a69a", "silat": "#212121"}[outfit]
        look["bottom"] = look["top"]
    if outfit == "angkasawan":
        look.update(top="#eceff1", bottom="#eceff1", glove="#eceff1")
    k0 = pen.k
    pen.k = k0 / s
    up = f'<g transform="translate(0,{SIT})">' if sit else "<g>"
    body = legs(pen, look, outfit, sit)
    arms = arm(pen, look, outfit, -1, la) + arm(pen, look, outfit, 1, ra)
    upper = backpack(pen) if outfit == "angkasawan" else ""
    upper += "" if arms_front else arms
    upper += torso(pen, look, outfit) if not (sit and outfit in ("kurung", "kaamatan")) else _sit_top(pen, look, outfit)
    torso_svg = upper
    upper = ""
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
    cap = hat(pen, headwear or {"bajumelayu": "songkok", "silat": "tanjak"}.get(outfit))
    upper += f'<g transform="translate(0,-14)">{cap}</g>' if look["hair"] == "tudung" and cap else cap
    if outfit == "angkasawan":
        upper = torso_svg + in_helmet(pen, upper) + helmet(pen)
    else:
        upper = torso_svg + upper
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
