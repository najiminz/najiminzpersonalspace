"""Backgrounds. Each scene factory returns fn(pen) -> (behind_vehicle, in_front_of_vehicle)."""
import math
import random

from draw import (DW, FRAME, GLASS, GROUND, INK, LW, ROAD_Y, SIDEWALK_Y, W, bird, blob_d, bush, cloud, cone,
                  cross_d, hills, palm, star_d, sun, tree, windows)

SKY = "#bfe7fb"


def sky(pen, color=SKY, bottom=SIDEWALK_Y):
    return f'<rect x="0" y="0" width="{W}" height="{bottom}" fill="{color}"/>' if pen.colored else ""


def clouds(pen):
    return cloud(pen, 50, 195, 330, 150) + cloud(pen, 330, 300, 190, 80)


def skyline(pen):
    out = pen.rect(140, 405, 72, 600, fill="#cfd8e6")
    out += windows(pen, 155, 430, 2, 6, 14, 16, 14, 26)
    out += pen.rect(238, 470, 52, 540, fill="#e3d6f0")
    out += pen.rect(286, 540, 66, 470, fill="#cfe3d6")
    out += windows(pen, 298, 560, 3, 5, 10, 13, 8, 20)
    return out


# ---------------------------------------------------------------- ground

def ground(pen, style="road"):
    x, y, w, h = FRAME
    if style == "road":
        out = pen.rect(x - 5, SIDEWALK_Y, w + 10, ROAD_Y - SIDEWALK_Y, fill="#d8d8d8")
        for sx in range(40, 900, 95):
            out += pen.line(sx, SIDEWALK_Y, sx - 10, ROAD_Y)
        out += pen.rect(x - 5, ROAD_Y, w + 10, 260, fill="#8e98a4")
        for dx in range(-30, 900, 160):
            out += pen.rect(dx, 1222, 82, 11, fill="#ffffff", rx=3, sw=DW)
        return out
    if style == "race":
        out = pen.rect(x - 5, SIDEWALK_Y, w + 10, ROAD_Y - SIDEWALK_Y, fill="#8bc34a")
        out += pen.rect(x - 5, ROAD_Y, w + 10, 260, fill="#6d7680")
        for i, kx in enumerate(range(0, 905, 40)):
            out += pen.rect(kx, ROAD_Y - 2, 40, 16, fill="#e53935" if i % 2 else "#ffffff", sw=DW)
        for r in range(12):
            for c in range(2):
                if (r + c) % 2 == 0:
                    out += pen.rect(110 + c * 20, ROAD_Y + 14 + r * 20, 20, 20, fill="#212121", sw=1.6)
                else:
                    out += pen.rect(110 + c * 20, ROAD_Y + 14 + r * 20, 20, 20, fill="#ffffff", sw=1.6)
        return out
    if style == "dirt":
        out = pen.rect(x - 5, SIDEWALK_Y, w + 10, 280, fill="#d7b48a")
        rnd = random.Random(5)
        for _ in range(26):
            px, py = rnd.uniform(30, 870), rnd.uniform(SIDEWALK_Y + 20, 1255)
            out += pen.ellipse(round(px), round(py), rnd.choice((7, 9, 12)), 5, fill="#a1887f", sw=DW - 0.4)
        out += pen.line(x, 1205, 887, 1205, sw=DW) + pen.line(x, 1240, 887, 1240, sw=DW)
        return out
    if style == "grass":
        out = pen.rect(x - 5, SIDEWALK_Y, w + 10, 280, fill="#9ccc65")
        rnd = random.Random(3)
        for _ in range(40):
            px, py = rnd.uniform(30, 870), rnd.uniform(SIDEWALK_Y + 25, 1255)
            out += pen.path(f"M{px - 8:.0f},{py:.0f} L{px - 3:.0f},{py - 14:.0f} L{px:.0f},{py:.0f} "
                            f"L{px + 4:.0f},{py - 16:.0f} L{px + 8:.0f},{py:.0f}", fill="none", w=DW - 0.4)
        return out
    if style == "rail":
        out = pen.rect(x - 5, SIDEWALK_Y, w + 10, 280, fill="#bcaaa4")
        for sx in range(-10, 905, 70):
            out += pen.rect(sx, GROUND + 6, 46, 22, fill="#8d6e63", rx=3, sw=DW)
        out += pen.rect(x - 5, GROUND, w + 10, 12, fill="#9e9e9e", sw=DW + 0.6)
        rnd = random.Random(8)
        for _ in range(30):
            px, py = rnd.uniform(30, 870), rnd.choice((rnd.uniform(1045, 1160), rnd.uniform(1205, 1255)))
            out += pen.circle(round(px), round(py), 4, fill="#8d8d8d", sw=1.6)
        return out
    return ""


