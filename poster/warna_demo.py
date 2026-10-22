"""Fully colored versions of a few coloring pages, for the coloring reveal in the demo video."""
import importlib.util
import os
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


def load(book, module):
    sys.path[:0] = [os.path.join(ROOT, "siri-kenderaan"), os.path.join(ROOT, "siri-budaya"), os.path.join(ROOT, book)]
    spec = importlib.util.spec_from_file_location(f"{book}_{module}", os.path.join(ROOT, book, f"{module}.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def colored_svg(T, num, page):
    class ColoredPen(T.Pen):
        def __init__(self, colored, prefix):
            super().__init__(True, prefix)
    plain = T.Pen
    T.Pen = ColoredPen
    try:
        return T.page_svg(num, page)
    finally:
        T.Pen = plain


def main():
    jobs = []
    jana = load("siri-budaya", "jana")
    jobs.append(("wau-bulan", jana.T, 1, jana.PAGES[0]))
    import generate as T  # Siri Kenderaan itself
    jobs.append(("bas-sekolah", T, 3, T.PAGES[2]))
    css = "".join(T.font_face("Fredoka", w, os.path.join(ROOT, "siri-kenderaan", "fonts", f"Fredoka-{n}.ttf"))
                  for w, n in ((400, "Regular"), (600, "SemiBold"), (700, "Bold")))
    for name, mod, num, page in jobs:
        svg = colored_svg(mod, num, page).replace('width="2480" height="3508"', 'width="1240" height="1754"', 1)
        with open(os.path.join("demo", f"{name}-warna.html"), "w") as fh:
            fh.write(f"<html><head><style>{css}body{{margin:0}}</style></head><body>{svg}</body></html>")
    print("ok")


if __name__ == "__main__":
    main()
