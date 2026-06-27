#!/usr/bin/env python3
"""
company_health.py -- Employer / single-stock health monitor for RSU &
concentration decisions.
============================================================================

WHY THIS EXISTS
---------------
If a big slice of your net worth is tied to one employer -- salary, bonus,
401(k) match in company stock, vesting RSUs, a pension -- then that company's
health is a retirement-planning input, not just a stock-watching hobby. This
module pulls public data on the ticker in your config and turns it into a few
concrete, decision-oriented signals:

  1. VALUATION & MOMENTUM   price, YTD / 1yr return, forward P/E, dividend yield,
                            analyst consensus target and implied upside.
  2. INSIDER SENTIMENT      SEC Form 4 open-market buys/sells by executives
                            (the people who know the most).
  3. EVENT RISK             recent 8-K material events and Form 144 planned-sale
                            filings (potential overhang).
  4. CONCENTRATION          your employer-stock exposure as a % of investable
                            assets, vs. your watch / trim thresholds -> a direct
                            "hold or sell the vesting RSUs?" prompt.

It is a MONITORING AID, not advice. See DISCLAIMER.md.

DATA SOURCES (all free, no API keys)
  - Yahoo Finance via yfinance        market data + analyst targets
  - SEC EDGAR via edgartools          Form 4 / 8-K / 144 filings

USAGE
  python3 engine/company_health.py                 # uses config ticker
  python3 engine/company_health.py --ticker MSFT   # override
  python3 engine/company_health.py --days 30 --json out.json

  from engine.company_health import run_company_health
  report = run_company_health(days=14)             # returns a dict
"""

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config_loader import (  # noqa: E402
    load_config, employer_stock_total, investable_total, employer_concentration_pct,
)

# ---------------------------------------------------------------------------
# Optional dependencies -- degrade gracefully so the module never hard-crashes.
# ---------------------------------------------------------------------------
try:
    import yfinance as yf
except ImportError:
    yf = None

try:
    from edgar import Company, set_identity
except ImportError:
    Company = None
    set_identity = None

# Transaction codes per SEC Form 4 taxonomy.
OPEN_MARKET_CODES = {"P", "S"}          # P = open-market buy, S = open-market sale
ROUTINE_CODES = {"A", "F", "M", "G"}    # award, tax-withhold, option-exercise, gift
CSUITE_KEYWORDS = [
    "chief executive", "ceo", "president", "chief financial", "cfo",
    "chief operating", "coo", "chief scientific", "chief medical",
    "executive vice president", "evp", "senior vice president", "svp",
]


# ===========================================================================
# 1. Market data
# ===========================================================================
def fetch_market(ticker):
    """Price, returns, valuation, analyst consensus. Returns a dict (keys may be None)."""
    out = {
        "ticker": ticker, "price": None, "forward_pe": None, "dividend_yield_pct": None,
        "ytd_return_pct": None, "one_yr_return_pct": None,
        "target_mean": None, "upside_pct": None,
        "analyst_buy": None, "analyst_hold": None, "analyst_sell": None,
        "source": "unavailable",
    }
    if yf is None:
        return out
    try:
        tk = yf.Ticker(ticker)
        info = tk.info or {}
        price = info.get("currentPrice") or info.get("regularMarketPrice")
        out["price"] = price
        out["forward_pe"] = info.get("forwardPE")
        dy = info.get("dividendYield")
        # yfinance returns dividendYield as a fraction in most versions
        if dy is not None:
            out["dividend_yield_pct"] = round(dy * 100, 2) if dy < 1 else round(dy, 2)
        out["target_mean"] = info.get("targetMeanPrice")
        if price and out["target_mean"]:
            out["upside_pct"] = round(100.0 * (out["target_mean"] - price) / price, 2)
        out["analyst_buy"] = info.get("recommendationKey")

        # Returns from price history
        hist = tk.history(period="1y", auto_adjust=True)
        if not hist.empty:
            last = float(hist["Close"].iloc[-1])
            first = float(hist["Close"].iloc[0])
            out["one_yr_return_pct"] = round(100.0 * (last - first) / first, 2)
            jan = hist[hist.index >= f"{dt.date.today().year}-01-01"]
            if not jan.empty:
                yb = float(jan["Close"].iloc[0])
                out["ytd_return_pct"] = round(100.0 * (last - yb) / yb, 2)
            if out["price"] is None:
                out["price"] = round(last, 2)
        out["source"] = "yfinance"
    except Exception as exc:  # noqa: BLE001
        out["source"] = f"error: {exc.__class__.__name__}"
    return out


