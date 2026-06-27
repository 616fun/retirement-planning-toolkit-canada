# Tests

La trousse fournit une suite `pytest` sous `tests/`. Elle s'exécute en CI à chaque
poussée sur Python 3.9–3.12, et vous pouvez l'exécuter localement en quelques secondes.

```bash
python3 -m pip install -r requirements.txt -r requirements-dev.txt
python3 -m pytest tests/ -q
```

(`tests/conftest.py` ajoute `engine/` au chemin d'importation, donc aucune installation
du paquet lui-même n'est nécessaire.)

## Ce qui est couvert

| Fichier | Objet |
|---|---|
| `test_tax_ca.py` | Moteur fiscal — tranches fédérales/de l'Ontario/du Québec, l'abattement québécois de 16,5 %, l'abri du MPB, les crédits pour âge + pension et leurs réductions progressives, les paliers du FSS québécois, la récupération de la SV, les valeurs de taux marginal, la monotonie et le repli province-inconnue → Ontario. Les valeurs attendues sont ancrées aux chiffres sourcés dans [`CANADA_RULES.md`](CANADA_RULES.md). |
| `test_config_loader.py` | Chargement de la configuration, `investable_total` (REEE exclu), calcul de concentration (y compris avec zéro montant investissable), `current_age` et `validate_config` — vérifie que chaque configuration fournie passe et que les mauvaises (1 ou 3 membres, section manquante, solde non numérique) lèvent une erreur `ConfigError` claire énumérant tous les problèmes. |
| `test_meltdown.py` | Facteurs prescrits du FERR, invariants de la simulation de fonte (le REER n'est jamais négatif, l'impôt terminal ≥ 0), l'optimiseur qui bat l'inaction, le déterminisme, le fait que le Québec coûte plus cher que l'Ontario pour le même ménage, et la reproductibilité de Monte-Carlo (germe fixe) + l'étendue. |
| `test_integration.py` | Les deux démos construisent les 8 onglets du classeur; le classeur fait un aller-retour via openpyxl; le tableau de bord s'affiche (avec et sans sommaire de Monte-Carlo); la superposition de saisie trimestrielle est sans effet lorsqu'aucun fichier n'est fourni. |

## Conventions

- **Déterminisme.** Le Monte-Carlo utilise un germe fixe, de sorte que les taux de
  réussite sont reproductibles et affirmés exactement. Gardez-le ainsi — n'introduisez
  pas d'aléatoire non germé dans le moteur.
- **Attentes sourcées.** Lorsque vous modifiez un chiffre fiscal, mettez à jour à la
  fois `engine/tax_ca.py` / la configuration et l'assertion correspondante, et citez
  l'année + la source dans `CANADA_RULES.md`.
- **Aucun réseau dans les tests.** Les tests n'accèdent jamais à Yahoo/EDGAR; le
  moniteur de santé d'entreprise est exercé séparément (et toléré comme pouvant
  échouer) dans l'exécution de démonstration de la CI.
