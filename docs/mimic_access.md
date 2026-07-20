# MIMIC-III access & tables

This project targets **MIMIC-III** (not MIMIC-IV) so your writeup matches common
tutorial literature. MIMIC-IV is a fine upgrade later; keep one version in v1.

## PhysioNet credentialing (step-by-step)

1. **Create a PhysioNet account**  
   https://physionet.org/

2. **Complete human-subjects / CITI training**  
   PhysioNet requires documented training in human research protections
   (commonly CITI “Data or Specimens Only Research” or equivalent accepted
   by MIT-LCP). Upload the completion report to your PhysioNet profile.

3. **Sign the Data Use Agreement (DUA)** for MIMIC-III  
   Request access to the MIMIC-III Clinical Database on PhysioNet and sign
   the DUA. Approval is not instant, plan days to a couple of weeks.

4. **Never commit credentialed files**  
   This repo gitignores `data/raw/*.csv`. Keep extracts local or on an
   encrypted volume. Do not paste patient-level rows into ChatGPT / public
   notebooks / screenshots with identifiers.

5. **Download only what you need** (see tables below)  
   Prefer cloud tools (BigQuery public MIMIC after credentialing, or PhysioNet
   download) over cloning the entire database on a laptop.

Official project page: https://physionet.org/content/mimiciii/

## Cohort definition (locked for this portfolio)

| Choice | Setting | WHY |
|--------|---------|-----|
| Population | Adult ICU stays (`ICUSTAYS`) | Pediatric physiology differs |
| Index time | End of a 48h observation window after ICU admit (or last 48h before outcome) | Matches “next 48h risk” framing |
| Label | Death within 48 hours of prediction time (`PATIENTS.DOD` / hospital expire flags reconciled carefully) | Short-horizon actionability |
| Features | Six vitals from `CHARTEVENTS` only | Scope control for entry-level timeline |
| Exclusion | Stays with &lt; 6 charted hours of any vital | Cannot build an honest sequence |

Document every exclusion count in `docs/methods.md` when you run the real ETL.

## Tables & columns to extract

### Identity / outcomes

| Table | Columns (minimum) | Role |
|-------|-------------------|------|
| `PATIENTS` | `SUBJECT_ID`, `GENDER`, `DOB`, `DOD`, `DOD_HOSP`, `EXPIRE_FLAG` | Age, death time |
| `ADMISSIONS` | `SUBJECT_ID`, `HADM_ID`, `ADMITTIME`, `DISCHTIME`, `DEATHTIME`, `HOSPITAL_EXPIRE_FLAG` | Hospital course |
| `ICUSTAYS` | `SUBJECT_ID`, `HADM_ID`, `ICUSTAY_ID`, `INTIME`, `OUTTIME`, `LOS` | ICU stay spine |

### Vitals

| Table | Columns | Role |
|-------|---------|------|
| `CHARTEVENTS` | `ICUSTAY_ID` (or `HADM_ID`), `ITEMID`, `CHARTTIME`, `VALUENUM`, `VALUEUOM` | Vital measurements |
| `D_ITEMS` | `ITEMID`, `LABEL`, `UNITNAME` | Confirm labels / units |

### Itemids used in this repo

See `src/config.py` → `MIMIC_ITEMIDS`. Always join `D_ITEMS` and spot-check
labels: CareVue vs Metavision eras use different itemids; temperature may be
°F (convert to °C).

Example mapping (verify on your extract):

| Vital | Typical ITEMIDs |
|-------|-----------------|
| Heart rate | 211, 220045 |
| Systolic BP | 51, 442, 455, 6701, 220050, 220179 |
| Diastolic BP | 8368, 8440, 8441, 8555, 220051, 220180 |
| Respiratory rate | 618, 615, 220210, 224690 |
| SpO₂ | 646, 220277 |
| Temperature | 223761 (°C), 678 (°F often) |

## Suggested extract shape

After ETL, aim for a long table compatible with the demo schema:

```text
stay_id, charttime, heart_rate, sys_bp, dias_bp, resp_rate, spo2, temperature_c
```

and a labels table:

```text
stay_id, label   # 1 = died within 48h of prediction time
```

Then reuse `src/preprocess/` unchanged.

## Legal / ethics reminder

MIMIC is de-identified but still protected under the DUA. Portfolio blogs may
describe methods and **aggregate** metrics only, not individual stays from
the real database. Keep using synthetic stays in the public Gradio demo unless
your deployment is access-controlled and DUA-compliant.
