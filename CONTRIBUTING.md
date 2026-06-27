# Contributing

Thanks for your interest! This is a small, friendly project — a foundation people
fork and adapt to their own situation. Contributions that keep it simple,
readable, and safe are very welcome.

## Ground rules

- **Never commit personal data.** Your real numbers live in `config/config.json`
  and the generated `model/` + `dashboard/` files — all git-ignored. Before every
  commit run `git status` and confirm none of them are staged. Don't add
  statements, tax slips, or anything matching `*credentials*` / `.env`.
- **Keep it config-driven.** No names, balances, tickers, or paths hardcoded in
  `engine/`. If a value is user-specific, it belongs in `config.example.json` and
  is read through `engine/config_loader.py`.
- **Keep tax/benefit figures sourced and dated.** Canadian figures change often
  (many reset annually or quarterly). If you update a number, cite the year and
  source in [`docs/CANADA_RULES.md`](docs/CANADA_RULES.md).
- **It's educational, not advice.** Don't add anything that presents output as
  personalized financial, tax, or investment advice. See [`DISCLAIMER.md`](DISCLAIMER.md).

## Setting up

```bash
python3 setup.py            # checks Python, installs deps, runs a smoke test
python3 engine/quarterly_update.py   # runs the demo end to end
```

The fictional "Tremblay household" (`config/examples/tremblay_config.json`) is the
demo fixture — please test changes against it so the demo always runs clean.

## Making a change

1. Fork the repo and create a branch (`git checkout -b my-change`).
2. Make your change. Keep functions small and readable; match the existing style.
3. Run the demo (`python3 engine/quarterly_update.py` and
   `python3 engine/company_health.py`) and confirm nothing breaks. The CI
   workflow runs the same demo on Python 3.9–3.12.
4. Open a pull request describing what changed and why. Screenshots help for
   anything that affects the dashboard.

## Reporting issues / ideas

Open a GitHub Issue. Helpful things to include: your OS and Python version, the
command you ran, and the output of `python3 setup.py --check`. Please **redact any
real financial figures** from logs or screenshots before posting.

## Ideas that would be especially welcome

- A fuller **RRSP-meltdown / OAS-clawback optimizer** tab (year-by-year withdrawal
  plan that maximizes melt while staying under the clawback line) that stays
  config-driven.
- **Province modules** — encode each province's brackets, surtaxes, and credits so
  the tool can compute take-home precisely (Quebec/QPP especially).
- A **RRIF minimum-withdrawal** schedule tab driven by the prescribed factors in
  `docs/CANADA_RULES.md`.
- Tests around the Monte Carlo and concentration math.
- Docs and setup improvements for non-developers.
