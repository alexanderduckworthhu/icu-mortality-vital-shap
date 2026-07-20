"""
Locked clinical and modeling constants for the ICU mortality portfolio project.

WHY comments are interview talking points in code form.
Change a knob only if you can rewrite the WHY sentence.
"""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
SAMPLE_DIR = DATA_DIR / "sample"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
MODEL_DIR = DATA_DIR / "models"
ASSETS_DIR = PROJECT_ROOT / "assets"

# --- Prediction task ---------------------------------------------------------
# WHY 48h: short enough for vital-sign dynamics to matter; long enough for a
# "next two days" risk conversation, not code-blue prediction or 30-day mortality.
HORIZON_HOURS = 48
SEQUENCE_HOURS = 48
RESAMPLE_FREQ = "1h"

# --- Vitals ------------------------------------------------------------------
# WHY these six: universally charted, continuous, clinician-readable.
# Labs / notes / interventions are v2, they explode missingness and scope.
VITAL_COLUMNS = [
    "heart_rate",
    "sys_bp",
    "dias_bp",
    "resp_rate",
    "spo2",
    "temperature_c",
]

# MIMIC-III Metavision / CareVue itemids, verify against D_ITEMS on your extract.
MIMIC_ITEMIDS: dict[str, list[int]] = {
    "heart_rate": [211, 220045],
    "sys_bp": [51, 442, 455, 6701, 220050, 220179],
    "dias_bp": [8368, 8440, 8441, 8555, 220051, 220180],
    "resp_rate": [618, 615, 220210, 224690],
    "spo2": [646, 220277],
    "temperature_c": [223761, 678],  # CareVue 678 is often °F, convert in ETL
}

# Values outside these ranges become NaN (not clipped) before imputation.
PLAUSIBLE_RANGES: dict[str, tuple[float, float]] = {
    "heart_rate": (20.0, 250.0),
    "sys_bp": (40.0, 300.0),
    "dias_bp": (20.0, 200.0),
    "resp_rate": (4.0, 60.0),
    "spo2": (50.0, 100.0),
    "temperature_c": (30.0, 43.0),
}

# Longer gaps stay missing and feed missingness-rate features.
FORWARD_FILL_LIMIT_HOURS = 2

# Lookback windows for baseline aggregates and SHAP heatmap columns.
FEATURE_WINDOWS_HOURS = (6, 24, 48)

# --- Model / evaluation ------------------------------------------------------
RANDOM_SEED = 42
TEST_FRACTION = 0.2
# Orientation only (not a grade): vital-only AUROC ~0.75–0.85; ECE ≲ 0.05–0.08.
EXPECTED_AUROC_MIN = 0.75
EXPECTED_AUROC_MAX = 0.85
EXPECTED_ECE_MAX = 0.08

# --- SHAP / demo UI ----------------------------------------------------------
SHAP_BACKGROUND_MAX_ROWS = 40
SHAP_KERNEL_NSAMPLES = 100
SHAP_TOP_K_DRIVERS = 5
CURATED_STAYS_PER_OUTCOME = 3
BLANK_PLOT_WIDTH_INCHES = 5.2
BLANK_PLOT_HEIGHT_INCHES = 3.2
CALIBRATION_IMAGE_HEIGHT_PX = 300

# Risk-band cutoffs shown in the UI (probability units, 0–1).
RISK_BAND_LOW_MAX = 0.10
RISK_BAND_MODERATE_MAX = 0.25
RISK_BAND_ELEVATED_MAX = 0.50

# Plot / chrome colors (keep in sync with src/styles.py CSS tokens).
COLOR_INK = "#0a0a0a"
COLOR_MUTED = "#333333"
COLOR_ACCENT = "#1a5c3a"
COLOR_ACCENT_DEEP = "#0d3d28"
COLOR_PLOT_LINE = "#0d3d28"
COLOR_PLOT_HIGHLIGHT = "#1a5c3a"

MODEL_PATH = MODEL_DIR / "baseline_mortality.joblib"
METRICS_PATH = PROCESSED_DIR / "demo_metrics.json"
CALIBRATION_PLOT_PATH = ASSETS_DIR / "calibration_demo.png"

DISCLAIMER_EN = (
    "Research / portfolio demo only. Not a medical device. Not for clinical "
    "decision-making. Predictions are probabilistic risk estimates with "
    "uncertainty, never a determination of outcome."
)

DISCLAIMER_FR = (
    "Démo de recherche / portfolio uniquement. Pas un dispositif médical. "
    "Pas destiné à la décision clinique. Les prédictions sont des estimations "
    "de risque probabilistes avec incertitude, jamais une détermination "
    "d'issue."
)