def foreground(pen, fill="#66bb55"):
    return bush(pen, 850, 1268, 150, 80, 7, fill=fill) + bush(pen, 35, 1268, 120, 60, 9, fill=fill)


# ---------------------------------------------------------------- town buildings

def hospital(pen):
    out = pen.rect(384, 520, 120, 490, fill="#e8f1fb")
    out += windows(pen, 400, 545, 3, 5, 22, 28, 12, 26)
    out += pen.rect(780, 520, 92, 490, fill="#e8f1fb")
    out += windows(pen, 794, 545, 2, 5, 24, 28, 14, 26)
    out += pen.rect(500, 480, 284, 530, fill="#ffffff")
    out += pen.rect(540, 418, 204, 122, fill="#ffffff")
    out += pen.path(cross_d(642, 456, 30, 10), fill="#e53935")
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


def hotel(pen):
    out = pen.line(400, 1000, 400, 470, sw=LW) + pen.path("M402,476 L452,486 L402,500 Z", fill="#e53935", w=DW)
    out += pen.rect(430, 500, 430, 510, fill="#ffe0b2")
    out += pen.rect(420, 486, 450, 22, fill="#8d6e63")
    out += pen.rect(540, 410, 210, 64, fill="#8d6e63", rx=10)
    out += pen.text(645, 456, "HOTEL", 42, fill_color="#ffffff", spacing=6)
    for i in range(5):
        out += pen.path(star_d(573 + i * 36, 486 - 2, 9, 4), fill="#fdd835", w=1.8)
    for r in range(4):
        y = 530 + r * 88
        out += windows(pen, 452, y, 6, 1, 48, 54, 18, 0)
        out += pen.rect(446, y + 54, 400, 10, fill="#ffffff", sw=DW)
    return out


def rumah_teres(pen):
    out = ""
    colors = ["#ffe082", "#b3e5fc", "#c5e1a5"]
    for i, x in enumerate((380, 545, 710)):
        out += pen.rect(x, 640, 165, 370, fill=colors[i])
        out += pen.path(f"M{x - 10},650 L{x + 82},560 L{x + 175},650 Z", fill="#d84315")
        out += pen.circle(x + 82, 618, 14, fill=GLASS, sw=DW)
        out += windows(pen, x + 22, 680, 2, 1, 52, 56, 18, 0)
        out += pen.rect(x + 12, 748, 141, 12, fill="#ffffff", sw=DW)
        out += pen.rect(x + 22, 800, 60, 200, fill="#8d6e63", rx=4)
        out += pen.rect(x + 96, 810, 52, 60, fill=GLASS, sw=DW)
        out += pen.circle(x + 72, 900, 4, fill="#fdd835", sw=1.6)
    out += pen.rect(372, 930, 500, 70, fill="none", sw=DW)
    for x in range(380, 872, 24):
        out += pen.line(x, 930, x, 1000, sw=1.8)
    return out


