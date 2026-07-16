"""
Streamlit demo: 48-hour ICU mortality risk from vitals with SHAP window attribution.

Sidebar matches Where Needs Overlap: Language → hint → guide → reset.
Run: streamlit run app.py
"""

from __future__ import annotations

import json
import logging
import os
from functools import lru_cache
from typing import Any

# Avoid macOS GUI matplotlib crashes inside Streamlit workers.
os.environ.setdefault("MPLBACKEND", "Agg")

import matplotlib

matplotlib.use("Agg", force=True)
import matplotlib.pyplot as plt
import streamlit as st

from src.config import (
    CALIBRATION_PLOT_PATH,
    METRICS_PATH,
    MODEL_PATH,
    SAMPLE_DIR,
    SHAP_TOP_K_DRIVERS,
)
from src.demo_data import feature_table_from_demo, load_demo_sequences, save_demo_sample
from src.explain.plots import plot_shap_heatmap, plot_vital_trajectory
from src.explain.shap_timestep import explain_instance
from src.i18n import LANGUAGE_LABELS, SUPPORTED_LANGS, normalize_lang, t
from src.models.baseline import TrainedBaseline, load_model
from src.styles import inject_styles
from src.ui_format import (
    curate_stay_choices,
    default_curated_choice,
    format_drivers_html,
    format_ethics_markdown,
    format_hero_html,
    format_metrics_markdown,
    format_risk_html,
    highlight_vital_from_drivers,
    stay_id_from_choice,
)

logger = logging.getLogger(__name__)

# Bump when plot/CSS chrome changes so cached session figures are discarded.
UI_STYLE_VERSION = "green-v3-distinct-vitals"

DemoBundle = tuple[
    TrainedBaseline,
    list,
    list[str],
    list[int],
    Any,
    dict[str, float | int | str],
]

st.set_page_config(
    page_title="48-hour ICU survival risk",
    page_icon="◎",
    layout="wide",
    initial_sidebar_state="expanded",
)


def _ensure_artifacts() -> None:
    """Create demo CSV and trained model artifacts if they are missing."""
    try:
        if not (SAMPLE_DIR / "demo_vitals_long.csv").exists():
            save_demo_sample(SAMPLE_DIR)
        if not MODEL_PATH.exists():
            from scripts.train_baseline import main as train_main

            train_main()
    except (OSError, ValueError, ImportError) as exc:
        logger.exception("Failed to prepare demo artifacts")
        raise RuntimeError(
            "Could not prepare demo data or model. "
            "Run `python -m scripts.build_demo_data` then "
            "`python -m scripts.train_baseline`."
        ) from exc


@st.cache_resource(show_spinner=False)
def _load_bundle() -> DemoBundle:
    """Load model, sequences, labels, features, and metrics once per process."""
    _ensure_artifacts()
    model = load_model(MODEL_PATH)
    sequences, stay_ids, labels = load_demo_sequences(SAMPLE_DIR)
    features = feature_table_from_demo(SAMPLE_DIR)
    metrics: dict[str, float | int | str] = {}
    if METRICS_PATH.exists():
        try:
            metrics = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            logger.warning("Could not read metrics file %s: %s", METRICS_PATH, exc)
    return model, sequences, stay_ids, labels, features, metrics


def _choice_labels(lang: str) -> list[str]:
    """Return curated dropdown labels for the given UI language."""
    _, _, stay_ids, labels, _, _ = _load_bundle()
    return [c.choice_label for c in curate_stay_choices(stay_ids, labels, lang=lang)]


def _read_metrics(lang_key: str) -> str:
    """Load metrics markdown for the metrics expander."""
    if not METRICS_PATH.exists():
        return format_metrics_markdown({}, lang_key)
    try:
        payload = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return format_metrics_markdown({}, lang_key)
    return format_metrics_markdown(payload, lang_key)


def _estimate_for_stay(stay_choice: str, lang_key: str) -> dict[str, Any]:
    """Run model + SHAP for one stay; returns display payloads."""
    model, sequences, stay_ids, labels, features, metrics = _load_bundle()
    stay_id = stay_id_from_choice(stay_choice)
    stay_index = stay_ids.index(stay_id)
    sequence = sequences[stay_index]

    feature_row = features.loc[features["stay_id"] == stay_id].iloc[0]
    instance_features = feature_row.drop(labels=["stay_id", "label"])
    background_features = features.drop(columns=["stay_id", "label"])

    attribution = explain_instance(
        model,
        instance_features,
        background_features,
        top_k=SHAP_TOP_K_DRIVERS,
    )
    plt.close("all")

    heatmap_figure = plot_shap_heatmap(
        attribution.vital_window_matrix,
        title=t("heatmap", lang_key),
        lang=lang_key,
    )
    trajectory_figure = plot_vital_trajectory(
        sequence,
        highlight_vital=highlight_vital_from_drivers(attribution.top_drivers),
        title=t("trajectory", lang_key),
        lang=lang_key,
    )
    return {
        "status": t("status_done", lang_key),
        "risk_html": format_risk_html(
            attribution.probability, labels[stay_index], lang_key
        ),
        "drivers_html": format_drivers_html(attribution.top_drivers, lang_key),
        "heatmap": heatmap_figure,
        "trajectory": trajectory_figure,
        "ethics": format_ethics_markdown(lang_key),
        "metrics": format_metrics_markdown(metrics, lang_key),
    }