# ===========================================================================
# 2 & 3. EDGAR filings: insider sentiment + event risk
# ===========================================================================
def _classify(position, name, major_holder_flag_name):
    pos = (position or "").lower()
    if major_holder_flag_name and major_holder_flag_name.upper() in (name or "").upper():
        return "major_holder"
    if any(k in pos for k in CSUITE_KEYWORDS):
        return "csuite"
    if "director" in pos:
        return "director"
    return "other"


def fetch_edgar(ticker, identity, days, major_holder_flag_name=None):
    """Form 4 (insider), 8-K (events), Form 144 (planned sales) over lookback window."""
    out = {
        "available": False, "lookback_days": days,
        "insider_sentiment": "unknown", "insider_summary": "EDGAR unavailable",
        "open_market_buys": 0, "open_market_sells": 0, "csuite_sells": 0,
        "form8k_count": 0, "form144_count": 0, "notes": [],
    }
    if Company is None or set_identity is None:
        out["notes"].append("edgartools not installed -- pip install edgartools")
        return out
    if not identity or "@" not in identity:
        out["notes"].append("Set a valid SEC identity ('Name email@example.com') in config.")
        return out

    end = dt.date.today()
    start = end - dt.timedelta(days=days)
    rng = f"{start:%Y-%m-%d}:{end:%Y-%m-%d}"
    try:
        set_identity(identity)
        company = Company(ticker)
        out["available"] = True

        # ---- Form 4: insider open-market activity ----
        buys = sells = csuite_sells = 0
        try:
            f4 = company.get_filings(form="4", date=rng)
            for i in range(len(f4)):
                try:
                    df = f4[i].obj().to_dataframe()
                    if df is None or df.empty:
                        continue
                    name = str(df["Insider"].iloc[0]) if "Insider" in df.columns else ""
                    pos = str(df["Position"].iloc[0]) if "Position" in df.columns else ""
                    klass = _classify(pos, name, major_holder_flag_name)
                    if klass == "major_holder":
                        continue  # charitable / passive holder, not a sentiment signal
                    codes = df["Code"].astype(str).tolist() if "Code" in df.columns else []
                    if "P" in codes:
                        buys += 1
                    if "S" in codes:
                        sells += 1
                        if klass == "csuite":
                            csuite_sells += 1
                except Exception:
                    continue
        except Exception:
            out["notes"].append("Form 4 fetch failed.")

        out["open_market_buys"] = buys
        out["open_market_sells"] = sells
        out["csuite_sells"] = csuite_sells

        if buys > 0:
            out["insider_sentiment"] = "bullish"
            out["insider_summary"] = f"{buys} open-market insider buy filing(s) -- rare and bullish."
        elif csuite_sells > 0:
            out["insider_sentiment"] = "watch"
            out["insider_summary"] = f"{csuite_sells} C-suite open-market sale(s) -- watch for clustering."
        elif sells > 0:
            out["insider_sentiment"] = "neutral"
            out["insider_summary"] = f"{sells} minor insider sale(s); no executive selling."
        else:
            out["insider_sentiment"] = "neutral"
            out["insider_summary"] = "No open-market insider trades in window."

        # ---- 8-K: material events ----
        try:
            f8 = company.get_filings(form="8-K", date=rng)
            out["form8k_count"] = len(f8)
        except Exception:
            pass

        # ---- Form 144: planned sales (potential overhang) ----
        try:
            f144 = company.get_filings(form="144", date=rng)
            out["form144_count"] = len(f144)
            if len(f144) > 0:
                out["notes"].append(
                    f"{len(f144)} planned-sale (Form 144) filing(s) -- potential overhang.")
        except Exception:
            pass

    except Exception as exc:  # noqa: BLE001
        out["notes"].append(f"EDGAR error: {exc.__class__.__name__}")
    return out


