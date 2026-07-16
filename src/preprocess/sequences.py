"""Build fixed-length 48-hour vital-sign sequences per ICU stay."""

from __future__ import annotations

import numpy as np
import pandas as pd

from src.config import (
    FEATURE_WINDOWS_HOURS,
    SEQUENCE_HOURS,
    VITAL_COLUMNS,
)
from src.preprocess.missingness import (
    add_missingness_indicators,
    apply_plausibility_bounds,
    final_impute_median,
    forward_fill_limited,
)


def resample_to_hourly(stay_df: pd.DataFrame, time_col: str = "charttime") -> pd.DataFrame:
    """
    Collapse irregular chart times onto a 1-hour grid (mean within the hour).

    WHY hourly: balances noise vs. empty cells for a 48h window. Minute-level
    is mostly sparse for non-invasive vitals in many MIMIC extracts.
    """
    df = stay_df.copy()
    df[time_col] = pd.to_datetime(df[time_col])
    df = df.set_index(time_col).sort_index()
    numeric = [c for c in VITAL_COLUMNS if c in df.columns]
    hourly = df[numeric].resample("1h").mean()
    return hourly


def pad_or_trim_sequence(
    hourly: pd.DataFrame,
    hours: int = SEQUENCE_HOURS,
) -> pd.DataFrame:
    """Ensure exactly `hours` rows: trim from the left (keep most recent) or pad front with NaN."""
    if len(hourly) >= hours:
        return hourly.iloc[-hours:].copy()
    pad_n = hours - len(hourly)
    pad = pd.DataFrame(
        np.nan,
        index=pd.RangeIndex(pad_n),
        columns=hourly.columns,
    )
    body = hourly.reset_index(drop=True)
    return pd.concat([pad, body], ignore_index=True)


def clean_hourly_sequence(
    hourly: pd.DataFrame,
    medians: dict[str, float] | None = None,
) -> tuple[pd.DataFrame, dict[str, float]]:
    """Full clinical cleaning path for one stay's hourly grid."""
    df = apply_plausibility_bounds(hourly)
    df = add_missingness_indicators(df)
    vital_only = df[VITAL_COLUMNS]
    vital_only = forward_fill_limited(vital_only)
    vital_only, used = final_impute_median(vital_only, medians=medians)
    for col in VITAL_COLUMNS:
        df[col] = vital_only[col]
    return df, used


def engineer_window_features(sequence: pd.DataFrame) -> dict[str, float]:
    """
    Baseline features: mean / min / max / last / slope over last 6h, 24h, 48h.

    WHY this shape: maps cleanly to SHAP bars that clinicians can read as
    "the last 6 hours of SpO2" rather than opaque LSTM hidden states.
    LSTM comes later if these aggregates underfit temporal patterns.
    """
    feats: dict[str, float] = {}
    n = len(sequence)
    for window in FEATURE_WINDOWS_HOURS:
        start = max(0, n - window)
        chunk = sequence.iloc[start:]
        for col in VITAL_COLUMNS:
            if col not in chunk.columns:
                continue
            vals = chunk[col].astype(float).values
            feats[f"{col}_mean_{window}h"] = float(np.nanmean(vals))
            feats[f"{col}_min_{window}h"] = float(np.nanmin(vals))
            feats[f"{col}_max_{window}h"] = float(np.nanmax(vals))
            feats[f"{col}_last_{window}h"] = float(vals[-1])
            if len(vals) >= 2:
                x = np.arange(len(vals), dtype=float)
                slope = np.polyfit(x, vals, 1)[0]
            else:
                slope = 0.0
            feats[f"{col}_slope_{window}h"] = float(slope)
            miss_col = f"{col}_missing"
            if miss_col in chunk.columns:
                feats[f"{col}_missrate_{window}h"] = float(chunk[miss_col].mean())
    return feats


def sequences_to_feature_frame(
    sequences: list[pd.DataFrame],
    stay_ids: list[str],
    labels: list[int] | None = None,
) -> pd.DataFrame:
    """Stack engineered features for sklearn training."""
    rows = []
    for i, seq in enumerate(sequences):
        row = engineer_window_features(seq)
        row["stay_id"] = stay_ids[i]
        if labels is not None:
            row["label"] = labels[i]
        rows.append(row)
    return pd.DataFrame(rows)