def taman(pen, playground=True):
    out = ""
    if playground:
        out += pen.tube("M400,1000 L420,700 M470,1000 L450,700", 10, "#ef5350")
        for y in range(740, 1000, 40):
            out += pen.line(414, y, 458, y, sw=DW + 0.6)
        out += pen.rect(410, 690, 80, 16, fill="#ef5350")
        out += pen.path("M480,690 Q520,700 560,840 Q590,960 650,990 L650,1004 Q570,990 540,860 Q508,720 480,712 Z",
                        fill="#fdd835")
        out += pen.tube("M660,1000 L700,700 L740,1000 M780,1000 L820,700 L860,1000", 10, "#42a5f5")
        out += pen.tube("M690,700 L830,700", 12, "#42a5f5")
        out += pen.line(740, 706, 740, 860, sw=DW) + pen.line(790, 706, 790, 860, sw=DW)
        out += pen.rect(726, 856, 78, 14, fill="#8d6e63", rx=4, sw=DW)
    else:
        # wakaf (open hut) and a lamp post
        out += pen.tube("M560,1000 L560,760 M820,1000 L820,760", 14, "#8d6e63")
        out += pen.path("M530,770 L690,640 L850,770 Z", fill="#d84315")
        out += pen.path("M600,712 L690,640 L780,712", fill="none", w=DW)
        out += pen.rect(552, 900, 276, 18, fill="#a1887f")
        out += pen.tube("M440,1000 L440,720", 10, "#424242")
        out += pen.circle(440, 708, 20, fill="#fff59d")
        for fx in range(600, 820, 46):
            out += pen.circle(fx, 975, 9, fill="#f06292", sw=DW) + pen.line(fx, 984, fx, 1000, sw=DW)
    out += pen.tube("M560,1000 L560,470 M840,1000 L840,470", 12, "#8d6e63")
    out += pen.rect(520, 420, 360, 70, fill="#2e7d32", rx=12)
    out += pen.text(700, 469, "TAMAN PERMAINAN" if playground else "TAMAN REKREASI", 30, fill_color="#ffffff")
    return out


def kedai(pen, signs, wall="#fff3e0", roof="#bf360c"):
    out = ""
    walls = wall if isinstance(wall, list) else [wall] * 3
    for i, x in enumerate((384, 546, 708)):
        out += pen.rect(x, 600, 162, 410, fill=walls[i])
        out += pen.path(f"M{x - 6},610 L{x + 20},560 L{x + 142},560 L{x + 168},610 Z", fill=roof)
        out += pen.rect(x + 22, 630, 50, 70, fill="#8d6e63", rx=24, sw=DW)
        out += pen.rect(x + 90, 630, 50, 70, fill="#8d6e63", rx=24, sw=DW)
        out += pen.line(x + 47, 650, x + 47, 700, sw=DW) + pen.line(x + 115, 650, x + 115, 700, sw=DW)
        out += pen.rect(x + 10, 724, 142, 46, fill="#ffffff", rx=6)
        out += pen.text(x + 81, 755, signs[i], 21, fill_color=INK, spacing=0)
        out += pen.path(f"M{x + 6},790 L{x + 156},790 L{x + 156},1010 L{x + 6},1010 Z", fill="none", w=DW)
        out += pen.path(f"M{x + 20},1010 L{x + 20},860 Q{x + 81},800 {x + 142},860 L{x + 142},1010",
                        fill=GLASS, w=DW)
    return out


def menara(pen, sign):
    out = pen.rect(380, 470, 200, 540, fill="#cfd8dc")
    out += windows(pen, 396, 490, 4, 9, 32, 34, 14, 20)
    out += pen.rect(600, 430, 260, 580, fill="#e3f2fd")
    out += pen.rect(626, 450, 208, 56, fill="#1565c0", rx=8)
    out += pen.text(730, 489, sign, 26, fill_color="#ffffff")
    out += windows(pen, 620, 530, 5, 7, 34, 40, 14, 24, fill="#b3e5fc")
    out += pen.tube("M884,1000 L884,700", 8, "#616161")
    return out


def gudang(pen, sign, extra=""):
    out = pen.rect(400, 600, 460, 410, fill="#eceff1")
    out += pen.path("M384,612 Q630,500 876,612 Z", fill="#90a4ae")
    out += pen.rect(470, 630, 320, 60, fill="#1565c0", rx=8)
    out += pen.text(630, 673, sign, 36 if len(sign) < 12 else 30, fill_color="#ffffff", spacing=2)
    out += pen.rect(480, 720, 300, 290, fill="#b0bec5")
    for y in range(740, 1000, 22):
        out += pen.line(486, y, 774, y, sw=1.6)
    return out + extra


def bengkel_extra(pen):
    out = ""
    for i in range(4):
        out += pen.ellipse(820, 990 - i * 26, 36, 13, fill="#424242", sw=DW + 0.6)
    return out


