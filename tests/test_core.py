"""Unit tests for preprocessing, metrics, and ethics framing."""

from __future__ import annotations

import numpy as np
import pandas as pd

from src.config import SEQUENCE_HOURS, VITAL_COLUMNS
from src.demo_data import generate_demo_cohort
from src.ethics.framing import format_probability_statement, risk_band
from src.metrics.calibration import expected_calibration_error
from src.metrics.discrimination import compute_discrimination
from src.preprocess.missingness import apply_plausibility_bounds
from src.preprocess.sequences import engineer_window_features, pad_or_trim_sequence


def test_plausibility_sets_impossible_spo2_to_nan():
    df = pd.DataFrame({"spo2": [98.0, 0.0, 105.0], "heart_rate": [80.0, 80.0, 80.0]})
    out = apply_plausibility_bounds(df)
    assert np.isnan(out.loc[1, "spo2"])
    assert np.isnan(out.loc[2, "spo2"])
    assert out.loc[0, "spo2"] == 98.0


def test_pad_or_trim_length():
    short = pd.DataFrame({c: [70.0] * 10 for c in VITAL_COLUMNS})
    padded = pad_or_trim_sequence(short, hours=SEQUENCE_HOURS)
    assert len(padded) == SEQUENCE_HOURS

    long = pd.DataFrame({c: np.arange(60, dtype=float) for c in VITAL_COLUMNS})
    trimmed = pad_or_trim_sequence(long, hours=SEQUENCE_HOURS)
    assert len(trimmed) == SEQUENCE_HOURS
    assert trimmed["heart_rate"].iloc[-1] == 59.0


def test_engineer_features_keys():
    seq = pd.DataFrame({c: np.linspace(60, 90, SEQUENCE_HOURS) for c in VITAL_COLUMNS})
    for c in VITAL_COLUMNS:
        seq[f"{c}_missing"] = 0
    feats = engineer_window_features(seq)
    assert "heart_rate_mean_6h" in feats
    assert "spo2_slope_24h" in feats


def test_demo_cohort_shapes():
    seqs, ids, labels = generate_demo_cohort(n_stays=20, seed=0)
    assert len(seqs) == 20
    assert len(ids) == 20
    assert set(labels) <= {0, 1}
    assert seqs[0].shape[0] == SEQUENCE_HOURS


def test_auroc_perfect_ranking():
    y = np.array([0, 0, 1, 1])
    p = np.array([0.1, 0.2, 0.8, 0.9])
    report = compute_discrimination(y, p)
    assert report.auroc == 1.0


def test_ece_perfect():
    y = np.array([0, 0, 1, 1], dtype=float)
    p = np.array([0.0, 0.0, 1.0, 1.0])
    assert expected_calibration_error(y, p, n_bins=2) == 0.0


def test_risk_language_not_fatalistic():
    text = format_probability_statement(0.42, lang="en")
    assert "42%" in text
    assert "Moderate" in risk_band(0.15, lang="en") or "moderate" in risk_band(0.15, lang="en").lower()
    assert "modéré" in risk_band(0.15, lang="fr").lower() or "Risque" in risk_band(0.15, lang="fr")


def test_friendly_feature_name():
    from src.ui_format import friendly_feature_name

    assert "Heart rate" in friendly_feature_name("heart_rate_mean_6h", "en")
    assert "6h" in friendly_feature_name("heart_rate_mean_6h", "en")
    assert "Fréquence" in friendly_feature_name("heart_rate_slope_24h", "fr")


def test_stay_id_from_choice():
    from src.ui_format import stay_id_from_choice

    assert stay_id_from_choice("demo-0003 · Calmer vitals (demo)") == "demo-0003"
    assert stay_id_from_choice("demo-0001  (label=1)") == "demo-0001"


def test_i18n_has_no_forbidden_filler():
    from src.i18n import COPY

    banned = ("simply", " just ", "easy", "feel free", "this project demonstrates", " — ")
    for lang, strings in COPY.items():
        blob = " ".join(strings.values()).lower()
        for word in banned:
            assert word not in blob, f"{lang} still contains {word!r}"
        for key, value in strings.items():
            assert "—" not in value, f"{lang}.{key} still uses an em dash"


def test_german_italian_and_mandarin_copy():
    from src.i18n import COPY, normalize_lang, t
    from src.ui_format import friendly_feature_name

    assert normalize_lang("de") == "de"
    assert normalize_lang("it") == "it"
    assert normalize_lang("zh") == "zh"
    assert normalize_lang("中文") == "zh"
    assert normalize_lang("pt") == "pt"
    assert normalize_lang("ru") == "ru"
    assert normalize_lang("русский") == "ru"
    assert "Herzfrequenz" in friendly_feature_name("heart_rate_mean_6h", "de")
    assert "Frequenza" in friendly_feature_name("heart_rate_mean_6h", "it")
    assert "心率" in friendly_feature_name("heart_rate_mean_6h", "zh")
    assert "Frequência" in friendly_feature_name("heart_rate_mean_6h", "pt")
    assert "сердечных" in friendly_feature_name("heart_rate_mean_6h", "ru")
    assert t("run", "de") == "Risiko schätzen"
    assert t("run", "it") == "Stima il rischio"
    assert t("run", "zh") == "估算风险"
    assert t("run", "pt") == "Estimar o risco"
    assert t("run", "ru") == "Оценить риск"
    assert set(COPY) >= {"en", "fr", "de", "it", "zh", "pt", "ru"}


def test_plot_labels_follow_language_and_cjk_font():
    import matplotlib

    matplotlib.use("Agg")
    import pandas as pd

    from src.explain.fonts import cjk_font_name
    from src.explain.plots import plot_shap_heatmap, plot_vital_trajectory
    from src.i18n import t

    assert cjk_font_name() is not None

    sequence = pd.DataFrame(
        {
            "heart_rate": [70.0, 72.0, 71.0],
            "sys_bp": [120.0, 118.0, 119.0],
            "dias_bp": [70.0, 68.0, 69.0],
            "resp_rate": [16.0, 17.0, 16.0],
            "spo2": [98.0, 97.0, 98.0],
            "temperature_c": [36.8, 36.9, 36.8],
        }
    )
    matrix = pd.DataFrame(
        [[0.1, -0.2, 0.05]],
        index=["heart_rate"],
        columns=["6h", "24h", "48h"],
    )

    traj = plot_vital_trajectory(sequence, title=t("trajectory", "zh"), lang="zh")
    heat = plot_shap_heatmap(matrix, title=t("heatmap", "zh"), lang="zh")
    assert "48" in traj._suptitle.get_text() or "生命" in traj._suptitle.get_text()
    assert "生命" in traj._suptitle.get_text() or "体征" in traj._suptitle.get_text()
    assert heat.axes[0].get_title()
    assert "心率" in [t.get_text() for t in heat.axes[0].get_yticklabels()]
    assert "小时" in heat.axes[0].xaxis.label.get_text() or "回看" in heat.axes[0].xaxis.label.get_text()

    fr = plot_vital_trajectory(sequence, lang="fr")
    assert "Heure" in fr.axes[0].xaxis.label.get_text()

