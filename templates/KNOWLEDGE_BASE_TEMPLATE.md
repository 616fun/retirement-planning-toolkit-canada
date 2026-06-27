# [Your Name] — Retirement Planning Knowledge Base 🇨🇦

> This is the heart of the toolkit. It's a structured brief you keep beside your
> numbers so an AI assistant (or future you) instantly has the full context to
> reason about your plan. Fill in the brackets, delete what doesn't apply, add
> what's missing. Keep it in sync with your config and spreadsheet.
>
> **Do not commit a filled-in copy to a public repo** — this file holds personal
> data. Keep your real version local (it's git-ignored as `CLAUDE.md` or
> `knowledge_base.md`).

**Last reviewed**: [date] | **Source of truth for figures**: `model/financial_plan.xlsx`
| **Parameter reference**: `docs/CANADA_RULES.md`

---

## 1. Identity & Household
- Names / ages / birth years: [...]
- **Province** of residence (tax jurisdiction): [e.g., Ontario — note Quebec = QPP + separate return]
- Filing: individual returns (Canada has no joint filing) — note which spouse is higher-income
- Dependents (kids with RESPs, aging parents, etc.): [...]
- Target retirement age(s) and date(s): [...]

## 2. Goals & Vision
- Target retirement spend (annual, today's dollars): [...]
- **Pre-CPP/OAS bridge** strategy if retiring before benefits start (non-registered + TFSA draw): [...]
- Education funding goals (RESP, CESG captured?): [...]
- Estate / legacy goals: [...]
- Explicit non-goals / things you will NOT do: [...]

## 3. Financial Snapshot (approximate — defer to the spreadsheet)
- Investable total and split by tax treatment:
  - **Tax-deferred** (RRSP / LIRA / RRIF): [...]
  - **Tax-free** (TFSA / FHSA): [...]
  - **Non-registered / taxable** (joint + individual): [...]
  - **Cash / GICs**: [...]
- RESP balances (earmarked for kids — excluded from investable): [...]
- Real estate (principal residence — capital-gains exempt on sale): [...]
- Income floor in retirement (DB pension, CPP, OAS, passive): [...]
- Current household income: [...]

## 4. Employer Stock & Concentration
- Employer, ticker, and why it matters (salary + RSUs + RRSP holdings + pension all tied to it?): [...]
- Current concentration % and your watch/trim thresholds: [...]
- RSU vesting schedule and your default action on vest (hold vs. diversify): [...]
- See `engine/company_health.py` — this section is what those signals inform.

## 5. Core Strategy
- Asset allocation target (e.g., 60/40 glide path): [...]
- **Account-location** strategy (what goes where for tax efficiency):
  - Foreign equity / interest-bearing → RRSP; growth → TFSA; etc.: [...]
- **RRSP-meltdown plan** and the **OAS clawback** ceiling you're managing to: [...]
- **TFSA** plan (max room every year; destination for melted-down RRSP funds): [...]
- **Withdrawal sequencing** (non-registered → RRSP/RRIF → TFSA last; manage clawback): [...]
- **RRSP → RRIF** conversion year (by Dec 31 of age 71) and **CPP/OAS claim ages**: [...]
- **Pension income splitting** plan (up to 50%; RRIF income splittable at 65): [...]

## 6. Tax Profile
- Province, marginal bracket, expected retirement bracket: [...]
- Key constraints you watch (**OAS clawback threshold**, RRSP/TFSA/FHSA room, RRIF minimums): [...]
- Capital-gains posture in non-registered accounts (50% inclusion): [...]

## 7. Estate Planning Status
- Wills / POA / personal directive (health): [done? pending?]
- **Beneficiary / successor-holder** designations:
  - TFSA **successor holder** (spouse) set? RRSP/RRIF **beneficiary**? RESP **subscriber/successor**?: [...]
- DB pension **survivor election** (joint-and-survivor %): [...]

## 8. Open Loops & Unresolved Questions
- [Decisions you keep circling back to — list them so they don't get lost.]

## 9. Communication Preferences (how you want the AI to respond)
- Tone, format (tables vs. prose), level of detail, expert persona to adopt: [...]

## 10. Maintenance Protocol
- When numbers change → update config + this file + rerun quarterly_update.py.
- Annually refresh tax/benefit figures from `docs/CANADA_RULES.md` (they index yearly/quarterly).
- Review cadence (e.g., quarterly + annual full review): [...]
