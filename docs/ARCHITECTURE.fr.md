# Architecture

La trousse est délibérément **pilotée par configuration** : aucune donnée personnelle
ne se trouve dans les scripts. Tout découle d'un seul fichier de configuration JSON,
de sorte que rediriger l'ensemble du système vers un autre ménage se fait en
remplaçant un seul fichier.

```
config/config.json  ─┐
                     ├─►  engine/config_loader.py  (single load point + derived math)
                     │
                     ├─►  engine/tax_ca.py             (federal + provincial tax + OAS clawback)
                     ├─►  engine/build_model.py        → model/financial_plan.xlsx
                     ├─►  engine/company_health.py      → live ticker health + RSU verdict
                     ├─►  engine/quarterly_update.py    → rebuild + Monte Carlo + dashboard
                     └─►  engine/refresh_dashboard.py   → dashboard/dashboard.html
```

Cette édition canadienne partage son moteur, son Monte-Carlo, son tableau de bord et
son moniteur de santé d'entreprise avec la
[Retirement Planning Toolkit](https://github.com/616fun/retirement-planning-toolkit)
américaine. Ce qui a changé, c'est la **couche métier** : la taxonomie des comptes,
le modèle des prestations gouvernementales, les contraintes fiscales et les onglets
du chiffrier.

## Source unique de vérité
`config/config.json` contient l'identité, les comptes, les actions de l'employeur,
les revenus, les **prestations gouvernementales (RPC/SV)** et les hypothèses. À
l'intérieur du **chiffrier**, l'onglet `Assumptions` joue le même rôle : tous les
autres onglets y renvoient au moyen de formules inter-feuilles plutôt que de coder en
dur des valeurs. Lorsque vous ajoutez une valeur, placez-la dans `Assumptions` et
créez un lien vers elle.

## Blocs de configuration (canadiens)
| Bloc | Contient |
|---|---|
| `household` | membres (avec `cpp_claim_age` + `oas_claim_age`), `province`, `pension_income_splitting` |
| `accounts` | REER, CELI, CRI, CELIAPP, non enregistré, non enregistré conjoint, encaisse/CPG, REEE |
| `employer_stock` | employeur, symbole boursier, volets, seuils de surveillance/réduction |
| `income` | salaire, prime, RSU, revenu du conjoint, régime de retraite à PD, passif |
| `government_benefits` | montants mensuels de RPC + SV par conjoint |
| `assumptions` | rendements, inflation, dépenses, répartition, **seuil de récupération de la SV**, montant personnel de base, âge de conversion du FERR, inclusion des gains en capital, plafonds REER/CELI, données provinciales |

`investable_total` **exclut le REEE** (réservé aux études d'un enfant, comme un 529
américain).

## Onglets du chiffrier (créés par build_model.py)
| Onglet | Rôle |
|---|---|
| Assumptions | Intrants maîtres — rendements, inflation, province, montant personnel de base, récupération de la SV, âge du FERR, RPC/SV, âges |
| Net Worth Snapshot | Tous les soldes de comptes + total + placements (excl. REEE + immobilier) |
| Income Streams | Salaire, prime, RSU, régime de retraite à PD, RPC + SV par conjoint, passif |
| Employer Concentration | Exposition aux actions de l'employeur c. seuils de surveillance/réduction |
| Year-by-Year Projections | Dépenses, pension, RPC+SV (intégrés progressivement à l'âge de demande de chaque conjoint), retraits du portefeuille, solde de fin d'année |
| Monte Carlo | Taux de réussite à 3 scénarios (alimenté par quarterly_update.py) |
| RRSP Meltdown | **Optimiseur d'impôt à vie** — recherche la cible de retrait qui minimise la valeur actualisée de l'impôt total (ci-dessous) |
| Action Plan | Éléments ouverts et vérifications récurrentes (maximisation du CELI, fonte, FERR avant 71 ans, fractionnement de pension, bénéficiaires) |

## Moteur fiscal et optimiseur de fonte (`engine/tax_ca.py` + l'onglet RRSP Meltdown)
`tax_ca.py` calcule l'impôt combiné **fédéral + provincial** sur le revenu ordinaire
(avec le montant personnel de base et la surtaxe de l'Ontario, le tout indexé à
l'inflation) plus l'**impôt de récupération de la SV** (récupération de la SV).
L'onglet RRSP Meltdown l'utilise pour effectuer une recherche par grille du retrait
annuel constant par conjoint de REER/FERR qui minimise la **valeur actualisée de
l'impôt total à vie** — l'impôt sur le revenu des deux conjoints de leur vivant +
la récupération de la SV, **plus l'impôt de disposition réputée terminal** sur tout
REER encore en place à l'horizon (le montant forfaitaire imposé à un seul déclarant
survivant, ce qui rend la fonte hâtive avantageuse). Il compare trois stratégies
(ne rien faire / remplir jusqu'à la récupération / optimale) et imprime le plan
année par année de la gagnante.

**Portée de la modélisation (mises en garde honnêtes).** Le fédéral + **les 10
provinces et 3 territoires** sont entièrement encodés; un code de province non
reconnu revient par défaut à l'Ontario avec un avertissement. Le Québec inclut ses
propres tranches, un montant personnel de base plus élevé, aucune surtaxe, et
l'**abattement fédéral de 16,5 %** (appliqué dans `income_tax()`); le RRQ est imposé
comme le RPC, alors inscrivez-le dans les champs `cpp_monthly`. Le moteur modélise
aussi les crédits pour **montant en raison de l'âge** et pour **revenu de pension**
(fédéral + ON + QC, symétriques) ainsi que la **cotisation au FSS** du Québec (voir
`docs/CANADA_RULES.md` §5c). L'optimiseur suppose que le revenu de retraite est
égalisé entre les conjoints à 65 ans et plus (fractionnement de pension / REER de
conjoint), actualise l'impôt au taux d'inflation, et traite le non enregistré + le
CELI + l'encaisse comme un coussin après impôt. Les réductions progressives du
montant personnel de base pour revenus élevés (fédéral et Manitoba) **sont**
modélisées (vérifiées par rapport à des calculatrices externes). Il ne modélise pas
encore l'impôt sur les **gains en capital** des comptes non enregistrés, le **crédit
d'impôt pour dividendes**, ni les plafonds de cotisation au CELI. À titre indicatif,
ce n'est pas un conseil — voir `docs/CANADA_RULES.md`.

## Convention de couleur des cellules
- Texte **vert** = lien inter-feuilles (`=Assumptions!C5`)
- Texte **noir** = formule intra-feuille
- Texte **bleu** = intrant codé en dur

## Modèle de dépersonnalisation
Parce que l'identité ne réside que dans la configuration et les fichiers de données
exclus de git, le partage du code est sûr par conception. Le `.gitignore` bloque
`config/config.json`, les artéfacts générés dans `model/` + `dashboard/`, les relevés,
et tout ce qui correspond à `*credentials*` ou `.env`.
