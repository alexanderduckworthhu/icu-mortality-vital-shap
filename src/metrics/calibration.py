"""Calibration metrics and reliability curve bins."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from sklearn.calibration import calibration_curve


@dataclass
class CalibrationReport:
    fraction_positives: np.ndarray
    mean_predicted: np.ndarray
    ece: float
    n_bins: int


def expected_calibration_error(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    n_bins: int = 10,
) -> float:
    """
    ECE: weighted average |confidence − accuracy| across probability bins.

    Clinicians hear a probability. Calibration asks whether ~20% of patients
    scored near 0.20 actually experienced the event. Discrimination alone
    does not answer that.
    """
    bins = np.linspace(0.0, 1.0, n_bins + 1)
    ece = 0.0
    for i in range(n_bins):
        lo, hi = bins[i], bins[i + 1]
        mask = (y_prob >= lo) & (y_prob < hi if i < n_bins - 1 else y_prob <= hi)
        if not np.any(mask):
            continue
        conf = float(y_prob[mask].mean())
        acc = float(y_true[mask].mean())
        ece += (mask.sum() / len(y_true)) * abs(acc - conf)
    return float(ece)


def compute_calibration(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    n_bins: int = 8,
) -> CalibrationReport:
    frac, mean_pred = calibration_curve(y_true, y_prob, n_bins=n_bins, strategy="quantile")
    ece = expected_calibration_error(y_true, y_prob, n_bins=10)
    return CalibrationReport(
        fraction_positives=frac,
        mean_predicted=mean_pred,
        ece=ece,
        n_bins=n_bins,
    )
