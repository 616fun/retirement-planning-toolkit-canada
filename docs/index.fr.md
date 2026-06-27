# Trousse de planification de retraite canadienne 🇨🇦

Une trousse de planification de retraite autogérée et pilotée par configuration,
conçue pour le **Canada** — un modèle de chiffrier multi-onglets, un moteur Monte-Carlo,
un tableau de bord HTML et un moniteur de santé de l’action de l’employeur. Elle
modélise le système canadien de bout en bout : **REER, CELI, FERR, CRI/FRV, CELIAPP,
REEE**, **RPC + SV**, la **récupération de la SV**, l’**optimiseur d’impôt à vie de la
fonte du REER**, et l’**impôt provincial pour les 10 provinces + 3 territoires**.

L’outil est **bilingue** : indiquez `"language": "fr"` dans votre configuration et le
tableau de bord et le chiffrier s’affichent en français. Cette documentation existe en
anglais et en français — utilisez le sélecteur de langue en haut.

!!! warning "À titre indicatif seulement"
    Pas un conseil financier, fiscal ou de placement. Les chiffres fiscaux et de
    prestations changent — vérifiez auprès de [canada.ca](https://www.canada.ca) avant
    d’agir. Voir l’avis dans le
    [dépôt](https://github.com/616fun/retirement-planning-toolkit-canada/blob/main/DISCLAIMER.fr.md).

## Démarrage rapide

```bash
git clone https://github.com/616fun/retirement-planning-toolkit-canada.git
cd retirement-planning-toolkit-canada

python3 setup.py                       # vérifie Python, installe les dépendances, test de fumée
python3 engine/build_model.py          # bâtit le modèle de chiffrier
python3 engine/quarterly_update.py     # Monte-Carlo + tableau de bord
open dashboard/dashboard.html

cp config/config.example.json config/config.json   # puis saisissez vos chiffres
```

La configuration complète (y compris le guide Claude Cowork) se trouve dans
[`INSTALL.md`](https://github.com/616fun/retirement-planning-toolkit-canada/blob/main/INSTALL.fr.md).

## Contenu

- **[Règles canadiennes](CANADA_RULES.md)** — la référence sourcée des paramètres 2025 :
  SV/RPC/SRG, tranches fédérales + provinciales, plafonds REER/FERR/CELI/CELIAPP/REEE,
  et la correspondance É.-U.→Canada.
- **[Architecture](ARCHITECTURE.md)** — comment s’imbriquent le moteur piloté par
  configuration, le module fiscal, Monte-Carlo, le tableau de bord et l’optimiseur de
  fonte du REER.
- **[Santé de l’entreprise](COMPANY_HEALTH.md)** — le moniteur de concentration de
  l’action de l’employeur.
- **[Routine trimestrielle](QUARTERLY_WORKFLOW.md)** — le rythme pour tenir le plan à jour.
- **[Tests](TESTING.md)** — la suite pytest et ce qu’elle couvre.

> Adapté de la [Retirement Planning Toolkit](https://github.com/616fun/retirement-planning-toolkit)
> américaine; le moteur est partagé, la couche comptes/impôt/prestations est refaite
> pour le Canada.
