#!/usr/bin/env python3
"""
i18n.py -- minimal English/French localization for the toolkit's user-facing
output: the HTML dashboard and the spreadsheet labels.

Strings live as DATA in engine/locales/<lang>.json (not in code), so they are
language-agnostic resource files: easy to scan/diff/proofread, shared by the
dashboard and the workbook, and reusable by any future (e.g. JS) frontend. This
module just loads them and resolves keys.

Driven by the optional top-level "language" key in config.json ("en" default,
"fr" for Canadian French). Anything missing in the target language falls back to
English, then to the key itself, so partial coverage never crashes.
"""

import json
from pathlib import Path

_LOCALE_DIR = Path(__file__).resolve().parent / "locales"
_CACHE = {}


def _load(lang):
    if lang not in _CACHE:
        path = _LOCALE_DIR / f"{lang}.json"
        try:
            _CACHE[lang] = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            _CACHE[lang] = {}
    return _CACHE[lang]


def lang_of(cfg):
    """Return the 2-letter language code from config ('en' default)."""
    return str((cfg or {}).get("language") or "en").lower()[:2]


def t(key, lang="en", **kw):
    """Look up a localized string by key; fall back to English, then the key."""
    s = _load(lang).get(key) or _load("en").get(key) or key
    return s.format(**kw) if kw else s


def keys(lang="en"):
    """Translatable keys for a locale (excludes _meta keys starting with '_')."""
    return {k for k in _load(lang) if not k.startswith("_")}
