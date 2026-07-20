# Methods

## Task

Estimate the probability of death within **48 hours** given the preceding
**48 hours** of vital signs, and attribute that estimate to vital × time windows.

## Preprocessing (clinical data science practice)

Pipeline implemented in `src/preprocess/`:

1. **Resample to 1-hour means**  
   Irregular `CHARTTIME` → hourly grid. Hourly is sparse-but-usable for
   non-invasive vitals over 48h.

2. **Plausibility bounds → NaN** (`PLAUSIBLE_RANGES` in `src/config.py`)  
   SpO₂ 0% from a disconnected probe is not “severe hypoxia” for modeling;
   it is missing data. We do **not** clip to the bound (that invents values).

3. **Missingness indicators before imputation**  
   ICU missingness is informative. Each vital gets a `*_missing` flag on the
   hourly grid; window miss-rates enter the baseline feature set.

4. **Limited forward-fill (2 hours)**  
   Short gaps ≈ charting cadence. Long gaps stay missing rather than drawing
   a smooth fantasy trajectory.

5. **Final fill with training-set medians**  
   Robust to skew. Medians are frozen at train time and reused at inference.

6. **Fixed length 48**  
   Trim oldest hours or pad the front with NaNs (then imputed). Prediction
   always uses the most recent window.

### Why not fancy multivariate imputation in v1?

MICE / MissForest are valid research tools, but they complicate auditability
for an entry-level portfolio and can leak future information if mis-specified.
Transparent rules + missingness flags are the better first story.

## Feature engineering (baseline)

For each vital and lookback window ∈ {6h, 24h, 48h}:

- mean, min, max, last value  
- linear slope  
- missingness rate  

This preserves a readable SHAP story: “last 6h SpO₂ slope” rather than a
hidden state.

## Model choice: baseline first, LSTM later

| | Logistic baseline | LSTM |
|--|-------------------|------|
| Data need | Modest | Higher; overfits small extracts |
| Calibration | Straightforward (isotonic / Platt) | Easy to break |
| Explanation | Tabular SHAP → window heatmap | Needs DeepSHAP / gradients |
| Debug cycle | Hours | Days |
| Interview story | “I set a floor” | “I earned complexity” |

**Start with the baseline.** Promote LSTM only when the checklist in
`src/models/lstm.py` is honestly true.

Implementation: `src/models/baseline.py`, `StandardScaler` → L2 logistic with
`class_weight='balanced'` → `CalibratedClassifierCV(method='isotonic')`.

## SHAP time-window attribution

1. KernelSHAP on the engineered feature vector (works with calibration wrapper).  
2. Aggregate feature SHAP values onto a **vital × window** matrix.  
3. Plot heatmap (`src/explain/plots.py`), red raises predicted risk, blue lowers.

Example reading: strong positive SHAP on `spo2_mean_6h` and `spo2_slope_6h`
means the model’s elevated score was driven by recent oxygenation pattern , 
a clinician can then look at the trajectory panel and accept or reject that
emphasis.

**Caveat to say out loud:** attribution is to the *model’s computation*, not
a causal claim that SpO₂ “caused” death.

## Metrics & what “good” looks like

### Discrimination

- **AUROC:** ranking quality. For vital-only short-horizon ICU mortality,
  published results vary by cohort; treat **~0.75–0.85** as a rough
  orientation band for a serious vital-sign baseline, not a pass/fail grade.
- **PR-AUC:** always report under class imbalance; a high AUROC can coexist
  with weak precision at useful operating points.

### Calibration

- Plot reliability curve (`calibration_curve`, quantile bins).  
- Report **ECE** (expected calibration error).  
- Orientation: **ECE ≲ 0.05–0.08** with a curve near the diagonal in
  populated mid-risk bins is a healthy target. Overconfident high-risk bins
  are especially dangerous ethically.

### What to put in the writeup

| Must show | Why |
|-----------|-----|
| AUROC + PR-AUC on held-out stays | Discrimination |
| Calibration curve + ECE | Probability meaning |
| Sample size + positive rate | Context for both |
| Subgroup or era check (CareVue vs Metavision) if sample allows | Drift honesty |

Demo metrics in `data/processed/demo_metrics.json` are **synthetic**, label
them as such until MIMIC results exist.

## Evaluation hygiene

- Split by **patient** (`SUBJECT_ID`), not row, when using MIMIC, prevents
  leakage across stays.
- Fix seed (`RANDOM_SEED`).
- Do not tune on the final test set; use a validation split or CV for
  calibration / thresholds.
