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


def badge(x=20, y=16):
    """White rounded badge with both logos, for the front covers."""
    pad, h_upsi, h_fsk = 14, 72, 54
    w_upsi, w_fsk = width("upsi", h_upsi), width("fskxpert", h_fsk)
    w = pad + w_upsi + 22 + w_fsk + pad
    h = h_upsi + 2 * 12
    sep = x + pad + w_upsi + 11
    return (f'<rect x="{x}" y="{y}" width="{w:.1f}" height="{h}" rx="18" fill="#ffffff" stroke="#1a3a8f" '
            f'stroke-width="2.5"/>'
            + logo("upsi", x + pad, y + 12, h_upsi)
            + f'<line x1="{sep:.1f}" y1="{y + 16}" x2="{sep:.1f}" y2="{y + h - 16}" stroke="#c5cae9" stroke-width="2"/>'
            + logo("fskxpert", sep + 11, y + (h - h_fsk) / 2, h_fsk))