# ===========================================================================
# 4. Concentration / RSU decision logic
# ===========================================================================
def assess_concentration(cfg):
    es = cfg["employer_stock"]
    exposure = employer_stock_total(cfg)
    inv = investable_total(cfg)
    pct = employer_concentration_pct(cfg)
    watch = es.get("watch_threshold_pct", 5.0)
    trim = es.get("trim_threshold_pct", 7.0)

    if pct >= trim:
        target_dollars = inv * (trim / 100.0)
        trim_amount = round(exposure - target_dollars)
        verdict = "TRIM"
        action = (f"Exposure {pct}% exceeds your {trim}% trim threshold. Consider selling "
                  f"~${trim_amount:,} of employer stock (vesting RSUs first -- they have the "
                  f"highest cost basis and least tax friction) to get back to target.")
    elif pct >= watch:
        verdict = "WATCH"
        action = (f"Exposure {pct}% is above your {watch}% watch line but below the {trim}% trim "
                  f"line. Direct future RSU vests to diversified funds rather than holding.")
    else:
        verdict = "OK"
        action = (f"Exposure {pct}% is below your {watch}% watch line. No concentration action "
                  f"needed; holding vesting RSUs is within tolerance.")

    return {
        "employer_name": es.get("employer_name"), "ticker": es.get("ticker"),
        "exposure_dollars": exposure, "investable_total": inv,
        "concentration_pct": pct, "watch_threshold_pct": watch,
        "trim_threshold_pct": trim, "verdict": verdict, "action": action,
    }


# ===========================================================================
# Orchestration + reporting
# ===========================================================================
def run_company_health(ticker=None, days=14, cfg=None, verbose=True):
    if cfg is None:
        cfg, _ = load_config()
    es = cfg["employer_stock"]
    ticker = ticker or es["ticker"]
    identity = es.get("sec_identity") or cfg.get("sec_identity") or "Example User user@example.com"

    market = fetch_market(ticker)
    edgar = fetch_edgar(ticker, identity, days, es.get("major_holder_flag_name"))
    conc = assess_concentration(cfg)

    report = {
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "ticker": ticker, "employer_name": es.get("employer_name"),
        "lookback_days": days, "market": market, "edgar": edgar,
        "concentration": conc,
    }

    if verbose:
        _print_report(report)
    return report


def _pct(v):
    return "n/a" if v is None else f"{v:+.2f}%"


def _usd(v):
    return "n/a" if v is None else f"${v:,.2f}"


def _print_report(r):
    m, e, c = r["market"], r["edgar"], r["concentration"]
    bar = "=" * 74
    print(f"\n{bar}")
    print(f"  EMPLOYER HEALTH MONITOR  |  {r['employer_name']} ({r['ticker']})")
    print(f"  Generated {r['generated_at']}   |   EDGAR lookback {r['lookback_days']}d")
    print(bar)

    print("\n  1. VALUATION & MOMENTUM")
    print(f"     Price ............. {_usd(m['price'])}    (source: {m['source']})")
    print(f"     YTD return ........ {_pct(m['ytd_return_pct'])}")
    print(f"     1-year return ..... {_pct(m['one_yr_return_pct'])}")
    print(f"     Forward P/E ....... {m['forward_pe'] if m['forward_pe'] else 'n/a'}")
    print(f"     Dividend yield .... {('%.2f%%' % m['dividend_yield_pct']) if m['dividend_yield_pct'] else 'n/a'}")
    print(f"     Analyst target .... {_usd(m['target_mean'])}   implied upside {_pct(m['upside_pct'])}")
    print(f"     Consensus ......... {m['analyst_buy'] or 'n/a'}")

    print("\n  2. INSIDER SENTIMENT  (SEC Form 4, open-market)")
    print(f"     Sentiment ......... {e['insider_sentiment'].upper()}")
    print(f"     {e['insider_summary']}")
    print(f"     Buys: {e['open_market_buys']}   Sells: {e['open_market_sells']}   "
          f"C-suite sells: {e['csuite_sells']}")

    print("\n  3. EVENT RISK")
    print(f"     8-K material events (window): {e['form8k_count']}")
    print(f"     Form 144 planned sales:       {e['form144_count']}")
    for n in e["notes"]:
        print(f"     - {n}")

    print("\n  4. CONCENTRATION & RSU DECISION")
    print(f"     Employer exposure ... {_usd(c['exposure_dollars'])} of {_usd(c['investable_total'])} "
          f"investable")
    print(f"     Concentration ....... {c['concentration_pct']}%  "
          f"(watch {c['watch_threshold_pct']}% / trim {c['trim_threshold_pct']}%)")
    print(f"     VERDICT ............. {c['verdict']}")
    print(f"     {c['action']}")
    print(f"\n{bar}\n")


def main():
    ap = argparse.ArgumentParser(description="Employer / single-stock health monitor")
    ap.add_argument("--ticker", help="Override the config ticker")
    ap.add_argument("--days", type=int, default=14, help="EDGAR lookback window (default 14)")
    ap.add_argument("--json", help="Also write the report dict to this JSON path")
    args = ap.parse_args()

    report = run_company_health(ticker=args.ticker, days=args.days)
    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(report, fh, indent=2)
        print(f"  Wrote {args.json}")


if __name__ == "__main__":
    main()
