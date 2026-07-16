#!/usr/bin/env python3
"""Print discrimination and calibration for the saved demo model."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.config import METRICS_PATH, MODEL_PATH, RANDOM_SEED, SAMPLE_DIR, TEST_FRACTION
from src.demo_data import feature_table_from_demo
from src.metrics.calibration import compute_calibration
from src.metrics.discrimination import compute_discrimination
from src.models.baseline import load_model, predict_proba


def main() -> None:
    """Evaluate the saved model on the synthetic held-out split and print JSON."""
    if not MODEL_PATH.exists():
        raise SystemExit("No model found. Run: python -m scripts.train_baseline")

    feature_table = feature_table_from_demo(SAMPLE_DIR)
    feature_columns = [c for c in feature_table.columns if c not in {"stay_id", "label"}]
    feature_matrix = feature_table[feature_columns]
    outcome_labels = feature_table["label"].values
    _, features_test, _, labels_test = train_test_split(
        feature_matrix,
        outcome_labels,
        test_size=TEST_FRACTION,
        random_state=RANDOM_SEED,
        stratify=outcome_labels,
    )
    model = load_model(MODEL_PATH)
    predicted_probabilities = predict_proba(model, features_test)
    discrimination = compute_discrimination(labels_test, predicted_probabilities)
    calibration = compute_calibration(labels_test, predicted_probabilities)
    report = {
        "auroc": discrimination.auroc,
        "pr_auc": discrimination.pr_auc,
        "ece": calibration.ece,
        "source_metrics_file": str(METRICS_PATH),
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
