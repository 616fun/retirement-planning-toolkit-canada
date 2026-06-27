# Translation status

The toolkit is bilingual — **English** and **Canadian French**. Both the product
output and the documentation are kept in sync, and CI enforces it:

- **UI strings** — `engine/locales/en.json` ↔ `engine/locales/fr.json` must have
  identical key sets (`tests/test_i18n.py`). The dashboard and the spreadsheet
  render in the language set by `"language"` in `config.json`.
- **Docs** — every English doc must have a `.fr.md` counterpart that stays
  structurally parallel (`tests/test_docs_parity.py`).

The hosted bilingual site (auto language selector + browser detection):
**https://616fun.github.io/retirement-planning-toolkit-canada/**

## Documentation

| English | Français | Status |
|---|---|---|
| `README.md` | `README.fr.md` | ✅ |
| `INSTALL.md` | `INSTALL.fr.md` | ✅ |
| `DISCLAIMER.md` | `DISCLAIMER.fr.md` | ✅ |
| `CONTRIBUTING.md` | `CONTRIBUTING.fr.md` | ✅ |
| `docs/index.md` | `docs/index.fr.md` | ✅ |
| `docs/CANADA_RULES.md` | `docs/CANADA_RULES.fr.md` | ✅ |
| `docs/ARCHITECTURE.md` | `docs/ARCHITECTURE.fr.md` | ✅ |
| `docs/COMPANY_HEALTH.md` | `docs/COMPANY_HEALTH.fr.md` | ✅ |
| `docs/QUARTERLY_WORKFLOW.md` | `docs/QUARTERLY_WORKFLOW.fr.md` | ✅ |
| `docs/TESTING.md` | `docs/TESTING.fr.md` | ✅ |

## When you change an English doc or string

1. Update its French counterpart in the **same change** (or mark the row 🚧 here
   and open a follow-up).
2. Run `python3 -m pytest tests/test_i18n.py tests/test_docs_parity.py -q`.
3. For UI strings, add the key to **both** `en.json` and `fr.json`.

French = Canadian French. Term mapping: RRSP=REER, TFSA=CELI, RRIF=FERR, LIRA=CRI,
LIF=FRV, FHSA=CELIAPP, RESP=REEE, CPP=RPC, OAS=SV, GIS=SRG, QPP=RRQ; "OAS clawback"
= « récupération de la SV »; "RRSP-meltdown" = « fonte du REER ».