inject_styles()

# Drop stale chart HTML from before the latest color/CSS pass.
if st.session_state.get("ui_style_version") != UI_STYLE_VERSION:
    st.session_state.pop("last_estimate", None)
    st.session_state.pop("last_estimated_stay", None)
    st.session_state["ui_style_version"] = UI_STYLE_VERSION

# --- Sidebar (same pattern as Where Needs Overlap) ---
with st.sidebar:
    st.markdown("### Language")
    lang = st.selectbox(
        "Language",
        options=list(SUPPORTED_LANGS),
        format_func=lambda code: LANGUAGE_LABELS.get(code, code),
        key="ui_lang",
        label_visibility="collapsed",
    )
    lang = normalize_lang(lang)
    st.caption(t("sidebar_hint", lang))
    st.markdown(t("sidebar_guide", lang))
    st.markdown("---")
    if st.button(t("reset_view", lang), type="secondary", use_container_width=True):
        st.session_state.pop("stay_choice", None)
        st.session_state.pop("last_estimate", None)
        st.session_state.pop("last_estimated_stay", None)
        st.rerun()

# --- Main ---
st.markdown(format_hero_html(lang), unsafe_allow_html=True)

choices = _choice_labels(lang)
default_stay = default_curated_choice(choices)
if "stay_choice" not in st.session_state or st.session_state["stay_choice"] not in choices:
    # Keep the same stay_id across language switches when possible.
    previous = st.session_state.get("stay_choice", "")
    previous_id = ""
    if previous:
        try:
            previous_id = stay_id_from_choice(previous)
        except ValueError:
            previous_id = ""
    matched = next((c for c in choices if c.startswith(previous_id)), None) if previous_id else None
    st.session_state["stay_choice"] = matched or default_stay

stay_choice = st.selectbox(
    t("select_stay", lang),
    options=choices,
    key="stay_choice",
    help=t("select_stay_info", lang),
)

col_run, _ = st.columns([1, 3])
with col_run:
    run_clicked = st.button(t("run", lang), type="primary", use_container_width=True)

st.caption(t("run_hint", lang))

cache_key = (stay_choice, lang, UI_STYLE_VERSION)
should_run = bool(stay_choice) and (
    run_clicked or st.session_state.get("last_estimate_key") != cache_key
)

if not stay_choice:
    st.info(t("empty_stay", lang))
elif should_run:
    with st.spinner(t("status_loading", lang)):
        try:
            result = _estimate_for_stay(stay_choice, lang)
            st.session_state["last_estimate"] = result
            st.session_state["last_estimated_stay"] = stay_choice
            st.session_state["last_estimate_key"] = cache_key
        except (ValueError, KeyError, IndexError, OSError, RuntimeError) as exc:
            logger.exception("Prediction failed for stay_choice=%r: %s", stay_choice, exc)
            st.session_state.pop("last_estimate", None)
            st.session_state.pop("last_estimate_key", None)
            st.error(t("status_error", lang))

result = st.session_state.get("last_estimate")
if result and st.session_state.get("last_estimate_key") == cache_key:
    st.markdown(
        f'<p class="icu-status">{result["status"]}</p>',
        unsafe_allow_html=True,
    )
    st.markdown(result["risk_html"], unsafe_allow_html=True)
    st.markdown(result["drivers_html"], unsafe_allow_html=True)
    st.pyplot(result["heatmap"], clear_figure=False, width="stretch")
    st.pyplot(result["trajectory"], clear_figure=False, width="stretch")

    with st.expander(t("ethics_heading", lang), expanded=False):
        st.markdown(result["ethics"])

    with st.expander(t("metrics_heading", lang), expanded=False):
        st.markdown(result["metrics"] or _read_metrics(lang))
        if CALIBRATION_PLOT_PATH.exists():
            st.markdown(f"**{t('calibration', lang)}**")
            st.image(str(CALIBRATION_PLOT_PATH))
            st.caption(t("calibration_alt", lang))
elif stay_choice and "last_estimate" not in st.session_state:
    st.info(t("status_idle", lang))