def pelabuhan_extra(pen):
    out = ""
    colors = ["#e53935", "#1e88e5", "#43a047", "#fb8c00", "#8e24aa", "#fdd835"]
    for i, (x, y) in enumerate(((380, 930), (380, 860), (380, 790), (800, 930), (800, 860))):
        out += pen.rect(x - 10, y, 90 if x > 700 else 120, 70, fill=colors[i % 6], sw=DW + 0.6)
        for lx in range(x, x + (78 if x > 700 else 108), 12):
            out += pen.line(lx, y + 8, lx, y + 62, sw=1.4)
    return out


def stesen_minyak(pen):
    out = pen.tube("M405,1000 L405,560", 12, "#616161")
    out += pen.rect(370, 430, 74, 140, fill="#ffffff", rx=8)
    out += pen.text(407, 470, "RON", 18, fill_color=INK)
    for i in range(3):
        out += pen.rect(380, 486 + i * 26, 54, 20, fill="#212121", rx=3, sw=1.6)
    out += pen.rect(520, 640, 330, 370, fill="#fff3e0")
    out += windows(pen, 600, 700, 3, 1, 60, 80, 20, 0)
    out += pen.tube("M500,1000 L500,560 M820,1000 L820,560", 18, "#bdbdbd")
    out += pen.rect(460, 520, 410, 60, fill="#e53935", rx=6)
    out += pen.text(665, 562, "STESEN MINYAK", 34, fill_color="#ffffff", spacing=2)
    for x in (560, 720):
        out += pen.rect(x, 870, 60, 130, fill="#ffffff", rx=6)
        out += pen.rect(x + 10, 884, 40, 28, fill="#212121", rx=3, sw=DW)
    return out


def city(building, trees=((80, 440, 150, 300), (850, 520, 90, 220)), extra_back="", extra_front=""):
    def scene(pen):
        back = sky(pen) + clouds(pen) + skyline(pen) + building(pen)
        for i, (cx, top, w, h) in enumerate(trees):
            back += tree(pen, cx, top, w, h, seed=hash((cx, top)) % 97)
        back += bush(pen, 200, SIDEWALK_Y, 170, 70, 3) + bush(pen, 860, SIDEWALK_Y, 120, 60, 4)
        back += ground(pen, "road")
        back += extra_back(pen) if callable(extra_back) else extra_back
        return back, foreground(pen) + (extra_front(pen) if callable(extra_front) else extra_front)
    return scene


def bins(pen):
    out = ""
    for x, c in ((60, "#43a047"), (120, "#1e88e5")):
        out += pen.rect(x, 948, 46, 56, fill=c, rx=4)
        out += pen.rect(x - 4, 938, 54, 12, fill=c, rx=4, sw=DW)
    return out


# ---------------------------------------------------------------- outdoor scenes

def rumah_kampung(pen):
    out = ""
    for x in (480, 560, 650, 740, 820):
        out += pen.rect(x, 860, 16, 140, fill="#8d6e63", sw=DW + 0.6)
    out += pen.rect(450, 690, 400, 176, fill="#d7a86e")
    for x in range(470, 850, 26):
        out += pen.line(x, 694, x, 862, sw=1.4)
    out += pen.path("M420,700 L560,560 L740,560 L880,700 Z", fill="#8d4f2a")
    out += pen.path("M560,560 L650,470 L740,560 Z", fill="#a1887f")
    out += pen.path("M600,520 L650,470 L700,520", fill="none", w=DW)
    out += pen.rect(500, 730, 70, 90, fill="#5d4037", sw=DW + 0.6)
    out += pen.rect(730, 730, 70, 90, fill="#5d4037", sw=DW + 0.6)
    out += pen.line(535, 730, 535, 820, sw=DW) + pen.line(765, 730, 765, 820, sw=DW)
    out += pen.rect(612, 730, 76, 132, fill="#5d4037", sw=DW + 0.6)
    out += pen.path("M600,866 L560,1000 M700,866 L740,1000", fill="none", w=LW)
    for i in range(4):
        y = 890 + i * 28
        out += pen.line(593 - i * 9, y, 707 + i * 9, y, sw=DW + 0.6)
    return out


