"""Visual layer: Streamlit inject + optional Gradio theme helpers."""

from __future__ import annotations

import streamlit as st

from src.config import COLOR_ACCENT, COLOR_ACCENT_DEEP

APP_MAX_WIDTH_PX = 960
BUTTON_HEIGHT_PX = 44

COLOR_BODY = "#0a0a0a"
COLOR_SECONDARY = "#333333"
COLOR_PANEL = "#ffffff"
COLOR_PAGE = "#ffffff"
COLOR_BORDER = "#d0d0d0"
COLOR_ACCENT_SOFT = "#e8f2ec"

APP_CSS = f"""
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=Fraunces:opsz,wght@9..144,600;9..144,700&display=swap');

/* Override Gradio theme tokens Soft uses for grey blocks */
.gradio-container,
.gradio-container .main,
html {{
  --body-background-fill: {COLOR_PAGE} !important;
  --background-fill-primary: {COLOR_PANEL} !important;
  --background-fill-secondary: {COLOR_PANEL} !important;
  --block-background-fill: {COLOR_PANEL} !important;
  --block-label-background-fill: {COLOR_PANEL} !important;
  --block-title-background-fill: {COLOR_PANEL} !important;
  --border-color-primary: {COLOR_BORDER} !important;
  --body-text-color: {COLOR_BODY} !important;
  --body-text-color-subdued: {COLOR_SECONDARY} !important;
  --block-label-text-color: {COLOR_BODY} !important;
  --block-title-text-color: {COLOR_BODY} !important;
  --neutral-50: #ffffff !important;
  --neutral-100: #ffffff !important;
  --neutral-200: #e8eef0 !important;
  --neutral-300: {COLOR_BORDER} !important;
  --neutral-600: {COLOR_SECONDARY} !important;
  --neutral-700: {COLOR_BODY} !important;
  --neutral-800: {COLOR_BODY} !important;
  --neutral-900: {COLOR_BODY} !important;
  --color-accent: {COLOR_ACCENT} !important;
}}

.gradio-container {{
  font-family: 'DM Sans', 'Segoe UI', sans-serif !important;
  max-width: {APP_MAX_WIDTH_PX}px !important;
  margin-left: auto !important;
  margin-right: auto !important;
  color: {COLOR_BODY} !important;
  background: {COLOR_PAGE} !important;
}}

.gradio-container .main,
.gradio-container .wrap,
.gradio-container .contain {{
  background: {COLOR_PAGE} !important;
  color: {COLOR_BODY} !important;
}}

/* Flatten every nested Gradio surface to white + dark text */
.gradio-container .block,
.gradio-container .gr-group,
.gradio-container .form,
.gradio-container .panel,
.gradio-container .html-container,
.gradio-container .padding,
.gradio-container .prose,
.gradio-container .md,
.gradio-container .markdown,
.gradio-container .svelte-phx28p,
.gradio-container .svelte-lag733,
.gradio-container .svelte-7ddecg,
.gradio-container .svelte-1nguped,
.gradio-container .svelte-vuh1yp,
.gradio-container .svelte-ydeks8,
.gradio-container [class*="html-container"],
.gradio-container [class*="prose"] {{
  background: {COLOR_PANEL} !important;
  background-color: {COLOR_PANEL} !important;
  color: {COLOR_BODY} !important;
}}

.gradio-container .block *,
.gradio-container .gr-group *,
.gradio-container .html-container *,
.gradio-container .prose *,
.gradio-container .md *,
.gradio-container .markdown * {{
  color: {COLOR_BODY} !important;
}}

.gradio-container .prose em,
.gradio-container .md em {{
  color: {COLOR_SECONDARY} !important;
}}

.gradio-container label,
.gradio-container .info-text {{
  color: {COLOR_BODY} !important;
}}

footer, .footer {{
  display: none !important;
}}

/* Self-contained cards with inline-proof classes */
.icu-card {{
  background: #ffffff !important;
  color: #0b1f26 !important;
  border: 1px solid {COLOR_BORDER} !important;
  border-radius: 12px !important;
  padding: 16px !important;
  margin: 0 0 16px 0 !important;
}}

.icu-card h2,
.icu-card .icu-panel-title {{
  margin: 0 0 8px 0 !important;
  font-size: 0.78rem !important;
  font-weight: 700 !important;
  letter-spacing: 0.05em !important;
  text-transform: uppercase !important;
  color: {COLOR_ACCENT_DEEP} !important;
}}

.icu-hero {{
  margin-bottom: 24px;
  color: {COLOR_BODY} !important;
}}

.icu-hero h1 {{
  font-family: 'Fraunces', Georgia, serif !important;
  font-weight: 700 !important;
  letter-spacing: -0.02em;
  color: #0d3d28 !important;
  font-size: 1.75rem !important;
  line-height: 1.25 !important;
  margin: 0 0 12px 0 !important;
}}

.icu-eyebrow {{
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: {COLOR_ACCENT_DEEP} !important;
  margin-bottom: 8px;
}}

.icu-lede {{
  color: {COLOR_SECONDARY} !important;
  font-size: 1rem;
  line-height: 1.55;
  max-width: 38rem;
  margin: 0 0 12px 0;
}}

.icu-what {{
  background: #ffffff !important;
  border: 1px solid {COLOR_BORDER};
  border-radius: 12px;
  padding: 12px 16px;
  margin: 0 0 16px 0;
  color: {COLOR_BODY} !important;
  font-size: 0.95rem;
  line-height: 1.5;
}}

.icu-what strong {{
  color: {COLOR_ACCENT_DEEP} !important;
}}

.icu-disclaimer {{
  color: {COLOR_SECONDARY} !important;
  font-size: 0.88rem;
  line-height: 1.45;
  margin: 0;
}}

.icu-status {{
  min-height: 1.35rem;
  color: {COLOR_ACCENT_DEEP} !important;
  font-size: 0.92rem;
  font-weight: 700;
  margin: 0 0 12px 0;
}}
.icu-status.is-busy {{
  opacity: 0.75;
}}
.icu-status.is-error {{
  color: #7a2e22 !important;
}}

#icu-actions {{
  gap: 12px !important;
  align-items: stretch !important;
  margin-bottom: 8px !important;
}}

#icu-run-btn,
#icu-reset-btn {{
  flex: 1 1 0 !important;
  min-width: 0 !important;
}}

#icu-run-btn button,
#icu-reset-btn button {{
  width: 100% !important;
  height: {BUTTON_HEIGHT_PX}px !important;
  min-height: {BUTTON_HEIGHT_PX}px !important;
  max-height: {BUTTON_HEIGHT_PX}px !important;
  padding: 0 16px !important;
  border-radius: 10px !important;
  font-size: 0.92rem !important;
  line-height: 1 !important;
  white-space: nowrap !important;
  box-sizing: border-box !important;
}}

#icu-run-btn button {{
  background: {COLOR_ACCENT_DEEP} !important;
  color: #ffffff !important;
  border: 1px solid {COLOR_ACCENT_DEEP} !important;
  font-weight: 700 !important;
}}
#icu-run-btn button:hover {{
  background: {COLOR_ACCENT} !important;
}}

#icu-reset-btn button {{
  background: #ffffff !important;
  color: {COLOR_BODY} !important;
  border: 1px solid {COLOR_BORDER} !important;
  font-weight: 600 !important;
}}
#icu-reset-btn button:hover {{
  background: #e8f1f2 !important;
}}

#icu-lang label,
#icu-stay label {{
  color: {COLOR_BODY} !important;
  font-weight: 700 !important;
}}

#icu-sidebar {{
  background: {COLOR_PANEL} !important;
}}

.icu-sidebar-hint {{
  color: {COLOR_SECONDARY} !important;
  font-size: 0.9rem !important;
  margin: 0 0 8px 0 !important;
}}

#icu-lang {{
  width: 100% !important;
  max-width: 100% !important;
}}

#icu-lang,
#icu-lang .form,
#icu-lang .wrap {{
  background: #ffffff !important;
  background-color: #ffffff !important;
}}

#icu-lang input,
#icu-lang .secondary-wrap {{
  background: #ffffff !important;
  color: {COLOR_BODY} !important;
  border-color: {COLOR_BORDER} !important;
  font-weight: 600 !important;
}}

#icu-reset-btn button {{
  width: 100% !important;
}}

.icu-risk-pct {{
  font-family: 'Fraunces', Georgia, serif;
  font-size: 2.75rem;
  font-weight: 700;
  color: {COLOR_ACCENT_DEEP} !important;
  line-height: 1;
  margin: 0 0 12px 0;
}}

.icu-risk-band {{
  font-size: 1.05rem;
  font-weight: 700;
  color: {COLOR_BODY} !important;
  margin: 0 0 8px 0;
}}

.icu-risk-explain {{
  font-size: 0.95rem;
  color: {COLOR_SECONDARY} !important;
  line-height: 1.5;
  margin: 0 0 12px 0;
}}

.icu-chip {{
  display: inline-block;
  background: #e8f1f2 !important;
  color: {COLOR_ACCENT_DEEP} !important;
  border: 1px solid {COLOR_BORDER};
  border-radius: 6px;
  padding: 4px 12px;
  font-size: 0.8rem;
  font-weight: 700;
}}

.icu-muted {{
  color: {COLOR_SECONDARY} !important;
  font-size: 0.88rem;
  line-height: 1.45;
  margin-top: 12px;
}}

.icu-hint {{
  color: {COLOR_SECONDARY} !important;
  font-size: 0.88rem;
  margin: 0 0 16px 0;
}}

.icu-driver-list {{
  margin: 12px 0 0 0;
  padding-left: 18px;
  color: {COLOR_BODY} !important;
}}

.icu-driver-list li {{
  margin-bottom: 8px;
  color: {COLOR_BODY} !important;
}}

.matplotlib {{
  background: #ffffff !important;
  width: 100% !important;
}}

.matplotlib img,
.icu-plot img,
.gradio-container img.svelte-j1jcu3 {{
  width: 100% !important;
  max-width: 100% !important;
  height: auto !important;
  display: block !important;
}}

/* Stretch vitals chart so matplotlib title + signals stay readable */
.icu-plot-traj,
.icu-plot-traj .matplotlib {{
  width: 100% !important;
}}

.icu-plot-traj img {{
  width: 100% !important;
  min-height: 560px !important;
  object-fit: contain !important;
  background: #ffffff !important;
}}

/* Stop Gradio columns collapsing to min(0px, 100%) and clipping plots */
.gradio-container .column,
.gradio-container .block {{
  min-width: 0 !important;
  max-width: 100% !important;
}}

.gradio-container .contain {{
  width: 100% !important;
  max-width: 960px !important;
}}
"""


