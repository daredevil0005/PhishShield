import json
from unittest.mock import patch

import pytest


@pytest.fixture
def client():
    import app as app_main

    app_main.app.config["TESTING"] = True
    app_main.app.config["WTF_CSRF_ENABLED"] = False
    with patch.object(app_main, "predict_url", return_value="Safe ✅ (Confidence: 0.99)"):
        yield app_main.app.test_client()


def test_api_check_success(client):
    r = client.post(
        "/api/check",
        data=json.dumps({"url": "https://example.com/path"}),
        content_type="application/json",
    )
    assert r.status_code == 200
    data = r.get_json()
    assert data["result"] == "Safe ✅ (Confidence: 0.99)"


def test_api_check_requires_json(client):
    r = client.post(
        "/api/check",
        data="not json",
        content_type="text/plain",
    )
    assert r.status_code == 400


def test_api_check_invalid_json(client):
    r = client.post(
        "/api/check",
        data="{",
        content_type="application/json",
    )
    assert r.status_code == 400


def test_api_check_missing_url(client):
    r = client.post(
        "/api/check",
        data=json.dumps({}),
        content_type="application/json",
    )
    assert r.status_code == 400


def test_api_check_empty_url(client):
    r = client.post(
        "/api/check",
        data=json.dumps({"url": "  "}),
        content_type="application/json",
    )
    assert r.status_code == 400


def test_api_check_url_not_string(client):
    r = client.post(
        "/api/check",
        data=json.dumps({"url": 123}),
        content_type="application/json",
    )
    assert r.status_code == 400