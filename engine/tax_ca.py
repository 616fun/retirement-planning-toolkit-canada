#!/usr/bin/env python3
"""
tax_ca.py -- a small Canadian personal income-tax engine.

Computes combined federal + provincial tax on an individual's taxable income,
the main retirement non-refundable credits (age amount + pension income amount),
the OAS Recovery Tax (clawback), and -- for Quebec -- the individual Health
Services Fund (HSF) contribution. Brackets, credits, and thresholds are indexed
forward from a base year by an inflation rate, so the engine works across a
multi-decade projection.

Scope / honesty:
  * Federal + ONTARIO + QUEBEC are fully encoded (sourced 2025 figures; see
    docs/CANADA_RULES.md). Other provinces fall back to Ontario with a one-time
    warning -- more per-province bracket modules are roadmapped.
  * Quebec is special: its own brackets and a higher Basic Personal Amount, NO
    provincial surtax, the 16.5% "Quebec abatement" that reduces a Quebec
    resident's FEDERAL tax, a bundled (family-income-tested) age/retirement
    credit, and the individual HSF contribution on pension/investment income.
    QPP is taxed like CPP (enter it in the cpp_monthly fields).
  * Retirement credits modelled: the age amount (65+, income-tested) and the
    pension income amount, federal + provincial. NOT modelled: every other
    non-refundable credit, the dividend tax credit, the capital-gains 50%
    inclusion, and the federal BPA high-income phase-down. Illustrative only.

This is illustrative, not tax advice. Verify against CRA / Revenu Quebec.
"""

BASE_YEAR = 2025

# (rate, upper_bound_of_bracket) ascending; last bound is None (open-ended).
FEDERAL_BRACKETS = [
    (0.145, 57375),     # 2025 blended (15% -> 14% cut mid-year)
    (0.205, 114750),
    (0.26, 177882),
    (0.2931, 253414),
    (0.33, None),
]
FEDERAL_BPA = 16129          # 2025 (phase-down ignored)

# Retirement non-refundable credits (2025). Amounts are credited at the
# jurisdiction's lowest bracket rate. Federal age amount phases out with income.
FEDERAL_AGE_AMOUNT = 9028
FEDERAL_AGE_PHASEOUT = 45522
FEDERAL_AGE_PHASEOUT_RATE = 0.15
FEDERAL_PENSION_MAX = 2000

# Quebec individual Health Services Fund contribution (Schedule F, 2025).
# Piecewise on income subject to HSF (pension/RRIF/investment; OAS + employment
# excluded). Bands index with inflation; the $1,000 cap is held flat.
QC_HSF = {"exemption": 18130, "band1_top": 33130, "band1_cap": 150.0,
          "band2_top": 63060, "band3_top": 148600, "rate": 0.01, "cap": 1000.0}

