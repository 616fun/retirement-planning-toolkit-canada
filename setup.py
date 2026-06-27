#!/usr/bin/env python3
"""
setup.py -- one-command bootstrap for the Canadian Retirement Planning Toolkit.

It checks your Python version, reports which dependencies are missing, ASKS
before installing anything, installs them, then runs a smoke test against the
fictional demo so you know everything works.

Usage:
  python3 setup.py            # interactive -- shows a plan and asks y/N
  python3 setup.py --yes      # install without prompting (for Cowork / CI)
  python3 setup.py --check    # report status only, install nothing
  python3 setup.py --core-only        # skip the company-health libs

Dependency groups
  core           openpyxl, numpy      -- model + Monte Carlo (required)
  company-health yfinance, edgartools -- live employer-stock monitor (optional)
"""

import argparse
import importlib
import os
import subprocess
import sys
from pathlib import Path

# Run from the repo root no matter where the user invokes this from, so the
# relative paths below (engine/, config/) always resolve. Removes the #1 snag.
ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)

CORE = [("openpyxl", "openpyxl>=3.1"), ("numpy", "numpy>=1.24")]
COMPANY_HEALTH = [("yfinance", "yfinance>=0.2.40"), ("edgar", "edgartools>=5.0")]

# Enable ANSI colors on Windows 10+ terminals; fall back to no color if unsupported.
if os.name == "nt":
    os.system("")  # turns on virtual-terminal escape processing in modern Windows
_COLOR = sys.stdout.isatty()
GREEN = "\033[92m" if _COLOR else ""
YELLOW = "\033[93m" if _COLOR else ""
RED = "\033[91m" if _COLOR else ""
RESET = "\033[0m" if _COLOR else ""


def _ok(msg):  print(f"  {GREEN}OK{RESET}    {msg}")
def _warn(msg): print(f"  {YELLOW}MISSING{RESET} {msg}")
def _err(msg): print(f"  {RED}FAIL{RESET}  {msg}")


def check_python():
    v = sys.version_info
    if (v.major, v.minor) < (3, 9):
        _err(f"Python {v.major}.{v.minor} found; 3.9+ required.")
        return False
    _ok(f"Python {v.major}.{v.minor}.{v.micro}")
    return True


def missing(group):
    out = []
    for import_name, pip_spec in group:
        try:
            importlib.import_module(import_name)
            _ok(f"{import_name} installed")
        except ImportError:
            _warn(f"{import_name} not installed  (will install '{pip_spec}')")
            out.append(pip_spec)
    return out


def pip_install(specs):
    """Install specs, falling back to --break-system-packages on PEP 668 setups."""
    cmd = [sys.executable, "-m", "pip", "install", "--quiet", *specs]
    print(f"\n  Running: {' '.join(cmd)}")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0 and "externally-managed-environment" in (res.stderr + res.stdout):
        print("  Externally-managed environment detected; retrying with --break-system-packages")
        print("  (Tip: a virtualenv is cleaner -- `python3 -m venv .venv && source .venv/bin/activate`)")
        res = subprocess.run(cmd + ["--break-system-packages"], capture_output=True, text=True)
    if res.returncode != 0:
        _err("pip install failed:")
        print(res.stderr[-600:])
        return False
    _ok("dependencies installed")
    return True


def smoke_test():
    print("\n  Smoke test (demo config)...")
    try:
        sys.path.insert(0, "engine")
        import config_loader  # noqa
        cfg, path = config_loader.load_config()
        inv = config_loader.investable_total(cfg)
        conc = config_loader.employer_concentration_pct(cfg)
        _ok(f"loaded {cfg['household']['name']} -- investable ${inv:,.0f}, "
            f"{cfg['employer_stock']['ticker']} concentration {conc}%")
        return True
    except Exception as exc:  # noqa: BLE001
        _err(f"smoke test failed: {exc}")
        return False


def main():
    ap = argparse.ArgumentParser(description="Bootstrap the Canadian Retirement Planning Toolkit")
    ap.add_argument("--yes", "-y", action="store_true", help="install without prompting")
    ap.add_argument("--check", action="store_true", help="report status only; install nothing")
    ap.add_argument("--core-only", action="store_true", help="skip the company-health libraries")
    args = ap.parse_args()

    print("\n" + "=" * 66)
    print("  Canadian Retirement Planning Toolkit -- setup")
    print("=" * 66 + "\n")

    if not check_python():
        sys.exit(1)

    if not (ROOT / "engine" / "config_loader.py").exists():
        _err(f"Can't find engine/ next to setup.py (looked in {ROOT}).")
        print("  Run this from inside the cloned repo folder.")
        sys.exit(1)

    print("\n  Checking dependencies:")
    needed = missing(CORE)
    if not args.core_only:
        needed += missing(COMPANY_HEALTH)
    else:
        print("  (skipping company-health libraries -- --core-only)")

    if args.check:
        print("\n  --check mode: nothing installed.")
        sys.exit(0)

    if needed:
        print(f"\n  {len(needed)} package(s) to install: {', '.join(needed)}")
        if not args.yes:
            try:
                resp = input("  Install these now? [y/N] ").strip().lower()
            except EOFError:
                resp = "n"
            if resp not in ("y", "yes"):
                print("\n  Skipped. Re-run with --yes to install, or install manually:")
                print(f"    {sys.executable} -m pip install {' '.join(needed)}")
                sys.exit(0)
        if not pip_install(needed):
            sys.exit(1)
    else:
        print("\n  All dependencies already present.")

    ok = smoke_test()
    print("\n" + "=" * 66)
    if ok:
        print("  Setup complete. Try it:")
        print("    python3 engine/build_model.py")
        print("    python3 engine/quarterly_update.py")
        print("    python3 engine/company_health.py")
        print("  Then make it yours: cp config/config.example.json config/config.json")
    else:
        print("  Setup finished with errors -- see messages above.")
    print("=" * 66 + "\n")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
