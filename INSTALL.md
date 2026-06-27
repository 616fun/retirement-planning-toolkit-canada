# Install Guide

Two ways to use this toolkit: inside **Claude Cowork** (no terminal needed) or
from a **terminal** with Python. Both use the same `setup.py` bootstrap, which
checks your Python, asks before installing anything, and runs a smoke test.

---

## Option A — Use it in Claude Cowork (recommended for non-developers)

1. **Get the files onto your computer.** Download this repo as a ZIP from GitHub
   (green **Code** button → **Download ZIP**) and unzip it, or `git clone` it.
2. **Open Claude desktop → Cowork mode** and **connect the folder** you just
   unzipped (the folder containing this `INSTALL.md`).
3. **Ask Claude to set it up.** For example:
   > "Run `python3 setup.py --yes` in this folder, then run the demo."

   Claude will ask your approval to run the command. `setup.py` checks for the
   four dependencies (`openpyxl`, `numpy`, `yfinance`, `edgartools`), installs any
   that are missing, and confirms with a smoke test. You approve the run — that's
   the install approval step. Nothing installs without your go-ahead.
4. **See it work on the demo.** Ask:
   > "Run the demo: build the model, run the quarterly update, and show me the dashboard."
5. **Make it yours.** Ask Claude to walk you through the interview:
   > "Use the retirement-interview skill to build my config and knowledge base."

   That produces your own `config/config.json` (which stays private and is never
   committed) and a personal knowledge base. From then on, just ask Claude to
   "run the quarterly update" or "check my company health" whenever you want.

> Optional: the included `skills/retirement-interview/SKILL.md` can be added as a
> Cowork skill so it's available by name. You can also just point Claude at it.

---

## Option B — Use it from a terminal

The toolkit is pure Python and runs the same on macOS, Linux, and Windows. Only
the shell commands differ. **Requires Python 3.9+** (from [python.org](https://www.python.org/downloads/);
on Windows, tick "Add Python to PATH" during install).

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

> Use `py` (the Windows Python launcher) or `python` — whichever your install
> provides. If PowerShell blocks the venv activation script, run
> `Set-ExecutionPolicy -Scope Process RemoteSigned` once in that window.

### Make it yours (both platforms)

```
# copy the example to config/config.json (git-ignored), then edit it:
#   macOS/Linux:  cp config/config.example.json config/config.json
#   Windows:      copy config\config.example.json config\config.json
```

Once `config/config.json` exists, every script **auto-detects it** — no
environment variable needed. Just re-run the commands above and they use your
data instead of the demo. (To point at a different file, set `RPT_CONFIG` to its
path.) `requirements.txt` is also provided if you prefer
`pip install -r requirements.txt`.

Set your **province** in `config.json` (`household.province`) and fill the
provincial figures in `assumptions` — the toolkit is province-agnostic and ships
with Ontario as the demo. See [`docs/CANADA_RULES.md`](docs/CANADA_RULES.md) for
current per-province and federal figures.

---

## What gets installed

| Group | Packages | Needed for |
|---|---|---|
| core | `openpyxl`, `numpy` | the spreadsheet model + Monte Carlo (required) |
| company-health | `yfinance`, `edgartools` | live employer-stock price, analyst, and (US) SEC-filing signals (optional) |

**No API keys are required.** All data comes from free public sources (Yahoo
Finance, SEC EDGAR). For Canadian cross-listed employers, use the **NYSE ticker**
(e.g. `RY`, `TD`, `ENB`, `SHOP`) for best Yahoo Finance coverage. The EDGAR
insider signal is US-specific and returns empty for Canadian-domiciled issuers —
price/analyst data still works. EDGAR only needs a contact identity string you set
in your config (`employer_stock.sec_identity`, e.g. `"Your Name you@example.com"`).

## Troubleshooting

Run `python3 setup.py --check` first — it diagnoses most issues without changing
anything. Common snags and fixes:

| Symptom | Cause | Fix |
|---|---|---|
| `Python 3.x found; 3.9+ required` | Old Python | Install Python 3.9+ (python.org or your package manager). macOS/Linux: use `python3`. Windows: use `py` or `python`. |
| `python3` / `py` not recognized (Windows) | Python not on PATH | Reinstall Python with "Add Python to PATH" ticked, or use the `py` launcher. |
| PowerShell won't run the venv activate script | Execution policy | Run `Set-ExecutionPolicy -Scope Process RemoteSigned` in that window, then activate again. |
| `error: externally-managed-environment` during install | PEP 668 (Homebrew/Debian Python) | `setup.py` auto-retries with `--break-system-packages`. Cleaner: use a venv (`python3 -m venv .venv && source .venv/bin/activate`) then re-run. |
| `Can't find engine/ next to setup.py` | Run from the wrong folder | `cd` into the cloned repo (the folder with this file), then re-run. `setup.py` itself is path-independent. |
| `company_health.py` shows "EDGAR unavailable" | `edgartools` not installed, or no SEC identity | `python3 setup.py --yes`, and set `employer_stock.sec_identity` in your config. (Empty insider data for a Canadian issuer is normal — not an error.) |
| Price/analyst fields show `n/a` | No internet, Yahoo throttled, or wrong ticker | Check your connection; use the NYSE listing for cross-listed Canadian names. The rest of the toolkit still runs offline. |
| `edgartools` install is slow | It pulls several data libraries | Normal on first install. Use `--core-only` to skip it if you don't need live company data. |
| Excel file "in use" / won't rebuild | The workbook is open in Excel | Close it, then re-run. |

If something still fails, `python3 setup.py --check` output is the most useful
thing to share when asking for help.

## Privacy reminder

Your real numbers live only in `config/config.json` and generated files — all
git-ignored. Before committing anything, run `git status` and confirm none of
those are staged. Never commit statements, tax slips (T4/T4A/T5/RRSP receipts), or
credentials.
