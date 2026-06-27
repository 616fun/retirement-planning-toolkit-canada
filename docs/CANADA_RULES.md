# Canadian Retirement & Tax Parameters — Reference

**Purpose:** Authoritative, dated parameter reference for a Canadian retirement-planning toolkit.
**Compiled:** June 2026.
**Convention:** Every figure is tagged with the year it applies to. Federal indexation for 2025 = 2.3%; for 2026 = 2.7% (CRA). Ontario is the default demonstration province.

> **Sourcing note:** Several primary canada.ca pages block automated fetching. Where a figure could not be read directly off canada.ca, it is corroborated from TaxTips.ca (a long-standing professional tax reference that mirrors CRA/ESDC values) and the originating canada.ca URL is still cited for traceability. Items that could not be fully confirmed are explicitly flagged **⚠ VERIFY**.

---

## 1. Old Age Security (OAS)

| Item | Value | Applies to | Source |
|---|---|---|---|
| Max monthly, age 65–74 | **$727.67/mo** | 2025 (Q1–Q4 base) | canada.ca OAS payments |
| Max monthly, age 75+ | **$800.44/mo** (~10% higher) | 2025 | canada.ca OAS payments |
| Max monthly, age 65–74 | **$742.31/mo** | 2026 | canada.ca OAS payments |
| Max monthly, age 75+ | **$816.54/mo** | 2026 | canada.ca OAS payments |
| Recovery-tax (clawback) threshold | **$93,454** net income | 2025 income year (affects OAS Jul 2026–Jun 2027) | canada.ca recovery-tax |
| Recovery rate | **15%** of net income above the threshold | ongoing | canada.ca recovery-tax |
| Full clawback ceiling, 65–74 | **≈ $151,668** net income | 2025 income year | TaxTips / canada.ca |
| Full clawback ceiling, 75+ | **≈ $157,490** net income | 2025 income year | TaxTips / canada.ca |
| Deferral increase | **+0.6%/month** past 65, up to **+36%** at age 70 | ongoing | canada.ca |

**Notes & flags:**
- OAS amounts are reset **quarterly** (Jan / Apr / Jul / Oct) for CPI; figures above are base/representative for the year. Treat as approximate within a year.
- The 75+ amount reflects the permanent 10% increase for seniors 75 and older (effective July 2022).
- ⚠ **VERIFY full-clawback ceilings:** sources diverge slightly. TaxTips/canada.ca-aligned figures give **$151,668 (65–74)** / **$157,490 (75+)** for the **2025 income year**. Some secondary calculators cite **$152,062 / $157,923** — these appear to be a different/later indexation cycle. The ceiling is mechanically: `threshold + (annual OAS / 0.15)`, so it moves with both the threshold and the current OAS amount. Compute dynamically in the toolkit rather than hardcoding.
- The clawback is assessed on **individual** net income (line 23400), not household.

---

## 2. Canada Pension Plan (CPP)

| Item | Value | Applies to | Source |
|---|---|---|---|
| Max monthly retirement pension @ 65 | **$1,433.00/mo** | 2025 | canada.ca CPP amounts |
| Max monthly retirement pension @ 65 | **$1,507.65/mo** | 2026 | canada.ca CPP amounts |
| Average monthly for new beneficiaries @ 65 | **≈ $900/mo (2025) / $925.35 (recent 2025–26 data)** | 2025–2026 | canada.ca CPP statistics |
| Early-claim reduction | **−0.6%/month** before 65 → up to **−36%** at age 60 | ongoing | canada.ca |
| Delayed-claim increase | **+0.7%/month** after 65 → up to **+42%** at age 70 | ongoing | canada.ca |

**Notes:**
- Maximum is rarely received; most retirees get well below it (hence the average ~$900). Toolkit should let users input an estimate, defaulting to the average rather than the max.
- CPP is taxable individual income. It does **not** count toward the OAS clawback test as a separate carve-out — it is ordinary net income.

