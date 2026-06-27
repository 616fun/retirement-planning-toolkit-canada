# Architecture

The toolkit is deliberately **config-driven**: there is no personal data in any
script. Everything flows from one JSON config, so pointing the whole system at a
different household is a one-file swap.

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

This Canadian edition shares its engine, Monte Carlo, dashboard, and
company-health monitor with the US
[Retirement Planning Toolkit](https://github.com/616fun/retirement-planning-toolkit).
What changed is the **domain layer**: the account taxonomy, the government-benefit
model, the tax constraints, and the spreadsheet tabs.

## Single source of truth
`config/config.json` holds identity, accounts, employer stock, income,
**government benefits (CPP/OAS)**, and assumptions. Inside the **spreadsheet**, the
`Assumptions` tab plays the same role: every other tab links back to it with
cross-sheet formulas instead of hardcoding values. When you add a value, put it in
`Assumptions` and link to it.

## Config blocks (Canadian)
| Block | Holds |
|---|---|
| `household` | members (with `cpp_claim_age` + `oas_claim_age`), `province`, `pension_income_splitting` |
| `accounts` | RRSP, TFSA, LIRA, FHSA, non-registered, joint non-registered, cash/GICs, RESP |
| `employer_stock` | employer, ticker, sleeves, watch/trim thresholds |
| `income` | salary, bonus, RSU, spouse income, DB pension, passive |
| `government_benefits` | per-spouse CPP + OAS monthly amounts |
| `assumptions` | returns, inflation, spend, allocation, **OAS clawback threshold**, BPA, RRIF conversion age, cap-gains inclusion, RRSP/TFSA limits, provincial figures |

`investable_total` **excludes RESP** (earmarked for a child's education, like a US 529).

## Spreadsheet tabs (built by build_model.py)
| Tab | Purpose |
|---|---|
| Assumptions | Master inputs — returns, inflation, province, BPA, OAS clawback, RRIF age, CPP/OAS, ages |
| Net Worth Snapshot | All account balances + total + investable (excl. RESP + real estate) |
| Income Streams | Salary, bonus, RSU, DB pension, per-spouse CPP + OAS, passive |
| Employer Concentration | Employer-stock exposure vs. watch/trim thresholds |
| Year-by-Year Projections | Spend, pension, CPP+OAS (phased in at each spouse's claim age), portfolio draw, EOY balance |
| Monte Carlo | 3-scenario success rates (populated by quarterly_update.py) |
| RRSP Meltdown | **Lifetime-tax optimizer** — searches the withdrawal target that minimizes the present value of total tax (below) |
| Action Plan | Open items and recurring checks (TFSA max, meltdown, RRIF-by-71, pension splitting, beneficiaries) |

## Tax engine & meltdown optimizer (`engine/tax_ca.py` + the RRSP Meltdown tab)
`tax_ca.py` computes combined **federal + provincial** ordinary-income tax (with the
Basic Personal Amount and the Ontario surtax, all inflation-indexed) plus the **OAS
Recovery Tax** (clawback). The RRSP Meltdown tab uses it to grid-search the level
annual per-spouse RRSP/RRIF withdrawal that minimizes the **present value of total
lifetime tax** — both spouses' in-life income tax + OAS clawback, **plus the terminal
deemed-disposition tax** on any RRSP still standing at the horizon (the lump taxed to
a single surviving filer, which is what makes melting early pay off). It compares
three strategies (do-nothing / fill-to-clawback / optimal) and prints the winner's
year-by-year plan.

**Modelling scope (honest caveats).** Federal + **Ontario** are fully encoded;
other provinces fall back to Ontario with a warning (per-province modules, esp.
**Quebec/QPP**, are roadmapped). The optimizer assumes retirement income is
equalized between spouses at 65+ (pension splitting / spousal RRSPs), discounts tax
at the inflation rate, and treats non-registered + TFSA + cash as an after-tax
buffer. It does **not** yet model non-registered **capital-gains** tax, the
**dividend tax credit**, the federal BPA high-income phase-down, or TFSA
contribution limits. Illustrative, not advice — see `docs/CANADA_RULES.md`.

## Cell color convention
- **Green** text = cross-sheet link (`=Assumptions!C5`)
- **Black** text = intra-sheet formula
- **Blue** text = hardcoded input

## De-identification model
Because identity lives only in config and the git-ignored data files, sharing the
code is safe by construction. The `.gitignore` blocks `config/config.json`,
generated `model/` + `dashboard/` artifacts, statements, and anything matching
`*credentials*` or `.env`.
