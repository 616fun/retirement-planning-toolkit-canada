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


class ConfigError(ValueError):
    """Raised when a config is structurally invalid (clear, user-facing message)."""


def load_config(path=None, validate=True):
    """Return (config_dict, resolved_path). Raises if nothing is found.

    When validate is True (default) the loaded config is checked against the
    expected shape and a ConfigError with a readable summary is raised on any
    problem -- far friendlier than a deep KeyError at build time.
    """
    for candidate in _candidate_paths(path):
        if candidate and candidate.exists():
            with open(candidate, "r", encoding="utf-8") as fh:
                cfg = json.load(fh)
            cfg["_resolved_path"] = str(candidate)
            cfg["_is_demo"] = "examples" in str(candidate)
            if validate:
                validate_config(cfg)
            return cfg, candidate
    raise FileNotFoundError(
        "No config found. Copy config/config.example.json to config/config.json "
        "and fill in your numbers, or run against the demo with "
        "RPT_CONFIG=config/examples/tremblay_config.json."
    )


# Keys the engine dereferences directly (no .get default), grouped by section.
_REQUIRED = {
    "household": ["name", "members", "province"],
    "employer_stock": ["employer_name", "ticker", "watch_threshold_pct",
                       "trim_threshold_pct", "holdings"],
    "accounts": [],
    "real_estate": [],
    "income": ["spouse_a_salary", "spouse_a_bonus_pct", "spouse_a_rsu_annual",
               "spouse_b_annual", "pension_monthly_at_retirement", "pension_cola",
               "passive_income_annual"],
    "government_benefits": ["spouse_a_cpp_monthly", "spouse_a_oas_monthly",
                            "spouse_b_cpp_monthly", "spouse_b_oas_monthly"],
    "assumptions": ["portfolio_return_base", "portfolio_return_conservative",
                    "portfolio_return_optimistic", "inflation_rate",
                    "retirement_spend_annual", "target_equity_pct", "target_bond_pct",
                    "bridge_target", "oas_clawback_threshold",
                    "basic_personal_amount_federal"],
    "paths": ["model_xlsx", "dashboard_html"],
}
_MEMBER_KEYS = ["id", "display_name", "birth_year", "retirement_age",
                "cpp_claim_age", "oas_claim_age"]


def validate_config(cfg):
    """Validate config shape; raise ConfigError listing every problem at once."""
    errors = []
    for section, keys in _REQUIRED.items():
        sec = cfg.get(section)
        if not isinstance(sec, dict):
            errors.append(f"missing or invalid section '{section}' (must be an object)")
            continue
        for k in keys:
            if k not in sec:
                errors.append(f"{section}.{k} is required")

    # The toolkit models a two-spouse household; enforce it clearly.
    members = cfg.get("household", {}).get("members")
    if not isinstance(members, list) or len(members) != 2:
        n = len(members) if isinstance(members, list) else "none"
        errors.append(
            f"household.members must be a list of exactly 2 members -- this toolkit "
            f"models a two-spouse household (got {n}). A single-person variant is on "
            f"the roadmap; for now duplicate the member or set the second spouse's "
            f"incomes/benefits to 0.")
    elif not errors:  # only dig into members if the section structure is sound
        for i, m in enumerate(members):
            if not isinstance(m, dict):
                errors.append(f"household.members[{i}] must be an object")
                continue
            for k in _MEMBER_KEYS:
                if k not in m:
                    errors.append(f"household.members[{i}].{k} is required")
                elif k != "id" and k != "display_name" and not _is_number(m[k]):
                    errors.append(f"household.members[{i}].{k} must be a number")

    # Numeric sanity on the money/rate fields the math depends on.
    for section in ("accounts", "real_estate"):
        for k, v in (cfg.get(section) or {}).items():
            if not _is_number(v):
                errors.append(f"{section}.{k} must be a number (got {v!r})")
    for k, v in (cfg.get("employer_stock", {}).get("holdings") or {}).items():
        if not _is_number(v):
            errors.append(f"employer_stock.holdings.{k} must be a number (got {v!r})")
    for k in ("spouse_a_cpp_monthly", "spouse_a_oas_monthly",
              "spouse_b_cpp_monthly", "spouse_b_oas_monthly"):
        v = cfg.get("government_benefits", {}).get(k)
        if v is not None and not _is_number(v):
            errors.append(f"government_benefits.{k} must be a number (got {v!r})")

    if errors:
        raise ConfigError(
            "Config validation failed (" + cfg.get("_resolved_path", "config") + "):\n  - "
            + "\n  - ".join(errors)
            + "\nSee config/config.example.json for the expected shape.")
    return cfg


def _is_number(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


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
