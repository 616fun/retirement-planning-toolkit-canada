
# Paramètres canadiens de retraite et d'impôt — Référence

**Objet :** Référence de paramètres faisant autorité et datée, destinée à une boîte à outils canadienne de planification de la retraite.
**Compilé :** Juin 2026.
**Convention :** Chaque chiffre est associé à l'année à laquelle il s'applique. Indexation fédérale pour 2025 = 2.3 %; pour 2026 = 2.7 % (ARC). L'Ontario est la province de démonstration par défaut.

> **Note sur les sources :** Plusieurs pages primaires de canada.ca bloquent la récupération automatisée. Lorsqu'un chiffre n'a pu être lu directement sur canada.ca, il est corroboré par TaxTips.ca (une référence fiscale professionnelle de longue date qui reproduit les valeurs de l'ARC/EDSC) et l'URL canada.ca d'origine est tout de même citée à des fins de traçabilité. Les éléments qui n'ont pu être pleinement confirmés sont explicitement signalés **⚠ VERIFY**.

---

## 1. Sécurité de la vieillesse (SV)

| Élément | Valeur | S'applique à | Source |
|---|---|---|---|
| Max mensuel, 65–74 ans | **$727.67/mo** | 2025 (T1–T4 de base) | canada.ca paiements SV |
| Max mensuel, 75 ans+ | **$800.44/mo** (~10 % plus élevé) | 2025 | canada.ca paiements SV |
| Max mensuel, 65–74 ans | **$742.31/mo** | 2026 | canada.ca paiements SV |
| Max mensuel, 75 ans+ | **$816.54/mo** | 2026 | canada.ca paiements SV |
| Seuil de l'impôt de récupération (récupération de la SV) | **$93,454** revenu net | année de revenu 2025 (touche la SV juil. 2026–juin 2027) | canada.ca impôt de récupération |
| Taux de récupération | **15%** du revenu net au-dessus du seuil | en vigueur | canada.ca impôt de récupération |
| Plafond de récupération complète, 65–74 ans | **≈ $151,668** revenu net | année de revenu 2025 | TaxTips / canada.ca |
| Plafond de récupération complète, 75 ans+ | **≈ $157,490** revenu net | année de revenu 2025 | TaxTips / canada.ca |
| Bonification pour report | **+0.6%/month** après 65 ans, jusqu'à **+36%** à 70 ans | en vigueur | canada.ca |

**Notes et signalements :**
- Les montants de la SV sont réajustés **trimestriellement** (janv. / avr. / juil. / oct.) selon l'IPC; les chiffres ci-dessus sont des valeurs de base/représentatives pour l'année. À traiter comme approximatifs à l'intérieur d'une année.
- Le montant pour les 75 ans+ reflète la bonification permanente de 10 % pour les aînés de 75 ans et plus (en vigueur depuis juillet 2022).
- ⚠ **VERIFY plafonds de récupération complète :** les sources divergent légèrement. Les chiffres alignés sur TaxTips/canada.ca donnent **$151,668 (65–74)** / **$157,490 (75+)** pour l'**année de revenu 2025**. Certains calculateurs secondaires citent **$152,062 / $157,923** — ceux-ci semblent correspondre à un cycle d'indexation différent/ultérieur. Le plafond se calcule mécaniquement ainsi : `threshold + (annual OAS / 0.15)`, de sorte qu'il évolue à la fois avec le seuil et le montant courant de la SV. Calculez-le dynamiquement dans la boîte à outils plutôt que de le coder en dur.
- La récupération est évaluée sur le revenu net **individuel** (ligne 23400), et non sur celui du ménage.

---

## 2. Régime de pensions du Canada (RPC)

| Élément | Valeur | S'applique à | Source |
|---|---|---|---|
| Pension de retraite mensuelle max @ 65 | **$1,433.00/mo** | 2025 | canada.ca montants RPC |
| Pension de retraite mensuelle max @ 65 | **$1,507.65/mo** | 2026 | canada.ca montants RPC |
| Moyenne mensuelle pour les nouveaux prestataires @ 65 | **≈ $900/mo (2025) / $925.35 (données récentes 2025–26)** | 2025–2026 | canada.ca statistiques RPC |
| Réduction pour demande anticipée | **−0.6%/month** avant 65 ans → jusqu'à **−36%** à 60 ans | en vigueur | canada.ca |
| Bonification pour demande différée | **+0.7%/month** après 65 ans → jusqu'à **+42%** à 70 ans | en vigueur | canada.ca |

**Notes :**
- Le maximum est rarement atteint; la plupart des retraités reçoivent bien en deçà (d'où la moyenne d'environ $900). La boîte à outils devrait permettre aux utilisateurs de saisir une estimation, en utilisant par défaut la moyenne plutôt que le maximum.
- Le RPC est un revenu individuel imposable. Il ne fait **pas** l'objet d'une exclusion distincte du test de récupération de la SV — c'est un revenu net ordinaire.

### RRQ (Régime de rentes du Québec) — équivalents
- Les résidents du Québec sont couverts par le **RRQ au lieu du RPC**. **Les montants maximaux et moyens des prestations sont essentiellement identiques au RPC** pour 2025–2026.
- La bonification pour report 65→70 est **la même : +0.7%/month (+42%)**.
- **Différence :** le RRQ peut être différé jusqu'à **72 ans** (contre 70 ans pour le RPC), ajoutant un autre +0.7%/mo (≈ +16.8 %), pour un maximum de **+58.8%** par rapport au montant à 65 ans. Le RPC plafonne à 70 ans.

---

## 3. Supplément de revenu garanti (SRG)

**Qui est admissible :** Un aîné à faible revenu qui (a) a **65 ans+**, (b) reçoit la **SV**, (c) est un **résident canadien**, et (d) a un revenu annuel inférieur au seuil du programme correspondant à son état matrimonial. Prestation non imposable; il faut généralement la redemander chaque année au moyen de la déclaration de revenus.

| Situation | Max mensuel (2025) | Plafond de revenu (approx.) |
|---|---|---|
| Célibataire / veuf(ve) / divorcé(e) | **≈ $1,086.88–$1,109.85/mo** | revenu inférieur à **≈ $22,056–$22,440** |
| Le conjoint reçoit la pleine SV | **≈ $654.23–$668.08/mo chacun** | revenu combiné inférieur à **≈ $29,136–$29,712** |
| Le conjoint ne reçoit PAS la SV/l'Allocation | **≈ $1,086.88/mo** | revenu combiné inférieur à **≈ $52,848–$53,904** |
| Le conjoint reçoit l'Allocation | **≈ $654.23/mo** | revenu combiné inférieur à **≈ $40,800–$41,616** |

**Source :** pages canada.ca montant des prestations / admissibilité du SRG (les chiffres sont réajustés trimestriellement).
- ⚠ **VERIFY trimestre exact :** les taux du SRG changent chaque trimestre et les plafonds de revenu sont indexés annuellement; les fourchettes ci-dessus couvrent les trimestres de 2025. Récupérez le chiffre trimestriel en direct pour un usage en production.
- Le revenu de SV (la pension de la SV elle-même) est **exclu** du test de revenu du SRG; la plupart des autres revenus sont comptabilisés.

---

## 4. Impôt fédéral sur le revenu (ARC)

### 4a. Tranches fédérales — 2025

| Taux | Fourchette de revenu imposable |
|---|---|
| **14.5%** | Premiers **$57,375** |
| 20.5% | $57,375 – $114,750 |
| 26.0% | $114,750 – $177,882 |
| 29.31% | $177,882 – $253,414 |
| 33.0% | Plus de $253,414 |

> Le taux le plus bas a été abaissé de 15 % à 14 % **à compter du 1er juillet 2025**, produisant un taux mixte de **14.5%** sur l'année complète pour 2025.

### 4b. Tranches fédérales — 2026

| Taux | Fourchette de revenu imposable |
|---|---|
| **14.0%** | Premiers **$58,523** |
| 20.5% | $58,523 – $117,045 |
| 26.0% | $117,045 – $181,440 |
| 29.29% | $181,440 – $258,482 |
| 33.0% | Plus de $258,482 |

**Source :** canada.ca taux d'impôt / TaxTips.ca.

### 4c. Montant personnel de base (MPB) — avec réduction graduelle pour revenu élevé

Le MPB fédéral est un montant **bonifié** qui se réduit graduellement pour les hauts revenus. La bonification diminue de façon linéaire à travers la tranche d'imposition supérieure; le montant de base demeure toujours.

| Année | MPB max (revenu ≤ seuil inférieur) | MPB min (revenu ≥ seuil supérieur) | Fourchette de revenu de réduction graduelle |
|---|---|---|---|
| **2025** | **$16,129** | **$14,538** | revenu net **$177,882 → $253,414** |
| **2026** | **$16,452** | **$14,829** | revenu net **$181,440 → $258,482** |

- Le MPB complet s'applique si le revenu net ≤ le seuil inférieur; le MPB minimum s'applique si ≥ le seuil supérieur; interpoler linéairement entre les deux.
- La fourchette de réduction graduelle = les bornes de la **4e tranche fédérale**.

---

## 5. Impôt provincial

### 5a. Taux marginaux supérieurs combinés par province/territoire (2025)

Fédéral + provincial combinés, tranche supérieure, revenu ordinaire.

| Province / Territoire | Taux marginal supérieur combiné (2025) |
|---|---|
| Terre-Neuve-et-Labrador | ~54.80% |
| Nouvelle-Écosse | ~54.00% |
| Île-du-Prince-Édouard | ~51.75% |
| Nouveau-Brunswick | ~52.50% |
| **Québec** | **~53.31%** |
| **Ontario** | **~53.53%** |
| Manitoba | ~50.40% |
| Saskatchewan | ~47.50% |
| **Alberta** | **~48.00%** |
| **Colombie-Britannique** | **~53.50%** |
| Yukon | ~48.00% |
| Territoires du Nord-Ouest | ~47.05% |
| Nunavut | ~44.50% |

**Source :** TaxTips.ca / PwC Tax Summaries (2025).

> ✅ **Les 13 administrations (10 provinces + 3 territoires) sont encodées** dans
> `engine/tax_ca.py` avec les tranches 2025 vérifiées, le MPB, les crédits d'âge/de pension, la surtaxe
> (Ontario seulement — celle de l'Î.-P.-É. a été éliminée en 2024), et, pour le Québec, l'abattement de 16.5 %
> + le FSS. Un test vérifie le taux marginal supérieur combiné de chacune. Un
> code de province non reconnu se replie sur l'Ontario avec un avertissement.
>
> ✅ **Vérifié indépendamment** par rapport à des calculateurs externes 2025 à $50k / $100k /
> $150k / $250k pour les 13 administrations — exact au dollar près aux revenus faibles/moyens; les
> revenus élevés concordent une fois appliquées les réductions graduelles du MPB pour revenu élevé fédérales ($16,129→$14,538)
> et du Manitoba ($15,780→$0) (toutes deux désormais modélisées dans `engine/tax_ca.py`).
> La 4e tranche fédérale est le **29%** prévu par la loi (un encodage antérieur de 29.31% —
> le taux effectif incluant la réduction du MPB — a été corrigé).

⚠ **VERIFY avant affichage :** ces chiffres de taux supérieurs varient de ~0.1–0.5 pp selon l'indexation annuelle et tout changement de taux; ON/BC/QC se regroupent étroitement près de 53.5 %. À traiter comme indicatifs; recalculez à partir des barèmes de tranches pour la précision.

### 5b. Ontario — barème provincial complet (2025, province de démonstration par défaut)

**Tranches :**

| Taux | Fourchette de revenu imposable |
|---|---|
| 5.05% | Premiers $52,886 |
| 9.15% | $52,886 – $105,775 |
| 11.16% | $105,775 – $150,000 |
| 12.16% | $150,000 – $220,000 |
| 13.16% | Plus de $220,000 |

**Surtaxe de l'Ontario** (appliquée à l'*impôt ontarien à payer*, et non au revenu) :
- **20%** sur l'impôt ontarien excédant **$5,710**
- **plus un montant additionnel de 36%** (soit 56 % au total) sur l'impôt ontarien excédant **$7,307**
- Effet net : le taux provincial *effectif* supérieur passe de 13.16 % à **~20.53%**, portant le taux supérieur combiné de l'Ontario à **~53.53%**.

> ⚠ Les seuils de surtaxe sont cités légèrement différemment selon les sources ($5,710/$7,307 vs $6,104/$7,812 vs $7,446) parce qu'ils sont indexés annuellement et que certaines sources les expriment comme le revenu imposable déclencheur équivalent plutôt que comme le seuil d'impôt à payer déclencheur. **Pour 2025, les seuils d'impôt à payer de l'ARC/TaxTips sont $5,710 (20 %) et $7,307 (36 %).** À vérifier par rapport au formulaire ON428 courant pour la production.

**Montant personnel de base de l'Ontario (2025) :** **$12,747** (crédité à 5.05 %).

L'Ontario prélève aussi une **contribution-santé** (jusqu'à $900/yr, fonction du revenu) — à noter par souci d'exhaustivité; encodez-la si vous modélisez précisément le revenu net après impôt en Ontario.

