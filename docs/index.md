# Canadian Retirement Planning Toolkit 🇨🇦

A config-driven, self-managed retirement planning kit for **Canada** — a multi-tab
spreadsheet model, a Monte Carlo engine, an HTML dashboard, and an employer-stock
health monitor. It models the Canadian system end to end: **RRSP, TFSA, RRIF,
LIRA/LIF, FHSA, RESP**, **CPP + OAS**, the **OAS clawback**, the **RRSP-meltdown**
lifetime-tax optimizer, and **provincial tax for all 10 provinces + 3 territories**.

The tool is **bilingual**: set `"language": "fr"` in your config and the dashboard
and spreadsheet render in French. These docs are available in English and French —
use the language selector at the top.

!!! warning "Illustrative only"
    Not financial, tax, or investment advice. Tax/benefit figures change — verify
    against [canada.ca](https://www.canada.ca) before acting. See the disclaimer in
    the [repository](https://github.com/616fun/retirement-planning-toolkit-canada/blob/main/DISCLAIMER.md).

## Quick start

```bash
git clone https://github.com/616fun/retirement-planning-toolkit-canada.git
cd retirement-planning-toolkit-canada

python3 setup.py                       # checks Python, installs deps, smoke test
python3 engine/build_model.py          # builds the spreadsheet model
python3 engine/quarterly_update.py     # Monte Carlo + dashboard
open dashboard/dashboard.html

cp config/config.example.json config/config.json   # then enter your numbers
```

Full setup (including the Claude Cowork walkthrough) is in
[`INSTALL.md`](https://github.com/616fun/retirement-planning-toolkit-canada/blob/main/INSTALL.md).

## What's here

- **[Canada rules](CANADA_RULES.md)** — the sourced 2025 parameter reference: OAS/CPP/GIS,
  federal + provincial brackets, RRSP/RRIF/TFSA/FHSA/RESP limits, and the US→Canada map.
- **[Architecture](ARCHITECTURE.md)** — how the config-driven engine, tax module, Monte
  Carlo, dashboard, and RRSP-meltdown optimizer fit together.
- **[Company health](COMPANY_HEALTH.md)** — the employer-stock concentration monitor.
- **[Quarterly workflow](QUARTERLY_WORKFLOW.md)** — the rhythm for keeping the plan current.
- **[Testing](TESTING.md)** — the pytest suite and what it covers.

> Adapted from the US [Retirement Planning Toolkit](https://github.com/616fun/retirement-planning-toolkit);
> the engine is shared, the account/tax/benefit domain layer is rebuilt for Canada.
