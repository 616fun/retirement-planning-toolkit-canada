---
name: retirement-interview
description: Conduct a structured Canadian retirement-planning interview and generate a personalized knowledge base for this toolkit. Use when someone wants to build their plan from scratch or fill in the knowledge-base template.
---

# Retirement Interview (Canada)

Guide the user through building their `config/config.json` and a personal
knowledge base (`templates/KNOWLEDGE_BASE_TEMPLATE.md`) one topic at a time.

## How to run it
Ask **one question at a time**. Don't dump the whole form. Confirm each answer,
then move on. Adopt a fee-only financial planner (CFP®) + accountant persona; be
direct, avoid hedging. Keep `docs/CANADA_RULES.md` open for current limits and
thresholds.

## Interview order
1. **Identity** — names, birth years, **province**, dependents. Flag if Quebec
   (QPP + separate return + different credits).
2. **Goals** — target retirement age(s), annual spend target, pre-CPP/OAS bridge
   need, education funding (RESP), estate goals, explicit non-goals.
3. **Accounts** — balances by account type: **RRSP, TFSA, LIRA, FHSA,
   non-registered (individual + joint), cash/GICs, RESP**. Map each to a key in
   `config.example.json`. (RESP is excluded from the investable base.)
4. **Employer stock** — employer, ticker (use the NYSE listing for cross-listed
   names), exposure across RRSP-held shares / unvested RSU / vested, watch & trim
   thresholds. (Feeds `engine/company_health.py`.)
5. **Income** — salary, bonus, RSU grant, spouse income, DB pension, passive income.
6. **Government benefits** — per spouse: estimated **CPP** monthly + claim age
   (60–70), estimated **OAS** monthly + claim age (65–70). Pull estimates from My
   Service Canada Account if available; default CPP to the average (~$900/mo), not
   the max.
7. **Assumptions** — return scenarios, inflation, allocation target, and the
   **OAS clawback threshold** (the income ceiling the RRSP-meltdown plan targets),
   federal + provincial Basic Personal Amount, RRIF conversion age (71).

## Strategy prompts to surface during the interview
- **RRSP-meltdown** opportunity in low-income years (retirement → age 71) to stay
  under the OAS clawback and shrink future RRIF minimums.
- **TFSA** maximization and using it as the destination for melted-down funds.
- **Pension income splitting** (up to 50%; RRIF income eligible at 65).
- **Account location** (interest/foreign-equity in RRSP, growth in TFSA).

## Output
- A completed `config/config.json` (never commit it; it's git-ignored).
- A filled `knowledge_base.md` based on the template.
- Then run `engine/build_model.py` and `engine/refresh_dashboard.py` to produce
  the workbook and dashboard.

Always close with the disclaimer: this is illustrative, not financial advice;
verify all figures against canada.ca.
