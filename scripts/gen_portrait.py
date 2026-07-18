"""Convierte source/photo.jpg en un retrato ASCII SVG con barrido L->R."""
import io
import os
import sys

import cv2
import numpy as np
from PIL import Image

from svg_common import PALETTE, esc, svg_close, svg_open

RAMP = " .:-=+*#%@"          # oscuro -> claro
COLS = 84                    # columnas de caracteres
CHAR_ASPECT = 0.52           # alto/ancho aprox de caracter monoespaciado
CELL_W = 7                   # px por columna en el SVG
CELL_H = 13                  # px por fila

_HERE = os.path.dirname(__file__)
SRC = os.path.join(_HERE, "..", "source", "photo.jpg")
OUT = os.path.join(_HERE, "..", "assets", "portrait.svg")


def brightness_to_char(v: float) -> str:
    idx = int(round((v / 255) * (len(RAMP) - 1)))
    return RAMP[idx]


def load_silhouette(path: str) -> np.ndarray:
    """Imagen gris (0..255) con fondo eliminado por rembg + CLAHE."""
    from rembg import remove

    with open(path, "rb") as f:
        cut = remove(f.read())                      # PNG bytes con alpha
    img = Image.open(io.BytesIO(cut)).convert("RGBA")
    bg = Image.new("RGBA", img.size, (0, 0, 0, 255))
    comp = Image.alpha_composite(bg, img).convert("L")
    arr = np.array(comp)
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    return clahe.apply(arr)


def _autocrop(gray: np.ndarray, thr: int = 12) -> np.ndarray:
    """Recorta al bounding box de la silueta (pixeles no negros)."""
    mask = gray > thr
    if not mask.any():
        return gray
    ys, xs = np.where(mask)
    y0, y1 = ys.min(), ys.max() + 1
    x0, x1 = xs.min(), xs.max() + 1
    return gray[y0:y1, x0:x1]


def to_grid(gray: np.ndarray) -> list:
    gray = _autocrop(gray)
    h, w = gray.shape
    rows = max(1, int(COLS * (h / w) * CHAR_ASPECT))
    small = cv2.resize(gray, (COLS, rows), interpolation=cv2.INTER_AREA)
    return ["".join(brightness_to_char(int(v)) for v in row) for row in small]


def render_svg(grid: list) -> str:
    cols = len(grid[0])
    rows = len(grid)
    W = cols * CELL_W + 20
    H = rows * CELL_H + 20
    style = (
        ".wipe{animation:sweep 1.7s cubic-bezier(.22,.61,.36,1) forwards}"
        "@keyframes sweep{to{width:%dpx}}" % W
    )
    parts = [svg_open(W, H, style)]
    parts.append(
        f'<clipPath id="wp"><rect class="wipe" x="0" y="0" width="0" '
        f'height="{H}"/></clipPath>'
    )
    parts.append(
        f'<g clip-path="url(#wp)" fill="{PALETTE["accent"]}" '
        f'font-size="{CELL_H - 1}" letter-spacing="0.5">'
    )
    for r, line in enumerate(grid):
        y = 14 + r * CELL_H
        parts.append(
            f'<text x="10" y="{y}" xml:space="preserve">{esc(line)}</text>'
        )
    parts.append("</g>")
    parts.append(svg_close())
    return "".join(parts)


def main():
    if not os.path.exists(SRC):
        print(f"ERROR: no existe {SRC}", file=sys.stderr)
        sys.exit(1)
    gray = load_silhouette(SRC)
    grid = to_grid(gray)
    svg = render_svg(grid)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        f.write(svg)
    print(f"OK: {OUT} ({len(grid[0])}x{len(grid)} chars)")


if __name__ == "__main__":
    main()
