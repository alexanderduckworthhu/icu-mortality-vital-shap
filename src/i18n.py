"""EN / FR / DE / IT / ZH / PT / RU micro-copy for the Gradio demo."""

from __future__ import annotations

SUPPORTED_LANGS = ("en", "fr", "de", "it", "zh", "pt", "ru")

LANGUAGE_LABELS: dict[str, str] = {
    "en": "English",
    "fr": "Français",
    "de": "Deutsch",
    "it": "Italiano",
    "zh": "中文",
    "pt": "Português",
    "ru": "Русский",
}

COPY: dict[str, dict[str, str]] = {
    "en": {
        "eyebrow": "Portfolio demo for clinical data science roles",
        "title": "Will this ICU patient survive the next 48 hours?",
        "subtitle": (
            "This tool estimates that chance from heart rate, blood pressure, "
            "breathing rate, oxygen level, and temperature over the last two days."
        ),
        "what_it_shows": (
            "<strong>What you get:</strong> a risk percentage, then a short list of "
            "which vital signs and time windows most influenced the score. "
            "Use it to ask better questions, not to decide care."
        ),
        "disclaimer_short": (
            "Research demo only. Not a medical device. Not for real clinical decisions."
        ),
        "select_stay": "Demo patient stay",
        "select_stay_info": "Six synthetic examples, from calmer to more unstable.",
        "lang": "Language",
        "sidebar_hint": "Switch language anytime. Everything on the page follows.",
        "sidebar_guide": 'Pick a demo stay, then read the risk and which vitals moved it. Ethics and metrics are optional depth.',
        "reset_view": 'Reset to default stay',
        "source": 'Data source',
        "source_synthetic": 'Synthetic demo (public)',
        "source_mimic": 'MIMIC-III (credentialed path)',
        "source_note_synthetic": 'This demo runs on synthetic hourly vitals in `data/sample/`. No PhysioNet login needed.',
        "source_note_mimic": 'MIMIC-III needs a PhysioNet account and DUA. See `docs/mimic_access.md`. The public UI stays on synthetic data.',
        "sidebar_about": 'About this demo',
        "run": "Estimate risk",
        "retry": "Try again",
        "reset": "Reset",
        "run_hint": "Tip: changing the stay above refreshes the estimate on its own.",
        "status_idle": "Pick a stay to begin.",
        "status_loading": "Reviewing the last 48 hours of vitals…",
        "status_done": "Estimate ready for this stay.",
        "status_error": (
            "Something went wrong. Pick another stay or tap Try again. "
            "If it keeps failing, re-run training from the README."
        ),
        "empty_stay": "Pick a demo stay above to see a risk estimate.",
        "risk_heading": "Chance of dying within 48 hours",
        "risk_explain_high": (
            "Among similar vital-sign patterns in this demo dataset, the model "
            "puts this stay in the higher-risk group. A clinician would still "
            "weigh diagnosis, treatments, and goals of care."
        ),
        "risk_explain_mid": (
            "The model sees a middling pattern in the vitals. Treat this as a "
            "conversation starter, not a forecast of what will happen."
        ),
        "risk_explain_low": (
            "The model sees a quieter vital-sign pattern relative to this demo. "
            "Low estimated risk does not mean the patient cannot worsen."
        ),
        "drivers_heading": "Which vitals moved this score",
        "drivers_lede": (
            "These are the model’s top clues from the last 6, 24, or 48 hours. "
            "They explain the score, not the biology of death."
        ),
        "drivers_empty": "No single vital stood out for this stay.",
        "heatmap": "Influence by vital and time window",
        "heatmap_legend": (
            "Warmer cells pushed risk up. Cooler cells pushed risk down. "
            "Each row is a vital sign."
        ),
        "trajectory": "Vital signs over 48 hours",
        "trajectory_lede": (
            "The shaded area marks the most recent 6 hours when that window mattered most."
        ),
        "ethics_heading": "How to read this number",
        "metrics_heading": "Model check (synthetic data)",
        "metrics_lede": (
            "These scores are from synthetic demo data and can look unrealistically strong. "
            "On real MIMIC-III data, vitals-only models often land near AUROC 0.75 to 0.85."
        ),
        "metrics_missing": (
            "Metrics file missing. From the project folder run: "
            "`python -m scripts.train_baseline`."
        ),
        "calibration": "Calibration on the held-out synthetic split",
        "calibration_alt": (
            "Does a 20% score mean about 20% of similar stays had the event? "
            "This chart checks that on demo data."
        ),
        "charts_heading": "Charts",
        "plot_hour_axis": "Hour (0 = oldest → right = newest)",
        "plot_lookback_axis": "Lookback window ending at prediction time",
        "plot_shap_colorbar": "SHAP → chance of death",
        "plot_cal_perfect": "Perfect calibration",
        "plot_cal_model": "Model",
        "plot_cal_xlabel": "Mean predicted probability",
        "plot_cal_ylabel": "Observed mortality fraction",
        "label_demo_0": "Calmer vitals (demo)",
        "label_demo_1": "Unstable late window (demo)",
        "label_hidden_note": "In a real ICU, the true outcome would stay hidden.",
        "raised_risk": "pushed risk up",
        "lowered_risk": "pushed risk down",
        "onboarding": "",
        "band_low": "Lower risk in this demo set",
        "band_moderate": "Moderate risk in this demo set",
        "band_elevated": "Elevated risk in this demo set",
        "band_high": "Higher risk in this demo set",
        "about_pct": "About {pct}%. {band}.",
        "window_phrase": "last {window}",
        "intended_use": (
            "**Intended use:** show how a score and a time-window explanation can "
            "*support* clinical reasoning, never replace it. "
            "**Not for:** triage, rationing, end-of-life decisions, or use as a medical device."
        ),
        "uncertainty_1": "Calibration comes from development data. It can drift in another hospital.",
        "uncertainty_2": "Vitals alone leave out diagnoses, treatments, and goals of care.",
        "uncertainty_3": (
            "A high score does not justify withdrawing care. "
            "A low score does not rule out worsening."
        ),
        "uncertainty_4": (
            "Model explanation (SHAP) describes the calculation, not the biological cause."
        ),
    },
    "fr": {
        "eyebrow": "Démo portfolio pour rôles en data science clinique",
        "title": "Ce patient de SI survivra-t-il les 48 prochaines heures ?",
        "subtitle": (
            "Cet outil estime cette chance à partir du rythme cardiaque, de la "
            "pression artérielle, de la respiration, de l’oxygène et de la "
            "température sur les deux derniers jours."
        ),
        "what_it_shows": (
            "<strong>Ce que vous voyez :</strong> un pourcentage de risque, puis "
            "les signes vitaux et fenêtres de temps qui ont le plus influencé le score. "
            "Pour poser de meilleures questions, pas pour décider des soins."
        ),
        "disclaimer_short": (
            "Démo de recherche uniquement. Pas un dispositif médical. "
            "Pas pour des décisions cliniques réelles."
        ),
        "select_stay": "Séjour patient démo",
        "select_stay_info": "Six exemples synthétiques, du plus calme au plus instable.",
        "lang": "Langue",
        "sidebar_hint": 'Changez de langue quand vous voulez. Toute la page suit.',
        "sidebar_guide": 'Choisissez un séjour démo, puis lisez le risque et les vitaux qui l’ont poussé. Éthique et métriques sont optionnels.',
        "reset_view": 'Revenir au séjour par défaut',
        "source": 'Source des données',
        "source_synthetic": 'Démo synthétique (public)',
        "source_mimic": 'MIMIC-III (accès restreint)',
        "source_note_synthetic": 'Cette démo utilise des signes vitaux horaires synthétiques dans `data/sample/`. Pas de compte PhysioNet requis.',
        "source_note_mimic": 'MIMIC-III exige un compte PhysioNet et un DUA. Voir `docs/mimic_access.md`. L’UI publique reste sur les données synthétiques.',
        "sidebar_about": 'À propos de cette démo',
        "run": "Estimer le risque",
        "retry": "Réessayer",
        "reset": "Réinitialiser",
        "run_hint": "Astuce : changer de séjour ci-dessus rafraîchit l’estimation tout seul.",
        "status_idle": "Choisissez un séjour pour commencer.",
        "status_loading": "Lecture des 48 dernières heures de signes vitaux…",
        "status_done": "Estimation prête pour ce séjour.",
        "status_error": (
            "Un problème est survenu. Choisissez un autre séjour ou touchez Réessayer. "
            "Si cela continue, relancez l’entraînement (README)."
        ),
        "empty_stay": "Choisissez un séjour démo ci-dessus pour voir une estimation.",
        "risk_heading": "Chance de décès dans les 48 heures",
        "risk_explain_high": (
            "Parmi des profils vitaux similaires dans cette démo, le modèle place "
            "ce séjour dans le groupe à risque plus élevé. Un clinicien tiendrait "
            "encore compte du diagnostic, des traitements et des directives."
        ),
        "risk_explain_mid": (
            "Le modèle voit un profil vital intermédiaire. Voyez cela comme un "
            "point de discussion, pas comme une prévision de ce qui arrivera."
        ),
        "risk_explain_low": (
            "Le modèle voit un profil vital plus calme dans cette démo. "
            "Un risque bas n’exclut pas une aggravation."
        ),
        "drivers_heading": "Quels signes vitaux ont bougé le score",
        "drivers_lede": (
            "Voici les principaux indices du modèle sur 6, 24 ou 48 heures. "
            "Ils expliquent le score, pas la biologie du décès."
        ),
        "drivers_empty": "Aucun signe vital ne se démarque pour ce séjour.",
        "heatmap": "Influence par vital et fenêtre de temps",
        "heatmap_legend": (
            "Les cases plus chaudes ont augmenté le risque. Les plus froides l’ont baissé. "
            "Chaque ligne est un signe vital."
        ),
        "trajectory": "Signes vitaux sur 48 heures",
        "trajectory_lede": (
            "La zone ombrée marque les 6 heures les plus récentes quand cette fenêtre comptait le plus."
        ),
        "ethics_heading": "Comment lire ce chiffre",
        "metrics_heading": "Contrôle du modèle (données synthétiques)",
        "metrics_lede": (
            "Ces scores viennent de données synthétiques et peuvent paraître trop forts. "
            "Sur MIMIC-III réel, les modèles signes vitaux seuls se situent souvent "
            "vers un AUROC de 0,75 à 0,85."
        ),
        "metrics_missing": (
            "Fichier de métriques manquant. Depuis le dossier du projet : "
            "`python -m scripts.train_baseline`."
        ),
        "calibration": "Calibration sur le jeu synthétique tenu à l’écart",
        "calibration_alt": (
            "Un score de 20 % signifie-t-il qu’environ 20 % des séjours similaires "
            "ont eu l’événement ? Ce graphique le vérifie sur la démo."
        ),
        "charts_heading": "Graphiques",
        "plot_hour_axis": "Heure (0 = plus ancien → droite = plus récent)",
        "plot_lookback_axis": "Fenêtre rétrospective jusqu’au moment de la prédiction",
        "plot_shap_colorbar": "SHAP → chance de décès",
        "plot_cal_perfect": "Calibration parfaite",
        "plot_cal_model": "Modèle",
        "plot_cal_xlabel": "Probabilité moyenne prédite",
        "plot_cal_ylabel": "Fraction de mortalité observée",
        "label_demo_0": "Signes vitaux plus calmes (démo)",
        "label_demo_1": "Fenêtre tardive instable (démo)",
        "label_hidden_note": "En SI réel, le vrai résultat resterait masqué.",
        "raised_risk": "a augmenté le risque",
        "lowered_risk": "a baissé le risque",
        "onboarding": "",
        "band_low": "Risque plus bas dans cette démo",
        "band_moderate": "Risque modéré dans cette démo",
        "band_elevated": "Risque élevé dans cette démo",
        "band_high": "Risque plus élevé dans cette démo",
        "about_pct": "Environ {pct}%. {band}.",
        "window_phrase": "dernières {window}",
        "intended_use": (
            "**Usage prévu :** montrer comment un score et une explication temporelle "
            "peuvent *soutenir* le raisonnement clinique, jamais le remplacer. "
            "**Pas pour :** triage, rationnement, décisions de fin de vie, dispositif médical."
        ),
        "uncertainty_1": (
            "La calibration vient des données de développement. "
            "Elle peut changer dans un autre hôpital."
        ),
        "uncertainty_2": (
            "Les signes vitaux seuls ignorent diagnostics, traitements et directives anticipées."
        ),
        "uncertainty_3": (
            "Un score élevé n’autorise pas à réduire les soins. "
            "Un score bas n’exclut pas l’aggravation."
        ),
        "uncertainty_4": (
            "L’explication du modèle (SHAP) décrit le calcul, pas la cause biologique."
        ),
    },
    "de": {
        "eyebrow": "Portfolio-Demo für klinische Data-Science-Rollen",
        "title": "Überlebt dieser Intensivpatient die nächsten 48 Stunden?",
        "subtitle": (
            "Dieses Tool schätzt diese Chance aus Herzfrequenz, Blutdruck, "
            "Atemfrequenz, Sauerstoffsättigung und Temperatur der letzten zwei Tage."
        ),
        "what_it_shows": (
            "<strong>Was Sie sehen:</strong> einen Risiko-Prozentsatz und eine kurze Liste, "
            "welche Vitalzeichen und Zeitfenster den Score am stärksten beeinflusst haben. "
            "Zum besseren Nachfragen, nicht zur Entscheidungsfindung über die Versorgung."
        ),
        "disclaimer_short": (
            "Nur Forschungsdemo. Kein Medizinprodukt. Nicht für echte klinische Entscheidungen."
        ),
        "select_stay": "Demo-Patientenaufenthalt",
        "select_stay_info": "Sechs synthetische Beispiele, von ruhiger bis instabiler.",
        "lang": "Sprache",
        "sidebar_hint": 'Sprache jederzeit wechseln. Die ganze Seite folgt.',
        "sidebar_guide": 'Wählen Sie einen Demo-Aufenthalt, dann lesen Sie Risiko und die treibenden Vitalzeichen. Ethik und Metriken sind optional.',
        "reset_view": 'Standard-Aufenthalt wiederherstellen',
        "source": 'Datenquelle',
        "source_synthetic": 'Synthetische Demo (öffentlich)',
        "source_mimic": 'MIMIC-III (zugangsbeschränkt)',
        "source_note_synthetic": 'Diese Demo nutzt synthetische Stunden-Vitalwerte in `data/sample/`. Kein PhysioNet-Login nötig.',
        "source_note_mimic": 'MIMIC-III braucht PhysioNet-Konto und DUA. Siehe `docs/mimic_access.md`. Die öffentliche UI bleibt bei synthetischen Daten.',
        "sidebar_about": 'Über diese Demo',
        "run": "Risiko schätzen",
        "retry": "Erneut versuchen",
        "reset": "Zurücksetzen",
        "run_hint": "Tipp: Ein anderer Aufenthalt oben aktualisiert die Schätzung automatisch.",
        "status_idle": "Wählen Sie einen Aufenthalt zum Start.",
        "status_loading": "Die letzten 48 Stunden der Vitalzeichen werden gelesen…",
        "status_done": "Schätzung für diesen Aufenthalt ist bereit.",
        "status_error": (
            "Etwas ist schiefgelaufen. Wählen Sie einen anderen Aufenthalt oder tippen Sie "
            "auf Erneut versuchen. Wenn es weiter fehlschlägt, Training laut README neu starten."
        ),
        "empty_stay": "Wählen Sie oben einen Demo-Aufenthalt für eine Risikoschätzung.",
        "risk_heading": "Chance, innerhalb von 48 Stunden zu sterben",
        "risk_explain_high": (
            "Bei ähnlichen Vitalzeichen-Mustern in diesem Demo-Datensatz ordnet das Modell "
            "diesen Aufenthalt der höheren Risikogruppe zu. Eine Klinik würde weiterhin "
            "Diagnose, Therapien und Therapieziele einbeziehen."
        ),
        "risk_explain_mid": (
            "Das Modell sieht ein mittleres Vitalzeichen-Muster. Nutzen Sie das als "
            "Gesprächsanstoß, nicht als Vorhersage dessen, was passieren wird."
        ),
        "risk_explain_low": (
            "Das Modell sieht ein ruhigeres Vitalzeichen-Muster in dieser Demo. "
            "Niedriges geschätztes Risiko heißt nicht, dass sich der Zustand nicht verschlechtern kann."
        ),
        "drivers_heading": "Welche Vitalzeichen den Score bewegt haben",
        "drivers_lede": (
            "Das sind die wichtigsten Hinweise des Modells aus den letzten 6, 24 oder 48 Stunden. "
            "Sie erklären den Score, nicht die Biologie des Todes."
        ),
        "drivers_empty": "Kein einzelnes Vitalzeichen sticht bei diesem Aufenthalt hervor.",
        "heatmap": "Einfluss nach Vitalzeichen und Zeitfenster",
        "heatmap_legend": (
            "Wärmere Zellen haben das Risiko erhöht. Kältere Zellen haben es gesenkt. "
            "Jede Zeile ist ein Vitalzeichen."
        ),
        "trajectory": "Vitalzeichen über 48 Stunden",
        "trajectory_lede": (
            "Der schattierte Bereich markiert die jüngsten 6 Stunden, wenn dieses Fenster am stärksten zählte."
        ),
        "ethics_heading": "Wie Sie diese Zahl lesen",
        "metrics_heading": "Modellcheck (synthetische Daten)",
        "metrics_lede": (
            "Diese Kennzahlen stammen von synthetischen Demo-Daten und können unrealistisch stark wirken. "
            "Auf echten MIMIC-III-Daten liegen Vitalzeichen-only-Modelle oft bei AUROC 0,75 bis 0,85."
        ),
        "metrics_missing": (
            "Kennzahlen-Datei fehlt. Im Projektordner ausführen: "
            "`python -m scripts.train_baseline`."
        ),
        "calibration": "Kalibrierung auf dem zurückgehaltenen synthetischen Split",
        "calibration_alt": (
            "Bedeutet ein Score von 20 %, dass etwa 20 % ähnlicher Aufenthalte das Ereignis hatten? "
            "Dieses Diagramm prüft das an den Demo-Daten."
        ),
        "charts_heading": "Diagramme",
        "plot_hour_axis": "Stunde (0 = älteste → rechts = neueste)",
        "plot_lookback_axis": "Rückblickfenster bis zum Vorhersagezeitpunkt",
        "plot_shap_colorbar": "SHAP → Sterberisiko",
        "plot_cal_perfect": "Perfekte Kalibrierung",
        "plot_cal_model": "Modell",
        "plot_cal_xlabel": "Mittlere vorhergesagte Wahrscheinlichkeit",
        "plot_cal_ylabel": "Beobachteter Mortalitätsanteil",
        "label_demo_0": "Ruhigere Vitalzeichen (Demo)",
        "label_demo_1": "Instabiles Spätfenster (Demo)",
        "label_hidden_note": "Auf einer echten Intensivstation bliebe der echte Ausgang verborgen.",
        "raised_risk": "hat das Risiko erhöht",
        "lowered_risk": "hat das Risiko gesenkt",
        "onboarding": "",
        "band_low": "Niedrigeres Risiko in diesem Demo-Satz",
        "band_moderate": "Mittleres Risiko in diesem Demo-Satz",
        "band_elevated": "Erhöhtes Risiko in diesem Demo-Satz",
        "band_high": "Höheres Risiko in diesem Demo-Satz",
        "about_pct": "Etwa {pct}%. {band}.",
        "window_phrase": "letzte {window}",
        "intended_use": (
            "**Vorgesehene Nutzung:** zeigen, wie ein Score und eine Zeitfenster-Erklärung "
            "klinisches Denken *unterstützen* können, nie ersetzen. "
            "**Nicht für:** Triage, Rationierung, Entscheidungen am Lebensende, Medizinprodukt."
        ),
        "uncertainty_1": (
            "Die Kalibrierung stammt aus Entwicklungsdaten. "
            "Sie kann in einem anderen Spital abweichen."
        ),
        "uncertainty_2": (
            "Vitalzeichen allein lassen Diagnosen, Therapien und Therapieziele aus."
        ),
        "uncertainty_3": (
            "Ein hoher Score rechtfertigt keine Reduktion der Versorgung. "
            "Ein niedriger Score schließt eine Verschlechterung nicht aus."
        ),
        "uncertainty_4": (
            "Die Modellerklärung (SHAP) beschreibt die Berechnung, nicht die biologische Ursache."
        ),
    },
    "it": {
        "eyebrow": "Demo portfolio per ruoli di data science clinica",
        "title": "Questo paziente di TI sopravviverà alle prossime 48 ore?",
        "subtitle": (
            "Questo strumento stima quella probabilità da frequenza cardiaca, pressione, "
            "frequenza respiratoria, ossigeno e temperatura degli ultimi due giorni."
        ),
        "what_it_shows": (
            "<strong>Cosa vede:</strong> una percentuale di rischio e un elenco breve di "
            "quali segni vitali e finestre temporali hanno influenzato di più il punteggio. "
            "Per fare domande migliori, non per decidere le cure."
        ),
        "disclaimer_short": (
            "Solo demo di ricerca. Non è un dispositivo medico. "
            "Non per decisioni cliniche reali."
        ),
        "select_stay": "Degenza paziente demo",
        "select_stay_info": "Sei esempi sintetici, dal più calmo al più instabile.",
        "lang": "Lingua",
        "sidebar_hint": 'Cambia lingua quando vuoi. Tutta la pagina segue.',
        "sidebar_guide": 'Scegli un ricovero demo, poi leggi il rischio e i vitali che lo hanno mosso. Etica e metriche sono profondità opzionale.',
        "reset_view": 'Torna al ricovero predefinito',
        "source": 'Fonte dati',
        "source_synthetic": 'Demo sintetica (pubblica)',
        "source_mimic": 'MIMIC-III (accesso con credenziali)',
        "source_note_synthetic": 'Questa demo usa segni vitali orari sintetici in `data/sample/`. Nessun account PhysioNet richiesto.',
        "source_note_mimic": 'MIMIC-III richiede account PhysioNet e DUA. Vedi `docs/mimic_access.md`. L’UI pubblica resta sui dati sintetici.',
        "sidebar_about": 'Informazioni su questa demo',
        "run": "Stima il rischio",
        "retry": "Riprova",
        "reset": "Reimposta",
        "run_hint": "Suggerimento: cambiare la degenza sopra aggiorna la stima da solo.",
        "status_idle": "Scegli una degenza per iniziare.",
        "status_loading": "Lettura delle ultime 48 ore di segni vitali…",
        "status_done": "Stima pronta per questa degenza.",
        "status_error": (
            "Qualcosa è andato storto. Scegli un’altra degenza o tocca Riprova. "
            "Se continua, rilancia l’addestramento dal README."
        ),
        "empty_stay": "Scegli sopra una degenza demo per vedere una stima del rischio.",
        "risk_heading": "Probabilità di decesso entro 48 ore",
        "risk_explain_high": (
            "Tra profili di segni vitali simili in questo dataset demo, il modello colloca "
            "questa degenza nel gruppo a rischio più alto. Un clinico terrebbe comunque "
            "conto di diagnosi, trattamenti e obiettivi di cura."
        ),
        "risk_explain_mid": (
            "Il modello vede un profilo intermedio dei segni vitali. Usalo come spunto "
            "di discussione, non come previsione di ciò che accadrà."
        ),
        "risk_explain_low": (
            "Il modello vede un profilo più calmo in questa demo. "
            "Un rischio basso non esclude un peggioramento."
        ),
        "drivers_heading": "Quali segni vitali hanno mosso il punteggio",
        "drivers_lede": (
            "Questi sono i principali indizi del modello sulle ultime 6, 24 o 48 ore. "
            "Spiegano il punteggio, non la biologia della morte."
        ),
        "drivers_empty": "Nessun segno vitale spicca per questa degenza.",
        "heatmap": "Influenza per segno vitale e finestra temporale",
        "heatmap_legend": (
            "Le celle più calde hanno alzato il rischio. Quelle più fredde l’hanno abbassato. "
            "Ogni riga è un segno vitale."
        ),
        "trajectory": "Segni vitali nelle 48 ore",
        "trajectory_lede": (
            "L’area ombreggiata segna le 6 ore più recenti quando quella finestra contava di più."
        ),
        "ethics_heading": "Come leggere questo numero",
        "metrics_heading": "Controllo del modello (dati sintetici)",
        "metrics_lede": (
            "Queste metriche arrivano da dati demo sintetici e possono sembrare troppo forti. "
            "Su MIMIC-III reale, i modelli solo segni vitali spesso stanno intorno ad AUROC 0,75–0,85."
        ),
        "metrics_missing": (
            "File delle metriche assente. Dalla cartella del progetto esegui: "
            "`python -m scripts.train_baseline`."
        ),
        "calibration": "Calibrazione sullo split sintetico tenuto da parte",
        "calibration_alt": (
            "Un punteggio del 20% significa che circa il 20% di degenze simili ha avuto l’evento? "
            "Questo grafico lo verifica sui dati demo."
        ),
        "charts_heading": "Grafici",
        "plot_hour_axis": "Ora (0 = più vecchia → destra = più recente)",
        "plot_lookback_axis": "Finestra retrospettiva fino al momento della predizione",
        "plot_shap_colorbar": "SHAP → probabilità di decesso",
        "plot_cal_perfect": "Calibrazione perfetta",
        "plot_cal_model": "Modello",
        "plot_cal_xlabel": "Probabilità media prevista",
        "plot_cal_ylabel": "Frazione di mortalità osservata",
        "label_demo_0": "Segni vitali più calmi (demo)",
        "label_demo_1": "Finestra tardiva instabile (demo)",
        "label_hidden_note": "In una TI reale, l’esito vero resterebbe nascosto.",
        "raised_risk": "ha alzato il rischio",
        "lowered_risk": "ha abbassato il rischio",
        "onboarding": "",
        "band_low": "Rischio più basso in questo set demo",
        "band_moderate": "Rischio moderato in questo set demo",
        "band_elevated": "Rischio elevato in questo set demo",
        "band_high": "Rischio più alto in questo set demo",
        "about_pct": "Circa {pct}%. {band}.",
        "window_phrase": "ultime {window}",
        "intended_use": (
            "**Uso previsto:** mostrare come un punteggio e una spiegazione temporale "
            "possano *supportare* il ragionamento clinico, mai sostituirlo. "
            "**Non per:** triage, razionamento, decisioni di fine vita, dispositivo medico."
        ),
        "uncertainty_1": (
            "La calibrazione viene dai dati di sviluppo. "
            "Può cambiare in un altro ospedale."
        ),
        "uncertainty_2": (
            "I soli segni vitali omettono diagnosi, trattamenti e obiettivi di cura."
        ),
        "uncertainty_3": (
            "Un punteggio alto non giustifica ridurre le cure. "
            "Un punteggio basso non esclude un peggioramento."
        ),
        "uncertainty_4": (
            "La spiegazione del modello (SHAP) descrive il calcolo, non la causa biologica."
        ),
    },
    "zh": {
        "eyebrow": "面向临床数据科学岗位的作品集演示",
        "title": "这名重症患者能否度过接下来的 48 小时？",
        "subtitle": (
            "本工具根据过去两天的心率、血压、呼吸频率、血氧和体温，估算这一可能性。"
        ),
        "what_it_shows": (
            "<strong>你会看到：</strong>一个风险百分比，以及哪些生命体征和时间窗口"
            "对分数影响最大的简短列表。用来提出更好的问题，而不是决定诊疗。"
        ),
        "disclaimer_short": "仅供研究演示。不是医疗器械。不用于真实临床决策。",
        "select_stay": "演示患者住院",
        "select_stay_info": "六个合成示例，从较平稳到较不稳定。",
        "lang": "语言",
        "sidebar_hint": '可随时切换语言，整页内容会一起更新。',
        "sidebar_guide": '先选择一条演示住院，再查看风险与推动分数的生命体征。伦理与指标为可选深入。',
        "reset_view": '重置为默认住院',
        "source": '数据来源',
        "source_synthetic": '合成演示（公开）',
        "source_mimic": 'MIMIC-III（需资质）',
        "source_note_synthetic": '本演示使用 `data/sample/` 中的合成小时级生命体征。无需 PhysioNet 登录。',
        "source_note_mimic": 'MIMIC-III 需要 PhysioNet 账号与数据使用协议。见 `docs/mimic_access.md`。公开界面仍使用合成数据。',
        "sidebar_about": '关于本演示',
        "run": "估算风险",
        "retry": "重试",
        "reset": "重置",
        "run_hint": "提示：上方更换住院记录会自动刷新估算。",
        "status_idle": "请选择一条住院记录开始。",
        "status_loading": "正在查看过去 48 小时的生命体征…",
        "status_done": "该住院记录的估算已就绪。",
        "status_error": (
            "出现问题。请另选一条记录或点击重试。"
            "若反复失败，请按 README 重新训练。"
        ),
        "empty_stay": "请在上方选择一条演示住院记录以查看风险估算。",
        "risk_heading": "48 小时内死亡的可能性",
        "risk_explain_high": (
            "在本演示数据中，与相似生命体征模式相比，模型将此住院归入较高风险组。"
            "临床医生仍需结合诊断、治疗与照护目标综合判断。"
        ),
        "risk_explain_mid": (
            "模型看到的是中等程度的生命体征模式。请把它当作讨论起点，而不是对结局的预测。"
        ),
        "risk_explain_low": (
            "相对于本演示，模型看到较平稳的生命体征模式。"
            "低风险估算并不意味着病情不会恶化。"
        ),
        "drivers_heading": "哪些生命体征推动了这个分数",
        "drivers_lede": (
            "这些是模型从过去 6、24 或 48 小时中得到的主要线索。"
            "它们解释分数，而不是死亡的生物学原因。"
        ),
        "drivers_empty": "此住院没有突出的单一生命体征。",
        "heatmap": "按生命体征与时间窗口的影响",
        "heatmap_legend": "暖色提高风险，冷色降低风险。每一行是一种生命体征。",
        "trajectory": "48 小时生命体征走势",
        "trajectory_lede": "阴影区域标出该窗口最重要的最近 6 小时。",
        "ethics_heading": "如何理解这个数字",
        "metrics_heading": "模型检查（合成数据）",
        "metrics_lede": (
            "这些指标来自合成演示数据，可能显得过强。"
            "在真实 MIMIC-III 上，仅用生命体征的模型 AUROC 常在 0.75 到 0.85 附近。"
        ),
        "metrics_missing": (
            "缺少指标文件。请在项目目录运行：`python -m scripts.train_baseline`。"
        ),
        "calibration": "在留出合成划分上的校准",
        "calibration_alt": (
            "20% 的分数是否意味着约 20% 的相似住院发生了该事件？"
            "此图用演示数据做检查。"
        ),
        "charts_heading": "图表",
        "plot_hour_axis": "小时（0 = 最早 → 右侧 = 最新）",
        "plot_lookback_axis": "截至预测时刻的回看时间窗口",
        "plot_shap_colorbar": "SHAP → 死亡可能性",
        "plot_cal_perfect": "理想校准",
        "plot_cal_model": "模型",
        "plot_cal_xlabel": "平均预测概率",
        "plot_cal_ylabel": "观察到的死亡比例",
        "label_demo_0": "较平稳生命体征（演示）",
        "label_demo_1": "后期不稳定窗口（演示）",
        "label_hidden_note": "在真实 ICU 中，真实结局会保持隐藏。",
        "raised_risk": "推高了风险",
        "lowered_risk": "降低了风险",
        "onboarding": "",
        "band_low": "本演示集中风险较低",
        "band_moderate": "本演示集中风险中等",
        "band_elevated": "本演示集中风险偏高",
        "band_high": "本演示集中风险较高",
        "about_pct": "约 {pct}%。{band}。",
        "window_phrase": "最近 {window}",
        "intended_use": (
            "**预期用途：**展示分数与时间窗口解释如何*辅助*临床推理，而非取代。"
            "**不用于：**分诊、资源配给、临终决策，或作为医疗器械。"
        ),
        "uncertainty_1": "校准来自开发数据，换到另一家医院可能漂移。",
        "uncertainty_2": "仅有生命体征会遗漏诊断、治疗与照护目标。",
        "uncertainty_3": "高分不构成减少照护的理由；低分也不能排除病情恶化。",
        "uncertainty_4": "模型解释（SHAP）描述的是计算过程，不是生物学因果。",
    },
    "pt": {
        "eyebrow": "Demo de portfólio para funções de data science clínica",
        "title": "Este doente de UCI sobreviverá às próximas 48 horas?",
        "subtitle": (
            "Esta ferramenta estima essa probabilidade a partir da frequência cardíaca, "
            "pressão arterial, frequência respiratória, oxigénio e temperatura "
            "dos últimos dois dias."
        ),
        "what_it_shows": (
            "<strong>O que vê:</strong> uma percentagem de risco e uma lista curta "
            "dos sinais vitais e janelas temporais que mais influenciaram o score. "
            "Use para fazer melhores perguntas, não para decidir cuidados."
        ),
        "disclaimer_short": (
            "Apenas demonstração de investigação. Não é um dispositivo médico. "
            "Não para decisões clínicas reais."
        ),
        "select_stay": "Internamento demo",
        "select_stay_info": "Seis exemplos sintéticos, do mais estável ao mais instável.",
        "lang": "Idioma",
        "sidebar_hint": 'Mude de idioma quando quiser. Toda a página segue.',
        "sidebar_guide": 'Escolha um internamento demo, depois leia o risco e os vitais que o moveram. Ética e métricas são profundidade opcional.',
        "reset_view": 'Repor o internamento padrão',
        "source": 'Fonte de dados',
        "source_synthetic": 'Demo sintética (pública)',
        "source_mimic": 'MIMIC-III (acesso com credenciais)',
        "source_note_synthetic": 'Esta demo usa sinais vitais horários sintéticos em `data/sample/`. Não é preciso login PhysioNet.',
        "source_note_mimic": 'MIMIC-III exige conta PhysioNet e DUA. Ver `docs/mimic_access.md`. A UI pública continua com dados sintéticos.',
        "sidebar_about": 'Sobre esta demo',
        "run": "Estimar o risco",
        "retry": "Tentar de novo",
        "reset": "Repor",
        "run_hint": "Dica: mudar o internamento acima atualiza a estimativa automaticamente.",
        "status_idle": "Escolha um internamento para começar.",
        "status_loading": "A rever as últimas 48 horas de sinais vitais…",
        "status_done": "Estimativa pronta para este internamento.",
        "status_error": (
            "Algo correu mal. Escolha outro internamento ou toque em Tentar de novo. "
            "Se continuar a falhar, volte a treinar seguindo o README."
        ),
        "empty_stay": "Escolha um internamento demo acima para ver uma estimativa de risco.",
        "risk_heading": "Probabilidade de morrer nas próximas 48 horas",
        "risk_explain_high": (
            "Entre padrões vitais semelhantes neste conjunto demo, o modelo "
            "coloca este internamento no grupo de risco mais elevado. Um clínico "
            "continuaria a ponderar diagnóstico, tratamentos e objetivos de cuidados."
        ),
        "risk_explain_mid": (
            "O modelo vê um padrão intermédio nos sinais vitais. Trate isto como "
            "ponto de partida para a discussão, não como previsão do que vai acontecer."
        ),
        "risk_explain_low": (
            "O modelo vê um padrão vital mais calmo relativamente a esta demo. "
            "Risco estimado baixo não significa que o doente não possa agravar."
        ),
        "drivers_heading": "Que sinais vitais moveram este score",
        "drivers_lede": (
            "Estas são as principais pistas do modelo das últimas 6, 24 ou 48 horas. "
            "Explicam o score, não a biologia da morte."
        ),
        "drivers_empty": "Nenhum sinal vital se destacou neste internamento.",
        "heatmap": "Influência por vital e janela temporal",
        "heatmap_legend": (
            "Células mais quentes aumentaram o risco. Células mais frias diminuíram. "
            "Cada linha é um sinal vital."
        ),
        "trajectory": "Sinais vitais ao longo de 48 horas",
        "trajectory_lede": (
            "A área sombreada marca as 6 horas mais recentes quando essa janela mais importou."
        ),
        "ethics_heading": "Como ler este número",
        "metrics_heading": "Verificação do modelo (dados sintéticos)",
        "metrics_lede": (
            "Estes scores vêm de dados demo sintéticos e podem parecer irrealisticamente fortes. "
            "Em MIMIC-III real, modelos só com vitais ficam muitas vezes perto de AUROC 0,75 a 0,85."
        ),
        "metrics_missing": (
            "Ficheiro de métricas em falta. Na pasta do projeto execute: "
            "`python -m scripts.train_baseline`."
        ),
        "calibration": "Calibração no split sintético de validação",
        "calibration_alt": (
            "Um score de 20% significa cerca de 20% de internamentos semelhantes com o evento? "
            "Este gráfico verifica isso nos dados demo."
        ),
        "charts_heading": "Gráficos",
        "plot_hour_axis": "Hora (0 = mais antiga → direita = mais recente)",
        "plot_lookback_axis": "Janela retrospetiva até ao momento da previsão",
        "plot_shap_colorbar": "SHAP → probabilidade de morte",
        "plot_cal_perfect": "Calibração perfeita",
        "plot_cal_model": "Modelo",
        "plot_cal_xlabel": "Probabilidade média prevista",
        "plot_cal_ylabel": "Fração de mortalidade observada",
        "label_demo_0": "Sinais vitais mais calmos (demo)",
        "label_demo_1": "Janela tardia instável (demo)",
        "label_hidden_note": "Numa UCI real, o desfecho verdadeiro ficaria oculto.",
        "raised_risk": "aumentou o risco",
        "lowered_risk": "diminuiu o risco",
        "onboarding": "",
        "band_low": "Risco mais baixo neste conjunto demo",
        "band_moderate": "Risco moderado neste conjunto demo",
        "band_elevated": "Risco elevado neste conjunto demo",
        "band_high": "Risco mais alto neste conjunto demo",
        "about_pct": "Cerca de {pct}%. {band}.",
        "window_phrase": "últimas {window}",
        "intended_use": (
            "**Uso previsto:** mostrar como um score e uma explicação por janela temporal "
            "podem *apoiar* o raciocínio clínico, nunca substituí-lo. "
            "**Não para:** triagem, racionamento, decisões de fim de vida, ou uso como dispositivo médico."
        ),
        "uncertainty_1": (
            "A calibração vem dos dados de desenvolvimento. "
            "Pode mudar noutro hospital."
        ),
        "uncertainty_2": (
            "Só os sinais vitais omitem diagnósticos, tratamentos e objetivos de cuidados."
        ),
        "uncertainty_3": (
            "Um score alto não justifica retirar cuidados. "
            "Um score baixo não exclui agravamento."
        ),
        "uncertainty_4": (
            "A explicação do modelo (SHAP) descreve o cálculo, não a causa biológica."
        ),
    },
    "ru": {
        "eyebrow": "Демо портфолио для ролей клинической data science",
        "title": "Переживёт ли этот пациент ОРИТ следующие 48 часов?",
        "subtitle": (
            "Инструмент оценивает эту вероятность по частоте сердечных сокращений, "
            "давлению, дыханию, насыщению кислородом и температуре за последние два дня."
        ),
        "what_it_shows": (
            "<strong>Что вы увидите:</strong> процент риска и короткий список "
            "жизненных показателей и временных окон, сильнее всего повлиявших на оценку. "
            "Это помогает задавать вопросы, а не принимать решения о лечении."
        ),
        "disclaimer_short": (
            "Только исследовательское демо. Не медицинское изделие. "
            "Не для реальных клинических решений."
        ),
        "select_stay": "Демо-случай госпитализации",
        "select_stay_info": "Шесть синтетических примеров: от более спокойных к менее стабильным.",
        "lang": "Язык",
        "sidebar_hint": 'Меняйте язык в любой момент. Вся страница следует за ним.',
        "sidebar_guide": 'Выберите демо-случай, затем прочитайте риск и показатели, которые его сдвинули. Этика и метрики - по желанию.',
        "reset_view": 'Сбросить к случаю по умолчанию',
        "source": 'Источник данных',
        "source_synthetic": 'Синтетическое демо (публичное)',
        "source_mimic": 'MIMIC-III (по доступу)',
        "source_note_synthetic": 'Это демо использует синтетические почасовые показатели в `data/sample/`. Логин PhysioNet не нужен.',
        "source_note_mimic": 'Для MIMIC-III нужны аккаунт PhysioNet и DUA. См. `docs/mimic_access.md`. Публичный интерфейс остаётся на синтетике.',
        "sidebar_about": 'Об этом демо',
        "run": "Оценить риск",
        "retry": "Повторить",
        "reset": "Сброс",
        "run_hint": "Подсказка: смена случая выше сама обновляет оценку.",
        "status_idle": "Выберите случай, чтобы начать.",
        "status_loading": "Просматриваем жизненные показатели за последние 48 часов…",
        "status_done": "Оценка для этого случая готова.",
        "status_error": (
            "Что-то пошло не так. Выберите другой случай или нажмите «Повторить». "
            "Если ошибка повторяется, переобучите модель по README."
        ),
        "empty_stay": "Выберите демо-случай выше, чтобы увидеть оценку риска.",
        "risk_heading": "Вероятность смерти в течение 48 часов",
        "risk_explain_high": (
            "Среди похожих паттернов жизненных показателей в этом демо набор "
            "модель относит этот случай к группе более высокого риска. Врач всё равно "
            "учтёт диагноз, лечение и цели ухода."
        ),
        "risk_explain_mid": (
            "Модель видит средний паттерн жизненных показателей. Рассматривайте это "
            "как начало обсуждения, а не прогноз исхода."
        ),
        "risk_explain_low": (
            "Относительно этого демо модель видит более спокойный паттерн. "
            "Низкий оценочный риск не значит, что состояние не может ухудшиться."
        ),
        "drivers_heading": "Какие показатели сдвинули эту оценку",
        "drivers_lede": (
            "Это главные подсказки модели за последние 6, 24 или 48 часов. "
            "Они объясняют оценку, а не биологическую причину смерти."
        ),
        "drivers_empty": "Ни один показатель не выделился для этого случая.",
        "heatmap": "Влияние по показателю и временному окну",
        "heatmap_legend": (
            "Тёплые ячейки повысили риск. Холодные понизили. "
            "Каждая строка - жизненный показатель."
        ),
        "trajectory": "Жизненные показатели за 48 часов",
        "trajectory_lede": (
            "Затенённая область отмечает последние 6 часов, когда это окно было важнее всего."
        ),
        "ethics_heading": "Как читать это число",
        "metrics_heading": "Проверка модели (синтетические данные)",
        "metrics_lede": (
            "Эти метрики с синтетических демо-данных и могут выглядеть слишком сильными. "
            "На реальном MIMIC-III модели только по витальным часто дают AUROC около 0,75–0,85."
        ),
        "metrics_missing": (
            "Файл метрик отсутствует. Из папки проекта выполните: "
            "`python -m scripts.train_baseline`."
        ),
        "calibration": "Калибровка на отложенной синтетической выборке",
        "calibration_alt": (
            "Означает ли оценка 20%, что около 20% похожих случаев имели событие? "
            "Этот график проверяет это на демо-данных."
        ),
        "charts_heading": "Графики",
        "plot_hour_axis": "Час (0 = самый старый → справа = самый новый)",
        "plot_lookback_axis": "Окно ретроспективы до момента прогноза",
        "plot_shap_colorbar": "SHAP → вероятность смерти",
        "plot_cal_perfect": "Идеальная калибровка",
        "plot_cal_model": "Модель",
        "plot_cal_xlabel": "Средняя предсказанная вероятность",
        "plot_cal_ylabel": "Наблюдаемая доля смертности",
        "label_demo_0": "Более спокойные показатели (демо)",
        "label_demo_1": "Нестабильное позднее окно (демо)",
        "label_hidden_note": "В реальной ОРИТ истинный исход оставался бы скрытым.",
        "raised_risk": "повысил риск",
        "lowered_risk": "снизил риск",
        "onboarding": "",
        "band_low": "Более низкий риск в этом демо-наборе",
        "band_moderate": "Умеренный риск в этом демо-наборе",
        "band_elevated": "Повышенный риск в этом демо-наборе",
        "band_high": "Более высокий риск в этом демо-наборе",
        "about_pct": "Около {pct}%. {band}.",
        "window_phrase": "последние {window}",
        "intended_use": (
            "**Назначение:** показать, как оценка и объяснение по временному окну "
            "могут *поддерживать* клиническое рассуждение, но не заменять его. "
            "**Не для:** сортировки, распределения ресурсов, решений о конце жизни "
            "или использования как медицинского изделия."
        ),
        "uncertainty_1": (
            "Калибровка основана на данных разработки. "
            "В другой больнице она может сместиться."
        ),
        "uncertainty_2": (
            "Только жизненные показатели не учитывают диагнозы, лечение и цели ухода."
        ),
        "uncertainty_3": (
            "Высокая оценка не оправдывает отказ от помощи. "
            "Низкая оценка не исключает ухудшения."
        ),
        "uncertainty_4": (
            "Объяснение модели (SHAP) описывает расчёт, а не биологическую причину."
        ),
    },
}


def normalize_lang(lang: str | None) -> str:
    """Return a supported language code from a control value."""
    if not lang:
        return "en"
    raw = str(lang).strip().lower()
    if raw in {"zh", "zh-cn", "zh-tw", "cn", "中文", "mandarin"}:
        return "zh"
    if raw in {"pt", "pt-br", "pt-pt", "portuguese", "português", "portugues"}:
        return "pt"
    if raw in {"ru", "ru-ru", "russian", "русский"}:
        return "ru"
    code = raw[:2]
    if code in SUPPORTED_LANGS:
        return code
    return "en"


def t(key: str, lang: str = "en") -> str:
    """Look up a UI string; fall back to English, then the key itself."""
    lang = normalize_lang(lang)
    return COPY[lang].get(key, COPY["en"].get(key, key))
