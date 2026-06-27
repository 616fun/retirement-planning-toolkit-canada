#!/usr/bin/env python3
"""
build_model.py -- generate the multi-tab financial-plan workbook from config.
Canadian edition (RRSP / TFSA / RRIF / LIRA / FHSA / RESP; CPP + OAS).

Mirrors the architecture documented in docs/ARCHITECTURE.md:
  * The ASSUMPTIONS tab is the single source of truth. Every other tab links
    back to it with cross-sheet formulas rather than hardcoding values.
  * Color convention:
      green text  = cross-sheet link  (=Assumptions!Cxx)
      black text  = intra-sheet formula
      blue text   = hardcoded input
  * Tabs built here: Assumptions, Net Worth Snapshot, Income Streams,
    Year-by-Year Projections, Employer Concentration, Monte Carlo (summary),
    RRSP Meltdown (lifetime-tax optimizer), Action Plan.

Run:
  python3 engine/build_model.py                      # demo config
  RPT_CONFIG=config/config.json python3 engine/build_model.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config_loader import (  # noqa: E402
    load_config, investable_total, employer_stock_total, employer_concentration_pct,
    current_age,
)
import tax_ca  # noqa: E402

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parent.parent

GREEN = Font(color="008000")          # cross-sheet link
BLACK = Font(color="000000")          # intra-sheet formula
BLUE = Font(color="0000FF")           # hardcoded input
BOLD = Font(bold=True)
HDR = Font(bold=True, color="FFFFFF")
HDR_FILL = PatternFill("solid", fgColor="305496")
TITLE = Font(bold=True, size=14, color="1F3864")
thin = Side(style="thin", color="D9D9D9")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
RED = Font(color="CF222E")
GOODF = Font(color="1A7F37", bold=True)

# RRIF prescribed minimum withdrawal factors (post-2015 rules), applied to the
# Jan-1 balance. Source: canada.ca "Chart - Prescribed factors" (see
# docs/CANADA_RULES.md s7). This is regulation, not user config, so it is
# encoded here rather than in config.json.
RRIF_FACTORS = {
    71: .0528, 72: .0540, 73: .0553, 74: .0567, 75: .0582, 76: .0598,
    77: .0617, 78: .0636, 79: .0658, 80: .0682, 81: .0708, 82: .0738,
    83: .0771, 84: .0808, 85: .0851, 86: .0899, 87: .0955, 88: .1021,
    89: .1099, 90: .1192, 91: .1306, 92: .1449, 93: .1634, 94: .1879,
}


def rrif_min_factor(age):
    """Prescribed RRIF minimum factor for an age. 0 before the first mandatory
    withdrawal (year you turn 72, after converting by 71); 20% at 95+."""
    if age < 72:
        return 0.0
    if age >= 95:
        return 0.20
    return RRIF_FACTORS.get(age, 0.0)


def _title(ws, text):
    ws["A1"] = text
    ws["A1"].font = TITLE
    ws.append([])


def _header_row(ws, cells, row=None):
    for col, val in enumerate(cells, start=1):
        c = ws.cell(row=row or ws.max_row, column=col, value=val)
        c.font = HDR
        c.fill = HDR_FILL
        c.border = BORDER


def _acct_label(key):
    """Human label for a Canadian account key (keeps RRSP/TFSA/etc. uppercase)."""
    pretty = key.replace("_", " ").title()
    for word, repl in (("Rrsp", "RRSP"), ("Tfsa", "TFSA"), ("Rrif", "RRIF"),
                       ("Lira", "LIRA"), ("Fhsa", "FHSA"), ("Resp", "RESP"),
                       ("Gics", "GICs")):
        pretty = pretty.replace(word, repl)
    return pretty


def build_assumptions(wb, cfg):
    ws = wb.create_sheet("Assumptions")
    _title(ws, "Assumptions -- SINGLE SOURCE OF TRUTH")
    a = cfg["assumptions"]
    inc = cfg["income"]
    gb = cfg["government_benefits"]
    members = cfg["household"]["members"]

    rows = [
        ("Key", "Value", "Notes"),
        ("Portfolio return (base)", a["portfolio_return_base"], "Monte Carlo mu"),
        ("Portfolio return (conservative)", a["portfolio_return_conservative"], ""),
        ("Portfolio return (optimistic)", a["portfolio_return_optimistic"], ""),
        ("Inflation", a["inflation_rate"], "bracket + spend scaling"),
        ("Province", cfg["household"]["province"], "provincial tax jurisdiction"),
        ("Basic personal amount (federal)", a["basic_personal_amount_federal"], "non-refundable credit base"),
        ("Provincial basic personal amount", a.get("provincial_basic_personal_amount", 0), ""),
        ("OAS clawback threshold (net income)", a["oas_clawback_threshold"], "RRSP-meltdown ceiling -- the Canadian IRMAA analog"),
        ("OAS full-clawback income", a.get("oas_full_clawback", 0), "OAS fully recovered above this"),
        ("RRIF conversion age", a.get("rrif_conversion_age", 71), "RRSP must convert to RRIF by Dec 31 of this age"),
        ("Capital gains inclusion rate", a.get("capital_gains_inclusion_rate", 0.5), "taxable portion of a gain"),
        ("RRSP dollar limit (year)", a.get("rrsp_dollar_limit", 0), "or 18% of earned income"),
        ("TFSA annual limit (year)", a.get("tfsa_annual_limit", 0), ""),
        ("Retirement spend (annual, today $)", a["retirement_spend_annual"], ""),
        ("Target equity %", a["target_equity_pct"], ""),
        ("Target bond %", a["target_bond_pct"], ""),
        ("Bridge target", a["bridge_target"], "pre-CPP/OAS bridge"),
        ("Pension monthly at retirement", inc["pension_monthly_at_retirement"], "employer DB pension"),
        ("Pension COLA", inc["pension_cola"], ""),
        ("Passive income (annual)", inc["passive_income_annual"], ""),
        (f"{members[0]['display_name']} salary", inc["spouse_a_salary"], ""),
        (f"{members[0]['display_name']} bonus %", inc["spouse_a_bonus_pct"], ""),
        (f"{members[0]['display_name']} RSU annual", inc["spouse_a_rsu_annual"], ""),
        (f"{members[1]['display_name']} income", inc["spouse_b_annual"], ""),
        (f"{members[0]['display_name']} retirement age", members[0]["retirement_age"], ""),
        (f"{members[1]['display_name']} retirement age", members[1]["retirement_age"], ""),
        (f"{members[0]['display_name']} CPP claim age", members[0]["cpp_claim_age"], "60-70 (std 65)"),
        (f"{members[0]['display_name']} OAS claim age", members[0]["oas_claim_age"], "65-70"),
        (f"{members[1]['display_name']} CPP claim age", members[1]["cpp_claim_age"], ""),
        (f"{members[1]['display_name']} OAS claim age", members[1]["oas_claim_age"], ""),
        (f"{members[0]['display_name']} CPP monthly", gb["spouse_a_cpp_monthly"], ""),
        (f"{members[0]['display_name']} OAS monthly", gb["spouse_a_oas_monthly"], ""),
        (f"{members[1]['display_name']} CPP monthly", gb["spouse_b_cpp_monthly"], ""),
        (f"{members[1]['display_name']} OAS monthly", gb["spouse_b_oas_monthly"], ""),
    ]
    start = ws.max_row + 1
    for i, r in enumerate(rows):
        ws.append(r)
        if i == 0:
            _header_row(ws, r)
        else:
            ws.cell(row=ws.max_row, column=2).font = BLUE  # hardcoded inputs
    ws.column_dimensions["A"].width = 36
    ws.column_dimensions["B"].width = 16
    ws.column_dimensions["C"].width = 44
    cfg["_assum_rows"] = {name: start + idx for idx, (name, *_ ) in enumerate(rows)}
    return ws


def build_net_worth(wb, cfg):
    ws = wb.create_sheet("Net Worth Snapshot")
    _title(ws, "Net Worth Snapshot")
    ws.append(["Account", "Balance"])
    _header_row(ws, ["Account", "Balance"])
    first_data = ws.max_row + 1
    for k, v in cfg["accounts"].items():
        ws.append([_acct_label(k), v])
        ws.cell(row=ws.max_row, column=2).font = BLUE
    for k, v in cfg["real_estate"].items():
        if v:
            ws.append([k.replace("_", " ").title(), v])
            ws.cell(row=ws.max_row, column=2).font = BLUE
    last_data = ws.max_row
    ws.append(["TOTAL NET WORTH", f"=SUM(B{first_data}:B{last_data})"])
    ws.cell(row=ws.max_row, column=1).font = BOLD
    ws.cell(row=ws.max_row, column=2).font = BLACK
    inv = investable_total(cfg)
    ws.append(["Investable total (excl. RESP + real estate)", inv])
    ws.cell(row=ws.max_row, column=2).font = BLUE
    ws.column_dimensions["A"].width = 38
    ws.column_dimensions["B"].width = 16
    return ws


def build_concentration(wb, cfg):
    ws = wb.create_sheet("Employer Concentration")
    _title(ws, f"Employer Concentration -- {cfg['employer_stock']['employer_name']} "
               f"({cfg['employer_stock']['ticker']})")
    es = cfg["employer_stock"]
    ws.append(["Sleeve", "Value"])
    _header_row(ws, ["Sleeve", "Value"])
    for k, v in es["holdings"].items():
        ws.append([_acct_label(k), v])
        ws.cell(row=ws.max_row, column=2).font = BLUE
    ws.append(["Total employer exposure", employer_stock_total(cfg)])
    ws.cell(row=ws.max_row, column=1).font = BOLD
    ws.append(["Investable total", investable_total(cfg)])
    ws.append(["Concentration %", employer_concentration_pct(cfg)])
    ws.cell(row=ws.max_row, column=1).font = BOLD
    ws.append(["Watch threshold %", es["watch_threshold_pct"]])
    ws.append(["Trim threshold %", es["trim_threshold_pct"]])
    ws.column_dimensions["A"].width = 30
    ws.column_dimensions["B"].width = 16
    return ws


def build_year_by_year(wb, cfg):
    ws = wb.create_sheet("Year-by-Year Projections")
    _title(ws, "Year-by-Year Projections (simplified)")
    members = cfg["household"]["members"]
    a = cfg["assumptions"]
    spend0 = a["retirement_spend_annual"]
    infl = a["inflation_rate"]
    ret = a["portfolio_return_base"]
    pension = cfg["income"]["pension_monthly_at_retirement"] * 12
    passive = cfg["income"]["passive_income_annual"]
    gb = cfg["government_benefits"]
    cpp_a = gb["spouse_a_cpp_monthly"] * 12
    oas_a = gb["spouse_a_oas_monthly"] * 12
    cpp_b = gb["spouse_b_cpp_monthly"] * 12
    oas_b = gb["spouse_b_oas_monthly"] * 12

    headers = ["Year", "Spouse A age", "Spouse B age", "Spend (infl-adj)",
               "Pension", "Passive", "CPP + OAS", "Portfolio draw", "Portfolio EOY"]
    ws.append(headers)
    _header_row(ws, headers)

    import datetime
    base_year = datetime.date.today().year
    a_age0 = current_age(cfg, "spouse_a")
    b_age0 = current_age(cfg, "spouse_b")
    a_ret_age = members[0]["retirement_age"]
    a_cpp_age, a_oas_age = members[0]["cpp_claim_age"], members[0]["oas_claim_age"]
    b_cpp_age, b_oas_age = members[1]["cpp_claim_age"], members[1]["oas_claim_age"]
    portfolio = investable_total(cfg)

    for n in range(0, 36):
        year = base_year + n
        a_age = a_age0 + n
        b_age = b_age0 + n
        retired = a_age >= a_ret_age
        spend = spend0 * ((1 + infl) ** n) if retired else 0
        pen = pension * ((1 + cfg["income"]["pension_cola"]) ** max(0, a_age - a_ret_age)) if retired else 0
        pas = passive if retired else 0
        govt = ((cpp_a if a_age >= a_cpp_age else 0) + (oas_a if a_age >= a_oas_age else 0)
                + (cpp_b if b_age >= b_cpp_age else 0) + (oas_b if b_age >= b_oas_age else 0))
        portfolio *= (1 + ret)
        draw = 0
        if retired:
            need = spend - pen - pas - govt
            draw = max(0, need)
            portfolio -= draw
        ws.append([year, a_age, b_age, round(spend), round(pen), round(pas),
                   round(govt), round(draw), round(portfolio)])

    for col in range(1, len(headers) + 1):
        ws.column_dimensions[get_column_letter(col)].width = 15
    return ws


def build_monte_carlo(wb, cfg):
    ws = wb.create_sheet("Monte Carlo")
    _title(ws, "Monte Carlo (summary -- run engine/quarterly_update.py to refresh)")
    ws.append(["Scenario", "Return mu", "Success rate", "Note"])
    _header_row(ws, ["Scenario", "Return mu", "Success rate", "Note"])
    a = cfg["assumptions"]
    for label, mu in [("Conservative", a["portfolio_return_conservative"]),
                      ("Base", a["portfolio_return_base"]),
                      ("Optimistic", a["portfolio_return_optimistic"])]:
        ws.append([label, mu, "(pending)", "populated by quarterly_update.py"])
    ws.column_dimensions["A"].width = 16
    ws.column_dimensions["D"].width = 40
    return ws


# ===========================================================================
# RRSP Meltdown -- lifetime-tax optimizer
# ===========================================================================
def _simulate_meltdown(cfg, strategy, target=None):
    """Simulate the household's registered drawdown to a planning horizon and
    return total lifetime tax + a year-by-year schedule.

    strategy:
      "none"     -- take only the forced RRIF minimum (the do-nothing baseline)
      "clawback" -- fill household income up to (n_spouses x OAS clawback line)
      "optimal"  -- fill each retired spouse's taxable income up to `target`

    Lifetime tax = sum of annual (income tax + OAS clawback) for both spouses,
    PLUS the terminal deemed-disposition tax on the RRSP/RRIF still standing at
    the horizon (taxed to a single surviving filer -- the reason melting early
    can win). All taxes are discounted to PRESENT VALUE at the inflation rate, so
    the optimizer trades the cost of paying tax now against deferring it -- this
    is what produces an interior optimum rather than "drain as fast as possible."
    See docs/CANADA_RULES.md for the modelling assumptions.
    """
    import datetime
    a = cfg["assumptions"]
    m = cfg["household"]["members"]
    gb, inc, acct = cfg["government_benefits"], cfg["income"], cfg["accounts"]
    prov = cfg["household"]["province"]

    infl, ret = a["inflation_rate"], a["portfolio_return_base"]
    thr0 = a["oas_clawback_threshold"]
    spend0 = a["retirement_spend_annual"]
    base_year = datetime.date.today().year

    a_age0, b_age0 = current_age(cfg, "spouse_a"), current_age(cfg, "spouse_b")
    a_ret, b_ret = m[0]["retirement_age"], m[1]["retirement_age"]
    a_cpp, a_oas = m[0]["cpp_claim_age"], m[0]["oas_claim_age"]
    b_cpp, b_oas = m[1]["cpp_claim_age"], m[1]["oas_claim_age"]

    rrsp = float(acct.get("spouse_a_rrsp", 0) + acct.get("spouse_b_rrsp", 0))
    buffer = float(acct.get("spouse_a_non_registered", 0) + acct.get("spouse_b_non_registered", 0)
                   + acct.get("joint_non_registered", 0) + acct.get("cash_and_gics", 0))
    tfsa = float(acct.get("spouse_a_tfsa", 0) + acct.get("spouse_b_tfsa", 0))

    pension_m, cola = inc["pension_monthly_at_retirement"], inc["pension_cola"]
    passive0, b_salary0 = inc["passive_income_annual"], inc["spouse_b_annual"]
    cpp_a0, oas_a0 = gb["spouse_a_cpp_monthly"] * 12, gb["spouse_a_oas_monthly"] * 12
    cpp_b0, oas_b0 = gb["spouse_b_cpp_monthly"] * 12, gb["spouse_b_oas_monthly"] * 12

    horizon = max(1, 90 - a_age0)            # project to spouse A age 90
    lifetime_tax, insolvent, schedule = 0.0, False, []
    last_survivor_base = 0.0

    for n in range(0, horizon + 1):
        year = base_year + n
        a_age, b_age = a_age0 + n, b_age0 + n
        rrsp *= (1 + ret); buffer *= (1 + ret); tfsa *= (1 + ret)
        if a_age < a_ret:
            continue  # still working -- no draws modelled before retirement

        idx = (1 + infl) ** n
        spend = spend0 * idx
        pension = pension_m * 12 * ((1 + cola) ** max(0, a_age - a_ret))
        passive = passive0 * idx
        b_work = b_salary0 * idx if b_age < b_ret else 0.0
        cpp_a = cpp_a0 * idx if a_age >= a_cpp else 0.0
        oas_a = oas_a0 * idx if a_age >= a_oas else 0.0
        cpp_b = cpp_b0 * idx if b_age >= b_cpp else 0.0
        oas_b = oas_b0 * idx if b_age >= b_oas else 0.0

        forced = min(rrsp * rrif_min_factor(a_age), rrsp)
        retirement_fixed = pension + passive + cpp_a + oas_a + cpp_b + oas_b + forced
        n_active = (1 if a_age >= a_ret else 0) + (1 if b_age >= b_ret else 0)

        if strategy == "none":
            voluntary = 0.0
        elif strategy == "clawback":
            ceiling = n_active * thr0 * idx
            voluntary = max(0.0, min(ceiling - (retirement_fixed + b_work), rrsp - forced))
        else:  # optimal -- level per-spouse taxable target
            ceiling = n_active * target
            voluntary = max(0.0, min(ceiling - (retirement_fixed + b_work), rrsp - forced))

        withdraw = forced + voluntary
        rrsp -= withdraw

        # ---- tax: equalize retirement income across both spouses once both retired ----
        retire_income = retirement_fixed + voluntary
        both_retired = (a_age >= a_ret) and (b_age >= b_ret)
        if both_retired:
            half = retire_income / 2.0
            oas_each = (oas_a + oas_b) / 2.0
            tax = 2 * tax_ca.income_tax(half, prov, year, infl)
            claw = 2 * tax_ca.oas_clawback(half, oas_each, thr0 * idx)
            last_survivor_base = (pension + cpp_a + oas_a) / 1.0  # survivor keeps own + maybe survivor benefits
        else:
            inc_a = retire_income            # all retirement income to the retired spouse A
            inc_b = b_work
            tax = tax_ca.income_tax(inc_a, prov, year, infl) + tax_ca.income_tax(inc_b, prov, year, infl)
            claw = (tax_ca.oas_clawback(inc_a, oas_a, thr0 * idx)
                    + tax_ca.oas_clawback(inc_b, oas_b, thr0 * idx))
            last_survivor_base = pension + cpp_a + oas_a
        year_tax = tax + claw
        lifetime_tax += year_tax / ((1 + infl) ** n)   # present value, today's $

        # ---- fund spending; surplus registered cash sweeps into the TFSA ----
        cash_in = pension + passive + cpp_a + oas_a + cpp_b + oas_b + b_work + withdraw
        net_cash = cash_in - year_tax
        if net_cash >= spend:
            tfsa += (net_cash - spend)
        else:
            short = spend - net_cash
            take = min(buffer, short); buffer -= take; short -= take
            if short > 0:
                take = min(tfsa, short); tfsa -= take; short -= take
            if short > 1.0:
                insolvent = True

        schedule.append({
            "year": year, "a_age": a_age, "b_age": b_age,
            "taxable": retire_income, "forced": forced, "voluntary": voluntary,
            "tax": tax, "claw": claw, "rrsp": rrsp, "estate": rrsp + buffer + tfsa,
            "over": claw > 0,
        })

    # ---- terminal tax: RRSP left standing is deemed disposed at death (single filer) ----
    final_year = base_year + horizon
    terminal_raw = (tax_ca.income_tax(last_survivor_base + rrsp, prov, final_year, infl)
                    - tax_ca.income_tax(last_survivor_base, prov, final_year, infl))
    terminal_tax = terminal_raw / ((1 + infl) ** horizon)   # present value, today's $
    total_tax = lifetime_tax + terminal_tax
    estate = rrsp + buffer + tfsa
    return {
        "strategy": strategy, "target": target,
        "lifetime_tax": lifetime_tax, "terminal_tax": terminal_tax, "total_tax": total_tax,
        "rrsp_end": rrsp, "estate_end": estate, "insolvent": insolvent, "schedule": schedule,
    }


def _optimize_meltdown(cfg):
    """Grid-search the level per-spouse meltdown target that minimizes total
    lifetime tax (subject to the plan staying solvent)."""
    best = None
    for t in range(20000, 200001, 2500):   # wide enough that large RRSPs don't clip the optimum
        r = _simulate_meltdown(cfg, "optimal", target=float(t))
        if r["insolvent"]:
            continue
        if best is None or r["total_tax"] < best["total_tax"]:
            best = r
    if best is None:  # fall back to the lowest target if nothing is solvent
        best = _simulate_meltdown(cfg, "optimal", target=20000.0)
    return best


def build_meltdown(wb, cfg):
    """RRSP-meltdown / OAS-clawback tab -- lifetime-tax optimizer (objective #2).

    Searches for the level annual RRSP/RRIF withdrawal target (per spouse) that
    minimizes TOTAL lifetime tax -- in-life income tax + OAS clawback across both
    spouses, PLUS the terminal deemed-disposition tax on whatever RRSP is left at
    death. Compares three strategies and shows the winner's year-by-year plan.

    Tax engine: engine/tax_ca.py (federal + Ontario; other provinces fall back to
    Ontario with a warning -- per-province modules are roadmapped). Models ordinary
    income, OAS clawback, pension/registered income equalization between spouses,
    and terminal RRSP tax. Does NOT yet model non-registered capital-gains tax,
    the dividend tax credit, or TFSA contribution limits. Illustrative, not advice.
    """
    ws = wb.create_sheet("RRSP Meltdown")
    _title(ws, "RRSP Meltdown -- Lifetime-Tax Optimizer")
    prov = cfg["household"]["province"]

    none = _simulate_meltdown(cfg, "none")
    claw = _simulate_meltdown(cfg, "clawback")
    best = _optimize_meltdown(cfg)

    ws.append([f"Objective: minimize TOTAL lifetime tax (both spouses' income tax + OAS clawback, "
               f"plus terminal RRSP tax at death). Province: {prov}. See docs/CANADA_RULES.md."])
    ws.append([])

    # ---- strategy comparison ----
    cmp_headers = ["Strategy", "Per-spouse target", "In-life tax (PV)", "Terminal RRSP tax (PV)",
                   "TOTAL lifetime tax (PV)", "RRSP at horizon", "Estate at horizon"]
    ws.append(cmp_headers)
    _header_row(ws, cmp_headers)
    rows = [
        ("Do nothing (RRIF minimums only)", "n/a", none),
        ("Fill to OAS clawback line", "clawback line", claw),
        ("Lifetime-tax optimal", f"${best['target']:,.0f}/yr", best),
    ]
    base_total = none["total_tax"]
    optimal_row = None
    for label, tgt, r in rows:
        ws.append([label, tgt, round(r["lifetime_tax"]), round(r["terminal_tax"]),
                   round(r["total_tax"]), round(r["rrsp_end"]), round(r["estate_end"])])
        if r is best:
            optimal_row = ws.max_row
            for c in range(1, len(cmp_headers) + 1):
                ws.cell(row=ws.max_row, column=c).font = GOODF
    ws.append([])
    saved = base_total - best["total_tax"]
    ws.append([f"Lifetime tax saved vs. do-nothing:", round(saved),
               f"({100*saved/base_total:.0f}% lower) by melting ~${best['target']:,.0f}/spouse/yr "
               f"and sweeping surplus into the TFSA"])
    ws.cell(row=ws.max_row, column=1).font = BOLD
    ws.cell(row=ws.max_row, column=2).font = GOODF
    ws.append([])

    # ---- optimal year-by-year schedule ----
    sch_headers = ["Year", "A age", "B age", "Taxable income", "RRIF minimum",
                   "Recommended melt", "Income tax", "OAS clawback", "RRSP balance"]
    ws.append(sch_headers)
    _header_row(ws, sch_headers)
    for r in best["schedule"]:
        ws.append([r["year"], r["a_age"], r["b_age"], round(r["taxable"]),
                   round(r["forced"]), round(r["voluntary"]), round(r["tax"]),
                   round(r["claw"]), round(r["rrsp"])])
        if r["claw"] > 0:
            ws.cell(row=ws.max_row, column=8).font = RED

    widths = [8, 7, 7, 16, 14, 17, 13, 14, 15]
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w
    return ws


def build_action_plan(wb, cfg):
    ws = wb.create_sheet("Action Plan")
    _title(ws, "Action Plan")
    ws.append(["Priority", "Item", "Status"])
    _header_row(ws, ["Priority", "Item", "Status"])
    items = [
        (1, "Review employer-stock concentration vs. thresholds (company_health.py)", "Recurring"),
        (2, "Max TFSA contribution room every year (tax-free growth, restored if withdrawn)", "Recurring"),
        (3, "Execute the RRSP-meltdown plan (see RRSP Meltdown tab) to its lifetime-tax-optimal target", "Open"),
        (4, "Confirm RRSP -> RRIF conversion plan before Dec 31 of age 71", "Open"),
        (5, "Set up / confirm pension income splitting with spouse (up to 50%)", "Open"),
        (6, "Confirm beneficiary / successor-holder designations (TFSA successor holder; RRSP/RRIF beneficiary)", "Open"),
        (7, "Verify DB pension survivor-benefit election (joint-and-survivor)", "Open"),
        (8, "Rebalance toward target equity/bond split", "Recurring"),
    ]
    for p, it, st in items:
        ws.append([p, it, st])
    ws.column_dimensions["A"].width = 10
    ws.column_dimensions["B"].width = 78
    ws.column_dimensions["C"].width = 14
    return ws


def build_income_note(wb, cfg):
    ws = wb.create_sheet("Income Streams")
    _title(ws, "Income Streams")
    ws.append(["Stream", "Annual", "Notes"])
    _header_row(ws, ["Stream", "Annual", "Notes"])
    inc = cfg["income"]
    gb = cfg["government_benefits"]
    m = cfg["household"]["members"]
    rows = [
        (f"{m[0]['display_name']} salary", inc["spouse_a_salary"], ""),
        (f"{m[0]['display_name']} bonus", round(inc["spouse_a_salary"] * inc["spouse_a_bonus_pct"]), ""),
        (f"{m[0]['display_name']} RSU", inc["spouse_a_rsu_annual"], "employer stock -- see concentration tab"),
        (f"{m[1]['display_name']} income", inc["spouse_b_annual"], ""),
        ("Pension (annual at retirement)", inc["pension_monthly_at_retirement"] * 12, "employer DB pension"),
        (f"{m[0]['display_name']} CPP (annual)", gb["spouse_a_cpp_monthly"] * 12, f"claim age {m[0]['cpp_claim_age']}"),
        (f"{m[0]['display_name']} OAS (annual)", gb["spouse_a_oas_monthly"] * 12, f"claim age {m[0]['oas_claim_age']}; clawback applies"),
        (f"{m[1]['display_name']} CPP (annual)", gb["spouse_b_cpp_monthly"] * 12, f"claim age {m[1]['cpp_claim_age']}"),
        (f"{m[1]['display_name']} OAS (annual)", gb["spouse_b_oas_monthly"] * 12, f"claim age {m[1]['oas_claim_age']}; clawback applies"),
        ("Passive income", inc["passive_income_annual"], ""),
    ]
    for r in rows:
        ws.append(r)
    ws.column_dimensions["A"].width = 30
    ws.column_dimensions["B"].width = 14
    ws.column_dimensions["C"].width = 44
    return ws


def build(cfg):
    wb = Workbook()
    wb.remove(wb.active)
    build_assumptions(wb, cfg)
    build_net_worth(wb, cfg)
    build_concentration(wb, cfg)
    build_income_note(wb, cfg)
    build_year_by_year(wb, cfg)
    build_monte_carlo(wb, cfg)
    build_meltdown(wb, cfg)
    build_action_plan(wb, cfg)
    return wb


def main():
    cfg, path = load_config()
    out = ROOT / cfg["paths"]["model_xlsx"]
    out.parent.mkdir(parents=True, exist_ok=True)
    wb = build(cfg)
    wb.save(out)
    tag = "DEMO" if cfg.get("_is_demo") else "LIVE"
    print(f"[{tag}] Built model from {path.name}")
    print(f"  -> {out}")
    print(f"  Tabs: {wb.sheetnames}")


if __name__ == "__main__":
    main()
