import json
import joblib
import pandas as pd
from urllib.parse import urlparse

from src.url_features import extract_url_features
from src.url_normalize import normalize_url

_model = None
_columns = None


def _get_model_and_columns():
    global _model, _columns
    if _model is None:
        _model = joblib.load("model/phishing_model.pkl")
        with open("model/columns.json", "r") as f:
            _columns = json.load(f)
    return _model, _columns


def rule_based_check(url):
    """
    High-precision heuristics only. Broad keyword / digit rules are left to the ML model.
    """
    parsed = urlparse(url)
    netloc = (parsed.netloc or "").lower()

    if "@" in netloc:
        return True

    if url.lower().count("//") > 1:
        return True

    suspicious_tlds = (".tk", ".ml", ".ga", ".cf")
    if any(netloc.endswith(tld) for tld in suspicious_tlds):
        return True

    return False


def predict_url(url):
    normalized = normalize_url(url)
    if normalized is None:
        return "Invalid URL — enter a valid http(s) or hostname address."

    if rule_based_check(normalized):
        return "Phishing 🚨 (Rule-Based Detection)"

    try:
        model, columns = _get_model_and_columns()
        features = extract_url_features(normalized)
        df = pd.DataFrame([features])

        for col in columns:
            if col not in df:
                df[col] = 0

        df = df[columns]

        prediction = model.predict(df)[0]
        prob = max(model.predict_proba(df)[0])

        if prediction == 1:
            return f"Phishing 🚨 (Confidence: {prob:.2f})"
        return f"Safe ✅ (Confidence: {prob:.2f})"
    except FileNotFoundError:
        return "Model files are missing. Train the model or add model/phishing_model.pkl."
    except (ValueError, KeyError, OSError):
        return "Could not analyze this URL. Check the format and try again."
    except Exception:
        return "An unexpected error occurred. Please try again later."