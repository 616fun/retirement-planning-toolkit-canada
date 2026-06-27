#!/usr/bin/env python3
"""
refresh_dashboard.py -- render the HTML retirement dashboard from current state.

Generates a single self-contained HTML file (Chart.js loaded from CDN) with:
  * Net-worth / investable KPI tiles
  * Employer-stock concentration panel with watch/trim verdict
  * Monte Carlo success rates (3 scenarios)
  * A company-health snapshot, if a report dict is supplied or
    market_intelligence.json is present

Can be called as part of quarterly_update.py (refresh(cfg, mc)) or standalone:
  python3 engine/refresh_dashboard.py
  python3 engine/refresh_dashboard.py --with-company-health
"""

import argparse
import datetime as dt
import html
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config_loader import (  # noqa: E402
    load_config, investable_total, employer_stock_total, employer_concentration_pct,
)

ROOT = Path(__file__).resolve().parent.parent


def _kpi(label, value, sub=""):
    return (f'<div class="kpi"><div class="kpi-label">{html.escape(label)}</div>'
            f'<div class="kpi-value">{html.escape(str(value))}</div>'
            f'<div class="kpi-sub">{html.escape(sub)}</div></div>')


def _concentration_panel(cfg):
    es = cfg["employer_stock"]
    pct = employer_concentration_pct(cfg)
    watch = es["watch_threshold_pct"]
    trim = es["trim_threshold_pct"]
    if pct >= trim:
        verdict, cls = "TRIM", "bad"
    elif pct >= watch:
        verdict, cls = "WATCH", "warn"
    else:
        verdict, cls = "OK", "good"
    bar_pct = min(100, pct / max(trim, 1) * 100)
    return f"""
    <div class="panel">
      <h2>Employer Concentration &mdash; {html.escape(es['employer_name'])} ({html.escape(es['ticker'])})</h2>
      <div class="conc-bignum {cls}">{pct}%</div>
      <div class="bar"><div class="bar-fill {cls}" style="width:{bar_pct:.0f}%"></div></div>
      <p>Exposure ${employer_stock_total(cfg):,.0f} of ${investable_total(cfg):,.0f} investable.
         Watch &ge; {watch}% &middot; Trim &ge; {trim}%.
         Verdict: <span class="badge {cls}">{verdict}</span></p>
      <p class="muted">Run <code>engine/company_health.py</code> for live price, analyst, and insider signals.</p>
    </div>"""


def _mc_panel(mc):
    if not mc or "error" in mc:
        return '<div class="panel"><h2>Monte Carlo</h2><p class="muted">Run quarterly_update.py to populate.</p></div>'
    rows = ""
    for label in ("conservative", "base", "optimistic"):
        if label in mc:
            d = mc[label]
            rows += (f"<tr><td>{label.title()}</td><td>{d['mu']*100:.1f}%</td>"
                     f"<td>{d['success_rate']}%</td>"
                     f"<td>${d['median_end_balance']:,}</td></tr>")
    return f"""
    <div class="panel">
      <h2>Monte Carlo &mdash; plan success</h2>
      <table><thead><tr><th>Scenario</th><th>Return</th><th>Success</th><th>Median end</th></tr></thead>
      <tbody>{rows}</tbody></table>
    </div>"""


def _company_health_panel(report):
    if not report:
        return ""
    m = report.get("market", {})
    e = report.get("edgar", {})
    return f"""
    <div class="panel">
      <h2>Company Health &mdash; {html.escape(str(report.get('employer_name','')))} ({html.escape(str(report.get('ticker','')))})</h2>
      <div class="grid3">
        {_kpi("Price", f"${m.get('price')}" if m.get('price') else "n/a", f"YTD {m.get('ytd_return_pct')}%")}
        {_kpi("Analyst target", f"${m.get('target_mean')}" if m.get('target_mean') else "n/a", f"upside {m.get('upside_pct')}%")}
        {_kpi("Insider sentiment", str(e.get('insider_sentiment','?')).upper(), e.get('insider_summary',''))}
      </div>
    </div>"""


