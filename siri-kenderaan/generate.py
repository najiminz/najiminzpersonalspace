"""Siri Kenderaan - 30 coloring pages (A4, 300 DPI) following the "Ambulans" template.

Builds one SVG per page (line art + a small colored reference picture in the
top-right box), then render.mjs turns them into 2480x3508 PNGs and this script
tags them with 300 DPI and bundles a print-ready PDF.

    python3 generate.py svg      # write build/*.html and output/svg/*.svg
    node render.mjs              # screenshot to build/*.png
    python3 generate.py finish   # set 300 DPI + make the PDF
"""
import base64
import os
import sys

from PIL import Image, ImageFont

import scenes as S
from back_cover import back_cover_svg
from cover import cover_svg
import vehicles as V
from draw import FRAME, GROUND, H, INK, W, Pen

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, "build")
OUT = os.path.join(HERE, "output")
FONT_BOLD = os.path.join(HERE, "fonts", "Fredoka-Bold.ttf")

PX_W, PX_H = 2480, 3508  # A4 @ 300 DPI
REF = (556, 30, 326, 352)  # colored reference box
REF_VIEW = (22, 400, 862)  # default crop of the scene shown in the reference box

city = S.city

# (title, vehicle, scene, placement) - placement: s=scale, y=baseline, x0=left edge, rot, ref=(x, y, size)
PAGES = [
    ("Ambulans", V.ambulans, city(S.hospital), {}),
    ("Kereta Polis", V.kereta_polis, city(S.balai_polis, trees=((80, 450, 150, 300), (300, 640, 120, 240))), {}),
    ("Bas Sekolah", V.bas_sekolah, city(S.sekolah, trees=((80, 440, 150, 300), (300, 650, 110, 220))), {}),
    ("Jentera Bomba", V.jentera_bomba,
     city(S.balai_bomba, trees=((80, 450, 150, 300), (320, 650, 110, 220))), {}),
    ("Teksi", V.teksi, city(S.hotel, trees=((80, 450, 150, 300), (320, 660, 110, 220))), {}),
    ("Kereta", V.kereta, city(S.rumah_teres, trees=((80, 450, 150, 300), (290, 640, 120, 240))), {}),
    ("Motosikal", V.motosikal, S.kampung, dict(s=1.45)),
    ("Basikal", V.basikal, city(lambda p: S.taman(p, playground=False),
                                trees=((80, 450, 150, 300), (300, 640, 120, 240))), dict(s=1.65)),
    ("Beca", V.beca, city(lambda p: S.kedai(p, ["CENDERAMATA", "KEDAI KOPI", "KEDAI KAIN"],
                                             wall=["#ef9a9a", "#e57373", "#ef9a9a"], roof="#8d4f2a"),
                          trees=((80, 450, 150, 300), (300, 650, 110, 220))), dict(s=1.3)),
    ("Bas Bandar", V.bas_bandar, city(lambda p: S.menara(p, "PUSAT BANDAR"),
                                      trees=((80, 450, 150, 300),)), {}),
    ("Van Aiskrim", V.van_aiskrim, city(S.taman, trees=((80, 450, 150, 300), (300, 650, 110, 220))),
     dict(ref=(22, 330, 900))),
    ("Lori", V.lori, city(lambda p: S.gudang(p, "GUDANG"), trees=((80, 450, 150, 300), (300, 650, 110, 220))), {}),
    ("Lori Sampah", V.lori_sampah, city(lambda p: S.kedai(p, ["KEDAI RUNCIT", "KEDAI ROTI", "FARMASI"]),
                                        trees=((80, 450, 150, 300), (300, 650, 110, 220)),
                                        extra_back=S.bins), {}),
    ("Lori Tangki", V.lori_tangki, city(S.stesen_minyak, trees=((80, 450, 150, 300), (280, 650, 110, 220))), {}),
    ("Trak Tunda", V.trak_tunda, city(lambda p: S.gudang(p, "BENGKEL KERETA", S.bengkel_extra(p)),
                                      trees=((80, 450, 150, 300), (300, 650, 110, 220))), {}),
    ("Treler", V.treler, city(lambda p: S.gudang(p, "PELABUHAN", S.pelabuhan_extra(p)),
                              trees=((80, 450, 150, 300),)), dict(s=0.94)),
    ("Jip", V.jip, S.hutan, {}),
    ("Kereta Lumba", V.kereta_lumba, S.litar, dict(s=0.98)),
    ("Traktor", V.traktor, S.ladang, dict(s=1.18, ref=(22, 330, 900))),
    ("Jentolak", V.jentolak, S.tapak_binaan(), dict(s=1.1)),
    ("Jengkaut", V.jengkaut, S.tapak_binaan(), dict(s=1.05, ref=(22, 350, 880))),
    ("Lori Simen", V.lori_simen, S.tapak_binaan(), {}),
    ("Kren", V.kren, S.tapak_binaan(), dict(s=0.98, ref=(22, 330, 900))),
    ("Penggelek Jalan", V.penggelek_jalan, S.tapak_binaan("KERJA JALAN", "road"), dict(s=1.12, ref=(22, 330, 900))),
    ("Kereta Api", V.kereta_api, S.stesen, dict(x0=70)),
    ("Kapal Terbang", V.kapal_terbang, S.lapangan_terbang, dict(y=560, rot=8, s=0.98, ref=(22, 260, 880))),
    ("Helikopter", V.helikopter, S.langit_bandar, dict(y=600, x0=40, s=0.86, ref=(22, 280, 880))),
    ("Belon Udara Panas", V.belon_udara, S.langit_bukit, dict(y=390, x0=450, s=1.12, ref=(22, 370, 880))),
    ("Kapal", V.kapal, S.laut, dict(y=1100, ref=(22, 400, 862))),
    ("Kapal Selam", V.kapal_selam, S.bawah_laut, dict(y=700, s=0.95, ref=(22, 300, 880))),
]