### 5c. Québec — barème provincial complet (2025) + l'abattement fédéral

Le Québec administre son propre impôt sur le revenu et les résidents du Québec produisent une **déclaration provinciale distincte**
(TP-1) en plus de la déclaration fédérale. Le moteur fiscal de la boîte à outils
(`engine/tax_ca.py`) encode le Québec en entier.

**Tranches du Québec (2025) :**

| Taux | Fourchette de revenu imposable |
|---|---|
| 14.00% | Premiers $53,255 |
| 19.00% | $53,255 – $106,495 |
| 24.00% | $106,495 – $129,590 |
| 25.75% | Plus de $129,590 |

(2026, indexé à 2.85 % : 14 % jusqu'à $54,345; 19 % jusqu'à $108,680; 24 % jusqu'à $132,245; 25.75 % au-delà.)

**Montant personnel de base du Québec (2025) :** **$18,571** (crédité à 14 %; aucune
réduction graduelle pour revenu élevé, contrairement au MPB fédéral).

**Aucune surtaxe provinciale** (contrairement à l'Ontario).

**L'abattement du Québec — 16.5 %.** C'est l'élément qui fait fonctionner le taux combiné
du Québec. L'**impôt fédéral de base d'un résident du Québec est réduit de 16.5 %**
(retrait historique : Ottawa cède 16,5 points de l'impôt fédéral des particuliers au Québec —
13,5 pour les paiements de remplacement au titre des programmes permanents + 3,0 pour les
allocations aux jeunes abandonnées — et le Québec finance ces services au moyen de son propre impôt provincial
plus élevé). Le moteur applique ceci dans `income_tax()` pour que les taux combinés du Québec ressortent
correctement : p. ex. le **taux marginal supérieur combiné est 53.31%** = fédéral 33 % × (1 − 0.165)
+ Québec 25.75 %. Sans l'abattement, les taux du Québec sembleraient ~9 pp trop élevés.

**RRQ au lieu du RPC.** Le Québec est couvert par le **Régime de rentes du Québec**. Les montants maximaux et
moyens sont **essentiellement identiques au RPC** (max 2025 de $1,433/mo à 65 ans), alors
saisissez le RRQ dans les champs `cpp_monthly`. Différences clés : le RRQ peut être **différé jusqu'à
72 ans** (contre 70 ans pour le RPC) pour un maximum de **+58.8%** par rapport au montant à 65 ans, et la réduction pour demande anticipée
est graduée à **0.5–0.6%/mo** (utilisez 0.6%/mo pour un demandeur à pension maximale).

**Particularités du Québec que le moteur modélise MAINTENANT** (ajoutées pour que l'outil n'induise pas en erreur les retraités
québécois) : la **contribution individuelle au Fonds des services de santé (FSS)** — 1 % sur le revenu de
pension / FERR / placement (SV et emploi **exclus**), avec une exemption de $18,130
et un plafond de $1,000/yr (de sorte qu'un retraité québécois qui liquide un REER la paie, jusqu'au
plafond) — et le **crédit groupé d'âge + de revenu de retraite** du Québec (14 % de l'âge $3,906 +
retraite $3,470, réduit de 18,75 % du revenu familial net au-delà de $42,090). Les crédits d'âge et
de pension sont modélisés **symétriquement** au fédéral et en Ontario aussi, de sorte que la
comparaison ON c. QC demeure équitable. Voir `engine/tax_ca.py`.

**Toujours PAS modélisés** (réellement de second ordre ici) : le « montant pour personne
vivant seule » du Québec, les différences de **retenue** REER/FERR (un acompte, et non un impôt final, de sorte qu'il
ne change pas la réponse en matière d'impôt sur la vie entière), et tout impôt sur les gains en capital non enregistrés.
L'ancienne **contribution santé du Québec par adulte a été abolie en 2017** — non modélisée.

⚠ **VERIFY** (pages Retraite Québec / Revenu Québec bloquées à la récupération automatisée) : la
prestation *moyenne* du RRQ 2025, les seuils exacts des bandes intermédiaires du FSS ($33,130 /
$63,060 / $148,600 — l'exemption, le taux de 1 % et le plafond de $1,000 sont fermes), et le libellé exact
de l'âge pour le fractionnement de pension au Québec. Confirmez avant de vous fier à ces spécificités.

**Source :** Revenu Québec; canada.ca (abattement du Québec, ligne 44000); TaxTips.ca;
Retraite Québec; tables RRQ/RPC RCGT 2025.

---

## 6. REER (Régime enregistré d'épargne-retraite)

| Élément | Valeur | Année |
|---|---|---|
| Plafond de cotisation annuel | **le moindre de 18 % du revenu gagné de l'année précédente OU $32,490** | 2025 |
| Plafond de cotisation annuel | **le moindre de 18 % du revenu gagné de l'année précédente OU $33,810** | 2026 |
| Conversion obligatoire | Doit convertir le REER → **FERR (ou rente) au plus tard le 31 déc. de l'année de vos 71 ans** | en vigueur |

- Les droits de cotisation REER inutilisés **se reportent** indéfiniment.
- Vous pouvez encore cotiser jusqu'au 31 déc. de l'année de vos 71 ans (à votre propre REER), après quoi il doit être liquidé.

### Retenue sur retrait forfaitaire d'un REER (résidents hors Québec)

| Montant du retrait | Retenue fédérale |
|---|---|
| Jusqu'à $5,000 | **10%** |
| $5,001 – $15,000 | **20%** |
| Plus de $15,000 | **30%** |

- **Résidents du Québec :** 5 % / 10 % / 15 % au fédéral **plus** 14 % de retenue du Québec.
- **Non-résidents :** taux fixe de **25%** (peut être réduit par convention fiscale).
- La retenue est un **acompte**, et non un impôt final — réconcilié à la déclaration. **Les retraits *minimaux* d'un FERR ne sont PAS assujettis à la retenue** (voir §7).

### Notions de base du REER de conjoint
- Le **conjoint à revenu plus élevé cotise** (et obtient la déduction) à un régime **dont le conjoint à revenu plus faible est titulaire**, lequel est imposé sur les retraits éventuels — un outil de fractionnement du revenu pour la retraite.
- **Règle d'attribution de 3 ans :** si le conjoint rentier retire dans l'année civile d'une cotisation ou les **2 années suivantes**, le retrait est réimposé au **cotisant** à concurrence des cotisations récentes.

---

## 7. FERR (Fonds enregistré de revenu de retraite)

**Facteurs de retrait minimal prescrits** (règles post-2015), appliqués au **solde du compte au 1er janv.** :

| Âge | Facteur | Âge | Facteur |
|---|---|---|---|
| 71 | 5.28% | 84 | 8.08% |
| 72 | 5.40% | 85 | 8.51% |
| 73 | 5.53% | 86 | 8.99% |
| 74 | 5.67% | 87 | 9.55% |
| 75 | 5.82% | 88 | 10.21% |
| 76 | 5.98% | 89 | 10.99% |
| 77 | 6.17% | 90 | 11.92% |
| 78 | 6.36% | 91 | 13.06% |
| 79 | 6.58% | 92 | 14.49% |
| 80 | 6.82% | 93 | 16.34% |
| 81 | 7.08% | 94 | 18.79% |
| 82 | 7.38% | 95+ | 20.00% |
| 83 | 7.71% | | |

**Source :** canada.ca « Tableau – Facteurs prescrits ».

- **Les minimums ne sont PAS assujettis à la retenue d'impôt.** Les montants retirés **au-dessus** du minimum sont assujettis aux mêmes paliers de retenue de 10/20/30 % que les retraits REER (§6).
- Pour les **âges inférieurs à 71 ans** (p. ex. une conversion anticipée en FERR), le facteur est `1 / (90 − age)`.
- Optionnel : vous pouvez fonder les minimums sur l'**âge d'un conjoint plus jeune** (à choisir lors de l'établissement du FERR) afin de réduire les retraits obligatoires.

---

## 8. CELI (Compte d'épargne libre d'impôt)

| Élément | Valeur |
|---|---|
| Plafond annuel, **2025** | **$7,000** |
| Plafond annuel, **2026** | **$7,000** (3e année à ce niveau) |
| **Droits cumulatifs depuis 2009** (admissible tout au long, jamais cotisé) | **$102,000 (au 2025)** → **$109,000 (au 2026)** |

- L'admissibilité à accumuler des droits commence l'année de vos **18** ans, en tant que résident canadien.
- **Les retraits rétablissent les droits** — mais **seulement l'année civile *suivante***, et non la même année. Recotiser un montant retiré la même année peut entraîner une pénalité pour cotisation excédentaire (1 %/mois sur l'excédent).
- La croissance et les retraits sont **entièrement libres d'impôt** et ne comptent **pas** comme un revenu (donc aucun impact sur la récupération de la SV ou le SRG) — un levier de planification clé.

**Historique des plafonds annuels (pour le calcul cumulatif) :** 2009–2012 $5,000; 2013–2014 $5,500; 2015 $10,000; 2016–2018 $5,500; 2019–2022 $6,000; 2023 $6,500; 2024–2026 $7,000.

---

## 9. REEE (Régime enregistré d'épargne-études)

| Élément | Valeur |
|---|---|
| Appariement de la **SCEE** (Subvention canadienne pour l'épargne-études) | **20%** des cotisations annuelles |
| SCEE max par bénéficiaire par année | **$500** (sur les premiers $2,500 cotisés; jusqu'à $1,000/yr en rattrapant une année antérieure) |
| SCEE max **à vie** par bénéficiaire | **$7,200** |
| Plafond de **cotisation à vie** au REEE par bénéficiaire | **$50,000** (aucun plafond annuel; cotisation excédentaire pénalisée à 1 %/mois) |
| Disponibilité de la SCEE | jusqu'à la fin de l'année où le bénéficiaire atteint **17** ans |

**SCEE supplémentaire (SCEE-S) :** les familles à revenu faible/moyen obtiennent un **10–20 %** additionnel sur les premiers $500 cotisés annuellement.

**Bon d'études canadien (BEC) :** pour les enfants de familles à **faible revenu** nés en **2004 ou après**. **Aucune cotisation requise.** **$500** la première année + **$100/year** par la suite jusqu'à un maximum à vie de **$2,000** (admissibilité jusqu'à 15 ans; peut être réclamé jusqu'à 20 ans par le bénéficiaire).

**Source :** pages canada.ca REEE / SCEE / BEC.

---

## 10. CELIAPP (Compte d'épargne libre d'impôt pour l'achat d'une première propriété)

| Élément | Valeur |
|---|---|
| Plafond de cotisation annuel | **$8,000** |
| Plafond de cotisation à vie | **$40,000** |
| Report | Jusqu'à **$8,000** de droits inutilisés se reportent à l'année suivante (soit un max de **$16,000** en une année); tout droit inutilisé au-delà de $8,000/yr est **perdu** |
| Durée de vie du compte | Doit être fermé au plus tard à la fin de l'année du **15e anniversaire** ou de l'année de vos **71** ans, selon la première éventualité |

**Mécanique :** Les cotisations sont **déductibles d'impôt** (comme un REER) **et** les retraits admissibles pour l'achat d'une première propriété sont **libres d'impôt** (comme un CELI) — le seul compte combinant les deux. Les droits commencent à s'accumuler **seulement après l'ouverture du compte** (contrairement au CELI/REER). Peut être combiné avec le **Régime d'accession à la propriété** du REER.

**Source :** pages canada.ca CELIAPP.

---

## 11. CRI / FRV (Comptes immobilisés)

- **CRI (Compte de retraite immobilisé) :** détient des fonds **transférés hors d'un régime de retraite enregistré d'employeur** lorsque vous quittez l'employeur. Comme un REER mais **immobilisé** — généralement **aucun retrait avant 55 ans**, et il ne peut pas être simplement encaissé.
- **Conversion :** Un CRI doit être converti en **FRV** (Fonds de revenu viager), en une variante de FERR immobilisé (FRRI/FRVR selon l'administration), ou en une **rente viagère** au plus tard le **31 déc. de l'année de vos 71 ans** — même échéance que REER→FERR.
- **Les retraits d'un FRV ont À LA FOIS un minimum ET un maximum :**
  - **Minimum** = mêmes facteurs FERR prescrits (§7).
  - **Maximum** = un plafond propre à l'administration, fonction de l'âge et du solde (conçu pour faire durer l'argent). Ce **double min/max** est la différence clé par rapport à un FERR ordinaire, qui n'a qu'un minimum.
- **Déblocage :** De nombreuses administrations permettent un **déblocage unique de 50 %** vers un REER/FERR à 55 ans (les règles varient au fédéral c. par province), en plus des dispositions de déblocage pour petit solde et difficultés financières.

⚠ **L'administration compte :** Les règles des comptes immobilisés sont fixées par l'**administration dont relève le régime de retraite** (fédéral/BSIF ou une province donnée). Les formules de retrait maximal et les droits de déblocage diffèrent. Encodez par administration; ne supposez pas une règle nationale unique.

---

## 12. Gains en capital et dividendes

### Taux d'inclusion des gains en capital — STATUT ACTUEL

- **Le taux d'inclusion est de 50 %.** ✅
- La hausse proposée à **66.67%** sur les gains au-delà de **$250,000/yr** (particuliers) — annoncée dans le Budget 2024, date d'entrée en vigueur le 25 juin 2024 — a été **reportée** (31 janv. 2025) puis **officiellement ANNULÉE** (annoncée le **21 mars 2025**). **Elle n'est jamais devenue loi.**
- Donc pour **2025 et 2026**, tous les gains en capital sont inclus à **50%**, sans palier de $250k.
- **Un changement qui A bel et bien été adopté :** l'**Exonération cumulative des gains en capital** (actions admissibles de petite entreprise / biens agricoles et de pêche admissibles) est passée à **$1.25 million** (rétroactif au 25 juin 2024).

**Source :** canada.ca ministère des Finances (report du 31 janv. 2025; annulation du 21 mars 2025).

### Crédit d'impôt pour dividendes déterminés (majoration + crédit) — conceptuel, 2025

| | Majoration | Crédit d'impôt fédéral pour dividendes |
|---|---|---|
| Dividendes **déterminés** (revenu de grande société) | **+38%** | **15.0198%** du montant majoré (imposable) |
| Dividendes **non déterminés** (revenu de petite entreprise SPCC) | **+15%** | **9.0301%** du montant majoré |

**Concept :** Le dividende est « majoré » pour approximer le revenu d'entreprise avant impôt, l'impôt est calculé sur le montant majoré, puis le **crédit d'impôt pour dividendes** compense l'impôt des sociétés déjà payé (intégration). Les provinces ajoutent leurs **propres** crédits d'impôt pour dividendes par-dessus. Effet net : les dividendes déterminés sont imposés à des taux avantageux — dans les tranches inférieures, le taux effectif combiné peut même être **négatif**.

---

## 13. Fractionnement du revenu de pension

- **Jusqu'à 50 %** du **revenu de pension admissible** peut être attribué à un époux/conjoint de fait au moyen d'un **choix conjoint (formulaire T1032)** produit avec les deux déclarations. Aucun argent ne change réellement de mains — c'est une réattribution aux fins de la déclaration fiscale.
- **Montant de revenu de pension de $2,000** — un crédit fédéral non remboursable sur jusqu'à $2,000 de revenu de pension admissible; le fractionnement peut permettre au conjoint **bénéficiaire** de réclamer aussi son propre crédit de $2,000.
- **Règles d'âge pour ce qui compte comme « revenu de pension admissible » :**
  - **Moins de 65 ans :** principalement les paiements de **rente viagère d'un régime de pension agréé (RPA)**. **Le revenu de FERR/rente REER NE se qualifie PAS encore** pour le fractionnement.
  - **65 ans+ :** la liste **s'élargit** pour inclure les **retraits de FERR, les paiements de rente REER et les paiements de FRV** — de sorte que **le revenu de FERR devient fractionnable à 65 ans**.
- Les deux conjoints doivent être **résidents du Canada le 31 déc.** de l'année d'imposition.

**Source :** canada.ca fractionnement du revenu de pension.

---

## 14. Principales différences conceptuelles par rapport au système américain (à encoder)

1. **Déclaration individuelle, et non conjointe.** Le Canada n'a **pas de déclaration conjointe pour personnes mariées**. Chaque conjoint produit séparément. C'est *pourquoi* les REER de conjoint, le fractionnement du revenu de pension et les transferts de crédit entre conjoints existent — ce sont les contournements de l'absence de déclaration conjointe. Le planificateur doit modéliser **deux déclarations fiscales distinctes** et optimiser le *placement* du revenu entre les conjoints.

2. **Aucun équivalent à l'IRMAA — sauf la récupération de la SV.** Il n'y a pas d'échelle de surcharge de prime d'assurance-maladie. L'analogue fonctionnel est l'**impôt de récupération de la SV** (§1) : dès que le revenu net individuel dépasse **$93,454 (2025)**, la SV est récupérée à **15 %**. C'est le « seuil-couperet de revenu » le plus important à gérer dans le séquençage du revenu de retraite canadien — le pendant direct de la gestion des paliers d'IRMAA aux États-Unis.

3. **Liquidation de REER ≈ échelle de conversion Roth.** Le Canada n'a **aucun compte Roth** ni **aucune conversion Roth**. La stratégie analogue est la **« liquidation de REER »** (RRSP meltdown) : retirer délibérément les soldes de REER/FERR pendant les **années à faible revenu** (généralement l'écart entre la retraite et l'âge de 71 ans / le début du RPC/de la SV) afin de (a) lisser le taux d'imposition, (b) éviter d'être forcé à de gros **retraits minimaux obligatoires de FERR** plus tard, et (c) maintenir le revenu futur **sous le seuil de récupération de la SV**. Même esprit qu'une échelle Roth — remplir tôt les tranches inférieures — mais c'est un *retrait-et-imposition*, et non une *conversion vers un compte libre d'impôt*. Le **CELI** est la destination des fonds liquidés dont vous n'avez pas besoin de dépenser (libres d'impôt, sans incidence sur la récupération).

4. **Aucun équivalent à l'HSA.** Le Canada a des **soins de santé publics**; il n'y a **aucun compte d'épargne-santé (Health Savings Account)** ni de nécessité de modéliser des cotisations/retraits d'HSA ou une ligne de prime d'assurance-maladie. (Remarque : des comptes de dépenses de santé privés/d'employeur existent, mais ce ne sont pas un véhicule d'épargne-retraite.) La modélisation des soins de santé à la retraite porte plutôt sur l'assurance complémentaire, les soins dentaires/visuels et les lacunes en médicaments d'ordonnance — et non sur un compte médical d'épargne fiscalement avantageux.

**Notes structurelles additionnelles pour le modèle :**
- L'**âge de 71 ans** est l'âge universel de « liquidation » : REER→FERR, CRI→FRV, fermeture du CELIAPP — le tout au plus tard le 31 déc. de cette année-là.
- La **SV/le SRG/le RPC** sont indexés et réajustés selon des cycles **trimestriels** (SV/SRG) ou **annuels** (RPC) — prévoyez des points d'actualisation plutôt que de coder en dur.
- Toute la croissance des comptes enregistrés est **à imposition différée (REER/FERR/CRI/FRV/REEE)** ou **libre d'impôt (CELI/CELIAPP)** à l'intérieur du compte; les événements fiscaux surviennent au **retrait** (comptes à imposition différée) uniquement.

---

## Source URLs (primary references)

- OAS amounts: https://www.canada.ca/en/services/benefits/publicpensions/old-age-security/payments.html
- OAS recovery tax: https://www.canada.ca/en/services/benefits/publicpensions/old-age-security/recovery-tax.html
- CPP amounts: https://www.canada.ca/en/services/benefits/publicpensions/cpp/payment-amounts.html
- CPP/OAS quarterly figures: https://www.canada.ca/en/employment-social-development/programs/pensions/pension/statistics/2026-quarterly-january-march.html
- GIS benefit amount: https://www.canada.ca/en/services/benefits/publicpensions/old-age-security/guaranteed-income-supplement/benefit-amount.html
- Federal tax rates: https://www.canada.ca/en/revenue-agency/services/tax/individuals/frequently-asked-questions-individuals/canadian-income-tax-rates-individuals-current-previous-years.html
- TaxTips federal: https://www.taxtips.ca/taxrates/canada.htm
- TaxTips Ontario: https://www.taxtips.ca/taxrates/on.htm
- RRSP withholding: https://www.canada.ca/en/revenue-agency/services/tax/individuals/topics/rrsps-related-plans/making-withdrawals/tax-rates-on-withdrawals.html
- RRIF prescribed factors: https://www.canada.ca/en/revenue-agency/services/tax/businesses/topics/completing-slips-summaries/t4rsp-t4rif-information-returns/payments/chart-prescribed-factors.html
- RESP / CESG: https://www.canada.ca/en/revenue-agency/services/tax/individuals/topics/registered-education-savings-plans-resps/canada-education-savings-programs-cesp/canada-education-savings-grant-cesg.html
- Canada Learning Bond: https://www.canada.ca/en/revenue-agency/services/tax/individuals/topics/registered-education-savings-plans-resps/canada-education-savings-programs-cesp/canada-learning-bond.html
- FHSA: https://www.canada.ca/en/revenue-agency/services/tax/individuals/topics/first-home-savings-account/contributing-your-fhsa.html
- Capital gains deferral/cancellation: https://www.canada.ca/en/department-finance/news/2025/01/government-of-canada-announces-deferral-in-implementation-of-change-to-capital-gains-inclusion-rate.html
- Federal dividend tax credit: https://www.canada.ca/en/revenue-agency/services/tax/individuals/topics/about-your-tax-return/tax-return/completing-a-tax-return/deductions-credits-expenses/line-40425-federal-dividend-tax-credit.html
- Pension income splitting: https://www.canada.ca/en/revenue-agency/services/tax/individuals/topics/pension-income-splitting.html
