"""Matplotlib figures for SHAP heatmaps, calibration, and vital trajectories."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.config import (
    COLOR_INK,
    COLOR_MUTED,
    COLOR_PLOT_HIGHLIGHT,
    COLOR_PLOT_LINE,
    VITAL_COLUMNS,
)
from src.explain.fonts import apply_text_font, plot_fontproperties
from src.i18n import normalize_lang, t

# Short subplot / axis labels (longer clinical names live in ui_format).
_PLOT_VITAL_NAMES: dict[str, dict[str, str]] = {
    "en": {
        "heart_rate": "Heart rate",
        "sys_bp": "Systolic BP",
        "dias_bp": "Diastolic BP",
        "resp_rate": "Resp. rate",
        "spo2": "SpO₂",
        "temperature_c": "Temp (°C)",
    },
    "fr": {
        "heart_rate": "Fréq. cardiaque",
        "sys_bp": "PAS",
        "dias_bp": "PAD",
        "resp_rate": "Fréq. respiratoire",
        "spo2": "SpO₂",
        "temperature_c": "Temp. (°C)",
    },
    "de": {
        "heart_rate": "Herzfrequenz",
        "sys_bp": "Syst. BD",
        "dias_bp": "Diast. BD",
        "resp_rate": "Atemfrequenz",
        "spo2": "SpO₂",
        "temperature_c": "Temp. (°C)",
    },
    "it": {
        "heart_rate": "Freq. cardiaca",
        "sys_bp": "PAS",
        "dias_bp": "PAD",
        "resp_rate": "Freq. respiratoria",
        "spo2": "SpO₂",
        "temperature_c": "Temp. (°C)",
    },
    "zh": {
        "heart_rate": "心率",
        "sys_bp": "收缩压",
        "dias_bp": "舒张压",
        "resp_rate": "呼吸频率",
        "spo2": "血氧 SpO2",
        "temperature_c": "体温 (C)",
    },
    "pt": {
        "heart_rate": "Freq. cardíaca",
        "sys_bp": "PAS",
        "dias_bp": "PAD",
        "resp_rate": "Freq. respiratória",
        "spo2": "SpO₂",
        "temperature_c": "Temp. (°C)",
    },
    "ru": {
        "heart_rate": "ЧСС",
        "sys_bp": "САД",
        "dias_bp": "ДАД",
        "resp_rate": "ЧД",
        "spo2": "SpO2",
        "temperature_c": "Темп. (C)",
    },
}

_VITAL_COLORS = {
    "heart_rate": "#0d3d28",  # dark green
    "sys_bp": "#1a6b8a",  # steel blue
    "dias_bp": "#c45c26",  # burnt orange
    "resp_rate": "#5a6b2f",  # olive
    "spo2": "#8a3d5c",  # wine
    "temperature_c": "#2f5c8a",  # mid blue
}


def _friendly_vital(column: str, lang: str = "en") -> str:
    """Map an internal vital column name to a short plot label."""
    lang = normalize_lang(lang)
    names = _PLOT_VITAL_NAMES.get(lang, _PLOT_VITAL_NAMES["en"])
    return names.get(column, column)


def _set_label(setter, text: str, lang: str, **kwargs):
    """Call axis set_*label / set_title and apply CJK font when needed."""
    artist = setter(text, **kwargs)
    apply_text_font(artist, lang)
    return artist


def plot_shap_heatmap(
    matrix: pd.DataFrame,
    title: str | None = None,
    lang: str = "en",
    save_path: Path | None = None,
) -> plt.Figure:
    """Draw a signed SHAP heatmap; returns the matplotlib Figure."""
    lang = normalize_lang(lang)
    if title is None:
        title = t("heatmap", lang)
    font = plot_fontproperties(lang)

    fig, ax = plt.subplots(figsize=(8.0, 3.8), facecolor="#ffffff")
    ax.set_facecolor("#ffffff")
    values = matrix.values.astype(float)
    vmax = float(np.max(np.abs(values))) if np.any(values) else 1.0
    image = ax.imshow(values, aspect="auto", cmap="RdBu_r", vmin=-vmax, vmax=vmax)
    ax.set_xticks(range(len(matrix.columns)))
    tick_kwargs = {"color": COLOR_INK}
    if font is not None:
        tick_kwargs["fontproperties"] = font
    ax.set_xticklabels(list(matrix.columns), **tick_kwargs)
    ax.set_yticks(range(len(matrix.index)))
    ax.set_yticklabels(
        [_friendly_vital(v, lang) for v in matrix.index],
        **tick_kwargs,
    )
    _set_label(
        ax.set_xlabel,
        t("plot_lookback_axis", lang),
        lang,
        color=COLOR_MUTED,
    )
    # Avoid bold for zh: bold cuts often lack CJK glyphs → empty squares.
    weight = "normal" if lang == "zh" else "bold"
    _set_label(
        ax.set_title,
        title,
        lang,
        color=COLOR_INK,
        fontsize=12,
        pad=10,
        fontweight=weight,
    )
    colorbar = fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
    colorbar.set_label(t("plot_shap_colorbar", lang), color=COLOR_MUTED)
    apply_text_font(colorbar.ax.yaxis.label, lang)
    fig.tight_layout()
    if save_path is not None:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, dpi=140, bbox_inches="tight", facecolor="#ffffff")
    return fig


def plot_vital_trajectory(
    sequence: pd.DataFrame,
    highlight_vital: str | None = None,
    title: str | None = None,
    lang: str = "en",
    save_path: Path | None = None,
) -> plt.Figure:
    """
    Draw a 2×3 grid of vital trajectories so each series stays visible.

    Returns the matplotlib Figure. Prefer this over a tall 6-row stack, which
    collapses into unreadable strips inside Gradio's narrow column.
    """
    lang = normalize_lang(lang)
    if title is None:
        title = t("trajectory", lang)
    font = plot_fontproperties(lang)

    columns = [c for c in VITAL_COLUMNS if c in sequence.columns]
    n_cols_grid = 2
    n_rows_grid = int(np.ceil(len(columns) / n_cols_grid))
    fig, axes = plt.subplots(
        n_rows_grid,
        n_cols_grid,
        figsize=(10.5, 2.7 * n_rows_grid),
        sharex=True,
        facecolor="#ffffff",
    )
    axes_flat = np.atleast_1d(axes).ravel()
    hours = np.arange(len(sequence))

    for index, column in enumerate(columns):
        axis = axes_flat[index]
        axis.set_facecolor("#ffffff")
        values = sequence[column].astype(float).values
        color = _VITAL_COLORS.get(column, COLOR_PLOT_LINE)
        line_width = 2.6 if column == highlight_vital else 2.0
        axis.plot(hours, values, color=color, lw=line_width, solid_capstyle="round")
        if highlight_vital == column:
            axis.axvspan(
                max(0, len(sequence) - 6),
                len(sequence) - 1,
                color=COLOR_PLOT_HIGHLIGHT,
                alpha=0.16,
            )
        _set_label(
            axis.set_title,
            _friendly_vital(column, lang),
            lang,
            loc="left",
            fontsize=12,
            color=COLOR_INK,
            pad=6,
        )
        axis.tick_params(colors=COLOR_INK, labelsize=10)
        if font is not None:
            for label in axis.get_xticklabels() + axis.get_yticklabels():
                label.set_fontproperties(font)
        axis.grid(True, alpha=0.28, color="#9aa8ae")
        for spine in axis.spines.values():
            spine.set_color("#c5d2d7")
        if len(values) and np.isfinite(values).any():
            y_min = float(np.nanmin(values))
            y_max = float(np.nanmax(values))
            pad = max((y_max - y_min) * 0.12, 0.5)
            axis.set_ylim(y_min - pad, y_max + pad)

    for index in range(len(columns), len(axes_flat)):
        axes_flat[index].set_visible(False)

    for axis in axes_flat[: len(columns)]:
        if axis.get_visible():
            _set_label(
                axis.set_xlabel,
                t("plot_hour_axis", lang),
                lang,
                color=COLOR_MUTED,
                fontsize=10,
            )

    weight = "normal" if lang == "zh" else "bold"
    suptitle_kwargs: dict = {
        "fontsize": 15,
        "color": COLOR_INK,
        "fontweight": weight,
        "y": 0.995,
    }
    if font is not None:
        # Drop fontweight when using CJK face: bold cuts often lack Han glyphs.
        if lang == "zh":
            del suptitle_kwargs["fontweight"]
        suptitle_kwargs["fontproperties"] = font
    fig.suptitle(title, **suptitle_kwargs)
    fig.tight_layout(rect=(0, 0, 1, 0.96), h_pad=1.25, w_pad=1.35)
    if save_path is not None:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, dpi=160, bbox_inches="tight", facecolor="#ffffff")
    return fig


def plot_calibration_curve(
    fraction_positives: np.ndarray,
    mean_predicted: np.ndarray,
    ece: float,
    title: str | None = None,
    lang: str = "en",
    save_path: Path | None = None,
) -> plt.Figure:
    """Draw a reliability diagram with ECE in the title; returns the Figure."""
    lang = normalize_lang(lang)
    if title is None:
        title = t("calibration", lang)
    font = plot_fontproperties(lang)

    fig, ax = plt.subplots(figsize=(5.2, 5.0), facecolor="#ffffff")
    ax.set_facecolor("#ffffff")
    ax.plot(
        [0, 1],
        [0, 1],
        ls="--",
        color="#888888",
        label=t("plot_cal_perfect", lang),
    )
    ax.plot(
        mean_predicted,
        fraction_positives,
        marker="o",
        color=COLOR_PLOT_LINE,
        label=t("plot_cal_model", lang),
    )
    _set_label(ax.set_xlabel, t("plot_cal_xlabel", lang), lang)
    _set_label(ax.set_ylabel, t("plot_cal_ylabel", lang), lang)
    weight = "normal" if lang == "zh" else "bold"
    _set_label(
        ax.set_title,
        f"{title} (ECE={ece:.3f})",
        lang,
        fontweight=weight,
    )
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    legend = ax.legend(frameon=False, prop=font)
    if legend is not None and font is not None:
        for text in legend.get_texts():
            text.set_fontproperties(font)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    if save_path is not None:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, dpi=140, bbox_inches="tight", facecolor="#ffffff")
    return fig