def slug(i, title):
    return f"{i:02d}-{title.lower().replace(' ', '-')}"


def scene(page, pen):
    title, vehicle, bg, place = page
    back, front = bg(pen)
    s = place.get("s", 1.0)
    pen.k = 1 / s
    v, length = vehicle(pen)
    pen.k = 1.0
    x0 = place.get("x0", round((W - length * s) / 2))
    y = place.get("y", GROUND)
    rot = place.get("rot", 0)
    cx = length / 2
    rotate = f" rotate({rot} {cx} 0)" if rot else ""
    return back + f'<g transform="translate({x0},{y}) scale({s}){rotate}">{v}</g>' + front


def title_layout(title):
    """One line if it fits big enough, otherwise two lines."""
    max_w = REF[0] - 18 - 168 - 24
    font = lambda size: ImageFont.truetype(FONT_BOLD, size)
    size = 58
    while size > 30 and font(size).getlength(title) > max_w:
        size -= 1
    if size >= 46 or " " not in title:
        return [title], size
    words = title.split()
    best = min(range(1, len(words)), key=lambda i: max(len(" ".join(words[:i])), len(" ".join(words[i:]))))
    lines = [" ".join(words[:best]), " ".join(words[best:])]
    size = 46
    while size > 30 and max(font(size).getlength(l) for l in lines) > max_w:
        size -= 1
    return lines, size


