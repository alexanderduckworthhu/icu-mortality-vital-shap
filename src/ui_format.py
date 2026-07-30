"""Presentation helpers for Gradio panels. Keep app.py thin."""

from __future__ import annotations

from dataclasses import dataclass

from src.config import CURATED_STAYS_PER_OUTCOME, FEATURE_WINDOWS_HOURS, VITAL_COLUMNS
from src.ethics.framing import (
    intended_use_block,
    risk_band,
    risk_explain_key,
    uncertainty_bullets,
)
from src.i18n import normalize_lang, t

_VITAL_LABELS: dict[str, dict[str, str]] = {
    "en": {
        "heart_rate": "Heart rate",
        "sys_bp": "Systolic blood pressure",
        "dias_bp": "Diastolic blood pressure",
        "resp_rate": "Respiratory rate",
        "spo2": "Oxygen saturation (SpO₂)",
        "temperature_c": "Temperature",
    },
    "fr": {
        "heart_rate": "Fréquence cardiaque",
        "sys_bp": "Pression artérielle systolique",
        "dias_bp": "Pression artérielle diastolique",
        "resp_rate": "Fréquence respiratoire",
        "spo2": "Saturation en oxygène (SpO₂)",
        "temperature_c": "Température",
    },
    "de": {
        "heart_rate": "Herzfrequenz",
        "sys_bp": "Systolischer Blutdruck",
        "dias_bp": "Diastolischer Blutdruck",
        "resp_rate": "Atemfrequenz",
        "spo2": "Sauerstoffsättigung (SpO₂)",
        "temperature_c": "Temperatur",
    },
    "it": {
        "heart_rate": "Frequenza cardiaca",
        "sys_bp": "Pressione arteriosa sistolica",
        "dias_bp": "Pressione arteriosa diastolica",
        "resp_rate": "Frequenza respiratoria",
        "spo2": "Saturazione di ossigeno (SpO₂)",
        "temperature_c": "Temperatura",
    },
    "zh": {
        "heart_rate": "心率",
        "sys_bp": "收缩压",
        "dias_bp": "舒张压",
        "resp_rate": "呼吸频率",
        "spo2": "血氧饱和度 (SpO₂)",
        "temperature_c": "体温",
    },
    "pt": {
        "heart_rate": "Frequência cardíaca",
        "sys_bp": "Pressão arterial sistólica",
        "dias_bp": "Pressão arterial diastólica",
        "resp_rate": "Frequência respiratória",
        "spo2": "Saturação de oxigénio (SpO₂)",
        "temperature_c": "Temperatura",
    },
    "ru": {
        "heart_rate": "Частота сердечных сокращений",
        "sys_bp": "Систолическое давление",
        "dias_bp": "Диастолическое давление",
        "resp_rate": "Частота дыхания",
        "spo2": "Насыщение кислородом (SpO₂)",
        "temperature_c": "Температура",
    },
}

_STAT_LABELS: dict[str, dict[str, str]] = {
    "en": {
        "mean": "average",
        "min": "lowest",
        "max": "highest",
        "last": "latest value",
        "slope": "trend",
        "missrate": "how often missing",
    },
    "fr": {
        "mean": "moyenne",
        "min": "plus bas",
        "max": "plus haut",
        "last": "dernière valeur",
        "slope": "tendance",
        "missrate": "part manquante",
    },
    "de": {
        "mean": "Durchschnitt",
        "min": "tiefster Wert",
        "max": "höchster Wert",
        "last": "letzter Wert",
        "slope": "Trend",
        "missrate": "wie oft fehlend",
    },
    "it": {
        "mean": "media",
        "min": "valore più basso",
        "max": "valore più alto",
        "last": "ultimo valore",
        "slope": "tendenza",
        "missrate": "quanto spesso mancante",
    },
    "zh": {
        "mean": "平均值",
        "min": "最低",
        "max": "最高",
        "last": "最新值",
        "slope": "趋势",
        "missrate": "缺失频率",
    },
    "pt": {
        "mean": "média",
        "min": "mais baixo",
        "max": "mais alto",
        "last": "último valor",
        "slope": "tendência",
        "missrate": "quão frequentemente em falta",
    },
    "ru": {
        "mean": "среднее",
        "min": "минимум",
        "max": "максимум",
        "last": "последнее значение",
        "slope": "тренд",
        "missrate": "как часто отсутствует",
    },
}


