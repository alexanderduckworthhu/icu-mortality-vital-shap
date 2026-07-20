# Ethics & uncertainty when showing a mortality estimate

You are not shipping a gadget. You are rehearsing how to speak about death
risk with humility. That is a feature for Geneva / Basel interviews, labs
and digital-health teams are rightly wary of overconfident ML.

## The moral object

A probability shown to a clinician can:

- **Help** by focusing attention on a deteriorating trajectory.  
- **Harm** by anchoring decisions, accelerating withdrawal-of-care bias,
  or creating self-fulfilling prophecies if treated as fate.  
- **Mislead** if uncalibrated (“20%” that is really 5% in this ward).

Your portfolio should prove you understand all three.

## Communication rules baked into the demo

Implemented in `src/ethics/framing.py` and the Gradio UI:

1. **Estimate, not verdict**, “about 42%” + risk band, never “will die.”  
2. **Intended use / not-for list**, support reasoning; not triage, rationing,
   or end-of-life determination.  
3. **Uncertainty bullets**, drift, missing clinical context, SHAP ≠ causation.  
4. **Hard disclaimer**, research/portfolio only; not a medical device.  
5. **Coarse bands**, avoid fake precision (0.1% displays).

## Interview-ready talking points (INFJ-aligned)

- *“I care less about winning a Kaggle metric than about whether a number
  deserves to be shown.”*  
- *“Calibration is an ethical metric here, not a nicety, clinicians hear
  probabilities as frequencies.”*  
- *“SHAP is a flashlight on the model, not a pathophysiology lecture.”*  
- *“If this were production, I’d ask who is liable, how overrides are logged,
  and how we monitor calibration drift after deployment.”*

## Design choices that encode values

| Choice | Ethical rationale |
|--------|-------------------|
| Baseline before LSTM | Prefer inspectability over awe |
| Vitals-only scope | Avoid pretending we modeled the whole patient |
| Missingness flags | Don’t erase the charting process |
| Isotonic calibration | Respect probability-as-frequency |
| Synthetic public demo | Honor MIMIC DUA; no credentialed rows in public UI |
| EN/FR copy | Meet Swiss bilingual workplace reality |

## What not to do in screenshots / blogs

- Do not sensationalize a high-risk demo stay.  
- Do not imply regulatory readiness (CE / FDA).  
- Do not hide the synthetic-data caveat.  
- Do not claim fairness without subgroup analysis.

## Further reading (cite thoughtfully)

- FDA / IMDRF materials on clinical decision support (CDS) vs devices  
- “Hidden curricula” of early warning scores and alert fatigue  
- Your own `docs/limitations.md`, honesty is part of ethics
