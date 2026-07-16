"""Matplotlib font helpers so CJK titles render (no tofu boxes)."""

from __future__ import annotations

from functools import lru_cache

from matplotlib import font_manager
from matplotlib.font_manager import FontProperties

# Prefer Simplified Chinese–capable faces available on macOS / common Linux installs.
_CJK_CANDIDATES = (
    "Hiragino Sans GB",
    "PingFang HK",
    "Songti SC",
    "STHeiti",
    "Arial Unicode MS",
    "Noto Sans CJK SC",
    "Noto Sans SC",
    "Source Han Sans SC",
    "WenQuanYi Micro Hei",
    "Microsoft YaHei",
)


@lru_cache(maxsize=1)
def cjk_font_name() -> str | None:
    """Return the first installed font that can draw Chinese glyphs, or None."""
    available = {f.name for f in font_manager.fontManager.ttflist}
    for name in _CJK_CANDIDATES:
        if name in available:
            return name
    return None


def plot_fontproperties(lang: str) -> FontProperties | None:
    """
    Font for plot text.

    Mandarin needs an explicit CJK face; DejaVu (matplotlib default) has no
    Chinese glyphs and draws empty squares. Skip bold weight for CJK: many
    system faces lack a bold cut and fall back to a Latin-only bold font.
    """
    if lang != "zh":
        return None
    name = cjk_font_name()
    if not name:
        return None
    return FontProperties(family=name, weight="normal")


def apply_text_font(artist, lang: str) -> None:
    """Set fontproperties on a matplotlib text artist when needed."""
    props = plot_fontproperties(lang)
    if props is not None and artist is not None:
        artist.set_fontproperties(props)
