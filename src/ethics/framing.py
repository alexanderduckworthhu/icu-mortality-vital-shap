"""Clinician-facing language for mortality risk estimates and uncertainty."""

from __future__ import annotations

from src.config import (
    DISCLAIMER_EN,
    DISCLAIMER_FR,
    RISK_BAND_ELEVATED_MAX,
    RISK_BAND_LOW_MAX,
    RISK_BAND_MODERATE_MAX,
)
from src.i18n import normalize_lang, t


def risk_band_key(probability: float) -> str:
    """Return the i18n key for the coarse risk band."""
    if probability < RISK_BAND_LOW_MAX:
        return "band_low"
    if probability < RISK_BAND_MODERATE_MAX:
        return "band_moderate"
    if probability < RISK_BAND_ELEVATED_MAX:
        return "band_elevated"
    return "band_high"


def risk_band(probability: float, lang: str = "en") -> str:
    """Map a probability to a coarse risk-band phrase for the UI."""
    return t(risk_band_key(probability), lang)


def risk_explain_key(probability: float) -> str:
    """Return the i18n key for the plain-language risk explanation."""
    if probability < RISK_BAND_MODERATE_MAX:
        return "risk_explain_low"
    if probability < RISK_BAND_ELEVATED_MAX:
        return "risk_explain_mid"
    return "risk_explain_high"


def format_probability_statement(probability: float, lang: str = "en") -> str:
    """Return a short estimate sentence for tests and plain text contexts."""
    lang = normalize_lang(lang)
    pct = int(round(probability * 100))
    band = risk_band(probability, lang=lang)
    return t("about_pct", lang).format(pct=pct, band=band)


def uncertainty_bullets(lang: str = "en") -> list[str]:
    """Return short uncertainty bullets for the ethics accordion."""
    return [
        t("uncertainty_1", lang),
        t("uncertainty_2", lang),
        t("uncertainty_3", lang),
        t("uncertainty_4", lang),
    ]


def intended_use_block(lang: str = "en") -> str:
    """Return intended-use / not-for copy for the ethics accordion."""
    return t("intended_use", lang)


def disclaimer(lang: str = "en") -> str:
    """Return the full legal-style disclaimer string."""
    lang = normalize_lang(lang)
    if lang == "fr":
        return DISCLAIMER_FR
    # DE/IT use the short UI disclaimer via i18n; keep EN legal text as fallback.
    return DISCLAIMER_EN
