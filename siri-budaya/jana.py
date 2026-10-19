"""Siri 8: Budaya Malaysia - 30 coloring pages + covers (A4, 300 DPI).

Uses the same page template as Siri Kenderaan (number badge, title bar,
colored reference box, rounded frame) with thicker lines.

    python3 jana.py svg          # write build/*.html and output/svg/*.svg
    BUILD_DIR=build node ../siri-kenderaan/render.mjs
    python3 jana.py finish       # set 300 DPI + make the PDF
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "siri-kenderaan"))
sys.path.insert(0, HERE)

from PIL import Image  # noqa: E402

import generate as T  # noqa: E402  (the shared Siri Kenderaan template)
from draw import Pen  # noqa: E402
from subjects import PAGES  # noqa: E402

Pen.weight = 1.25  # thick, clear lines for small hands

BUILD = os.path.join(HERE, "build")
OUT = os.path.join(HERE, "output")
PDF = "siri-8-budaya-malaysia-A4-300dpi.pdf"
COVER, BACK = "00-kulit-hadapan", "99-kulit-belakang"


def wanted():
    only = os.environ.get("PAGES")
    return {int(n) for n in only.split(",")} if only else None


def jobs():
    nums = wanted()
    out = [(T.slug(i, page[0]), lambda i=i, page=page: T.page_svg(i, page))
           for i, page in enumerate(PAGES, 1) if nums is None or i in nums]
    if nums is None or 0 in nums:
        from covers import front_cover_svg
        out.insert(0, (COVER, front_cover_svg))
    if nums is None or 99 in nums:
        from covers import back_cover_svg
        out.append((BACK, back_cover_svg))
    return out


def build_svg():
    for d in (BUILD, os.path.join(OUT, "svg"), os.path.join(OUT, "png")):
        os.makedirs(d, exist_ok=True)
    for f in os.listdir(BUILD):
        os.remove(os.path.join(BUILD, f))
    fonts = os.path.join(HERE, "..", "siri-kenderaan", "fonts")
    css = "".join(T.font_face("Fredoka", w, os.path.join(fonts, f"Fredoka-{n}.ttf"))
                  for w, n in ((400, "Regular"), (500, "Medium"), (600, "SemiBold"), (700, "Bold")))
    todo = jobs()
    for name, make in todo:
        svg = make()
        with open(os.path.join(OUT, "svg", f"{name}.svg"), "w") as fh:
            fh.write(svg.replace("<defs>", f"<defs><style>{css}</style>", 1))
        with open(os.path.join(BUILD, f"{name}.html"), "w") as fh:
            fh.write(f"<!doctype html><html><head><meta charset='utf-8'><style>{css}"
                     f"html,body{{margin:0;padding:0;background:#fff}}svg{{display:block}}</style></head>"
                     f"<body>{svg}</body></html>")
    print(f"{len(todo)} pages")


def finish():
    names = sorted(f[:-4] for f in os.listdir(BUILD) if f.endswith(".png"))
    pngs = []
    for name in names:
        im = Image.open(os.path.join(BUILD, f"{name}.png")).convert("RGB")
        assert im.size == (T.PX_W, T.PX_H), im.size
        dst = os.path.join(OUT, "png", f"{name}.png")
        im.save(dst, dpi=(300, 300), optimize=True)
        pngs.append(dst)
    if len(pngs) == len(PAGES) + 2:
        import img2pdf
        a4 = img2pdf.get_layout_fun((img2pdf.mm_to_pt(210), img2pdf.mm_to_pt(297)))
        with open(os.path.join(OUT, PDF), "wb") as fh:
            fh.write(img2pdf.convert(pngs, layout_fun=a4))
    print("done", len(pngs))


if __name__ == "__main__":
    {"svg": build_svg, "finish": finish}[sys.argv[1]]()
