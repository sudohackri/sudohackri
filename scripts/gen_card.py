"""Genera assets/card.svg: tarjeta neofetch minimalista (role + stack)."""
import os

from svg_common import PALETTE, esc, svg_close, svg_open

HEADER = "sudohackri@github"
LINES = [
    ("role", "Product Maker"),
    ("stack", "React · TS · Node · Postgres"),
    ("infra", "VPS · Nginx · Traefik · Docker"),
    ("flow", "AI-augmented · Claude Code · Zed"),
]
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "card.svg")


def render() -> str:
    W = 430
    lh = 30
    y0 = 92                        # baseline de la primera línea key/value
    H = y0 + len(LINES) * lh - 8
    style = (
        ".ln{opacity:0;transform:translateY(6px);"
        "animation:in .45s ease forwards}"
        "@keyframes in{to{opacity:1;transform:translateY(0)}}"
    )
    p = [svg_open(W, H, style)]
    p.append(
        f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="8" '
        f'fill="none" stroke="{PALETTE["dim"]}" stroke-opacity="0.4"/>'
    )
    p.append(
        f'<text class="ln" x="22" y="40" fill="{PALETTE["accent_light"]}" '
        f'font-size="17" font-weight="bold" style="animation-delay:0s">'
        f"{esc(HEADER)}</text>"
    )
    p.append(
        f'<text class="ln" x="22" y="58" fill="{PALETTE["dim"]}" '
        f'font-size="15" xml:space="preserve" style="animation-delay:.1s">'
        f'{esc("-" * len(HEADER))}</text>'
    )
    y = y0
    for i, (k, v) in enumerate(LINES):
        d = 0.28 + i * 0.15
        p.append(
            f'<text class="ln" x="22" y="{y}" font-size="15" '
            f'xml:space="preserve" style="animation-delay:{d}s">'
            f'<tspan fill="{PALETTE["accent"]}">{esc(k):<8}</tspan>'
            f'<tspan fill="#c9d1d9">{esc(v)}</tspan></text>'
        )
        y += lh
    p.append(svg_close())
    return "".join(p)


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        f.write(render())
    print(f"OK: {OUT}")


if __name__ == "__main__":
    main()
