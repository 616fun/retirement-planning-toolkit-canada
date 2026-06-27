# Testing

The toolkit ships a `pytest` suite under `tests/`. It runs in CI on every push
across Python 3.9–3.12, and you can run it locally in seconds.

```bash
python3 -m pip install -r requirements.txt -r requirements-dev.txt
python3 -m pytest tests/ -q
```

(`tests/conftest.py` puts `engine/` on the import path, so no install of the
package itself is needed.)

## What's covered

| File | Focus |
|---|---|
| `test_tax_ca.py` | Tax engine — federal/Ontario/Quebec brackets, the 16.5% Quebec abatement, BPA shelter, age + pension credits and their phase-outs, the Quebec HSF bands, OAS clawback, marginal-rate values, monotonicity, and the unknown-province → Ontario fallback. Expected values are anchored to the sourced figures in [`CANADA_RULES.md`](CANADA_RULES.md). |
| `test_config_loader.py` | Config loading, `investable_total` (RESP excluded), concentration math (incl. zero-investable), `current_age`, and `validate_config` — that every shipped config passes and that bad ones (1 or 3 members, missing section, non-numeric balance) raise a clear `ConfigError` listing all problems. |
| `test_meltdown.py` | RRIF prescribed factors, meltdown simulation invariants (RRSP never negative, terminal tax ≥ 0), the optimizer beating do-nothing, determinism, that Quebec costs more than Ontario for the same household, and Monte Carlo reproducibility (fixed seed) + range. |
| `test_integration.py` | Both demos build all 8 workbook tabs; the workbook round-trips through openpyxl; the dashboard renders (with and without a Monte Carlo summary); the quarterly input overlay is a no-op when given no file. |

## Conventions

- **Determinism.** The Monte Carlo uses a fixed seed, so success rates are
  reproducible and asserted exactly. Keep it that way — don't introduce
  unseeded randomness into the engine.
- **Sourced expectations.** When you change a tax figure, update both
  `engine/tax_ca.py` / config and the matching assertion, and cite the year +
  source in `CANADA_RULES.md`.
- **No network in tests.** Tests never hit Yahoo/EDGAR; the company-health
  monitor is exercised separately (and tolerated to fail) in the CI demo run.