def friendly_feature_name(feature: str, lang: str = "en") -> str:
    """Convert feature keys like heart_rate_mean_6h into clinician-readable labels."""
    lang = normalize_lang(lang)
    vital = next((v for v in VITAL_COLUMNS if feature.startswith(v + "_")), None)
    if vital is None:
        return feature.replace("_", " ")
    rest = feature[len(vital) + 1 :]
    window = ""
    for hours in FEATURE_WINDOWS_HOURS:
        suffix = f"_{hours}h"
        if rest.endswith(suffix):
            window = f"{hours}h"
            rest = rest[: -len(suffix)]
            break
    labels = _STAT_LABELS.get(lang, _STAT_LABELS["en"])
    vital_labels = _VITAL_LABELS.get(lang, _VITAL_LABELS["en"])
    stat = labels.get(rest, rest)
    vital_label = vital_labels.get(vital, vital)
    window_text = t("window_phrase", lang).format(window=window)
    return f"{vital_label}, {stat} ({window_text})"


def format_drivers_html(
    top_drivers: list[tuple[str, float]],
    lang: str = "en",
) -> str:
    """Build an HTML card for the attribution list (avoids grey Markdown chrome)."""
    if not top_drivers:
        body = f'<p style="color:#333333;margin:0">{t("drivers_empty", lang)}</p>'
    else:
        items = []
        for feature_name, shap_value in top_drivers:
            direction = t("raised_risk" if shap_value > 0 else "lowered_risk", lang)
            items.append(
                "<li>"
                f"<strong style='color:#0a0a0a'>{friendly_feature_name(feature_name, lang)}</strong>"
                f"<span style='color:#333333'>: {direction}</span>"
                "</li>"
            )
        body = (
            f'<p style="color:#333333;margin:0 0 8px 0">{t("drivers_lede", lang)}</p>'
            f'<p style="color:#333333;margin:0 0 12px 0;font-size:0.9rem">'
            f'{t("heatmap_legend", lang)}</p>'
            f'<ul class="icu-driver-list">{"".join(items)}</ul>'
            f'<p style="color:#333333;margin:12px 0 0 0;font-size:0.9rem">'
            f'{t("trajectory_lede", lang)}</p>'
        )
    return (
        '<div class="icu-card" style="background:#ffffff;color:#0a0a0a;'
        'border:1px solid #d0d0d0;border-radius:12px;padding:16px">'
        f'<div class="icu-panel-title" style="color:#0d3d28">{t("drivers_heading", lang)}</div>'
        f"{body}"
        "</div>"
    )


def format_drivers_markdown(
    top_drivers: list[tuple[str, float]],
    lang: str = "en",
) -> str:
    """Compatibility wrapper; prefer format_drivers_html in the UI."""
    return format_drivers_html(top_drivers, lang)


def format_risk_html(
    probability: float,
    demo_label: int,
    lang: str = "en",
) -> str:
    """Build an HTML card for the primary risk panel with forced white background."""
    lang = normalize_lang(lang)
    pct = int(round(probability * 100))
    label_key = "label_demo_1" if demo_label == 1 else "label_demo_0"
    band = risk_band(probability, lang=lang)
    explain = t(risk_explain_key(probability), lang)
    return (
        '<div class="icu-card" style="background:#ffffff;color:#0a0a0a;'
        'border:1px solid #d0d0d0;border-radius:12px;padding:16px">'
        f'<div class="icu-panel-title" style="color:#0d3d28">{t("risk_heading", lang)}</div>'
        f'<p class="icu-risk-pct" style="color:#0d3d28" '
        f'aria-label="{t("risk_heading", lang)}: {pct}%">{pct}%</p>'
        f'<p class="icu-risk-band" style="color:#0a0a0a">{band}</p>'
        f'<p class="icu-risk-explain" style="color:#333333">{explain}</p>'
        f'<span class="icu-chip" style="background:#e8f2ec;color:#0d3d28">'
        f'{t(label_key, lang)}</span>'
        f'<div class="icu-muted" style="color:#333333">{t("label_hidden_note", lang)}</div>'
        "</div>"
    )


