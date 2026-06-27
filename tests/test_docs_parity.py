"""Drift control: every English doc must have a French counterpart that stays
structurally parallel. Combined with tests/test_i18n.py (UI string parity), this
makes CI fail when a translation falls behind."""
import pathlib

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent

# English docs that are part of the bilingual surface (each needs a .fr.md).
EN_DOCS = [
    "README.md", "INSTALL.md", "DISCLAIMER.md", "CONTRIBUTING.md",
    "docs/index.md", "docs/ARCHITECTURE.md", "docs/CANADA_RULES.md",
    "docs/COMPANY_HEALTH.md", "docs/QUARTERLY_WORKFLOW.md", "docs/TESTING.md",
]


def _fr(path):
    return path[:-3] + ".fr.md"


@pytest.mark.parametrize("doc", EN_DOCS)
def test_every_english_doc_has_french(doc):
    assert (ROOT / doc).exists(), f"missing English doc: {doc}"
    assert (ROOT / _fr(doc)).exists(), f"missing French translation: {_fr(doc)}"


def _headings(path):
    return [ln for ln in path.read_text(encoding="utf-8").splitlines()
            if ln.lstrip().startswith("#")]


@pytest.mark.parametrize("doc", EN_DOCS)
def test_translation_structurally_parallel(doc):
    en, fr = ROOT / doc, ROOT / _fr(doc)
    if not (en.exists() and fr.exists()):
        pytest.skip("counterpart missing (covered by the other test)")
    en_h, fr_h = len(_headings(en)), len(_headings(fr))
    # Allow a small delta for the language-switcher line; a larger gap signals drift.
    assert abs(en_h - fr_h) <= 1, (
        f"{doc}: heading count EN={en_h} vs FR={fr_h} — likely translation drift")
