"""
Synthetic ICU vital-sign sequences for the Gradio demo.

WHY synthetic until PhysioNet credentialing completes:
- You can ship a reproducible portfolio demo without committing PHI or MIMIC files.
- Interviewers can clone and run immediately.
- Swap `data/sample` for a real MIMIC extract later without changing the UI contract.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from src.config import RANDOM_SEED, SEQUENCE_HOURS, VITAL_COLUMNS
from src.preprocess.sequences import (
    clean_hourly_sequence,
    engineer_window_features,
    pad_or_trim_sequence,
)


def _simulate_stay(rng: np.random.Generator, high_risk: bool) -> pd.DataFrame:
    hours = SEQUENCE_HOURS
    t = np.arange(hours)

    # Baselines near physiological norms; high-risk drifts toward instability.
    hr = 78 + rng.normal(0, 6, hours)
    sbp = 118 + rng.normal(0, 8, hours)
    dbp = 72 + rng.normal(0, 5, hours)
    rr = 16 + rng.normal(0, 2.0, hours)
    spo2 = 97 + rng.normal(0, 1.2, hours)
    temp = 36.8 + rng.normal(0, 0.2, hours)

    if high_risk:
        # Progressive late-window deterioration — what SHAP should surface.
        # Strength + label noise keep demo AUROC in a believable band (not 1.0).
        strength = float(rng.uniform(0.35, 0.85))
        ramp = np.clip((t - 28) / 20.0, 0, 1) * strength
        hr = hr + 25 * ramp
        sbp = sbp - 18 * ramp
        dbp = dbp - 8 * ramp
        rr = rr + 7 * ramp
        spo2 = spo2 - 8 * ramp
        temp = temp + 0.5 * ramp
        if rng.random() < 0.22:
            # Unmeasured factors: labeled high-risk but vitals look quieter
            hr = 82 + rng.normal(0, 6, hours)
            sbp = 115 + rng.normal(0, 8, hours)
            spo2 = 96 + rng.normal(0, 1.5, hours)
    else:
        hr = hr + 4 * np.sin(t / 8)
        if rng.random() < 0.18:
            # Stable label, briefly ugly vitals (false-alarm physiology)
            bump = np.clip((t - 34) / 14.0, 0, 1)
            spo2 = spo2 - rng.uniform(4, 9) * bump
            hr = hr + rng.uniform(8, 18) * bump
            sbp = sbp - rng.uniform(8, 15) * bump

    # Sparse missingness (more missing early for stable; irregular for both)
    df = pd.DataFrame(
        {
            "heart_rate": hr,
            "sys_bp": sbp,
            "dias_bp": dbp,
            "resp_rate": rr,
            "spo2": np.clip(spo2, 55, 100),
            "temperature_c": temp,
        }
    )
    miss_rate = 0.08 if not high_risk else 0.12
    for col in VITAL_COLUMNS:
        drop = rng.random(hours) < miss_rate
        df.loc[drop, col] = np.nan
    return df


def generate_demo_cohort(
    n_stays: int = 200,
    positive_rate: float = 0.22,
    seed: int = RANDOM_SEED,
) -> tuple[list[pd.DataFrame], list[str], list[int]]:
    rng = np.random.default_rng(seed)
    n_pos = int(round(n_stays * positive_rate))
    labels = [1] * n_pos + [0] * (n_stays - n_pos)
    rng.shuffle(labels)

    sequences: list[pd.DataFrame] = []
    stay_ids: list[str] = []
    for i, y in enumerate(labels):
        raw = _simulate_stay(rng, high_risk=bool(y))
        raw = pad_or_trim_sequence(raw, SEQUENCE_HOURS)
        cleaned, _ = clean_hourly_sequence(raw)
        sequences.append(cleaned)
        stay_ids.append(f"demo-{i:04d}")
    return sequences, stay_ids, labels


def save_demo_sample(
    out_dir: Path,
    n_stays: int = 200,
) -> Path:
    """Write long-format CSV + labels for transparency."""
    sequences, stay_ids, labels = generate_demo_cohort(n_stays=n_stays)
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    for stay_id, seq, y in zip(stay_ids, sequences, labels):
        tmp = seq[VITAL_COLUMNS].copy()
        tmp["hour"] = np.arange(len(tmp))
        tmp["stay_id"] = stay_id
        tmp["label"] = y
        rows.append(tmp)
    long_df = pd.concat(rows, ignore_index=True)
    path = out_dir / "demo_vitals_long.csv"
    long_df.to_csv(path, index=False)

    label_path = out_dir / "demo_labels.csv"
    pd.DataFrame({"stay_id": stay_ids, "label": labels}).to_csv(label_path, index=False)
    return path


def load_demo_sequences(sample_dir: Path) -> tuple[list[pd.DataFrame], list[str], list[int]]:
    path = sample_dir / "demo_vitals_long.csv"
    labels_path = sample_dir / "demo_labels.csv"
    if not path.exists():
        save_demo_sample(sample_dir)
    long_df = pd.read_csv(path)
    labels_df = pd.read_csv(labels_path)
    label_map = dict(zip(labels_df["stay_id"], labels_df["label"]))

    sequences = []
    stay_ids = []
    labels = []
    for stay_id, group in long_df.groupby("stay_id", sort=True):
        group = group.sort_values("hour")
        seq = group[VITAL_COLUMNS].reset_index(drop=True)
        # Re-attach missingness indicators for feature engineering consistency
        cleaned, _ = clean_hourly_sequence(seq)
        sequences.append(cleaned)
        stay_ids.append(str(stay_id))
        labels.append(int(label_map[stay_id]))
    return sequences, stay_ids, labels


def feature_table_from_demo(sample_dir: Path) -> pd.DataFrame:
    sequences, stay_ids, labels = load_demo_sequences(sample_dir)
    rows = []
    for seq, sid, y in zip(sequences, stay_ids, labels):
        row = engineer_window_features(seq)
        row["stay_id"] = sid
        row["label"] = y
        rows.append(row)
    return pd.DataFrame(rows)
