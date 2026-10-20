"""Use a supplied picture (e.g. a cover made in Gemini) as the front cover page.

The picture is scaled to fill an A4 page at 300 DPI (2480 x 3508), centre-cropped
to the A4 shape and lightly sharpened after upscaling.
"""
import os

from PIL import Image, ImageFilter

A4 = (2480, 3508)


def supplied_cover(book_dir):
    path = os.path.join(book_dir, "kulit-hadapan.jpg")
    return path if os.path.exists(path) else None


def make_cover_png(src, dst, size=A4):
    im = Image.open(src).convert("RGB")
    scale = max(size[0] / im.width, size[1] / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
    left, top = (im.width - size[0]) // 2, (im.height - size[1]) // 2
    im = im.crop((left, top, left + size[0], top + size[1]))
    im = im.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
    im.save(dst)
