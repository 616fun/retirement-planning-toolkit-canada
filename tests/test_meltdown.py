"""Unit tests for the RRSP-meltdown optimizer and Monte Carlo determinism."""
import pathlib

import pytest
import config_loader as cl
import build_model as bm
import quarterly_update as qu

ROOT = pathlib.Path(__file__).resolve().parent.parent


def _cfg(name):
    cfg, _ = cl.load_config(str(ROOT / "config" / "examples" / name))
    return cfg


def test_rrif_factors():
    assert bm.rrif_min_factor(60) == 0.0
    assert bm.rrif_min_factor(71) == 0.0           # first mandatory withdrawal is at 72
    assert bm.rrif_min_factor(72) == pytest.approx(0.0540)
    assert bm.rrif_min_factor(94) == pytest.approx(0.1879)
    assert bm.rrif_min_factor(95) == 0.20
    assert bm.rrif_min_factor(110) == 0.20


def test_simulation_invariants():
    r = bm._simulate_meltdown(_cfg("tremblay_config.json"), "optimal", target=90000.0)
    assert r["total_tax"] > 0
    assert all(row["rrsp"] >= -1e-6 for row in r["schedule"])     # never goes negative
    assert all(row["voluntary"] >= -1e-6 for row in r["schedule"])
    assert r["terminal_tax"] >= 0


@pytest.mark.parametrize("name", ["tremblay_config.json", "gagnon_config.json"])
def test_optimal_beats_do_nothing(name):
    cfg = _cfg(name)
    best = bm._optimize_meltdown(cfg)
    none = bm._simulate_meltdown(cfg, "none")
    assert best["total_tax"] <= none["total_tax"]
    assert best["target"] is not None


def test_optimizer_is_deterministic():
    cfg = _cfg("tremblay_config.json")
    a = bm._optimize_meltdown(cfg)
    b = bm._optimize_meltdown(cfg)
    assert a["target"] == b["target"]
    assert a["total_tax"] == pytest.approx(b["total_tax"])


def test_quebec_costs_more_than_ontario_same_household():
    # gagnon mirrors tremblay's balances but in Quebec -> strictly higher tax.
    on = bm._optimize_meltdown(_cfg("tremblay_config.json"))
    qc = bm._optimize_meltdown(_cfg("gagnon_config.json"))
    assert qc["total_tax"] > on["total_tax"]


def test_monte_carlo_deterministic_and_in_range():
    cfg = _cfg("tremblay_config.json")
    m1 = qu.monte_carlo(cfg, n_sims=500)
    m2 = qu.monte_carlo(cfg, n_sims=500)
    for k in ("conservative", "base", "optimistic"):
        assert 0.0 <= m1[k]["success_rate"] <= 100.0
        assert m1[k]["success_rate"] == m2[k]["success_rate"]   # fixed seed -> reproducible
    assert m1["conservative"]["success_rate"] <= m1["optimistic"]["success_rate"]
