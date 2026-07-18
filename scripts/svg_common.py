"""Helpers compartidos para generar SVG autocontenidos (sin JS)."""

PALETTE = {
    "bg": "#0d1117",
    "dim": "#8b949e",
    "accent": "#f0883e",
    "accent_light": "#ffa657",
    "heat": ["#161b22", "#5a2e0a", "#8a4610", "#d97316", "#ffa657"],
}


def svg_open(w: int, h: int, style: str = "") -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" '
        f'font-family="ui-monospace,SFMono-Regular,Menlo,monospace">'
        f"<style>{style}</style>"
        f'<rect width="{w}" height="{h}" fill="{PALETTE["bg"]}"/>'
    )


def svg_close() -> str:
    return "</svg>"


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )
