"""The official UPSI and FSKXpert logos, embedded into the covers."""
import base64
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
_cache = {}


def _load(name):
    if name not in _cache:
        path = os.path.join(HERE, "logo", f"{name}.png")
        w, h = Image.open(path).size
        data = base64.b64encode(open(path, "rb").read()).decode()
        _cache[name] = (w / h, data)
    return _cache[name]


def width(name, h):
    return _load(name)[0] * h


def logo(name, x, y, h):
    """Logo `name` ("upsi" or "fskxpert") with its top-left corner at (x, y) and height h."""
    aspect, data = _load(name)
    return (f'<image href="data:image/png;base64,{data}" x="{x:.1f}" y="{y:.1f}" width="{aspect * h:.1f}" '
            f'height="{h:.1f}" preserveAspectRatio="xMidYMid meet"/>')


def badge(x=20, y=16, h=60):
    """White rounded tag with the FSKXpert logo, for the front covers."""
    return (f'<rect x="{x}" y="{y}" width="{width("fskxpert", h) + 32:.1f}" height="{h + 24}" rx="18" '
            f'fill="#ffffff" stroke="#1a3a8f" stroke-width="2.5"/>' + logo("fskxpert", x + 16, y + 12, h))
