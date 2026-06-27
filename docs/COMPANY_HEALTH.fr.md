# Santé de l'entreprise et décisions sur les RSU

Lorsqu'une grande part de votre valeur nette repose sur un seul employeur — paie,
prime, actions de l'entreprise détenues dans votre REER, RSU en acquisition, et
souvent un régime de retraite à PD — la santé de cette entreprise est un **intrant de
planification de la retraite**, et non un passe-temps secondaire. Les employés des
grandes banques, télécoms, sociétés ferroviaires et entreprises énergétiques
canadiennes connaissent bien cette exposition. `engine/company_health.py` transforme
les données publiques sur le symbole boursier que vous avez configuré en quelques
signaux axés sur la décision.

## Ce qu'il extrait (gratuit, sans clés d'API)
| Source | Ce qu'elle vous donne |
|---|---|
| Yahoo Finance (`yfinance`) | Cours, rendement depuis le début de l'année / sur 1 an, ratio C/B prévisionnel, rendement du dividende, cible de consensus des analystes + potentiel de hausse implicite |
| SEC EDGAR (`edgartools`) | Achats/ventes d'initiés sur le marché libre (formulaire 4) (sentiment), événements importants (8-K), ventes planifiées (formulaire 144) (surplomb) |
| Votre configuration | Exposition aux actions de l'employeur en % des actifs en placement c. vos seuils de surveillance/réduction |

> **Note canadienne.** Utilisez l'**inscription au NYSE** des titres inscrits à plus
> d'une bourse pour la meilleure couverture Yahoo Finance — `RY`, `TD`, `BNS`, `ENB`,
> `CNQ`, `SHOP`, `CNR`, etc. Le **signal d'initiés SEC EDGAR est propre aux
> États-Unis** : les émetteurs domiciliés au Canada déclarent sur **SEDI** (le système
> des initiés du Canada), et non sur le formulaire 4 de la SEC, de sorte que le
> panneau initiés/8-K/144 revient vide pour eux. Le module se dégrade gracieusement —
> le cours, les rendements, la valorisation et les cibles des analystes fonctionnent
> toujours. (Un symbole TSX `.TO` fonctionne aussi pour les données de cours via
> Yahoo; l'inscription au NYSE offre habituellement des champs d'analystes plus
> riches.)

## Les quatre signaux
1. **Valorisation et momentum** — l'action est-elle bon marché/chère et en tendance
   haussière ou baissière?
2. **Sentiment des initiés** — (déclarants américains) les dirigeants achètent rarement
   leurs propres actions à moins d'être optimistes; une vente groupée par la haute
   direction mérite d'être surveillée.
3. **Risque d'événement** — (déclarants américains) des 8-K récents et un bond des
   ventes planifiées (formulaire 144) peuvent signaler un surplomb avant qu'il
   n'apparaisse dans le cours.
4. **Verdict de concentration** — `OK` / `WATCH` / `TRIM` selon vos seuils, avec un
   montant concret en dollars à réduire si vous dépassez.

## Comment cela éclaire les décisions sur les RSU
Chaque fois que des RSU sont acquises, vous choisissez : conserver ou diversifier. Le
moniteur vous donne une base reproductible pour cette décision —

- **Verdict TRIM** → vendez d'abord les RSU en acquisition (coût de base le plus élevé,
  moins de friction fiscale) pour ramener l'exposition sous votre seuil de réduction.
  (Dans un compte **non enregistré**, tenez compte du gain en capital à inclusion de
  50 % sur la vente.)
- **Verdict WATCH** → dirigez les nouvelles acquisitions vers des fonds diversifiés
  plutôt que de les conserver.
- **Verdict OK** → conserver l'acquisition reste dans la tolérance.

Configurez-le dans `config.json` :
```json
"employer_stock": {
  "employer_name": "Royal Bank of Canada",
  "ticker": "RY",
  "watch_threshold_pct": 5.0,
  "trim_threshold_pct": 7.0,
  "holdings": { "employer_stock_in_rrsp": 0, "unvested_rsu_value": 0, "vested_shares_value": 0 }
}
```

SEC EDGAR exige une chaîne d'identité de contact (`"Your Name you@example.com"`).
Définissez-la comme `employer_stock.sec_identity` (ou `sec_identity` au niveau
supérieur). Elle ne sert qu'à la recherche d'initiés américains — sans danger de la
laisser à la valeur par défaut pour un émetteur uniquement canadien.

## Exécution
```bash
python3 engine/company_health.py                 # uses your config ticker
python3 engine/company_health.py --ticker TD     # any public company
python3 engine/company_health.py --days 30 --json health.json
```

> Aide à la surveillance seulement — pas une recommandation d'achat/vente. Voir
> `DISCLAIMER.md`.
