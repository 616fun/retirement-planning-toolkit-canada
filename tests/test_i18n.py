"""Unit tests for the i18n loader and the JSON locale files."""
import i18n


def test_lookup_french():
    assert i18n.t("kpi.investable", "fr") == "Actifs investissables"


def test_falls_back_to_english_for_missing_locale():
    # German isn't a locale we carry -> English text, not a crash.
    assert i18n.t("kpi.investable", "de") == "Investable"


def test_unknown_key_returns_key():
    assert i18n.t("does.not.exist", "fr") == "does.not.exist"


def test_formatting_kwargs():
    s = i18n.t("conc.thresholds", "fr", watch=5, trim=7)
    assert "5 %" in s and "7 %" in s


def test_lang_of():
    assert i18n.lang_of({"language": "fr"}) == "fr"
    assert i18n.lang_of({"language": "FR"}) == "fr"
    assert i18n.lang_of({}) == "en"
    assert i18n.lang_of({"language": None}) == "en"


def test_french_has_every_english_key():
    # Drift guard: every English (canonical) key must exist in French, so nothing
    # silently falls back to English in the localized product.
    missing = i18n.keys("en") - i18n.keys("fr")
    assert not missing, f"fr.json missing keys: {sorted(missing)}"


def test_no_extra_french_keys():
    extra = i18n.keys("fr") - i18n.keys("en")
    assert not extra, f"fr.json has keys not in en.json (typos?): {sorted(extra)}"
