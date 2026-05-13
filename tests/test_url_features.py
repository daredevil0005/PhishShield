import pytest

from src.url_normalize import normalize_url
from src.url_features import extract_url_features


def test_normalize_adds_scheme():
    assert normalize_url("example.com") == "http://example.com"


def test_normalize_https_preserved():
    assert normalize_url("https://example.com/x") == "https://example.com/x"


def test_normalize_rejects_javascript():
    assert normalize_url("javascript:alert(1)") is None


def test_normalize_rejects_empty():
    assert normalize_url("") is None
    assert normalize_url("   ") is None
    assert normalize_url(None) is None


def test_extract_features_schemeless_host():
    f = extract_url_features("google.com")
    assert f["length_url"] > 0
    assert "nb_dots" in f


def test_extract_features_invalid_raises():
    with pytest.raises(ValueError):
        extract_url_features("javascript:void(0)")