def format_ethics_markdown(lang: str = "en") -> str:
    """Build markdown for intended use and uncertainty bullets."""
    bullets = "\n".join(f"- {b}" for b in uncertainty_bullets(lang))
    return f"{intended_use_block(lang)}\n\n{bullets}"


def format_metrics_markdown(metrics: dict[str, float | int | str], lang: str = "en") -> str:
    """Build markdown summarizing discrimination and calibration metrics."""
    if not metrics:
        return f"_{t('metrics_missing', lang)}_"
    return "\n".join(
        [
            t("metrics_lede", lang),
            "",
            f"- AUROC: **{float(metrics.get('auroc', float('nan'))):.3f}**",
            f"- PR-AUC: **{float(metrics.get('pr_auc', float('nan'))):.3f}**",
            f"- ECE: **{float(metrics.get('ece', float('nan'))):.3f}**",
            f"- Train / test stays: **{metrics.get('n_train', '?')}** / "
            f"**{metrics.get('n_test', '?')}**",
        ]
    )


def format_hero_html(lang: str = "en") -> str:
    """Build the hero HTML block with a plain-language task explanation.

    Use a styled div for the title (not <h1>): Streamlit rewrites heading tags
    and drops inline color styles.
    """
    return (
        f'<div class="icu-hero">'
        f'<div class="icu-title" role="heading" aria-level="1">{t("title", lang)}</div>'
        f'<p class="icu-lede">{t("subtitle", lang)}</p>'
        f'<div class="icu-what">{t("what_it_shows", lang)}</div>'
        f'<p class="icu-disclaimer">{t("disclaimer_short", lang)}</p>'
        f"</div>"
    )


@dataclass(frozen=True)
class CuratedStay:
    """One demo stay exposed in the Gradio dropdown."""

    stay_id: str
    label: int
    choice_label: str


def curate_stay_choices(
    stay_ids: list[str],
    labels: list[int],
    lang: str = "en",
    n_each: int = CURATED_STAYS_PER_OUTCOME,
) -> list[CuratedStay]:
    """Return a short mixed list of quieter and higher-risk demo stays."""
    lang = normalize_lang(lang)
    quieter = [(sid, y) for sid, y in zip(stay_ids, labels) if y == 0]
    higher_risk = [(sid, y) for sid, y in zip(stay_ids, labels) if y == 1]
    picked = quieter[:n_each] + higher_risk[:n_each]
    if not picked:
        picked = list(zip(stay_ids[: n_each * 2], labels[: n_each * 2]))
    curated: list[CuratedStay] = []
    for stay_id, outcome_label in picked:
        tag = t("label_demo_1" if outcome_label == 1 else "label_demo_0", lang)
        curated.append(
            CuratedStay(
                stay_id=stay_id,
                label=outcome_label,
                choice_label=f"{stay_id} · {tag}",
            )
        )
    return curated


def default_curated_choice(choices: list[str]) -> str | None:
    """Prefer a higher-risk demo stay so attribution is visible on first load."""
    if not choices:
        return None
    for choice in choices:
        lowered = choice.lower()
        if any(
            token in lowered
            for token in ("unstable", "instable", "instabil", "instabile")
        ):
            return choice
    return choices[0]


def highlight_vital_from_drivers(
    top_drivers: list[tuple[str, float]],
) -> str | None:
    """Return the vital column name for the strongest absolute SHAP driver."""
    if not top_drivers:
        return None
    top_feature = top_drivers[0][0]
    for vital in VITAL_COLUMNS:
        if top_feature.startswith(vital):
            return vital
    return None


def stay_id_from_choice(choice: str) -> str:
    """Parse stay_id from 'demo-0003 · …' or legacy dashed labels."""
    if not choice:
        raise ValueError("empty stay choice")
    for separator in (" · ", ", ", " - ", "  ("):
        if separator in choice:
            return choice.split(separator)[0].strip()
    return choice.split("(")[0].strip()
