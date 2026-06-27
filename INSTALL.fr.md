**Français** · [English](INSTALL.md)

# Guide d'installation

Deux façons d'utiliser cette trousse : à l'intérieur de **Claude Cowork** (aucun terminal requis) ou
à partir d'un **terminal** avec Python. Les deux utilisent le même bootstrap `setup.py`, qui
vérifie votre Python, demande avant d'installer quoi que ce soit, et exécute un test de fumée.

---

## Option A — L'utiliser dans Claude Cowork (recommandé pour les non-développeurs)

1. **Récupérez les fichiers sur votre ordinateur.** Téléchargez ce dépôt sous forme de ZIP depuis GitHub
   (bouton vert **Code** → **Download ZIP**) et décompressez-le, ou faites un `git clone`.
2. **Ouvrez Claude desktop → mode Cowork** et **connectez le dossier** que vous venez de
   décompresser (le dossier contenant ce `INSTALL.md`).
3. **Demandez à Claude de le configurer.** Par exemple :
   > « Exécute `python3 setup.py --yes` dans ce dossier, puis lance la démo. »

   Claude vous demandera votre approbation pour exécuter la commande. `setup.py` vérifie les
   quatre dépendances (`openpyxl`, `numpy`, `yfinance`, `edgartools`), installe celles
   qui manquent, et confirme par un test de fumée. Vous approuvez l'exécution — c'est
   l'étape d'approbation de l'installation. Rien ne s'installe sans votre feu vert.
4. **Voyez-le fonctionner sur la démo.** Demandez :
   > « Lance la démo : construis le modèle, exécute la mise à jour trimestrielle, et montre-moi le tableau de bord. »
5. **Personnalisez-le.** Demandez à Claude de vous guider à travers l'entrevue :
   > « Utilise la compétence retirement-interview pour construire ma configuration et ma base de connaissances. »

   Cela produit votre propre `config/config.json` (qui reste privé et n'est jamais
   committé) et une base de connaissances personnelle. À partir de là, demandez simplement à Claude de
   « lancer la mise à jour trimestrielle » ou de « vérifier la santé de mon entreprise » quand vous le souhaitez.

> Optionnel : le `skills/retirement-interview/SKILL.md` inclus peut être ajouté comme
> compétence Cowork afin d'être accessible par son nom. Vous pouvez aussi simplement y pointer Claude.

---

## Option B — L'utiliser à partir d'un terminal

