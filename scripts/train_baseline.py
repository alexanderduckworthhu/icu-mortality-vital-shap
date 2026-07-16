#!/usr/bin/env python3
"""Train calibrated logistic baseline on demo (or future MIMIC feature table)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.config import (
    ASSETS_DIR,
    CALIBRATION_PLOT_PATH,
    EXPECTED_AUROC_MAX,
    EXPECTED_AUROC_MIN,
    METRICS_PATH,
    MODEL_PATH,
    RANDOM_SEED,
    SAMPLE_DIR,
    TEST_FRACTION,
)
from src.demo_data import feature_table_from_demo, save_demo_sample
from src.explain.plots import plot_calibration_curve
from src.metrics.calibration import compute_calibration
from src.metrics.discrimination import compute_discrimination
from src.models.baseline import predict_proba, save_model, train_baseline


def main() -> None:
    """Train the calibrated baseline, write metrics JSON, and save a calibration plot."""
    if not (SAMPLE_DIR / "demo_vitals_long.csv").exists():
        save_demo_sample(SAMPLE_DIR)

    feature_table = feature_table_from_demo(SAMPLE_DIR)
    feature_columns = [c for c in feature_table.columns if c not in {"stay_id", "label"}]
    feature_matrix = feature_table[feature_columns]
    outcome_labels = feature_table["label"].values

    features_train, features_test, labels_train, labels_test = train_test_split(
        feature_matrix,
        outcome_labels,
        test_size=TEST_FRACTION,
        random_state=RANDOM_SEED,
        stratify=outcome_labels,
    )

    model = train_baseline(
        features_train,
        labels_train,
        feature_names=feature_columns,
        calibrate=True,
    )
    save_model(model, MODEL_PATH)

    predicted_probabilities = predict_proba(model, features_test)
    discrimination = compute_discrimination(labels_test, predicted_probabilities)
    calibration = compute_calibration(labels_test, predicted_probabilities)

    metrics = {
        "n_train": int(len(labels_train)),
        "n_test": int(len(labels_test)),
        "positive_rate_test": float(np.mean(labels_test)),
        "auroc": discrimination.auroc,
        "pr_auc": discrimination.pr_auc,
        "ece": calibration.ece,
        "cohort": "synthetic_demo",
        "note": (
            f"SYNTHETIC demo metrics (may sit near ceiling by construction). "
            f"After PhysioNet credentialing, report MIMIC-III patient-level "
            f"held-out AUROC in the {EXPECTED_AUROC_MIN:.2f}–{EXPECTED_AUROC_MAX:.2f} "
            f"orientation band for vitals-only baselines."
        ),
    }
    METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    METRICS_PATH.write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    plot_calibration_curve(
        calibration.fraction_positives,
        calibration.mean_predicted,
        calibration.ece,
        title="Demo calibration (synthetic)",
        save_path=CALIBRATION_PLOT_PATH,
    )

    print(json.dumps(metrics, indent=2))
    print(f"Model → {MODEL_PATH}")
    print(f"Metrics → {METRICS_PATH}")


if __name__ == "__main__":
    main()
