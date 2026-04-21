import joblib
import pandas as pd
import json
from src.url_features import extract_url_features

model = joblib.load("model/phishing_model.pkl")

with open("model/columns.json", "r") as f:
    columns = json.load(f)

def rule_based_check(url):
    url = url.lower()

    if "login" in url or "verify" in url or "bank" in url:
        return True

    if "@" in url:
        return True

    if url.count("//") > 1:
        return True

    if any(tld in url for tld in [".tk", ".ml", ".ga", ".cf"]):
        return True

    if any(char.isdigit() for char in url.split("//")[-1].split("/")[0]):
        return True

    return False

def predict_url(url):
    # 🔥 Rule-based first (STRONG SIGNAL)
    if rule_based_check(url):
        return "Phishing 🚨 (Rule-Based Detection)"

    # ML fallback
    features = extract_url_features(url)
    df = pd.DataFrame([features])

    for col in columns:
        if col not in df:
            df[col] = 0

    df = df[columns]

    prediction = model.predict(df)[0]
    prob = max(model.predict_proba(df)[0])

    if prediction == 1:
        return f"Phishing 🚨 (Confidence: {prob:.2f})"
    else:
        return f"Safe ✅ (Confidence: {prob:.2f})"