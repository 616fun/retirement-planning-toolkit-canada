#!/usr/bin/env python3
"""
tax_ca.py -- a small Canadian personal income-tax engine.

Computes combined federal + provincial tax on an individual's taxable income,
plus the OAS Recovery Tax (clawback). Brackets, the Basic Personal Amount, and
the Ontario surtax are indexed forward from a base year by an inflation rate, so
the engine works across a multi-decade projection.

Scope / honesty:
  * Federal + ONTARIO are fully encoded (sourced 2025 figures; see
    docs/CANADA_RULES.md). Other provinces fall back to Ontario with a one-time
    warning -- per-province bracket modules (esp. Quebec/QPP) are roadmapped.
  * Models ordinary income. It does NOT yet model the dividend tax credit, the
    capital-gains 50% inclusion, the federal BPA high-income phase-down, or the
    Ontario Health Premium. These are refinements, not load-bearing for the
    RRSP-meltdown question (which turns on ordinary registered-withdrawal income).

This is illustrative, not tax advice. Verify against CRA before acting.
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
    },
}

_warned = set()


def _bracket_tax(income, brackets, year, infl):
    tax, lo = 0.0, 0.0
    for rate, upper in brackets:
        hi = float("inf") if upper is None else upper * ((1 + infl) ** (year - BASE_YEAR))
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
    bpa = FEDERAL_BPA * ((1 + infl) ** (year - BASE_YEAR))
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
    bpa = p["bpa"] * ((1 + infl) ** (year - BASE_YEAR))
    tax = max(0.0, gross - p["brackets"][0][0] * min(income, bpa))
    # Ontario surtax: an extra % of provincial tax PAYABLE above each threshold.
    surtax = 0.0
    for extra_rate, thr in p.get("surtax", []):
        thr_idx = thr * ((1 + infl) ** (year - BASE_YEAR))
        surtax += extra_rate * max(0.0, tax - thr_idx)
    return tax + surtax


def income_tax(income, province="ON", year=BASE_YEAR, infl=0.021):
    """Combined federal + provincial ordinary-income tax for one individual."""
    return federal_tax(income, year, infl) + provincial_tax(income, province, year, infl)


def oas_clawback(net_income, oas_received, threshold, recovery_rate=0.15):
    """OAS Recovery Tax: 15% of net income over the threshold, capped at OAS received."""
    if oas_received <= 0 or net_income <= threshold:
        return 0.0
    return min(oas_received, recovery_rate * (net_income - threshold))


def marginal_rate(income, province="ON", year=BASE_YEAR, infl=0.021, step=100.0):
    """Approximate combined marginal rate at an income level."""
    return (income_tax(income + step, province, year, infl)
            - income_tax(income, province, year, infl)) / step


if __name__ == "__main__":
    # Sanity check: monotonic, sensible effective rates for Ontario.
    for inc in (20000, 50000, 90000, 150000, 250000):
        t = income_tax(inc, "ON")
        print(f"  ON ${inc:>7,}: tax ${t:>9,.0f}  (avg {100*t/inc:4.1f}%, "
              f"marginal {100*marginal_rate(inc,'ON'):4.1f}%)")
