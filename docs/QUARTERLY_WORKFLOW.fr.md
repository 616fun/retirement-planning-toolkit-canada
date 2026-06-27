# Flux de travail trimestriel

Un rythme reproductible pour garder le plan à jour.

## Chaque trimestre
1. Copiez `templates/quarterly_input_TEMPLATE.json` → `quarterly_input_Q#_YYYY.json`.
2. Saisissez les nouveaux soldes de comptes (CAD) à partir de vos relevés (laissez `null` pour conserver la valeur précédente).
3. Mettez à jour `employer_stock_holdings` pour que la vérification de concentration reste exacte.
4. Exécutez le pipeline :
   ```bash
   RPT_CONFIG=config/config.json \
   python3 engine/quarterly_update.py --input quarterly_input_Q3_2026.json
   ```
   Cela reconstruit le classeur, exécute un Monte-Carlo de 10 000 trajectoires sur
   trois scénarios de rendement, inscrit les taux de réussite dans le modèle et
   actualise le tableau de bord.
5. Exécutez la vérification de santé de l'entreprise et examinez le verdict
   RSU/concentration :
   ```bash
   python3 engine/company_health.py
   ```
6. Parcourez le tableau de bord (`dashboard/dashboard.html`) et mettez à jour votre
   base de connaissances si quelque chose d'important a changé.

## Annuellement
- Rafraîchissez les **tranches d'imposition fédérales + provinciales**, le **montant
  personnel de base** et les plafonds de cotisation (**plafond en dollars du REER**,
  **plafond annuel du CELI**, **CELIAPP**) dans `config.json`. Voir
  [`docs/CANADA_RULES.md`](CANADA_RULES.md).
- Rafraîchissez le **seuil de récupération de la SV**
  (`assumptions.oas_clawback_threshold`) — il s'indexe chaque année et constitue le
  plafond que vise votre plan de fonte du REER.
- Revérifiez les estimations de prestations du **RPC/SV** (Mon dossier Service Canada)
  et votre **choix de prestation de survivant** du régime de retraite à PD (régime
  réversible recommandé).
- Confirmez la piste de **conversion du REER → FERR** : elle doit avoir lieu au plus
  tard le **31 décembre de l'année où le conjoint le plus âgé atteint 71 ans**
  (CRI → FRV à la même échéance).
- Réexaminez le **fractionnement du revenu de pension** (admissible à 65 ans pour le
  revenu de FERR).
- Relecture complète de la base de connaissances; réinitialisez sa date de
  « Dernière révision ».

## Surveillez la ligne de récupération de la SV
Parce que les montants de la SV/du SRG sont réinitialisés **trimestriellement** et que
le seuil de récupération s'indexe **annuellement**, traitez ces chiffres comme des
intrants vivants. Lorsque le revenu net projeté d'un conjoint approche de
`oas_clawback_threshold`, c'est le signal d'alléger les retraits du REER/FERR cette
année-là (ou de modifier l'ordre des retraits) — l'équivalent canadien de la gestion
des paliers IRMAA américains.

## Sécurité
- `config/config.json` et tous les fichiers `quarterly_input_Q*.json` sont exclus de git.
- Ne validez jamais de relevés ni quoi que ce soit contenant des soldes réels. Le
  `.gitignore` est configuré pour les bloquer, mais vérifiez `git status` avant chaque
  validation.
