"""Unit tests for the Canadian tax engine. Expected values are anchored to the
sourced 2025 figures in docs/CANADA_RULES.md (verified vs CRA / Revenu Quebec)."""
import pytest
import tax_ca


def test_zero_and_negative_income():
    assert tax_ca.income_tax(0, "ON") == 0
    assert tax_ca.income_tax(-5000, "ON") == 0


@pytest.mark.parametrize("prov", ["ON", "QC"])
def test_monotonic_increasing(prov):
    prev = -1.0
    for inc in range(0, 300001, 10000):
        t = tax_ca.income_tax(inc, prov)
        assert t >= prev - 1e-6, f"{prov} not monotonic at {inc}"
        prev = t


def test_bpa_shelters_low_income():
    # Below the federal + Ontario Basic Personal Amounts, tax is ~0.
    assert tax_ca.income_tax(10000, "ON") == pytest.approx(0, abs=1)


def test_ontario_marginal_rates():
    # 50k: fed 14.5% + ON 5.05% = 19.55%; 90k: fed 20.5% + ON 9.15% = 29.65%
    assert tax_ca.marginal_rate(50000, "ON") == pytest.approx(0.1955, abs=0.01)
    assert tax_ca.marginal_rate(90000, "ON") == pytest.approx(0.2965, abs=0.01)


def test_quebec_top_marginal_includes_abatement():
    # Top: fed 33% x (1 - 0.165 abatement) + QC 25.75% = 53.305%
    assert tax_ca.marginal_rate(300000, "QC") == pytest.approx(0.533, abs=0.006)
    # ...and must be well below the un-abated 33% + 25.75% = 58.75%
    assert tax_ca.marginal_rate(300000, "QC") < 0.56


def test_oas_clawback():
    assert tax_ca.oas_clawback(50000, 8000, 93454) == 0          # below threshold
    assert tax_ca.oas_clawback(100000, 8000, 93454) == pytest.approx(981.9, abs=0.5)
    assert tax_ca.oas_clawback(1_000_000, 8000, 93454) == 8000   # capped at OAS received


def test_quebec_hsf_bands():
    f = tax_ca.quebec_hsf
    assert f(18130) == 0                                  # at exemption
    assert f(20000) == pytest.approx(18.70, abs=0.05)     # ramp 1
    assert f(33130) == pytest.approx(150, abs=0.5)        # top of ramp 1
    assert f(50000) == 150                                # flat band
    assert f(100000) == pytest.approx(519.4, abs=1)       # ramp 2
    assert f(200000) == 1000                              # cap


@pytest.mark.parametrize("prov", ["ON", "QC"])
def test_retirement_credits_reduce_tax(prov):
    working = tax_ca.income_tax(40000, prov)
    retiree = tax_ca.income_tax(40000, prov, age=70, pension_income=40000, hsf_base=40000)
    assert retiree < working   # age amount + pension credit apply at 65+


def test_age_amount_phases_out_at_high_income():
    # At $90k the federal age amount is largely phased out, so the retiree
    # discount is much smaller than at $40k.
    d_low = tax_ca.income_tax(40000, "ON") - tax_ca.income_tax(40000, "ON", age=70, pension_income=40000)
    d_high = tax_ca.income_tax(90000, "ON") - tax_ca.income_tax(90000, "ON", age=70, pension_income=90000)
    assert d_low > d_high > 0


def test_unknown_province_falls_back_to_ontario():
    assert tax_ca.income_tax(80000, "BC") == tax_ca.income_tax(80000, "ON")
