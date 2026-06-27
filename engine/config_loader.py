#!/usr/bin/env python3
"""
config_loader.py -- single entry point for loading household configuration.

Every script in engine/ loads its inputs through here, so there are NO
hardcoded names, balances, or tickers anywhere in the codebase. De-identifying
the toolkit is therefore structural: swap config.json and the whole system
re-points at a different household.

Resolution order:
  1. path passed explicitly to load_config()
  2. $RPT_CONFIG environment variable
  3. config/config.json   (your real, git-ignored data)
  4. config/examples/tremblay_config.json  (fictional demo fallback)
"""

import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _candidate_paths(explicit=None):
    if explicit:
        yield Path(explicit)
    env = os.environ.get("RPT_CONFIG")
    if env:
        yield Path(env)
    yield ROOT / "config" / "config.json"
    yield ROOT / "config" / "examples" / "tremblay_config.json"


def load_config(path=None):
    """Return (config_dict, resolved_path). Raises if nothing is found."""
    for candidate in _candidate_paths(path):
        if candidate and candidate.exists():
            with open(candidate, "r", encoding="utf-8") as fh:
                cfg = json.load(fh)
            cfg["_resolved_path"] = str(candidate)
            cfg["_is_demo"] = "examples" in str(candidate)
            return cfg, candidate
    raise FileNotFoundError(
        "No config found. Copy config/config.example.json to config/config.json "
        "and fill in your numbers, or run against the demo with "
        "RPT_CONFIG=config/examples/tremblay_config.json."
    )


# ---- Derived helpers (keep math in one place) -----------------------------

def investable_total(cfg):
    """Sum of all liquid/retirement accounts (excludes real estate and RESPs).

    RESPs are earmarked for a child's education, not retirement, so they are
    excluded from the investable base the same way US 529s were in the original.
    """
    acct = cfg["accounts"]
    exclude = {"resp_a", "resp_b"}
    return sum(v for k, v in acct.items() if k not in exclude and isinstance(v, (int, float)))


def employer_stock_total(cfg):
    """Total dollar exposure to the employer's stock across all sleeves."""
    h = cfg["employer_stock"]["holdings"]
    return sum(v for v in h.values() if isinstance(v, (int, float)))


def employer_concentration_pct(cfg):
    """Employer-stock exposure as a percent of investable assets."""
    inv = investable_total(cfg)
    if inv <= 0:
        return 0.0
    return round(100.0 * employer_stock_total(cfg) / inv, 2)


def current_age(cfg, member_id):
    import datetime
    for m in cfg["household"]["members"]:
        if m["id"] == member_id:
            return datetime.date.today().year - m["birth_year"]
    return None


if __name__ == "__main__":
    cfg, p = load_config()
    tag = "DEMO" if cfg.get("_is_demo") else "LIVE"
    print(f"[{tag}] Loaded config: {p}")
    print(f"  Household: {cfg['household']['name']}")
    print(f"  Investable total: ${investable_total(cfg):,.0f}")
    print(f"  Employer ({cfg['employer_stock']['ticker']}) exposure: "
          f"${employer_stock_total(cfg):,.0f} "
          f"({employer_concentration_pct(cfg)}% of investable)")
