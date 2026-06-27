"""Unit tests for config loading, derived math, and validation."""
import copy
import datetime
import json
import pathlib

import pytest
import config_loader as cl

ROOT = pathlib.Path(__file__).resolve().parent.parent
EXAMPLES = [ROOT / "config" / "config.example.json",
            ROOT / "config" / "examples" / "tremblay_config.json",
            ROOT / "config" / "examples" / "gagnon_config.json"]


def _load(p):
    cfg, _ = cl.load_config(str(p))
    return cfg


# ---- shipped configs all parse and validate ------------------------------
@pytest.mark.parametrize("path", EXAMPLES, ids=lambda p: p.name)
def test_shipped_configs_valid(path):
    cfg = _load(path)
    assert cfg["household"]["name"]
    assert cfg["household"]["province"] in ("ON", "QC", "XX") or isinstance(cfg["household"]["province"], str)


@pytest.mark.parametrize("path", EXAMPLES, ids=lambda p: p.name)
def test_configs_are_valid_json(path):
    json.loads(path.read_text())  # raises if malformed


# ---- derived math --------------------------------------------------------
def test_investable_excludes_resp():
    cfg = {"accounts": {"spouse_a_rrsp": 100, "resp_a": 50, "resp_b": 25, "cash_and_gics": 10}}
    assert cl.investable_total(cfg) == 110


def test_concentration_math():
    cfg = {"accounts": {"spouse_a_rrsp": 900}, "employer_stock": {"holdings": {"x": 100}}}
    assert cl.employer_concentration_pct(cfg) == pytest.approx(11.11, abs=0.01)


def test_concentration_zero_investable_is_safe():
    cfg = {"accounts": {}, "employer_stock": {"holdings": {"x": 100}}}
    assert cl.employer_concentration_pct(cfg) == 0.0


def test_current_age():
    cfg = {"household": {"members": [{"id": "spouse_a", "birth_year": 1975}]}}
    assert cl.current_age(cfg, "spouse_a") == datetime.date.today().year - 1975


# ---- validation ----------------------------------------------------------
def _good():
    return copy.deepcopy(_load(ROOT / "config" / "examples" / "tremblay_config.json"))


def test_validate_accepts_good_config():
    assert cl.validate_config(_good()) is not None


def test_validate_rejects_one_member():
    cfg = _good()
    cfg["household"]["members"] = cfg["household"]["members"][:1]
    with pytest.raises(cl.ConfigError) as e:
        cl.validate_config(cfg)
    assert "exactly 2 members" in str(e.value)


def test_validate_rejects_three_members():
    cfg = _good()
    cfg["household"]["members"].append(cfg["household"]["members"][0])
    with pytest.raises(cl.ConfigError):
        cl.validate_config(cfg)


def test_validate_rejects_missing_section():
    cfg = _good()
    del cfg["government_benefits"]
    with pytest.raises(cl.ConfigError) as e:
        cl.validate_config(cfg)
    assert "government_benefits" in str(e.value)


def test_validate_rejects_nonnumeric_balance():
    cfg = _good()
    cfg["accounts"]["spouse_a_rrsp"] = "lots"
    with pytest.raises(cl.ConfigError) as e:
        cl.validate_config(cfg)
    assert "must be a number" in str(e.value)


def test_validate_collects_multiple_errors():
    cfg = _good()
    del cfg["paths"]["model_xlsx"]
    cfg["accounts"]["spouse_a_tfsa"] = None
    with pytest.raises(cl.ConfigError) as e:
        cl.validate_config(cfg)
    msg = str(e.value)
    assert "paths.model_xlsx is required" in msg and "must be a number" in msg
