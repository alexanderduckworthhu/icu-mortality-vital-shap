"""Clinical plausibility filters and missingness handling for ICU vitals."""

from __future__ import annotations

import numpy as np
import pandas as pd

from src.config import FORWARD_FILL_LIMIT_HOURS, PLAUSIBLE_RANGES, VITAL_COLUMNS


def apply_plausibility_bounds(
    df: pd.DataFrame,
    vital_cols: list[str] | None = None,
    ranges: dict[str, tuple[float, float]] | None = None,
) -> pd.DataFrame:
    """
    Set physiologically impossible values to NaN.

    WHY: ICU charts contain probe disconnects (SpO2=0), unit mix-ups, and
    typed errors. Clipping invents physiology; NaN lets imputation + missing
    flags stay honest about what was not observed.
    """
    vital_cols = vital_cols or VITAL_COLUMNS
    ranges = ranges or PLAUSIBLE_RANGES
    out = df.copy()
    for col in vital_cols:
        if col not in out.columns:
            continue
        lo, hi = ranges[col]
        bad = (out[col] < lo) | (out[col] > hi)
        out.loc[bad, col] = np.nan
    return out


def add_missingness_indicators(
    df: pd.DataFrame,
    vital_cols: list[str] | None = None,
) -> pd.DataFrame:
    """
    Binary flags for each vital at each timestamp BEFORE imputation.

    WHY: In ICU data, absence is often informative (unstable patients get more
    charting; comfort-care pathways chart differently). Models that only see
    filled numbers discard that signal.
    """
    vital_cols = vital_cols or VITAL_COLUMNS
    out = df.copy()
    for col in vital_cols:
        if col not in out.columns:
            continue
        out[f"{col}_missing"] = out[col].isna().astype(np.int8)
    return out


def forward_fill_limited(
    df: pd.DataFrame,
    vital_cols: list[str] | None = None,
    limit_hours: int = FORWARD_FILL_LIMIT_HOURS,
) -> pd.DataFrame:
    """
    Forward-fill vitals up to `limit_hours` on an hourly grid; leave longer gaps.

    Assumes `df` is already sorted by time and indexed (or grouped) per stay.
    Remaining NaNs after limited ffill are left for a final median/stay fill.
    """
    vital_cols = vital_cols or VITAL_COLUMNS
    out = df.copy()
    cols = [c for c in vital_cols if c in out.columns]
    out[cols] = out[cols].ffill(limit=limit_hours)
    return out


def final_impute_median(
    df: pd.DataFrame,
    vital_cols: list[str] | None = None,
    medians: dict[str, float] | None = None,
) -> tuple[pd.DataFrame, dict[str, float]]:
    """
    Fill remaining NaNs with training-set medians (passed in at inference).

    WHY median (not mean): vital distributions are skewed; mean chases outliers.
    WHY not interpolate across long gaps: invents a smooth trajectory the nurse
    never charted, dangerous for a mortality story.
    """
    vital_cols = vital_cols or VITAL_COLUMNS
    out = df.copy()
    used: dict[str, float] = {}
    for col in vital_cols:
        if col not in out.columns:
            continue
        if medians is not None and col in medians:
            fill = float(medians[col])
        else:
            fill = float(out[col].median(skipna=True))
            if np.isnan(fill):
                fill = 0.0
        used[col] = fill
        out[col] = out[col].fillna(fill)
    return out, used
