# 90-second talking points

## Opening (15s)
“I built a portfolio demo that estimates 48-hour ICU mortality from vital signs
and shows which time windows drove the score — because a naked probability is
not enough for clinical audiences.”

## Method (25s)
“I use six vitals on an hourly 48-hour grid. Cleaning is clinical: implausible
values become missing, missingness is flagged, short gaps forward-fill, then
training medians. I start with a calibrated logistic model on 6/24/48-hour
aggregates — not LSTM-first — so I can explain and calibrate cleanly.”

## Demo beat (25s)
“In Gradio you pick a stay, see a risk band with uncertainty language, a SHAP
heatmap over vitals and lookback windows, and the trajectory. Red cells raised
the model’s risk; they don’t prove causation.”

## Metrics (15s)
“I report AUROC, PR-AUC, and ECE with a calibration curve. On MIMIC I’ll quote
held-out patient-level splits; today the live demo is synthetic so anyone can
run it without PhysioNet access.”

## Close (10s)
“I’m targeting clinical data science in Geneva and Basel. I want teams that
care whether a number deserves to be shown — not only whether it ranks well.”

## If asked “why not deep learning?”
“LSTM is on a checklist: it has to beat this baseline on the same split without
breaking calibration, and I need attribution ready. Complexity is earned.”
