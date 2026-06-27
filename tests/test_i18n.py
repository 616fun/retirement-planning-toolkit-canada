"""Unit tests for the i18n string table and helpers."""
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


def test_every_string_has_english():
    # English is the fallback; a missing "en" would break t() for that key.
    missing = [k for k, v in i18n.STRINGS.items() if "en" not in v]
    assert not missing, f"strings missing English: {missing}"
