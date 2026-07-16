"""
Baseline: calibrated logistic regression on window aggregates.

WHY start here (not LSTM):
1. You can train, calibrate, and explain it in a week with pandas + sklearn.
2. Window aggregates already capture much of the vital-sign signal.
3. SHAP on tabular features is stable and interview-friendly.
4. An LSTM only earns its complexity if this baseline plateaus and error
   analysis shows missed *trajectory* patterns (e.g., progressive SpO2 decline
   that means/mins wash out).

Interview line: "I establish a discrimination floor with a calibrated
logistic model, then justify any sequence model against that floor."
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


@dataclass
class TrainedBaseline:
    pipeline: Pipeline
    feature_names: list[str]
    medians: dict[str, float]


def build_baseline_pipeline(random_state: int = 42) -> Pipeline:
    """
    Standardize → L2 logistic → optional calibration wrapper applied outside.

    class_weight='balanced' because mortality is rare; without it the model
    collapses toward "always survive."
    """
    clf = LogisticRegression(
        max_iter=2000,
        class_weight="balanced",
        solver="lbfgs",
        random_state=random_state,
    )
    return Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("clf", clf),
        ]
    )


def train_baseline(
    X: pd.DataFrame,
    y: np.ndarray | pd.Series,
    feature_names: list[str] | None = None,
    medians: dict[str, float] | None = None,
    calibrate: bool = True,
    random_state: int = 42,
) -> TrainedBaseline:
    """Fit baseline; wrap with isotonic calibration on a CV split when possible."""
    feature_names = feature_names or list(X.columns)
    X_mat = X[feature_names]
    pipe = build_baseline_pipeline(random_state=random_state)

    if calibrate and len(np.unique(y)) > 1 and len(y) >= 30:
        # Isotonic calibration: better for showing clinicians probability meaning.
        model: Pipeline | CalibratedClassifierCV = CalibratedClassifierCV(
            pipe,
            method="isotonic",
            cv=3,
        )
        model.fit(X_mat, y)
        # Store as a thin Pipeline-like object for joblib + predict_proba
        final = model
    else:
        pipe.fit(X_mat, y)
        final = pipe

    return TrainedBaseline(
        pipeline=final,  # type: ignore[arg-type]
        feature_names=feature_names,
        medians=medians or {},
    )


def predict_proba(model: TrainedBaseline, X: pd.DataFrame) -> np.ndarray:
    X_mat = X[model.feature_names]
    return model.pipeline.predict_proba(X_mat)[:, 1]


def save_model(model: TrainedBaseline, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {
            "pipeline": model.pipeline,
            "feature_names": model.feature_names,
            "medians": model.medians,
        },
        path,
    )


def load_model(path: Path) -> TrainedBaseline:
    blob = joblib.load(path)
    return TrainedBaseline(
        pipeline=blob["pipeline"],
        feature_names=blob["feature_names"],
        medians=blob.get("medians", {}),
    )
