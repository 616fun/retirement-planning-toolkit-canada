# Company Health & RSU Decisions

When a large share of your net worth rides on one employer — paycheque, bonus,
company stock held in your RRSP, vesting RSUs, and often a DB pension — that
company's health is a **retirement-planning input**, not a side hobby. Employees of
the big Canadian banks, telcos, railways, and energy names know this exposure well.
`engine/company_health.py` turns public data on your configured ticker into a few
decision-oriented signals.

## What it pulls (free, no API keys)
| Source | What it gives you |
|---|---|
| Yahoo Finance (`yfinance`) | Price, YTD / 1-yr return, forward P/E, dividend yield, analyst consensus target + implied upside |
| SEC EDGAR (`edgartools`) | Form 4 open-market insider buys/sells (sentiment), 8-K material events, Form 144 planned sales (overhang) |
| Your config | Employer-stock exposure as a % of investable assets vs. your watch/trim thresholds |

> **Canadian note.** Use the **NYSE listing** of cross-listed names for the best
> Yahoo Finance coverage — `RY`, `TD`, `BNS`, `ENB`, `CNQ`, `SHOP`, `CNR`, etc.
> The **SEC EDGAR insider signal is US-specific**: Canadian-domiciled issuers file
> on **SEDI** (Canada's insider system), not SEC Form 4, so the insider/8-K/144
> panel comes back empty for them. The module degrades gracefully — price, returns,
> valuation, and analyst targets still work. (A `.TO` TSX ticker also works for
> price data via Yahoo; the NYSE listing usually has richer analyst fields.)

## The four signals
1. **Valuation & momentum** — is the stock cheap/expensive and trending up or down?
2. **Insider sentiment** — (US filers) executives rarely buy their own stock unless
   they're optimistic; clustered C-suite selling is worth watching.
3. **Event risk** — (US filers) recent 8-Ks and a spike in Form 144 planned sales
   can flag overhang before it shows up in the price.
4. **Concentration verdict** — `OK` / `WATCH` / `TRIM` based on your thresholds,
   with a concrete dollar figure to trim if you're over.

## How it informs RSU decisions
Each time RSUs vest you choose: hold or diversify. The monitor gives you a
repeatable basis for that call —

- **TRIM verdict** → sell vesting RSUs first (highest basis, least tax friction)
  to get exposure back under your trim threshold. (In a **non-registered** account,
  mind the 50%-inclusion capital gain on the sale.)
- **WATCH verdict** → direct new vests into diversified funds rather than holding.
- **OK verdict** → holding the vest is within tolerance.

Configure it in `config.json`:
```json
"employer_stock": {
  "employer_name": "Royal Bank of Canada",
  "ticker": "RY",
  "watch_threshold_pct": 5.0,
  "trim_threshold_pct": 7.0,
  "holdings": { "employer_stock_in_rrsp": 0, "unvested_rsu_value": 0, "vested_shares_value": 0 }
}
```

SEC EDGAR requires a contact identity string (`"Your Name you@example.com"`).
Set it as `employer_stock.sec_identity` (or `sec_identity` at the top level). It's
only used for the US insider lookup — harmless to leave at the default for a
Canadian-only issuer.

## Run it
```bash
python3 engine/company_health.py                 # uses your config ticker
python3 engine/company_health.py --ticker TD     # any public company
python3 engine/company_health.py --days 30 --json health.json
```

> Monitoring aid only — not a buy/sell recommendation. See `DISCLAIMER.md`.
