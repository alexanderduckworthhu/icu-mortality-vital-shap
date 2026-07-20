# Limitations

- **Synthetic demo metrics ≠ clinical performance.** Replace before claiming
  relevance to Unilabs / Roche / startup product conversations.
- **Vitals-only** ignores labs, ventilation, vasopressors, comorbidities,
  and goals of care, major drivers of real mortality risk.
- **MIMIC-III** is a single US academic center (2001–2012 era mix); Swiss
  hospital practice and charting differ.
- **Label leakage risks** if death time and chart times are not carefully
  aligned; document exclusions.
- **KernelSHAP** is approximate and background-sensitive; attributions can
  shift with background sample size.
- **No fairness audit** yet (sex, age, service line).
- **Not a medical device**; no prospective validation, no human-factors study,
  no monitoring plan for calibration drift.
- **Class imbalance** means operating-point selection matters more than AUROC
  headlines, discuss alert burden if asked.
