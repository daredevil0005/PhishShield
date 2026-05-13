from src.predictor import rule_based_check
from src.url_normalize import normalize_url


def test_rule_userinfo_in_host():
    u = normalize_url("http://legit-looking@evil.com/path")
    assert u is not None
    assert rule_based_check(u) is True


def test_rule_double_slash_obfuscation():
    u = normalize_url("http://phish.com/https://real-bank.com")
    assert u is not None
    assert rule_based_check(u) is True


def test_rule_suspicious_tld():
    u = normalize_url("http://something.tk/x")
    assert u is not None
    assert rule_based_check(u) is True


def test_rule_safe_common_site():
    u = normalize_url("https://www.worldbank.org/en/home")
    assert u is not None
    assert rule_based_check(u) is False