def kampung(pen):
    back = sky(pen) + sun(pen, 120, 260, 50) + cloud(pen, 250, 230, 230, 90)
    back += hills(pen, SIDEWALK_Y, [(250, 330, 360), (700, 360, 280)], fill="#aed581")
    back += rumah_kampung(pen)
    back += palm(pen, 110, SIDEWALK_Y, 430, lean=40) + palm(pen, 330, SIDEWALK_Y, 320, lean=-30)
    back += bush(pen, 230, SIDEWALK_Y, 150, 60, 3) + bush(pen, 880, SIDEWALK_Y, 120, 60, 4)
    back += ground(pen, "road")
    for x, y in ((420, 330), (470, 360)):
        back += bird(pen, x, y)
    return back, foreground(pen)


def hutan(pen):
    back = sky(pen) + sun(pen, 120, 250, 46) + cloud(pen, 230, 230, 220, 80)
    back += hills(pen, SIDEWALK_Y, [(220, 300, 520), (560, 300, 440), (860, 260, 360)], fill="#81c784")
    for i, (cx, top, w, h) in enumerate(((60, 620, 130, 300), (190, 680, 120, 260), (420, 640, 140, 300),
                                         (560, 690, 120, 250), (700, 640, 130, 300), (850, 690, 110, 250))):
        back += tree(pen, cx, top, w, h, seed=i + 30)
    back += pen.tube("M640,1000 L640,700 M800,1000 L800,700", 12, "#8d6e63")
    back += pen.rect(610, 650, 220, 64, fill="#a1887f", rx=8)
    back += pen.text(720, 693, "HUTAN LIPUR", 30, fill_color="#ffffff")
    back += ground(pen, "dirt")
    back += pen.ellipse(760, 1230, 70, 14, fill="#90caf9", sw=DW)
    return back, foreground(pen, "#43a047")


def ladang(pen):
    back = sky(pen) + sun(pen, 120, 250, 46) + cloud(pen, 240, 230, 220, 80)
    back += hills(pen, SIDEWALK_Y, [(260, 360, 330), (760, 320, 260)], fill="#aed581")
    back += pen.rect(480, 640, 330, 370, fill="#e53935")
    back += pen.path("M466,650 L520,560 L645,520 L770,560 L824,650 Z", fill="#8d6e63")
    back += pen.rect(560, 590, 170, 50, fill="#ffffff", rx=8)
    back += pen.text(645, 627, "LADANG", 34, fill_color=INK)
    back += pen.rect(570, 790, 150, 220, fill="#ffffff")
    back += pen.path("M570,790 L720,1010 M720,790 L570,1010", fill="none", w=DW + 0.6)
    back += pen.rect(510, 680, 50, 50, fill=GLASS, sw=DW) + pen.rect(730, 680, 50, 50, fill=GLASS, sw=DW)
    back += tree(pen, 120, 560, 160, 320, seed=40) + tree(pen, 360, 680, 120, 240, seed=41)
    back += pen.rect(20, 950, 880, 10, fill="#d7a86e", sw=DW) + pen.rect(20, 975, 880, 10, fill="#d7a86e", sw=DW)
    for x in range(30, 900, 70):
        back += pen.rect(x, 930, 14, 70, fill="#d7a86e", sw=DW)
    back += ground(pen, "grass")
    for x in (220, 300):
        back += pen.rect(x, 1040, 60, 44, fill="#ffd54f", rx=10)
    return back, foreground(pen)


