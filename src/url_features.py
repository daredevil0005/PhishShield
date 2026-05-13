import re
from urllib.parse import urlparse
import ipaddress
import math

from src.url_normalize import normalize_url


def entropy(s):
    if not s:
        return 0.0
    prob = [float(s.count(c)) / len(s) for c in set(s)]
    return -sum([p * math.log2(p) for p in prob])


def extract_url_features(url):
    normalized = normalize_url(url)
    if normalized is None:
        raise ValueError("invalid or unsupported URL")

    url = normalized
    parsed = urlparse(url)
    domain = parsed.netloc

    features = {}

    features["length_url"] = len(url)
    features["nb_dots"] = url.count(".")
    features["nb_hyphens"] = url.count("-")
    features["https_token"] = 1 if parsed.scheme == "https" else 0

    digits = sum(c.isdigit() for c in url)
    features["ratio_digits_url"] = digits / len(url) if len(url) > 0 else 0

    features["nb_subdomains"] = domain.count(".")

    keywords = [
        "login",
        "verify",
        "bank",
        "secure",
        "account",
        "update",
        "free",
        "bonus",
    ]
    features["suspicious_words"] = sum(word in url.lower() for word in keywords)

    host = parsed.hostname
    if host:
        try:
            ipaddress.ip_address(host)
            features["has_ip"] = 1
        except ValueError:
            features["has_ip"] = 0
    else:
        features["has_ip"] = 0

    features["special_chars"] = len(re.findall(r'[!@#$%^&*(),?":{}|<>]', url))

    features["is_long_url"] = 1 if len(url) > 75 else 0

    suspicious_tlds = [".tk", ".ml", ".ga", ".cf"]
    features["suspicious_tld"] = (
        1 if any(domain.endswith(tld) for tld in suspicious_tlds) else 0
    )

    features["has_numbers_in_domain"] = (
        1 if any(c.isdigit() for c in domain) else 0
    )

    features["url_entropy"] = entropy(url)

    features["double_slash"] = 1 if url.count("//") > 1 else 0

    return features
