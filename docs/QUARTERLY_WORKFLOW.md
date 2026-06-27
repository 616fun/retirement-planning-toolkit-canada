# Quarterly Workflow

A repeatable rhythm to keep the plan current.

## Each quarter
1. Copy `templates/quarterly_input_TEMPLATE.json` → `quarterly_input_Q#_YYYY.json`.
2. Fill in new account balances (CAD) from your statements (leave `null` to keep prior).
3. Update `employer_stock_holdings` so the concentration check stays accurate.
4. Run the pipeline:
   ```bash
   RPT_CONFIG=config/config.json \
   python3 engine/quarterly_update.py --input quarterly_input_Q3_2026.json
   ```
   This rebuilds the workbook, runs a 10,000-path Monte Carlo across three return
   scenarios, stamps the success rates into the model, and refreshes the dashboard.
5. Run the company-health check and review the RSU/concentration verdict:
   ```bash
   python3 engine/company_health.py
   ```
6. Skim the dashboard (`dashboard/dashboard.html`) and update your knowledge base
   if anything material changed.

## Annually
- Refresh **federal + provincial tax brackets**, the **Basic Personal Amount**, and
  contribution limits (**RRSP dollar limit**, **TFSA annual limit**, **FHSA**) in
  `config.json`. See [`docs/CANADA_RULES.md`](CANADA_RULES.md).
- Refresh the **OAS clawback threshold** (`assumptions.oas_clawback_threshold`) — it
  indexes each year and is the ceiling your RRSP-meltdown plan targets.
- Re-verify **CPP/OAS** benefit estimates (My Service Canada Account) and your DB
  **pension survivor election** (joint-and-survivor recommended).
- Confirm the **RRSP → RRIF conversion** runway: it must happen by **Dec 31 of the
  year the older spouse turns 71** (LIRA → LIF on the same deadline).
- Revisit **pension income splitting** (eligible at 65 for RRIF income).
- Full re-read of the knowledge base; reset its "Last reviewed" date.

## Watch the OAS clawback line
Because OAS/GIS amounts reset **quarterly** and the clawback threshold indexes
**annually**, treat those figures as living inputs. When a spouse's projected net
income approaches `oas_clawback_threshold`, that's the cue to lighten RRSP/RRIF
draws that year (or shift the order of withdrawals) — the Canadian analog of
managing US IRMAA tiers.

## Safety
- `config/config.json` and all `quarterly_input_Q*.json` files are git-ignored.
- Never commit statements or anything with real balances. The `.gitignore` is set
  up to block them, but check `git status` before every commit.