def page_svg(num, page):
    fx, fy, fw, fh = FRAME
    rx, ry, rw, rh = REF
    vx, vy, vs = page[3].get("ref", REF_VIEW)
    lines, size = title_layout(page[0])
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{PX_W}" height="{PX_H}" '
         f'viewBox="0 0 {W} {H}" preserveAspectRatio="none">']
    s.append(f'<defs><clipPath id="frame"><rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" rx="22"/></clipPath>'
             f'<clipPath id="refclip"><rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="16"/></clipPath></defs>')
    s.append(f'<rect width="{W}" height="{H}" fill="#fff"/>')
    s.append(f'<g clip-path="url(#frame)">{scene(page, Pen(False, "l"))}</g>')
    s.append(f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" rx="22" fill="none" stroke="{INK}" stroke-width="4.5"/>')
    s.append(f'<rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="16" fill="#fff"/>')
    s.append(f'<g clip-path="url(#refclip)"><svg x="{rx}" y="{ry}" width="{rw}" height="{rh}" '
             f'viewBox="{vx} {vy} {vs} {vs}" preserveAspectRatio="xMidYMid slice">'
             f'<g clip-path="url(#frame)">{scene(page, Pen(True, "c"))}</g></svg></g>')
    s.append(f'<rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="16" fill="none" stroke="{INK}" stroke-width="4.5"/>')
    s.append(f'<rect x="110" y="24" width="{rx - 110 - 18}" height="112" rx="24" fill="#fde3c8" stroke="{INK}" stroke-width="4.5"/>')
    if len(lines) == 1:
        ys = [80 + size * 0.36]
    else:
        ys = [80 - size * 0.18, 80 + size * 0.9]
    for line, ty in zip(lines, ys):
        s.append(f'<text x="168" y="{ty:.1f}" font-family="Fredoka" font-weight="700" '
                 f'font-size="{size}" fill="{INK}">{line}</text>')
    s.append(f'<circle cx="86" cy="82" r="68" fill="#fff" stroke="{INK}" stroke-width="4.5"/>')
    s.append('<circle cx="86" cy="82" r="56" fill="#e8402f"/>')
    nsize = 84 if num < 10 else 66
    s.append(f'<text x="86" y="{82 + nsize * 0.35:.1f}" text-anchor="middle" font-family="Fredoka" font-weight="700" '
             f'font-size="{nsize}" letter-spacing="-2" fill="#fff">{num}</text>')
    s.append("</svg>")
    return "\n".join(s)


def font_face(name, weight, path):
    data = base64.b64encode(open(path, "rb").read()).decode()
    return (f"@font-face{{font-family:'{name}';font-weight:{weight};"
            f"src:url(data:font/ttf;base64,{data}) format('truetype');}}")


COVER = "00-kulit-hadapan"
BACK = "99-kulit-belakang"  # PAGES=99 builds just the back cover


def wanted():
    only = os.environ.get("PAGES")
    return {int(n) for n in only.split(",")} if only else None


def selected():
    nums = wanted()
    return [(i, p) for i, p in enumerate(PAGES, 1) if nums is None or i in nums]


def build_svg():
    for d in (BUILD, os.path.join(OUT, "svg"), os.path.join(OUT, "png")):
        os.makedirs(d, exist_ok=True)
    for f in os.listdir(BUILD):
        os.remove(os.path.join(BUILD, f))
    css = "".join(font_face("Fredoka", w, os.path.join(HERE, "fonts", f"Fredoka-{n}.ttf"))
                  for w, n in ((400, "Regular"), (500, "Medium"), (600, "SemiBold"), (700, "Bold")))
    jobs = [(slug(i, page[0]), lambda i=i, page=page: page_svg(i, page)) for i, page in selected()]
    if wanted() is None or 0 in wanted():
        jobs.insert(0, (COVER, cover_svg))
    if wanted() is None or 99 in wanted():
        jobs.append((BACK, back_cover_svg))
    for name, make in jobs:
        svg = make()
        with open(os.path.join(OUT, "svg", f"{name}.svg"), "w") as fh:
            fh.write(svg.replace("<defs>", f"<defs><style>{css}</style>", 1))
        html = (f"<!doctype html><html><head><meta charset='utf-8'><style>{css}"
                f"html,body{{margin:0;padding:0;background:#fff}}svg{{display:block}}</style></head>"
                f"<body>{svg}</body></html>")
        with open(os.path.join(BUILD, f"{name}.html"), "w") as fh:
            fh.write(html)
    print(f"{len(jobs)} pages")


def finish():
    pngs = []
    names = [slug(i, page[0]) for i, page in selected()]
    if os.path.exists(os.path.join(BUILD, f"{COVER}.png")):
        names.insert(0, COVER)
    if os.path.exists(os.path.join(BUILD, f"{BACK}.png")):
        names.append(BACK)
    for name in names:
        im = Image.open(os.path.join(BUILD, f"{name}.png")).convert("RGB")
        assert im.size == (PX_W, PX_H), im.size
        dst = os.path.join(OUT, "png", f"{name}.png")
        im.save(dst, dpi=(300, 300), optimize=True)
        pngs.append(dst)
    if len(pngs) == len(PAGES) + 2:
        import img2pdf
        a4 = img2pdf.get_layout_fun((img2pdf.mm_to_pt(210), img2pdf.mm_to_pt(297)))
        with open(os.path.join(OUT, "siri-kenderaan-30-muka-A4-300dpi.pdf"), "wb") as fh:
            fh.write(img2pdf.convert(pngs, layout_fun=a4))
    print("done", len(pngs))


if __name__ == "__main__":
    {"svg": build_svg, "finish": finish}[sys.argv[1]]()
