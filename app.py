import os
import re

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect

from src.predictor import predict_url


def _cors_origin_patterns():
    origins = [
        "http://127.0.0.1:5000",
        "http://localhost:5000",
        re.compile(r"^chrome-extension://[\w-]+$"),
    ]
    for o in os.environ.get("CORS_EXTRA_ORIGINS", "").split(","):
        o = o.strip()
        if o:
            origins.append(o)
    return origins


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "dev-only-insecure-set-SECRET_KEY-in-production"
)
app.config["WTF_CSRF_ENABLED"] = True

csrf = CSRFProtect(app)
CORS(app, origins=_cors_origin_patterns())
limiter = Limiter(
    get_remote_address,
    app=app,
    storage_uri="memory://",
)


@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    if request.method == "POST":
        url = (request.form.get("url") or "").strip()
        if not url:
            result = "Please enter a URL."
        else:
            result = predict_url(url)
    return render_template("index.html", result=result)


@app.route("/api/check", methods=["POST"])
@csrf.exempt
@limiter.limit("90 per minute")
def check_url():
    if not request.is_json:
        return jsonify({"error": "Expected application/json"}), 400

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON body"}), 400

    url = data.get("url")
    if url is None or (isinstance(url, str) and not url.strip()):
        return jsonify({"error": "Missing or empty \"url\" field"}), 400
    if not isinstance(url, str):
        return jsonify({"error": "\"url\" must be a string"}), 400

    result = predict_url(url)
    return jsonify({"result": result})


if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "").lower() in ("1", "true", "yes")
    app.run(debug=debug, host="127.0.0.1")