def tapak_binaan(sign="TAPAK BINAAN", ground_style="dirt"):
    def scene(pen):
        back = sky(pen) + cloud(pen, 50, 215, 260, 110)
        # tower crane
        back += pen.path("M150,1000 L150,420 M190,1000 L190,420", fill="none", w=LW)
        for y in range(420, 1000, 40):
            back += pen.line(150, y, 190, y + 40, sw=DW) + pen.line(150, y, 190, y, sw=DW)
        back += pen.rect(60, 396, 480, 24, fill="#fbc02d")
        for x in range(80, 540, 30):
            back += pen.line(x, 398, x + 15, 418, sw=1.6)
        back += pen.rect(60, 420, 50, 50, fill="#757575")
        back += pen.rect(190, 420, 50, 44, fill=GLASS)
        back += pen.line(470, 420, 470, 560, sw=DW)
        back += pen.rect(430, 560, 80, 40, fill="#a1887f", sw=DW + 0.6)
        # building frame
        for x in (400, 550, 700, 850):
            back += pen.rect(x, 520, 18, 480, fill="#bdbdbd", sw=DW + 0.6)
        for y in (520, 640, 760, 880):
            back += pen.rect(392, y, 474, 18, fill="#bdbdbd", sw=DW + 0.6)
        for x in range(612, 700, 22):
            back += pen.line(x, 520, x, 1000, sw=1.6)
        back += pen.rect(20, 900, 880, 100, fill="#1e88e5")
        for x in range(120, 900, 110):
            back += pen.line(x, 900, x, 1000, sw=DW)
        back += pen.rect(310, 914, 290, 72, fill="#ffffff", rx=8)
        back += pen.text(455, 962, sign, 34, fill_color="#e53935", spacing=2)
        back += ground(pen, ground_style)
        back += cone(pen, 60, 1050) + cone(pen, 860, 1050)
        if ground_style == "dirt":
            back += pen.path("M700,1040 Q760,960 830,1040 Z", fill="#d7a86e")
        return back, cone(pen, 870, 1260, 1.3)
    return scene


