#!/usr/bin/env python3
"""
i18n.py -- minimal English/French localization for the toolkit's user-facing
output: the HTML dashboard and the spreadsheet labels. Driven by the optional
top-level "language" key in config.json ("en" default, or "fr").

The CLI / developer-facing prints stay English. To localize a new string: add an
entry below with "en" and "fr" text, then call t("key", lang, **kwargs).
Anything missing a "fr" value falls back to English, so partial coverage is safe.

French is Canadian French. Note the standard term mapping:
  CPP -> RPC, OAS -> SV, RRSP -> REER, TFSA -> CELI, RRIF -> FERR.
"""


def lang_of(cfg):
    """Return the 2-letter language code from config ('en' default)."""
    return str((cfg or {}).get("language") or "en").lower()[:2]


def t(key, lang="en", **kw):
    """Look up a localized string by key; fall back to English, then the key."""
    entry = STRINGS.get(key, {})
    s = entry.get(lang) or entry.get("en") or key
    return s.format(**kw) if kw else s


STRINGS = {
    # ---- dashboard: header / chrome ----
    "dash.title": {"en": "Retirement Dashboard", "fr": "Tableau de bord de retraite"},
    "dash.generated": {"en": "Generated", "fr": "Généré le"},
    "dash.demo_banner": {
        "en": "DEMO DATA — fictional {name}. Replace config/config.json with your own.",
        "fr": "DONNÉES DE DÉMONSTRATION — ménage fictif {name}. Remplacez config/config.json par vos données.",
    },
    "dash.disclaimer": {
        "en": "Illustrative only — not financial advice. See DISCLAIMER.md.",
        "fr": "À titre indicatif seulement — pas un conseil financier. Voir DISCLAIMER.md.",
    },
    # ---- dashboard: KPI tiles ----
    "kpi.total_net_worth": {"en": "Total net worth", "fr": "Valeur nette totale"},
    "kpi.investable": {"en": "Investable", "fr": "Actifs investissables"},
    "kpi.spend_target": {"en": "Retirement spend target", "fr": "Objectif de dépenses à la retraite"},
    "kpi.bridge_target": {"en": "Pre-CPP/OAS bridge target", "fr": "Objectif du pont avant RPC/SV"},
    "unit.per_year": {"en": "/yr", "fr": "/an"},
    # ---- dashboard: concentration panel ----
    "conc.title": {"en": "Employer Concentration", "fr": "Concentration de l’employeur"},
    "conc.exposure": {
        "en": "Exposure ${exp} of ${inv} investable.",
        "fr": "Exposition de {exp} $ sur {inv} $ investissables.",
    },
    "conc.thresholds": {
        "en": "Watch ≥ {watch}% · Trim ≥ {trim}%.",
        "fr": "Surveiller ≥ {watch} % · Réduire ≥ {trim} %.",
    },
    "conc.verdict": {"en": "Verdict:", "fr": "Verdict :"},
    "verdict.OK": {"en": "OK", "fr": "OK"},
    "verdict.WATCH": {"en": "WATCH", "fr": "SURVEILLER"},
    "verdict.TRIM": {"en": "TRIM", "fr": "RÉDUIRE"},
    "conc.run_health": {
        "en": "Run <code>engine/company_health.py</code> for live price, analyst, and insider signals.",
        "fr": "Exécutez <code>engine/company_health.py</code> pour les signaux de prix, d’analystes et d’initiés en direct.",
    },
    # ---- dashboard: Monte Carlo panel ----
    "mc.title": {"en": "Monte Carlo — plan success", "fr": "Monte-Carlo — réussite du plan"},
    "mc.pending": {
        "en": "Run quarterly_update.py to populate.",
        "fr": "Exécutez quarterly_update.py pour le remplir.",
    },
    "mc.col.scenario": {"en": "Scenario", "fr": "Scénario"},
    "mc.col.return": {"en": "Return", "fr": "Rendement"},
    "mc.col.success": {"en": "Success", "fr": "Réussite"},
    "mc.col.median_end": {"en": "Median end", "fr": "Solde médian final"},
    "scenario.conservative": {"en": "Conservative", "fr": "Prudent"},
    "scenario.base": {"en": "Base", "fr": "Base"},
    "scenario.optimistic": {"en": "Optimistic", "fr": "Optimiste"},
    # ---- dashboard: company-health panel ----
    "ch.title": {"en": "Company Health", "fr": "Santé de l’entreprise"},
    "ch.price": {"en": "Price", "fr": "Prix"},
    "ch.target": {"en": "Analyst target", "fr": "Cible des analystes"},
    "ch.insider": {"en": "Insider sentiment", "fr": "Sentiment des initiés"},
    "ch.ytd": {"en": "YTD {v}%", "fr": "cumul annuel {v} %"},
    "ch.upside": {"en": "upside {v}%", "fr": "potentiel {v} %"},
}
