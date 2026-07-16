"""Discrimination metrics (AUROC, optional PR-AUC)."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from sklearn.metrics import average_precision_score, roc_auc_score, roc_curve


@dataclass
class DiscriminationReport:
    auroc: float
    pr_auc: float
    fpr: np.ndarray
    tpr: np.ndarray
    thresholds: np.ndarray


def compute_discrimination(y_true: np.ndarray, y_prob: np.ndarray) -> DiscriminationReport:
    """
    AUROC = ranking quality (can the model order higher-risk above lower-risk?).
    PR-AUC = better under class imbalance — always report both for mortality.
    """
    auroc = float(roc_auc_score(y_true, y_prob))
    pr_auc = float(average_precision_score(y_true, y_prob))
    fpr, tpr, thr = roc_curve(y_true, y_prob)
    return DiscriminationReport(
        auroc=auroc,
        pr_auc=pr_auc,
        fpr=fpr,
        tpr=tpr,
        thresholds=thr,
    )
