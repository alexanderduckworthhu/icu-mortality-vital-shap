"""
SHAP attributions mapped from window features to vital × lookback narratives.

KernelExplainer works with CalibratedClassifierCV. Aggregate feature SHAP onto
a vital × window matrix so the UI can show which windows drove the score.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
import shap

from src.config import (
    FEATURE_WINDOWS_HOURS,
    RANDOM_SEED,
    SHAP_BACKGROUND_MAX_ROWS,
    SHAP_KERNEL_NSAMPLES,
    VITAL_COLUMNS,
)
from src.models.baseline import TrainedBaseline


@dataclass
class AttributionResult:
    """Probability plus feature-level and vital×window SHAP summaries."""

    probability: float
    shap_by_feature: dict[str, float]
    vital_window_matrix: pd.DataFrame
    top_drivers: list[tuple[str, float]]


def _predict_positive_class(
    model: TrainedBaseline,
    feature_matrix: np.ndarray,
) -> np.ndarray:
    """Return P(mortality) for a numpy feature matrix."""
    frame = pd.DataFrame(feature_matrix, columns=model.feature_names)
    return model.pipeline.predict_proba(frame)[:, 1]


def explain_instance(
    model: TrainedBaseline,
    feature_row: pd.Series | pd.DataFrame,
    background_features: pd.DataFrame,
    top_k: int = 8,
) -> AttributionResult:
    """Compute KernelSHAP for one stay and return attribution summaries."""
    if isinstance(feature_row, pd.Series):
        instance = feature_row[model.feature_names].to_frame().T
    else:
        instance = feature_row[model.feature_names]

    background = background_features[model.feature_names]
    if len(background) > SHAP_BACKGROUND_MAX_ROWS:
        background = background.sample(SHAP_BACKGROUND_MAX_ROWS, random_state=RANDOM_SEED)

    explainer = shap.KernelExplainer(
        lambda data: _predict_positive_class(model, data),
        background.values,
        link="identity",
    )
    shap_values = explainer.shap_values(instance.values, nsamples=SHAP_KERNEL_NSAMPLES)
    if isinstance(shap_values, list):
        shap_values = shap_values[1]
    values = np.asarray(shap_values).reshape(-1)
    shap_by_feature = {
        name: float(value) for name, value in zip(model.feature_names, values)
    }

    probability = float(_predict_positive_class(model, instance.values)[0])
    vital_window_matrix = aggregate_to_vital_window(shap_by_feature)
    top_drivers = sorted(
        shap_by_feature.items(),
        key=lambda item: abs(item[1]),
        reverse=True,
    )[:top_k]
    return AttributionResult(
        probability=probability,
        shap_by_feature=shap_by_feature,
        vital_window_matrix=vital_window_matrix,
        top_drivers=top_drivers,
    )


def aggregate_to_vital_window(shap_by_feature: dict[str, float]) -> pd.DataFrame:
    """Sum signed SHAP values onto a vital × lookback-window matrix."""
    matrix_data = {
        f"{window_hours}h": {vital: 0.0 for vital in VITAL_COLUMNS}
        for window_hours in FEATURE_WINDOWS_HOURS
    }
    for feature_name, shap_value in shap_by_feature.items():
        vital = next(
            (v for v in VITAL_COLUMNS if feature_name.startswith(v + "_")),
            None,
        )
        if vital is None:
            continue
        window_hours = next(
            (
                hours
                for hours in FEATURE_WINDOWS_HOURS
                if feature_name.endswith(f"_{hours}h")
            ),
            None,
        )
        if window_hours is None:
            continue
        matrix_data[f"{window_hours}h"][vital] += float(shap_value)
    return pd.DataFrame(matrix_data, index=VITAL_COLUMNS)