La trousse est du Python pur et fonctionne de la même façon sous macOS, Linux et Windows. Seules
les commandes shell diffèrent. **Nécessite Python 3.9+** (depuis [python.org](https://www.python.org/downloads/);
sous Windows, cochez « Add Python to PATH » lors de l'installation).

### macOS / Linux

```bash
git clone https://github.com/616fun/retirement-planning-toolkit-canada.git
cd retirement-planning-toolkit-canada

python3 -m venv .venv && source .venv/bin/activate   # optional but recommended

python3 setup.py            # checks, asks before installing, smoke-tests
#   --yes / --check / --core-only as needed

python3 engine/build_model.py
python3 engine/quarterly_update.py
python3 engine/company_health.py
open dashboard/dashboard.html
```

### Windows (PowerShell)

```powershell
git clone https://github.com/616fun/retirement-planning-toolkit-canada.git
cd retirement-planning-toolkit-canada

py -3 -m venv .venv ; .\.venv\Scripts\Activate.ps1     # optional but recommended

py setup.py                 # same flags: --yes / --check / --core-only

py engine\build_model.py
py engine\quarterly_update.py
py engine\company_health.py
start dashboard\dashboard.html
```

> Utilisez `py` (le lanceur Python de Windows) ou `python` — selon ce que votre installation
> fournit. Si PowerShell bloque le script d'activation du venv, exécutez
> `Set-ExecutionPolicy -Scope Process RemoteSigned` une fois dans cette fenêtre.

### Personnalisez-le (les deux plateformes)

```
# copy the example to config/config.json (git-ignored), then edit it:
#   macOS/Linux:  cp config/config.example.json config/config.json
#   Windows:      copy config\config.example.json config\config.json
```

Une fois que `config/config.json` existe, chaque script **le détecte automatiquement** — aucune
variable d'environnement requise. Réexécutez simplement les commandes ci-dessus et elles utiliseront vos
données au lieu de la démo. (Pour pointer vers un autre fichier, définissez `RPT_CONFIG` à son
chemin.) Un `requirements.txt` est aussi fourni si vous préférez
`pip install -r requirements.txt`.

Définissez votre **province** dans `config.json` (`household.province`) et remplissez les
chiffres provinciaux dans `assumptions` — la trousse est indépendante de la province et est livrée
avec l'Ontario comme démo. Voir [`docs/CANADA_RULES.md`](docs/CANADA_RULES.md) pour les
chiffres actuels par province et fédéraux.

---

## Ce qui est installé

| Groupe | Paquets | Nécessaire pour |
|---|---|---|
| core | `openpyxl`, `numpy` | le modèle de chiffrier + Monte-Carlo (requis) |
| company-health | `yfinance`, `edgartools` | prix, analystes et signaux de dépôts SEC (É.-U.) en direct de l'action de l'employeur (optionnel) |

**Aucune clé API n'est requise.** Toutes les données proviennent de sources publiques gratuites (Yahoo
Finance, SEC EDGAR). Pour les employeurs canadiens à double cote, utilisez le **symbole NYSE**
(p. ex. `RY`, `TD`, `ENB`, `SHOP`) pour la meilleure couverture par Yahoo Finance. Le signal
d'initiés EDGAR est propre aux États-Unis et revient vide pour les émetteurs domiciliés au Canada —
les données de prix/analystes fonctionnent toujours. EDGAR n'a besoin que d'une chaîne d'identité de contact que vous définissez
dans votre configuration (`employer_stock.sec_identity`, p. ex. `"Your Name you@example.com"`).

## Dépannage

Exécutez d'abord `python3 setup.py --check` — il diagnostique la plupart des problèmes sans rien
changer. Accrocs courants et solutions :

| Symptôme | Cause | Solution |
|---|---|---|
| `Python 3.x found; 3.9+ required` | Python trop ancien | Installez Python 3.9+ (python.org ou votre gestionnaire de paquets). macOS/Linux : utilisez `python3`. Windows : utilisez `py` ou `python`. |
| `python3` / `py` non reconnu (Windows) | Python pas dans le PATH | Réinstallez Python avec « Add Python to PATH » coché, ou utilisez le lanceur `py`. |
| PowerShell refuse d'exécuter le script d'activation du venv | Politique d'exécution | Exécutez `Set-ExecutionPolicy -Scope Process RemoteSigned` dans cette fenêtre, puis activez de nouveau. |
| `error: externally-managed-environment` durant l'installation | PEP 668 (Python Homebrew/Debian) | `setup.py` réessaie automatiquement avec `--break-system-packages`. Plus propre : utilisez un venv (`python3 -m venv .venv && source .venv/bin/activate`) puis réexécutez. |
| `Can't find engine/ next to setup.py` | Exécuté depuis le mauvais dossier | Faites un `cd` dans le dépôt cloné (le dossier contenant ce fichier), puis réexécutez. `setup.py` lui-même est indépendant du chemin. |
| `company_health.py` affiche « EDGAR unavailable » | `edgartools` non installé, ou aucune identité SEC | `python3 setup.py --yes`, et définissez `employer_stock.sec_identity` dans votre configuration. (Des données d'initiés vides pour un émetteur canadien sont normales — ce n'est pas une erreur.) |
| Les champs prix/analystes affichent `n/a` | Pas d'Internet, Yahoo limité, ou mauvais symbole | Vérifiez votre connexion; utilisez la cote NYSE pour les titres canadiens à double cote. Le reste de la trousse fonctionne toujours hors ligne. |
| L'installation de `edgartools` est lente | Elle tire plusieurs bibliothèques de données | Normal à la première installation. Utilisez `--core-only` pour la sauter si vous n'avez pas besoin de données d'entreprise en direct. |
| Le fichier Excel « en cours d'utilisation » / refuse de se reconstruire | Le classeur est ouvert dans Excel | Fermez-le, puis réexécutez. |

Si quelque chose échoue encore, la sortie de `python3 setup.py --check` est l'élément le plus utile
à partager lorsque vous demandez de l'aide.

## Rappel de confidentialité

Vos vrais chiffres ne vivent que dans `config/config.json` et les fichiers générés — tous
ignorés par git. Avant de committer quoi que ce soit, exécutez `git status` et confirmez qu'aucun de
ceux-ci n'est mis en index (staged). Ne committez jamais de relevés, de feuillets fiscaux (T4/T4A/T5/reçus REER), ni de
justificatifs (credentials).