def litar(pen):
    back = sky(pen) + clouds(pen)
    back += pen.rect(380, 600, 490, 410, fill="#eceff1")
    for i in range(6):
        y = 700 + i * 50
        back += pen.rect(390 + i * 0, y, 470, 50, fill="#90a4ae" if i % 2 else "#cfd8dc", sw=DW)
        for x in range(410, 860, 34):
            back += pen.circle(x, y + 16, 10, fill=["#e53935", "#fdd835", "#1e88e5", "#43a047"][(x // 34 + i) % 4],
                               sw=1.8)
    back += pen.tube("M400,700 L400,560 M850,700 L850,560", 12, "#757575")
    back += pen.rect(370, 540, 510, 40, fill="#e53935")
    back += pen.rect(470, 470, 310, 64, fill="#212121", rx=8)
    back += pen.text(625, 514, "LITAR LUMBA", 38, fill_color="#ffffff", spacing=2)
    back += pen.path("M20,440 Q200,480 380,440", fill="none", w=DW)
    for i in range(7):
        x = 40 + i * 48
        y = 440 + 40 * math.sin(math.pi * (x - 20) / 360) * 0.9
        back += pen.path(f"M{x},{y:.0f} L{x + 28},{y:.0f} L{x + 14},{y + 34:.0f} Z",
                         fill=["#e53935", "#fdd835", "#1e88e5"][i % 3], w=DW)
    back += pen.tube("M110,1000 L110,560", 10, "#757575")
    for r in range(4):
        for c in range(5):
            back += pen.rect(116 + c * 22, 566 + r * 22, 22, 22, fill="#212121" if (r + c) % 2 else "#ffffff", sw=1.6)
    back += tree(pen, 250, 690, 130, 260, seed=50)
    back += ground(pen, "race")
    return back, ""


def stesen(pen):
    back = sky(pen) + clouds(pen)
    back += hills(pen, SIDEWALK_Y, [(150, 260, 300)], fill="#aed581")
    back += pen.rect(400, 600, 460, 400, fill="#fff8e1")
    back += pen.path("M380,610 L630,470 L880,610 Z", fill="#1565c0")
    back += pen.circle(630, 560, 30, fill="#ffffff", sw=DW + 0.6)
    back += pen.line(630, 560, 630, 538, sw=DW) + pen.line(630, 560, 646, 566, sw=DW)
    back += pen.rect(440, 626, 380, 56, fill="#1565c0", rx=8)
    back += pen.text(630, 666, "STESEN KERETA API", 30, fill_color="#ffffff", spacing=1)
    for x in (430, 530, 640, 750):
        back += pen.path(f"M{x},{880} L{x},{760} Q{x + 35},{715} {x + 70},{760} L{x + 70},{880} Z", fill=GLASS, w=DW)
    back += pen.rect(380, 940, 500, 60, fill="#bdbdbd")
    back += tree(pen, 90, 600, 140, 300, seed=60) + tree(pen, 280, 700, 110, 220, seed=61)
    back += ground(pen, "rail")
    return back, ""


def lapangan_terbang(pen):
    back = sky(pen, bottom=1090) + cloud(pen, 40, 200, 260, 110) + cloud(pen, 330, 330, 160, 64)
    back += pen.rect(20, 980, 880, 110, fill="#9ccc65")
    back += pen.rect(180, 870, 560, 160, fill="#eceff1")
    back += windows(pen, 200, 930, 9, 1, 46, 70, 14, 0)
    back += pen.rect(220, 830, 480, 46, fill="#1565c0", rx=8)
    back += pen.text(460, 864, "LAPANGAN TERBANG", 30, fill_color="#ffffff", spacing=1)
    back += pen.rect(780, 800, 60, 230, fill="#eceff1")
    back += pen.path("M754,800 L866,800 L850,730 L770,730 Z", fill=GLASS)
    back += pen.rect(760, 716, 100, 16, fill="#90a4ae")
    back += pen.rect(-5, 1090, 915, 200, fill="#6d7680")
    for x in range(-20, 905, 130):
        back += pen.rect(x, 1170, 80, 12, fill="#ffffff", rx=3, sw=DW)
    for x in range(40, 900, 120):
        back += pen.circle(x, 1096, 6, fill="#fdd835", sw=1.8)
    return back, ""


def langit_bandar(pen):
    back = sky(pen, bottom=1262) + cloud(pen, 40, 210, 280, 110) + cloud(pen, 600, 760, 240, 90)
    back += bird(pen, 420, 330) + bird(pen, 460, 360) + bird(pen, 760, 640, 1.2)
    specs = [(20, 980, 110), (130, 900, 120, True), (250, 1020, 90), (340, 940, 130), (470, 1000, 100),
             (570, 880, 140, True), (710, 960, 90), (800, 1010, 100)]
    for s in specs:
        x, top, w = s[0], s[1], s[2]
        back += pen.rect(x, top, w, 1300 - top, fill=["#cfd8e6", "#e3d6f0", "#cfe3d6", "#ffe0b2"][x % 4])
        back += windows(pen, x + 14, top + 24, max(1, (w - 14) // 34), 6, 20, 22, 14, 20)
        if len(s) > 3:
            back += pen.ellipse(x + w / 2, top - 6, w * 0.42, 10, fill="#9e9e9e", sw=DW + 0.6)
            back += pen.text(x + w / 2, top - 1, "H", 16, fill_color="#fdd835")
    return back, ""


def langit_bukit(pen):
    back = sky(pen, bottom=1262) + sun(pen, 110, 250, 46) + cloud(pen, 600, 830, 220, 80)
    back += bird(pen, 260, 300) + bird(pen, 300, 330)
    for cx, cy, s, c in ((120, 640, 0.32, "#43a047"), (790, 520, 0.26, "#1e88e5")):
        back += pen.path(f"M{cx},{cy} C{cx + 180 * s},{cy} {cx + 262 * s},{cy + 120 * s} {cx + 252 * s},{cy + 232 * s} "
                         f"C{cx + 242 * s},{cy + 330 * s} {cx + 124 * s},{cy + 400 * s} {cx + 72 * s},{cy + 462 * s} "
                         f"L{cx - 72 * s},{cy + 462 * s} C{cx - 124 * s},{cy + 400 * s} {cx - 242 * s},{cy + 330 * s} "
                         f"{cx - 252 * s},{cy + 232 * s} C{cx - 262 * s},{cy + 120 * s} {cx - 180 * s},{cy} {cx},{cy} Z",
                         fill=c, w=DW + 0.6)
        back += pen.line(cx - 20, cy + 462 * s, cx - 14, cy + 540 * s, sw=1.8)
        back += pen.line(cx + 20, cy + 462 * s, cx + 14, cy + 540 * s, sw=1.8)
        back += pen.rect(cx - 18, cy + 540 * s, 36, 26, fill="#c8a165", rx=4, sw=DW)
    back += hills(pen, 1262, [(150, 330, 200), (560, 380, 250), (900, 260, 170)], fill="#9ccc65")
    back += hills(pen, 1262, [(330, 300, 120), (760, 320, 110)], fill="#7cb342")
    for i, (cx, top) in enumerate(((90, 1090), (460, 1040), (640, 1080))):
        back += tree(pen, cx, top, 70, 140, seed=70 + i, base=top + 150)
    return back, ""


def laut(pen):
    sea_y = 980
    back = sky(pen, bottom=sea_y) + sun(pen, 120, 250, 46) + cloud(pen, 250, 230, 240, 90)
    back += hills(pen, sea_y, [(760, 220, 150)], fill="#a5d6a7")
    back += pen.path("M40,980 Q60,900 110,890 Q170,900 190,980 Z", fill="#a1887f")
    back += pen.path("M86,900 L96,640 L134,640 L144,900 Z", fill="#ffffff")
    back += pen.clipped("M86,900 L96,640 L134,640 L144,900 Z",
                        pen.fillrect(70, 700, 90, 40, "#e53935") + pen.fillrect(70, 790, 90, 40, "#e53935"))
    back += pen.rect(88, 600, 54, 44, fill=GLASS)
    back += pen.path("M80,602 L115,560 L150,602 Z", fill="#e53935")
    back += bird(pen, 420, 330) + bird(pen, 460, 300) + bird(pen, 520, 360, 0.8)
    if pen.colored:
        back += f'<rect x="0" y="{sea_y}" width="{W}" height="400" fill="#4fc3f7"/>'
    back += pen.line(18, sea_y, 887, sea_y, sw=LW)
    for y, off in ((1010, 0), (1040, 60)):
        for x in range(30 + off, 900, 120):
            back += pen.path(f"M{x},{y} q15,-12 30,0 q15,12 30,0", fill="none", w=DW)
    front = ""
    wave = "M0,1110 " + "".join(f"q35,-30 70,0 " for _ in range(14)) + "L905,1290 L0,1290 Z"
    front += pen.path(wave, fill="#29b6f6")
    for y, off in ((1170, 20), (1225, 70)):
        for x in range(off, 900, 140):
            front += pen.path(f"M{x},{y} q15,-12 30,0 q15,12 30,0", fill="none", w=DW)
    return back, front


def fish(pen, x, y, s, color, flip=False):
    sx = -s if flip else s
    return (f'<g transform="translate({x},{y}) scale({sx},{s})">'
            + pen.path("M0,0 Q30,-30 70,0 Q30,30 0,0 Z M66,0 L92,-20 L92,20 Z", fill=color, w=DW / s)
            + pen.circle(18, -4, 4, fill="#212121", sw=1.4 / s) + "</g>")


def bawah_laut(pen):
    back = f'<rect x="0" y="0" width="{W}" height="{1280}" fill="#4fc3f7"/>' if pen.colored else ""
    back += pen.path("M0,240 " + "".join("q32,-22 64,0 " for _ in range(15)) + "L905,0 L0,0 Z", fill="#bfe7fb")
    back += pen.path("M0,1110 Q120,1070 240,1100 Q400,1140 560,1090 Q720,1050 905,1100 L905,1290 L0,1290 Z",
                     fill="#ffe0a3")
    for x, h, c in ((70, 300, "#43a047"), (110, 220, "#66bb6a"), (820, 280, "#43a047"), (780, 200, "#66bb6a")):
        back += pen.tube(f"M{x},1110 q-30,-{h / 4} 0,-{h / 2} q30,-{h / 4} 0,-{h / 2}", 16, c)
    back += pen.path("M330,1110 Q320,1040 350,1030 Q360,990 390,1010 Q420,980 430,1030 Q460,1050 440,1110 Z",
                     fill="#f06292")
    back += pen.path("M600,1100 Q610,1050 650,1060 Q700,1040 700,1100 Z", fill="#9e9e9e")
    for i, (x, y, s, c, fl) in enumerate(((140, 380, 0.9, "#fb8c00", False), (640, 330, 0.8, "#fdd835", True),
                                          (760, 960, 0.7, "#e53935", True), (180, 960, 0.75, "#ab47bc", False),
                                          (420, 920, 0.6, "#26a69a", False))):
        back += fish(pen, x, y, s, c, fl)
    for x, y, r in ((200, 600, 10), (215, 560, 7), (230, 530, 5), (850, 700, 9), (840, 660, 6), (500, 300, 8)):
        back += pen.circle(x, y, r, fill="#e1f5fe", sw=DW)
    back += pen.path(star_d(520, 1140, 30, 13), fill="#ff7043", w=DW + 0.6)
    return back, ""

