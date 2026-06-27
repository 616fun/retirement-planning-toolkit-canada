# Contribution

**Français** · [English](CONTRIBUTING.md)

Merci de votre intérêt! Il s'agit d'un petit projet convivial — une base que les gens
peuvent forker et adapter à leur propre situation. Les contributions qui le gardent
simple, lisible et sûr sont les bienvenues.

## Règles de base

- **Ne jamais valider de données personnelles.** Vos vrais chiffres se trouvent dans
  `config/config.json` ainsi que dans les fichiers `model/` + `dashboard/` générés —
  tous ignorés par git. Avant chaque validation, lancez `git status` et confirmez
  qu'aucun d'eux n'est indexé. N'ajoutez pas de relevés, de feuillets fiscaux ni quoi
  que ce soit correspondant à `*credentials*` / `.env`.
- **Restez piloté par la configuration.** Aucun nom, solde, symbole boursier ou chemin
  codé en dur dans `engine/`. Si une valeur est propre à l'utilisateur, elle doit se
  trouver dans `config.example.json` et être lue par
  `engine/config_loader.py`.
- **Gardez les chiffres fiscaux et de prestations sourcés et datés.** Les chiffres
  canadiens changent souvent (bon nombre sont rajustés annuellement ou
  trimestriellement). Si vous mettez à jour un chiffre, citez l'année et la source dans
  [`docs/CANADA_RULES.md`](docs/CANADA_RULES.md).
- **C'est éducatif, pas un conseil.** N'ajoutez rien qui présente les résultats comme
  un conseil financier, fiscal ou en placement personnalisé. Consultez
  [`DISCLAIMER.md`](DISCLAIMER.md).

## Installation

```bash
python3 setup.py            # checks Python, installs deps, runs a smoke test
python3 engine/quarterly_update.py   # runs the demo end to end

python3 -m pip install -r requirements-dev.txt   # pytest
python3 -m pytest tests/ -q                       # run the test suite
```

Le « ménage Tremblay » fictif (`config/examples/tremblay_config.json`, Ontario)
et le « ménage Gagnon » (`config/examples/gagnon_config.json`, Québec) sont les
montages de démonstration — veuillez tester vos modifications par rapport aux deux pour
que les démos s'exécutent toujours sans accroc. Consultez
[`docs/TESTING.md`](docs/TESTING.md) pour savoir ce qui est couvert.

## Apporter une modification

1. Forkez le dépôt et créez une branche (`git checkout -b my-change`).
2. Apportez votre modification. Gardez les fonctions petites et lisibles; respectez le
   style existant.
3. Lancez `python3 -m pytest tests/ -q` et la démo
   (`python3 engine/quarterly_update.py`) et confirmez que rien ne casse. Le flux
   d'intégration continue (CI) exécute la suite de tests **et** la démo sur Python
   3.9–3.12; ajoutez un test pour tout nouveau comportement.
4. Ouvrez une demande de tirage (pull request) décrivant ce qui a changé et pourquoi.
   Des captures d'écran aident pour tout ce qui touche le tableau de bord.

## Signaler des problèmes / des idées

Ouvrez une issue GitHub. Éléments utiles à inclure : votre système d'exploitation et
votre version de Python, la commande que vous avez lancée et la sortie de
`python3 setup.py --check`. Veuillez **caviarder tout chiffre financier réel** des
journaux ou des captures d'écran avant de publier.

## Idées qui seraient particulièrement bienvenues

- Un onglet d'**optimiseur de fonte du REER / de récupération de la SV** plus complet
  (plan de retrait année par année qui maximise la fonte tout en restant sous la ligne
  de récupération) qui reste piloté par la configuration.
- **Modules provinciaux** — encoder les tranches, les surtaxes et les crédits de chaque
  province pour que l'outil puisse calculer le revenu net avec précision (le
  Québec/RRQ en particulier).
- Un onglet d'horaire de **retrait minimal du FERR** piloté par les facteurs prescrits
  dans `docs/CANADA_RULES.md`.
- Des tests sur les calculs de Monte-Carlo et de concentration.
- Des améliorations de la documentation et de l'installation pour les non-développeurs.
