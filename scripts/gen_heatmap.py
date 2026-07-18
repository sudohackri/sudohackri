"""Scrapea el calendario publico de github.com/<user> y genera heatmap SVG.

Fallo seguro: si el scrape falla o no hay celdas, NO sobreescribe el SVG
existente; sale con codigo != 0.
"""
import os
import sys

import requests
from bs4 import BeautifulSoup

from svg_common import PALETTE, svg_close, svg_open

USER = os.environ.get("GH_USER", "sudohackri")
_HERE = os.path.dirname(__file__)
OUT = os.path.join(_HERE, "..", "assets", "heatmap.svg")
UA = {"User-Agent": "Mozilla/5.0 (profile-readme-generator)"}


def count_to_level(c: int) -> int:
    if c <= 0:
        return 0
    if c <= 2:
        return 1
    if c <= 5:
        return 2
    if c <= 9:
        return 3
    return 4


def scrape_contributions(user: str) -> list:
    url = f"https://github.com/users/{user}/contributions"
    r = requests.get(url, headers=UA, timeout=20)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    cells = []
    for td in soup.select("td.ContributionCalendar-day"):
        date = td.get("data-date")
        if not date:
            continue
        lvl = td.get("data-level")
        level = int(lvl) if lvl is not None and lvl.isdigit() else 0
        cells.append({"date": date, "level": level})
    return cells


def render(cells: list) -> str:
    cells = sorted(cells, key=lambda c: c["date"])
    box, gap, pad = 11, 3, 12
    weeks = (len(cells) + 6) // 7
    W = pad * 2 + weeks * (box + gap)
    H = pad * 2 + 7 * (box + gap)
    style = (
        ".c{opacity:0;animation:pop .3s ease forwards}"
        "@keyframes pop{from{opacity:0;transform:scale(.4)}"
        "to{opacity:1;transform:scale(1)}}"
    )
    p = [svg_open(W, H, style)]
    for i, cell in enumerate(cells):
        col, row = divmod(i, 7)
        x = pad + col * (box + gap)
        y = pad + row * (box + gap)
        fill = PALETTE["heat"][cell["level"]]
        delay = (col + row) * 0.012
        p.append(
            f'<rect class="c" x="{x}" y="{y}" width="{box}" height="{box}" '
            f'rx="2" fill="{fill}" style="animation-delay:{delay:.3f}s;'
            f"transform-origin:{x + box / 2}px {y + box / 2}px\"/>"
        )
    p.append(svg_close())
    return "".join(p)


def main():
    try:
        cells = scrape_contributions(USER)
    except Exception as e:
        print(f"ERROR scrape: {e}", file=sys.stderr)
        sys.exit(1)
    if not cells:
        print(
            "ERROR: 0 celdas (markup cambiado?), no sobreescribo",
            file=sys.stderr,
        )
        sys.exit(1)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        f.write(render(cells))
    print(f"OK: {OUT} ({len(cells)} celdas)")


if __name__ == "__main__":
    main()