def inject_styles() -> None:
    """Force white page, dark-green accent, white primary-button text."""
    css = f"""
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=Fraunces:opsz,wght@9..144,600;9..144,700&display=swap');

:root {{
  --primary-color: #0d3d28;
  --background-color: #ffffff;
  --secondary-background-color: #ffffff;
  --text-color: #0a0a0a;
}}

html, body, .stApp, [data-testid="stAppViewContainer"],
[data-testid="stMain"], [data-testid="stMainBlockContainer"],
.block-container, .main, section.main {{
  background: #ffffff !important;
  background-color: #ffffff !important;
  color: #0a0a0a !important;
  font-family: 'DM Sans', 'Helvetica Neue', sans-serif !important;
}}

section[data-testid="stSidebar"],
[data-testid="stSidebarContent"],
[data-testid="stSidebarUserContent"],
section[data-testid="stSidebar"] > div {{
  background: #ffffff !important;
  background-color: #ffffff !important;
  color: #0a0a0a !important;
  border-right: 1px solid #d0d0d0 !important;
}}

.block-container {{
  /* Clear the floating sidebar-toggle / Deploy toolbar so it does not overlap the hero title */
  padding-top: 4.5rem !important;
  padding-bottom: 2rem !important;
  max-width: {APP_MAX_WIDTH_PX}px;
}}

.icu-hero {{
  margin-top: 0.5rem !important;
}}

#MainMenu, footer {{ visibility: hidden; }}

/* Top toolbar / header: transparent over white page */
header[data-testid="stHeader"],
.stAppHeader,
[data-testid="stToolbar"],
.stAppToolbar,
div[data-testid="stDecoration"] {{
  background: transparent !important;
  background-color: transparent !important;
  box-shadow: none !important;
  border: none !important;
}}
header[data-testid="stHeader"]::before {{
  background: transparent !important;
}}

.stMarkdown p, .stMarkdown li,
[data-testid="stMarkdownContainer"] p,
[data-testid="stWidgetLabel"] p,
label {{
  color: #0a0a0a !important;
}}

/* Estimate risk: white text on dark green */
div[data-testid="stButton"] > button[kind="primary"],
button[kind="primary"],
button[data-testid="stBaseButton-primary"],
[data-testid="stBaseButton-primary"] {{
  background-color: #0d3d28 !important;
  background-image: none !important;
  border: 1px solid #0d3d28 !important;
  color: #ffffff !important;
}}
div[data-testid="stButton"] > button[kind="primary"] *,
button[kind="primary"] *,
button[data-testid="stBaseButton-primary"] *,
[data-testid="stBaseButton-primary"] * {{
  color: #ffffff !important;
}}
div[data-testid="stButton"] > button[kind="primary"]:hover,
button[data-testid="stBaseButton-primary"]:hover {{
  background-color: #1a5c3a !important;
  border-color: #1a5c3a !important;
  color: #ffffff !important;
}}

button[kind="secondary"],
[data-testid="stBaseButton-secondary"] {{
  background: #ffffff !important;
  border: 1px solid #d0d0d0 !important;
  color: #0a0a0a !important;
}}

.icu-eyebrow {{
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #0d3d28 !important;
  margin-bottom: 0.35rem;
}}
.icu-title {{
  display: block !important;
  font-family: 'Fraunces', Georgia, serif !important;
  font-weight: 700 !important;
  font-size: clamp(1.65rem, 4vw, 2.4rem) !important;
  line-height: 1.15 !important;
  letter-spacing: -0.02em !important;
  color: #0d3d28 !important;
  margin: 0 0 0.75rem 0 !important;
}}
.icu-lede, .icu-what {{ color: #0a0a0a !important; line-height: 1.55; }}
.icu-disclaimer {{ color: #333333 !important; font-size: 0.9rem; }}
.icu-status {{ color: #0d3d28 !important; font-weight: 600; margin: 0.5rem 0 1rem 0; }}
.icu-card, .icu-panel {{
  background: #ffffff !important;
  border: 1px solid #d0d0d0 !important;
  border-radius: 12px;
  padding: 1rem 1.1rem;
  margin: 0 0 1rem 0;
  color: #0a0a0a !important;
}}
.icu-panel-title {{ font-weight: 700; color: #0d3d28 !important; margin-bottom: 0.5rem; }}
.icu-risk-pct {{
  font-family: 'Fraunces', Georgia, serif;
  font-size: 2.75rem;
  font-weight: 700;
  color: #0d3d28 !important;
  line-height: 1;
  margin: 0 0 12px 0;
}}
.icu-chip {{ background: #e8f2ec !important; color: #0d3d28 !important; }}

/* Demo-patient select: readable text + visible border (avoid white-on-white) */
div[data-testid="stSelectbox"] label p {{
  color: #0a0a0a !important;
  font-weight: 600 !important;
}}
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {{
  background-color: #ffffff !important;
  border: 1.5px solid #0d3d28 !important;
  border-radius: 8px !important;
  color: #0a0a0a !important;
  min-height: 44px !important;
  box-shadow: none !important;
}}
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:hover {{
  border-color: #1a5c3a !important;
}}
div[data-testid="stSelectbox"] div[data-baseweb="select"] span,
div[data-testid="stSelectbox"] div[data-baseweb="select"] svg {{
  color: #0a0a0a !important;
  fill: #0a0a0a !important;
}}
ul[role="listbox"],
div[data-baseweb="popover"] ul,
div[data-baseweb="menu"] {{
  background-color: #ffffff !important;
  border: 1px solid #d0d0d0 !important;
}}
ul[role="listbox"] li,
div[data-baseweb="menu"] li {{
  background-color: #ffffff !important;
  color: #0a0a0a !important;
}}
ul[role="listbox"] li:hover,
div[data-baseweb="menu"] li:hover {{
  background-color: #e8f2ec !important;
}}

/* Arabic RTL: mirror text flow and list/legend indents; charts stay LTR images */
html[dir="rtl"] body,
html[dir="rtl"] .stApp,
html[dir="rtl"] .block-container {{
  direction: rtl;
  text-align: right;
}}
html[dir="rtl"] section[data-testid="stSidebar"],
html[dir="rtl"] [data-testid="stSidebarContent"] {{
  text-align: right;
}}
html[dir="rtl"] .stMarkdown p,
html[dir="rtl"] .stMarkdown li,
html[dir="rtl"] [data-testid="stMarkdownContainer"] p,
html[dir="rtl"] [data-testid="stMarkdownContainer"] li,
html[dir="rtl"] [data-testid="stCaptionContainer"],
html[dir="rtl"] label {{
  text-align: right;
}}
html[dir="rtl"] .icu-driver-list,
html[dir="rtl"] [data-testid="stMarkdownContainer"] ul,
html[dir="rtl"] [data-testid="stMarkdownContainer"] ol {{
  padding-right: 18px;
  padding-left: 0;
}}
html[dir="rtl"] .icu-eyebrow,
html[dir="rtl"] .icu-title,
html[dir="rtl"] .icu-lede,
html[dir="rtl"] .icu-what,
html[dir="rtl"] .icu-disclaimer,
html[dir="rtl"] .icu-status,
html[dir="rtl"] .icu-risk-pct,
html[dir="rtl"] .icu-risk-band,
html[dir="rtl"] .icu-risk-explain {{
  text-align: right;
}}
"""
    try:
        st.html(f"<style>{css}</style>")
    except Exception:
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def apply_direction(lang: str) -> None:
    """Apply RTL/LTR direction via CSS (Cloud-safe; no components.v1.html)."""
    direction = "rtl" if lang == "ar" else "ltr"
    st.markdown(
        f"""
        <style>
          html, body,
          [data-testid="stAppViewContainer"],
          [data-testid="stSidebar"],
          [data-testid="stSidebarContent"],
          section.main, .block-container {{
            direction: {direction};
          }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def theme():
    """Optional Gradio theme helper (unused by Streamlit app)."""
    return None