PROVINCES = {
    "ON": {
        "name": "Ontario",
        "brackets": [
            (0.0505, 52886),
            (0.0915, 105775),
            (0.1116, 150000),
            (0.1216, 220000),
            (0.1316, None),
        ],
        "bpa": 12747,
        # Ontario surtax applies to provincial tax PAYABLE (after the BPA credit).
        "surtax": [(0.20, 5710), (0.36, 7307)],  # (extra_rate, tax-payable threshold)
        "abatement": 0.0,
        "age_amount": 6223, "age_phaseout": 46330, "age_phaseout_rate": 0.15,
        "pension_max": 1762,
    },
    "QC": {
        "name": "Quebec",
        # Quebec 2025 brackets (Revenu Quebec). Quebec administers its own income
        # tax and files a separate provincial return.
        "brackets": [
            (0.14, 53255),
            (0.19, 106495),
            (0.24, 129590),
            (0.2575, None),
        ],
        "bpa": 18571,            # 2025 (Quebec's BPA is notably higher than ON's)
        "surtax": [],            # Quebec levies no provincial surtax
        # The 16.5% Quebec abatement reduces a Quebec resident's FEDERAL tax.
        "abatement": 0.165,
        # Bundled age + retirement-income amounts (Schedule B), reduced by 18.75%
        # of NET FAMILY income over the threshold, then credited at 14%.
        "qc_age_amount": 3906, "qc_retirement_amount": 3470,
        "qc_reduction_threshold": 42090, "qc_reduction_rate": 0.1875,
    },
    "BC": {
        "name": "British Columbia",
        "brackets": [
            (0.0506, 49279), (0.0770, 98560), (0.1050, 113158), (0.1229, 137407),
            (0.1470, 186306), (0.1680, 259829), (0.2050, None),
        ],
        "bpa": 12932,
        "surtax": [],
        "abatement": 0.0,
        "age_amount": 5799, "age_phaseout": 43169, "age_phaseout_rate": 0.15,
        "pension_max": 1000,
    },
    "AB": {
        "name": "Alberta",
        # 2025 added an 8% first bracket on the first $60,000.
        "brackets": [
            (0.08, 60000), (0.10, 151234), (0.12, 181481), (0.13, 241974),
            (0.14, 362961), (0.15, None),
        ],
        "bpa": 22323,            # highest provincial BPA
        "surtax": [],
        "abatement": 0.0,
        "age_amount": 6221, "age_phaseout": 46308, "age_phaseout_rate": 0.15,
        "pension_max": 1719,    # Alberta indexes this (most provinces are $1,000)
    },
    "MB": {
        "name": "Manitoba",
        # 2025 brackets/BPA frozen at 2024 levels (no indexation).
        "brackets": [(0.108, 47000), (0.1275, 100000), (0.174, None)],
        "bpa": 15780,
        "surtax": [],
        "abatement": 0.0,
        "age_amount": 3728, "age_phaseout": 27749, "age_phaseout_rate": 0.15,
        "pension_max": 1000,
    },
    "SK": {
        "name": "Saskatchewan",
        "brackets": [(0.105, 53463), (0.125, 152750), (0.145, None)],
        "bpa": 19491,
        "surtax": [],
        "abatement": 0.0,
        "age_amount": 5785, "age_phaseout": 43065, "age_phaseout_rate": 0.15,
        "pension_max": 1000,
    },
    "NS": {
        "name": "Nova Scotia",
        # 2025: Nova Scotia began indexing brackets/credits; the income-tested BPA
        # supplement was replaced by a flat $11,744 BPA.
        "brackets": [(0.0879, 30507), (0.1495, 61015), (0.1667, 95883),
                     (0.175, 154650), (0.21, None)],
        "bpa": 11744,
        "surtax": [],
        "abatement": 0.0,
        "age_amount": 5734, "age_phaseout": 30828, "age_phaseout_rate": 0.15,
        "pension_max": 1173,
    },
    "NB": {
        "name": "New Brunswick",
        "brackets": [(0.094, 51306), (0.14, 102614), (0.16, 190060), (0.195, None)],
        "bpa": 13396,
        "surtax": [],
        "abatement": 0.0,
        "age_amount": 6037, "age_phaseout": 44945, "age_phaseout_rate": 0.15,
        "pension_max": 1000,
    },
    "NL": {
        "name": "Newfoundland and Labrador",
        "brackets": [(0.087, 44192), (0.145, 88382), (0.158, 157792), (0.178, 220910),
                     (0.198, 282214), (0.208, 564429), (0.213, 1128858), (0.218, None)],
        "bpa": 11067,
        "surtax": [],
        "abatement": 0.0,
        "age_amount": 7064, "age_phaseout": 38712, "age_phaseout_rate": 0.15,
        "pension_max": 1000,
    },
    "PE": {
        "name": "Prince Edward Island",
        # PEI moved to a 5-bracket schedule and ELIMINATED its 10% surtax (2024).
        "brackets": [(0.095, 33328), (0.1347, 64656), (0.166, 105000),
                     (0.1762, 140000), (0.19, None)],
        "bpa": 14650,
        "surtax": [],
        "abatement": 0.0,
        "age_amount": 6510, "age_phaseout": 36600, "age_phaseout_rate": 0.15,
        "pension_max": 1000,
    },
}

_warned = set()


def _f(year, infl):
    """Inflation index factor from the base year."""
    return (1 + infl) ** (year - BASE_YEAR)


def _bracket_tax(income, brackets, year, infl):
    tax, lo = 0.0, 0.0
    for rate, upper in brackets:
        hi = float("inf") if upper is None else upper * _f(year, infl)
        if income > lo:
            tax += rate * (min(income, hi) - lo)
        lo = hi
        if income <= lo:
            break
    return tax


def federal_tax(income, year=BASE_YEAR, infl=0.021):
    if income <= 0:
        return 0.0
    gross = _bracket_tax(income, FEDERAL_BRACKETS, year, infl)
    bpa = FEDERAL_BPA * _f(year, infl)
    credit = FEDERAL_BRACKETS[0][0] * min(income, bpa)
    return max(0.0, gross - credit)


def provincial_tax(income, province="ON", year=BASE_YEAR, infl=0.021):
    if income <= 0:
        return 0.0
    p = PROVINCES.get(province)
    if p is None:
        if province not in _warned:
            print(f"  [tax_ca] province '{province}' not yet encoded; using Ontario "
                  f"as a stand-in. Per-province modules are roadmapped.")
            _warned.add(province)
        p = PROVINCES["ON"]
    gross = _bracket_tax(income, p["brackets"], year, infl)
    bpa = p["bpa"] * _f(year, infl)
    tax = max(0.0, gross - p["brackets"][0][0] * min(income, bpa))
    # Ontario surtax: an extra % of provincial tax PAYABLE above each threshold.
    surtax = 0.0
    for extra_rate, thr in p.get("surtax", []):
        surtax += extra_rate * max(0.0, tax - thr * _f(year, infl))
    return tax + surtax


# ---- retirement credits + Quebec HSF --------------------------------------

def _federal_retire_credit(income, year, infl, age, pension_income):
    """Federal age amount (65+, income-tested) + pension income amount, in $."""
    f = _f(year, infl)
    amount = 0.0
    if age is not None and age >= 65:
        aa = FEDERAL_AGE_AMOUNT * f
        aa -= FEDERAL_AGE_PHASEOUT_RATE * max(0.0, income - FEDERAL_AGE_PHASEOUT * f)
        amount += max(0.0, aa)
    amount += min(max(0.0, pension_income), FEDERAL_PENSION_MAX * f)
    return FEDERAL_BRACKETS[0][0] * amount


