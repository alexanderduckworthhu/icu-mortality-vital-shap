"""
LSTM placeholder, intentionally not the default path.

Use this module only after the baseline is reported and you have evidence that
temporal order (beyond window aggregates) improves AUROC / calibration on a
held-out set. Until then, keep the Gradio demo on the logistic baseline.
"""

from __future__ import annotations

# Pseudocode architecture (do not train until baseline is solid):
#
# Input:  (batch, 48 hours, 6 vitals [+ optional missingness channels])
# Layer:  Masking → LSTM(64) → Dropout(0.3) → Dense(1, sigmoid)
# Loss:   binary cross-entropy with class weights
# Attr:   Gradient×Input or DeepSHAP over time × vital heatmap
#
# Dependencies (add later): torch or tensorflow
# Risk:   overfit on small credentialed extracts; harder ethics story if you
#         cannot explain *which window* drove the score.


def lstm_justification_checklist() -> list[str]:
    return [
        "Baseline AUROC and calibration published on the same cohort split",
        "Error analysis shows missed progressive trajectories",
        "Sample size supports sequence model without severe overfit",
        "SHAP/gradient attribution implemented before claiming interpretability",
        "Calibration still acceptable after switching architectures",
    ]