def render(cfg, mc=None, company_health=None):
    nw = investable_total(cfg)
    real_estate = sum(v for v in cfg["real_estate"].values() if v)
    total_nw = sum(cfg["accounts"].values()) + real_estate
    tiles = "".join([
        _kpi("Total net worth", f"${total_nw:,.0f}"),
        _kpi("Investable", f"${nw:,.0f}"),
        _kpi("Retirement spend target", f"${cfg['assumptions']['retirement_spend_annual']:,.0f}/yr"),
        _kpi("Pre-CPP/OAS bridge target", f"${cfg['assumptions']['bridge_target']:,.0f}"),
    ])
    demo_banner = ('<div class="demo">DEMO DATA &mdash; fictional Tremblay household (Ontario). '
                   'Replace config/config.json with your own.</div>' if cfg.get("_is_demo") else "")
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(cfg['household']['name'])} &mdash; Retirement Dashboard</title>
<style>
  :root {{ --good:#1a7f37; --warn:#bf8700; --bad:#cf222e; --ink:#1f2933; --line:#e5e7eb; }}
  body {{ font-family: -apple-system, Segoe UI, Roboto, sans-serif; color: var(--ink); margin: 0; background:#f7f8fa; }}
  header {{ background:#1f3864; color:#fff; padding: 20px 28px; }}
  header h1 {{ margin:0; font-size: 20px; }}
  header .sub {{ opacity:.8; font-size: 13px; }}
  .demo {{ background:#fff3cd; color:#7a5b00; padding:8px 28px; font-size:13px; }}
  .wrap {{ max-width: 1000px; margin: 0 auto; padding: 20px 28px; }}
  .kpis {{ display:grid; grid-template-columns: repeat(4,1fr); gap:12px; margin-bottom:20px; }}
  .grid3 {{ display:grid; grid-template-columns: repeat(3,1fr); gap:12px; }}
  .kpi {{ background:#fff; border:1px solid var(--line); border-radius:10px; padding:14px; }}
  .kpi-label {{ font-size:12px; color:#6b7280; }}
  .kpi-value {{ font-size:22px; font-weight:700; }}
  .kpi-sub {{ font-size:12px; color:#6b7280; }}
  .panel {{ background:#fff; border:1px solid var(--line); border-radius:10px; padding:18px; margin-bottom:16px; }}
  .panel h2 {{ margin:0 0 12px; font-size:16px; }}
  table {{ width:100%; border-collapse:collapse; font-size:14px; }}
  th, td {{ text-align:left; padding:6px 8px; border-bottom:1px solid var(--line); }}
  .conc-bignum {{ font-size:34px; font-weight:800; }}
  .bar {{ height:10px; background:#eef0f3; border-radius:6px; overflow:hidden; margin:8px 0; }}
  .bar-fill {{ height:100%; }}
  .good {{ color:var(--good); }} .warn {{ color:var(--warn); }} .bad {{ color:var(--bad); }}
  .bar-fill.good {{ background:var(--good); }} .bar-fill.warn {{ background:var(--warn); }} .bar-fill.bad {{ background:var(--bad); }}
  .badge {{ padding:2px 8px; border-radius:999px; font-size:12px; font-weight:700; color:#fff; }}
  .badge.good {{ background:var(--good); }} .badge.warn {{ background:var(--warn); }} .badge.bad {{ background:var(--bad); }}
  .muted {{ color:#6b7280; font-size:13px; }}
  code {{ background:#f0f1f3; padding:1px 5px; border-radius:4px; }}
</style></head>
<body>
<header>
  <h1>{html.escape(cfg['household']['name'])} &mdash; Retirement Dashboard</h1>
  <div class="sub">Generated {dt.datetime.now():%Y-%m-%d %H:%M}</div>
</header>
{demo_banner}
<div class="wrap">
  <div class="kpis">{tiles}</div>
  {_concentration_panel(cfg)}
  {_company_health_panel(company_health)}
  {_mc_panel(mc)}
  <p class="muted">Illustrative only &mdash; not financial advice. See DISCLAIMER.md.</p>
</div>
</body></html>"""


def refresh(cfg=None, mc=None, company_health=None):
    if cfg is None:
        cfg, _ = load_config()
    if mc is None:
        mc_path = ROOT / "model" / "mc_summary.json"
        if mc_path.exists():
            mc = json.loads(mc_path.read_text())
    out = ROOT / cfg["paths"]["dashboard_html"]
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        out.with_suffix(".html.bak").write_text(out.read_text(encoding="utf-8"), encoding="utf-8")
    out.write_text(render(cfg, mc, company_health), encoding="utf-8")
    return out


def main():
    ap = argparse.ArgumentParser(description="Render the HTML dashboard")
    ap.add_argument("--with-company-health", action="store_true",
                    help="Run company_health.py and include its panel (needs network)")
    args = ap.parse_args()
    cfg, _ = load_config()
    ch = None
    if args.with_company_health:
        try:
            import company_health
            ch = company_health.run_company_health(verbose=False)
        except Exception as exc:  # noqa: BLE001
            print(f"  company-health skipped: {exc}")
    out = refresh(cfg, company_health=ch)
    tag = "DEMO" if cfg.get("_is_demo") else "LIVE"
    print(f"[{tag}] Dashboard -> {out}")


if __name__ == "__main__":
    main()