def _provincial_retire_credit(income, province, year, infl, age, pension_income, family_net_income):
    p = PROVINCES.get(province, PROVINCES["ON"])
    rate = p["brackets"][0][0]
    f = _f(year, infl)
    if province == "QC":
        # Bundled age + retirement-income amount, reduced by 18.75% of net family
        # income over the threshold (Schedule B), then credited at 14%.
        amt = 0.0
        if age is not None and age >= 65:
            amt += p["qc_age_amount"] * f
        amt += min(max(0.0, pension_income), p["qc_retirement_amount"] * f)
        amt -= p["qc_reduction_rate"] * max(0.0, family_net_income - p["qc_reduction_threshold"] * f)
        return rate * max(0.0, amt)
    amount = 0.0
    if age is not None and age >= 65 and "age_amount" in p:
        aa = p["age_amount"] * f - p["age_phaseout_rate"] * max(0.0, income - p["age_phaseout"] * f)
        amount += max(0.0, aa)
    if "pension_max" in p:
        amount += min(max(0.0, pension_income), p["pension_max"] * f)
    return rate * amount


def quebec_hsf(hsf_base, year=BASE_YEAR, infl=0.021):
    """Quebec individual Health Services Fund contribution on HSF-eligible income."""
    f = _f(year, infl)
    ex, b1, b2, b3 = (QC_HSF["exemption"] * f, QC_HSF["band1_top"] * f,
                      QC_HSF["band2_top"] * f, QC_HSF["band3_top"] * f)
    if hsf_base <= ex:
        return 0.0
    if hsf_base <= b1:
        return min(QC_HSF["band1_cap"], QC_HSF["rate"] * (hsf_base - ex))
    if hsf_base <= b2:
        return QC_HSF["band1_cap"]
    if hsf_base <= b3:
        return min(QC_HSF["cap"], QC_HSF["band1_cap"] + QC_HSF["rate"] * (hsf_base - b2))
    return QC_HSF["cap"]


def income_tax(income, province="ON", year=BASE_YEAR, infl=0.021,
               age=None, pension_income=0.0, family_net_income=None, hsf_base=None):
    """Combined federal + provincial ordinary-income tax for one individual.

    Optional retirement inputs:
      age              -- enables the age amount (65+); None = working-age.
      pension_income   -- eligible pension/RRIF income for the pension credit.
      family_net_income-- drives Quebec's family-income-tested bundled credit.
      hsf_base         -- income subject to the Quebec HSF (exclude OAS +
                          employment); defaults to `income`.
    For Quebec residents the federal portion is reduced by the 16.5% abatement.
    """
    if family_net_income is None:
        family_net_income = income
    if hsf_base is None:
        hsf_base = income
    p = PROVINCES.get(province, PROVINCES["ON"])

    fed = max(0.0, federal_tax(income, year, infl)
              - _federal_retire_credit(income, year, infl, age, pension_income))
    fed *= (1 - p.get("abatement", 0.0))

    prov = max(0.0, provincial_tax(income, province, year, infl)
               - _provincial_retire_credit(income, province, year, infl, age, pension_income, family_net_income))

    hsf = quebec_hsf(hsf_base, year, infl) if province == "QC" else 0.0
    return fed + prov + hsf


def oas_clawback(net_income, oas_received, threshold, recovery_rate=0.15):
    """OAS Recovery Tax: 15% of net income over the threshold, capped at OAS received."""
    if oas_received <= 0 or net_income <= threshold:
        return 0.0
    return min(oas_received, recovery_rate * (net_income - threshold))


def marginal_rate(income, province="ON", year=BASE_YEAR, infl=0.021, step=100.0):
    """Approximate combined marginal rate at an income level (working-age)."""
    return (income_tax(income + step, province, year, infl)
            - income_tax(income, province, year, infl)) / step


if __name__ == "__main__":
    # Working-age: monotonic, sensible marginal rates per province.
    for prov in ("ON", "QC"):
        print(f"  --- {PROVINCES[prov]['name']} ({prov}) | working-age ---")
        for inc in (20000, 50000, 90000, 150000, 250000):
            t = income_tax(inc, prov)
            print(f"  {prov} ${inc:>7,}: tax ${t:>9,.0f}  (avg {100*t/inc:4.1f}%, "
                  f"marginal {100*marginal_rate(inc,prov):4.1f}%)")
    # Age-70 retiree (all income eligible pension): shows age/pension credits + QC HSF.
    print("  --- age-70 retiree, income all eligible pension ---")
    for prov in ("ON", "QC"):
        for inc in (40000, 90000):
            t = income_tax(inc, prov, age=70, pension_income=inc, hsf_base=inc)
            tw = income_tax(inc, prov)
            print(f"  {prov} ${inc:>6,}: retiree ${t:>8,.0f}  vs working ${tw:>8,.0f}  "
                  f"(credits/HSF delta ${t-tw:+,.0f})")
