import re
from urllib.parse import urlparse
import ipaddress
import math

def entropy(s):
    prob = [float(s.count(c)) / len(s) for c in set(s)]
    return -sum([p * math.log2(p) for p in prob])

def extract_url_features(url):
    parsed = urlparse(url)
    domain = parsed.netloc

    features = {}

    # Basic
    features['length_url'] = len(url)
    features['nb_dots'] = url.count('.')
    features['nb_hyphens'] = url.count('-')
    features['https_token'] = 1 if parsed.scheme == 'https' else 0

    # Digits
    digits = sum(c.isdigit() for c in url)
    features['ratio_digits_url'] = digits / len(url) if len(url) > 0 else 0

    # Subdomains
    features['nb_subdomains'] = domain.count('.')

    # Suspicious keywords
    keywords = ['login', 'verify', 'bank', 'secure', 'account', 'update', 'free', 'bonus']
    features['suspicious_words'] = sum(word in url.lower() for word in keywords)

    # IP address
    try:
        ipaddress.ip_address(domain)
        features['has_ip'] = 1
    except:
        features['has_ip'] = 0

    # Special characters
    features['special_chars'] = len(re.findall(r'[!@#$%^&*(),?":{}|<>]', url))

    # Long URL
    features['is_long_url'] = 1 if len(url) > 75 else 0

    # Suspicious TLD
    suspicious_tlds = ['.tk', '.ml', '.ga', '.cf']
    features['suspicious_tld'] = 1 if any(domain.endswith(tld) for tld in suspicious_tlds) else 0

    # Numbers in domain
    features['has_numbers_in_domain'] = 1 if any(c.isdigit() for c in domain) else 0

    # URL entropy (very powerful)
    features['url_entropy'] = entropy(url)

    # Double slash trick
    features['double_slash'] = 1 if url.count('//') > 1 else 0

    return features