### QPP (Quebec Pension Plan) — equivalents
- Quebec residents are covered by **QPP instead of CPP**. **Maximum and average benefit amounts are essentially identical to CPP** for 2025–2026.
- Deferral increase 65→70 is the **same +0.7%/month (+42%)**.
- **Difference:** QPP can be deferred to **age 72** (vs CPP's 70), adding a further +0.7%/mo (≈ +16.8%), for up to **+58.8%** vs the age-65 amount. CPP caps at age 70.

---

## 3. Guaranteed Income Supplement (GIS)

**Who qualifies:** A low-income senior who (a) is **65+**, (b) receives **OAS**, (c) is a **Canadian resident**, and (d) has annual income below the program threshold for their marital status. Non-taxable benefit; must generally be reapplied for via the annual tax return.

| Situation | Max monthly (2025) | Income cutoff (approx.) |
|---|---|---|
| Single / widowed / divorced | **≈ $1,086.88–$1,109.85/mo** | income below **≈ $22,056–$22,440** |
| Spouse receives full OAS | **≈ $654.23–$668.08/mo each** | combined income below **≈ $29,136–$29,712** |
| Spouse does NOT receive OAS/Allowance | **≈ $1,086.88/mo** | combined income below **≈ $52,848–$53,904** |
| Spouse receives the Allowance | **≈ $654.23/mo** | combined income below **≈ $40,800–$41,616** |

**Source:** canada.ca GIS benefit-amount / eligibility pages (figures reset quarterly).
- ⚠ **VERIFY exact quarter:** GIS rates change every quarter and income cutoffs index annually; ranges above span 2025 quarters. Pull the live quarterly figure for production use.
- OAS income (the OAS pension itself) is **excluded** from the GIS income test; most other income counts.

---

## 4. Federal Income Tax (CRA)

### 4a. Federal brackets — 2025

| Rate | Taxable income range |
|---|---|
| **14.5%** | First **$57,375** |
| 20.5% | $57,375 – $114,750 |
| 26.0% | $114,750 – $177,882 |
| 29.31% | $177,882 – $253,414 |
| 33.0% | Over $253,414 |

> The lowest rate was cut from 15% to 14% **effective July 1, 2025**, producing a **blended 14.5%** full-year rate for 2025.

### 4b. Federal brackets — 2026

| Rate | Taxable income range |
|---|---|
| **14.0%** | First **$58,523** |
| 20.5% | $58,523 – $117,045 |
| 26.0% | $117,045 – $181,440 |
| 29.29% | $181,440 – $258,482 |
| 33.0% | Over $258,482 |

**Source:** canada.ca tax rates / TaxTips.ca.

### 4c. Basic Personal Amount (BPA) — with high-income phase-down

The federal BPA is an **enhanced** amount that phases down for high earners. The enhancement reduces linearly across the top tax bracket; the base amount always remains.

| Year | Max BPA (income ≤ low threshold) | Min BPA (income ≥ high threshold) | Phase-down income range |
|---|---|---|---|
| **2025** | **$16,129** | **$14,538** | net income **$177,882 → $253,414** |
| **2026** | **$16,452** | **$14,829** | net income **$181,440 → $258,482** |

- Full BPA applies if net income ≤ the lower threshold; minimum BPA applies if ≥ the upper threshold; interpolate linearly in between.
- The phase-down range = the **4th federal bracket** boundaries.

---

## 5. Provincial Tax

### 5a. Combined top marginal rates by province/territory (2025)

Combined federal + provincial, top bracket, ordinary income.

| Province / Territory | Combined top marginal rate (2025) |
|---|---|
| Newfoundland & Labrador | ~54.80% |
| Nova Scotia | ~54.00% |
| Prince Edward Island | ~51.75% |
| New Brunswick | ~52.50% |
| **Quebec** | **~53.31%** |
| **Ontario** | **~53.53%** |
| Manitoba | ~50.40% |
| Saskatchewan | ~47.50% |
| **Alberta** | **~48.00%** |
| **British Columbia** | **~53.50%** |
| Yukon | ~48.00% |
| Northwest Territories | ~47.05% |
| Nunavut | ~44.50% |

**Source:** TaxTips.ca / PwC Tax Summaries (2025).

> ✅ **All 13 jurisdictions (10 provinces + 3 territories) are encoded** in
> `engine/tax_ca.py` with verified 2025 brackets, BPA, age/pension credits, surtax
> (Ontario only — PEI's was eliminated in 2024), and, for Quebec, the 16.5%
> abatement + HSF. A test asserts each one's top combined marginal rate. An
> unrecognized province code falls back to Ontario with a warning.

⚠ **VERIFY before display:** these top-rate figures shift by ~0.1–0.5 pp with annual indexation and any rate changes; ON/BC/QC cluster tightly near 53.5%. Treat as indicative; recompute from bracket schedules for precision.

### 5b. Ontario — full provincial schedule (2025, default demo province)

**Brackets:**

| Rate | Taxable income range |
|---|---|
| 5.05% | First $52,886 |
| 9.15% | $52,886 – $105,775 |
| 11.16% | $105,775 – $150,000 |
| 12.16% | $150,000 – $220,000 |
| 13.16% | Over $220,000 |

**Ontario surtax** (applied to *Ontario tax payable*, not income):
- **20%** on Ontario tax exceeding **$5,710**
- **plus an additional 36%** (i.e., 56% total) on Ontario tax exceeding **$7,307**
- Net effect: top *effective* provincial rate rises from 13.16% to **~20.53%**, lifting Ontario's combined top rate to **~53.53%**.

> ⚠ Surtax thresholds are quoted slightly differently across sources ($5,710/$7,307 vs $6,104/$7,812 vs $7,446) because they index annually and some sources express them as the equivalent taxable-income trigger rather than the tax-payable trigger. **For 2025, the CRA/TaxTips tax-payable triggers are $5,710 (20%) and $7,307 (36%).** Verify against the current ON428 form for production.

**Ontario Basic Personal Amount (2025):** **$12,747** (credited at 5.05%).

Ontario also levies a **Health Premium** (up to $900/yr, income-tested) — note for completeness; encode if modeling Ontario take-home precisely.

### 5c. Quebec — full provincial schedule (2025) + the federal abatement

Quebec administers its own income tax and Quebec residents file a **separate
provincial return** (TP-1) on top of the federal return. The toolkit's tax engine
(`engine/tax_ca.py`) encodes Quebec fully.

**Quebec brackets (2025):**

| Rate | Taxable income range |
|---|---|
| 14.00% | First $53,255 |
| 19.00% | $53,255 – $106,495 |
| 24.00% | $106,495 – $129,590 |
| 25.75% | Over $129,590 |

(2026, indexed 2.85%: 14% to $54,345; 19% to $108,680; 24% to $132,245; 25.75% above.)

**Quebec Basic Personal Amount (2025):** **$18,571** (credited at 14%; no
high-income phase-out, unlike the federal BPA).

**No provincial surtax** (unlike Ontario).

**The Quebec abatement — 16.5%.** This is the piece that makes Quebec's combined
rate work out. A Quebec resident's **basic federal tax is reduced by 16.5%**
(historical opt-out: Ottawa vacates 16.5 points of federal personal tax in Quebec —
13.5 for the Alternative Payments for Standing Programs + 3.0 for the discontinued
Youth Allowances — and Quebec funds those services via its own higher provincial
tax). The engine applies this in `income_tax()` so combined Quebec rates come out
right: e.g. the **top combined marginal rate is 53.31%** = federal 33% × (1 − 0.165)
+ Quebec 25.75%. Without the abatement, Quebec rates would read ~9 pp too high.

**QPP instead of CPP.** Quebec is covered by the **Quebec Pension Plan**. Max and
average amounts are **essentially identical to CPP** (2025 max $1,433/mo at 65), so
enter QPP in the `cpp_monthly` fields. Key differences: QPP can be **deferred to age
72** (vs CPP's 70) for up to **+58.8%** vs the age-65 amount, and the early-claim
reduction is graduated **0.5–0.6%/mo** (use 0.6%/mo for a max-pension claimant).

**Quebec wrinkles the engine NOW models** (added so the tool doesn't mislead Quebec
retirees): the **individual Health Services Fund (HSF) contribution** — 1% on
pension / RRIF / investment income (OAS and employment **excluded**), with a $18,130
exemption and a $1,000/yr cap (so a Quebec retiree melting an RRSP pays it, up to the
cap) — and Quebec's bundled **age + retirement-income credit** (14% of age $3,906 +
retirement $3,470, reduced by 18.75% of net family income over $42,090). The age and
pension credits are modelled **symmetrically** federally and in Ontario too, so the
ON-vs-QC comparison stays fair. See `engine/tax_ca.py`.

**Still NOT modelled** (genuinely second-order here): Quebec's "amount for a person
living alone," RRSP/RRIF **withholding** differences (a prepayment, not final tax, so
it doesn't change the lifetime-tax answer), and any non-registered capital-gains tax.
The old per-adult **Quebec health contribution was abolished in 2017** — not modelled.

⚠ **VERIFY** (Retraite Québec / Revenu Québec pages blocked automated fetch): the
2025 QPP *average* benefit, the exact HSF intermediate band breakpoints ($33,130 /
$63,060 / $148,600 — the exemption, 1% rate, and $1,000 cap are firm), and the exact
Quebec pension-splitting age wording. Confirm before relying on those specifics.

**Source:** Revenu Québec; canada.ca (Quebec Abatement, Line 44000); TaxTips.ca;
Retraite Québec; RCGT 2025 QPP/CPP tables.

---

## 6. RRSP (Registered Retirement Savings Plan)

| Item | Value | Year |
|---|---|---|
| Annual contribution limit | **lesser of 18% of prior-year earned income OR $32,490** | 2025 |
| Annual contribution limit | **lesser of 18% of prior-year earned income OR $33,810** | 2026 |
| Mandatory conversion | Must convert RRSP → **RRIF (or annuity) by Dec 31 of the year you turn 71** | ongoing |

- Unused RRSP room **carries forward** indefinitely.
- Can still contribute up to Dec 31 of the year you turn 71 (to your own RRSP), then it must be wound up.

### RRSP lump-sum withdrawal withholding (residents outside Quebec)

| Withdrawal amount | Federal withholding |
|---|---|
| Up to $5,000 | **10%** |
| $5,001 – $15,000 | **20%** |
| Over $15,000 | **30%** |

- **Quebec residents:** 5% / 10% / 15% federal **plus** 14% Quebec withholding.
- **Non-residents:** flat **25%** (may be treaty-reduced).
- Withholding is a **prepayment**, not a final tax — reconciled on the return. **RRIF *minimum* withdrawals are NOT subject to withholding** (see §7).

### Spousal RRSP basics
- The **higher-income spouse contributes** (and gets the deduction) to a plan **owned by the lower-income spouse**, who is taxed on eventual withdrawals — an income-splitting tool for retirement.
- **3-year attribution rule:** if the annuitant spouse withdraws within the calendar year of a contribution or the **2 following years**, the withdrawal is taxed back to the **contributor** to the extent of recent contributions.

---

## 7. RRIF (Registered Retirement Income Fund)

**Prescribed minimum withdrawal factors** (post-2015 rules), applied to the **Jan 1 account balance**:

| Age | Factor | Age | Factor |
|---|---|---|---|
| 71 | 5.28% | 84 | 8.08% |
| 72 | 5.40% | 85 | 8.51% |
| 73 | 5.53% | 86 | 8.99% |
| 74 | 5.67% | 87 | 9.55% |
| 75 | 5.82% | 88 | 10.21% |
| 76 | 5.98% | 89 | 10.99% |
| 77 | 6.17% | 90 | 11.92% |
| 78 | 6.36% | 91 | 13.06% |
| 79 | 6.58% | 92 | 14.49% |
| 80 | 6.82% | 93 | 16.34% |
| 81 | 7.08% | 94 | 18.79% |
| 82 | 7.38% | 95+ | 20.00% |
| 83 | 7.71% | | |

**Source:** canada.ca "Chart – Prescribed factors."

- **Minimums are NOT subject to withholding tax.** Amounts withdrawn **above** the minimum are subject to the same 10/20/30% withholding tiers as RRSP withdrawals (§6).
- For **ages below 71** (e.g., an early RRIF conversion), the factor is `1 / (90 − age)`.
- Optional: you may base minimums on a **younger spouse's age** (must elect at RRIF setup) to reduce mandatory drawdowns.

---

## 8. TFSA (Tax-Free Savings Account)

| Item | Value |
|---|---|
| Annual limit, **2025** | **$7,000** |
| Annual limit, **2026** | **$7,000** (3rd year at this level) |
| **Cumulative room since 2009** (eligible whole time, never contributed) | **$102,000 (as of 2025)** → **$109,000 (as of 2026)** |

- Eligibility to accrue room starts the year you turn **18** and are a Canadian resident.
- **Withdrawals restore room** — but **only in the *following* calendar year**, not the same year. Re-contributing a withdrawn amount in the same year can cause an over-contribution penalty (1%/month on the excess).
- Growth and withdrawals are **fully tax-free** and do **not** count as income (so no impact on OAS clawback or GIS) — a key planning lever.

**Annual limit history (for cumulative math):** 2009–2012 $5,000; 2013–2014 $5,500; 2015 $10,000; 2016–2018 $5,500; 2019–2022 $6,000; 2023 $6,500; 2024–2026 $7,000.

---

## 9. RESP (Registered Education Savings Plan)

| Item | Value |
|---|---|
| **CESG** (Canada Education Savings Grant) match | **20%** of annual contributions |
| CESG max per beneficiary per year | **$500** (on first $2,500 contributed; up to $1,000/yr if catching up one prior year) |
| CESG **lifetime** max per beneficiary | **$7,200** |
| RESP **lifetime contribution** limit per beneficiary | **$50,000** (no annual cap; over-contribution penalized 1%/mo) |
| CESG availability | until end of year beneficiary turns **17** |

**Additional CESG (A-CESG):** lower/middle-income families get an extra **10–20%** on the first $500 contributed annually.

**Canada Learning Bond (CLB):** for children from **low-income** families born **2004 or later**. **No contribution required.** **$500** first year + **$100/year** thereafter to a **$2,000** lifetime max (eligibility to age 15; can be claimed up to age 20 by the beneficiary).

**Source:** canada.ca RESP / CESG / CLB pages.

---

## 10. FHSA (First Home Savings Account)

| Item | Value |
|---|---|
| Annual contribution limit | **$8,000** |
| Lifetime contribution limit | **$40,000** |
| Carry-forward | Up to **$8,000** of unused room carries to the next year (so max **$16,000** in one year); excess unused room beyond $8,000/yr is **lost** |
| Account lifespan | Must close by end of year of **15th anniversary** or the year you turn **71**, whichever is first |

**Mechanics:** Contributions are **tax-deductible** (like an RRSP) **and** qualified withdrawals for a first-home purchase are **tax-free** (like a TFSA) — the only account combining both. Room begins accumulating **only after the account is opened** (unlike TFSA/RRSP). Can be combined with the RRSP **Home Buyers' Plan**.

**Source:** canada.ca FHSA pages.

---

## 11. LIRA / LIF (Locked-In Accounts)

- **LIRA (Locked-In Retirement Account):** holds funds **transferred out of an employer registered pension plan** when you leave the employer. Like an RRSP but **locked** — generally **no withdrawals before age 55**, and it cannot simply be cashed out.
- **Conversion:** A LIRA must be converted to a **LIF** (Life Income Fund), a locked-in RRIF variant (LRIF/RLIF depending on jurisdiction), or a **life annuity** by **Dec 31 of the year you turn 71** — same deadline as RRSP→RRIF.
- **LIF withdrawals have BOTH a minimum AND a maximum:**
  - **Minimum** = same prescribed RRIF factors (§7).
  - **Maximum** = a jurisdiction-specific cap based on age and balance (designed to make the money last). This **dual min/max** is the key difference vs a regular RRIF, which has only a minimum.
- **Unlocking:** Many jurisdictions allow a **one-time 50% unlocking** to an RRSP/RRIF at age 55 (rules vary federally vs by province), plus small-balance and financial-hardship unlocking provisions.

⚠ **Jurisdiction matters:** Locked-in account rules are set by the **pension's governing jurisdiction** (federal/OSFI or a specific province). Max-withdrawal formulas and unlocking rights differ. Encode by jurisdiction; do not assume one national rule.

---

## 12. Capital Gains & Dividends

### Capital gains inclusion rate — CURRENT STATUS

- **Inclusion rate is 50%.** ✅
- The proposed increase to **66.67%** on gains above **$250,000/yr** (individuals) — announced in Budget 2024, effective date June 25, 2024 — was **deferred** (Jan 31, 2025) and then **officially CANCELLED** (announced **March 21, 2025**). **It never became law.**
- So for **2025 and 2026**, all capital gains are included at **50%**, with no $250k tier.
- **One change that DID pass:** the **Lifetime Capital Gains Exemption** (qualified small-business shares / qualified farm & fishing property) rose to **$1.25 million** (retroactive to June 25, 2024).

**Source:** canada.ca Dept. of Finance (Jan 31, 2025 deferral; Mar 21, 2025 cancellation).

### Eligible dividend tax credit (gross-up + credit) — conceptual, 2025

| | Gross-up | Federal dividend tax credit |
|---|---|---|
| **Eligible** dividends (large-corp income) | **+38%** | **15.0198%** of the grossed-up (taxable) amount |
| **Non-eligible** dividends (CCPC small-biz income) | **+15%** | **9.0301%** of the grossed-up amount |

**Concept:** The dividend is "grossed up" to approximate pre-tax corporate income, tax is computed on the grossed-up amount, then the **dividend tax credit** offsets the corporate tax already paid (integration). Provinces add their **own** dividend tax credits on top. Net effect: eligible dividends are taxed at favourable rates — in lower brackets the combined effective rate can even be **negative**.

---

## 13. Pension Income Splitting

- **Up to 50%** of **eligible pension income** may be allocated to a spouse/common-law partner via a **joint election (Form T1032)** filed with both returns. No money actually moves — it's a tax-reporting reallocation.
- **$2,000 Pension Income Amount** — a federal non-refundable credit on up to $2,000 of eligible pension income; splitting can let the **receiving** spouse also claim their own $2,000 credit.
- **Age rules for what counts as "eligible pension income":**
  - **Under 65:** mainly **registered pension plan (RPP) lifetime annuity** payments. **RRIF/RRSP-annuity income does NOT yet qualify** for splitting.
  - **Age 65+:** the list **broadens** to include **RRIF withdrawals, RRSP annuity payments, and LIF payments** — so **RRIF income becomes splittable at 65**.
- Both spouses must be **residents of Canada on Dec 31** of the tax year.

**Source:** canada.ca pension-income-splitting.

---

## 14. Key Conceptual Differences vs. the US System (encode these)

1. **Individual, not joint, filing.** Canada has **no married-filing-jointly**. Each spouse files separately. This is *why* spousal RRSPs, pension income splitting, and spousal-credit transfers exist — they're the workarounds for the lack of joint filing. The planner must model **two separate tax returns** and optimize income *placement* between spouses.

2. **No IRMAA equivalent — except the OAS clawback.** There is no Medicare-premium surcharge ladder. The functional analog is the **OAS Recovery Tax** (§1): once individual net income exceeds **$93,454 (2025)**, OAS is clawed back at **15%**. This is the single most important "income-threshold cliff" to manage in Canadian retirement income sequencing — the direct counterpart to US IRMAA tier management.

3. **RRSP-meltdown ≈ Roth-conversion ladder.** Canada has **no Roth account** and **no Roth conversion**. The analogous strategy is the **"RRSP meltdown"**: deliberately drawing down RRSP/RRIF balances in **low-income years** (typically the gap between retirement and age 71/CPP/OAS commencement) to (a) smooth the tax rate, (b) avoid being forced into large **mandatory RRIF minimums** later, and (c) keep future income **under the OAS clawback threshold**. Same spirit as a Roth ladder — fill up low brackets early — but it's *withdrawal-and-taxation*, not *conversion into a tax-free account*. The **TFSA** is the destination for melted-down funds you don't need to spend (tax-free, no clawback impact).

4. **No HSA equivalent.** Canada has **public healthcare**; there is **no Health Savings Account** and no need to model HSA contributions/withdrawals or a Medicare-premium line. (Note: private/employer health-spending accounts exist but are not a retirement-savings vehicle.) Retirement healthcare modeling focuses instead on supplemental insurance, dental/vision, and prescription gaps — not a tax-advantaged medical savings account.

**Additional structural notes for the model:**
- **Age 71** is the universal "wind-up" age: RRSP→RRIF, LIRA→LIF, FHSA close — all by Dec 31 of that year.
- **OAS/GIS/CPP** are indexed and reset on **quarterly** (OAS/GIS) or **annual** (CPP) cycles — build refresh hooks rather than hardcoding.
- All registered-account growth is **tax-deferred (RRSP/RRIF/LIRA/LIF/RESP)** or **tax-free (TFSA/FHSA)** inside the account; tax events occur on **withdrawal** (deferred accounts) only.

---

## Source URLs (primary references)

- OAS amounts: https://www.canada.ca/en/services/benefits/publicpensions/old-age-security/payments.html
- OAS recovery tax: https://www.canada.ca/en/services/benefits/publicpensions/old-age-security/recovery-tax.html
- CPP amounts: https://www.canada.ca/en/services/benefits/publicpensions/cpp/payment-amounts.html
- CPP/OAS quarterly figures: https://www.canada.ca/en/employment-social-development/programs/pensions/pension/statistics/2026-quarterly-january-march.html
- GIS benefit amount: https://www.canada.ca/en/services/benefits/publicpensions/old-age-security/guaranteed-income-supplement/benefit-amount.html
- Federal tax rates: https://www.canada.ca/en/revenue-agency/services/tax/individuals/frequently-asked-questions-individuals/canadian-income-tax-rates-individuals-current-previous-years.html
- TaxTips federal: https://www.taxtips.ca/taxrates/canada.htm
- TaxTips Ontario: https://www.taxtips.ca/taxrates/on.htm
- RRSP withholding: https://www.canada.ca/en/revenue-agency/services/tax/individuals/topics/rrsps-related-plans/making-withdrawals/tax-rates-on-withdrawals.html
- RRIF prescribed factors: https://www.canada.ca/en/revenue-agency/services/tax/businesses/topics/completing-slips-summaries/t4rsp-t4rif-information-returns/payments/chart-prescribed-factors.html
- RESP / CESG: https://www.canada.ca/en/revenue-agency/services/tax/individuals/topics/registered-education-savings-plans-resps/canada-education-savings-programs-cesp/canada-education-savings-grant-cesg.html
- Canada Learning Bond: https://www.canada.ca/en/revenue-agency/services/tax/individuals/topics/registered-education-savings-plans-resps/canada-education-savings-programs-cesp/canada-learning-bond.html
- FHSA: https://www.canada.ca/en/revenue-agency/services/tax/individuals/topics/first-home-savings-account/contributing-your-fhsa.html
- Capital gains deferral/cancellation: https://www.canada.ca/en/department-finance/news/2025/01/government-of-canada-announces-deferral-in-implementation-of-change-to-capital-gains-inclusion-rate.html
- Federal dividend tax credit: https://www.canada.ca/en/revenue-agency/services/tax/individuals/topics/about-your-tax-return/tax-return/completing-a-tax-return/deductions-credits-expenses/line-40425-federal-dividend-tax-credit.html
- Pension income splitting: https://www.canada.ca/en/revenue-agency/services/tax/individuals/topics/pension-income-splitting.html
