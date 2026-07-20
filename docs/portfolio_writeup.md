# Portfolio writeup frame (clinically thoughtful)

Use this structure for LinkedIn project posts, CV bullets, and case-study PDFs.
Tone: calm, specific, ethically awake, not “I built an AI that predicts death.”

## Headline options

- “Calibrated 48-hour ICU mortality risk from vitals, with SHAP window attribution”  
- “What should a clinician see when a model estimates mortality risk?”

## One-paragraph abstract

I built an entry-level clinical ML portfolio project that estimates 48-hour
ICU mortality from vital-sign time series and explains each score with SHAP
attributions over vital × lookback windows. I start with a calibrated logistic
baseline on clinically motivated aggregates (not an LSTM-first approach),
report discrimination and calibration, and treat uncertainty communication as
part of the deliverable. The public Gradio demo uses synthetic data; the
pipeline is designed to accept MIMIC-III after PhysioNet credentialing.

## CV bullet (tight)

- Designed a 48h ICU mortality risk pipeline (vitals → calibrated logistic →
  SHAP window heatmap) with explicit missingness handling, AUROC/PR-AUC/ECE
  reporting, and clinician-facing uncertainty language; Gradio demo + MIMIC-III
  access path documented for Geneva/Basel clinical data science roles.

## Section order employers actually finish

1. **Clinical question** (48h risk, not vague “AI in healthcare”)  
2. **Why this scope** (six vitals, baseline first)  
3. **One screenshot**: probability + SHAP heatmap + disclaimer visible  
4. **Metrics table** (label synthetic vs MIMIC)  
5. **Ethics paragraph** (calibration, non-use cases)  
6. **Next step** (MIMIC results, patient-level split, optional LSTM)

## Phrases to prefer / avoid

| Prefer | Avoid |
|--------|-------|
| Risk estimate / probability | Predicts who will die |
| Supports clinical reasoning | Replaces clinicians |
| Calibration / ECE | Accuracy alone |
| Model attribution (SHAP) | “AI found the cause” |
| Portfolio demo / research | Deployed in hospitals |
| Limitations documented | State-of-the-art claim |

## Tie to Swiss targets (light touch)

- **Unilabs / diagnostics-adjacent teams:** data quality, missingness, audit trails.  
- **Roche digital health:** calibration, explainability, responsible CDS framing.  
- **Startups:** shipping a thin vertical slice (demo + metrics + ethics) beats
  an unfinished deep learning thesis.

Do not name-drop as if you worked there. Show that you speak their language.
