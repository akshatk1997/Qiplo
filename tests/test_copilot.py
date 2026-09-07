import sys
from pathlib import Path
import os
import json

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import app as app_module
import churn_analysis


def test_get_database_context_summary_empty(tmp_path):
    db_path = tmp_path / "empty_copilot.db"
    res = churn_analysis.get_database_context_summary(db_path)
    assert "file does not exist" in res.lower()


def test_get_database_context_summary_populated(tmp_path):
    db_path = tmp_path / "populated_copilot.db"
    schema_path = Path(__file__).resolve().parents[1] / "sql" / "schema.sql"
    
    churn_analysis.ensure_database(db_path, schema_path)
    # The ensure_database will populate it with 25 records and train
    
    res = churn_analysis.get_database_context_summary(db_path)
    assert "system database context" in res.lower()
    assert "total customer records: 25" in res.lower()
    assert "highest risk" in res.lower()


def test_chat_api_missing_key():
    flask_app = app_module.create_app()
    flask_app.config.update(TESTING=True)
    client = flask_app.test_client()

    # Clear env key if any
    old_key = os.environ.get("GEMINI_API_KEY")
    if "GEMINI_API_KEY" in os.environ:
        del os.environ["GEMINI_API_KEY"]

    try:
        response = client.post(
            "/api/chat",
            data=json.dumps({"message": "Hello"}),
            content_type="application/json"
        )
        assert response.status_code == 200
        payload = response.get_json()
        assert "senior data science consultation" in payload["response"].lower()
    finally:
        if old_key:
            os.environ["GEMINI_API_KEY"] = old_key


def test_chat_api_no_data(tmp_path):
    import sqlite3
    db_path = tmp_path / "empty_copilot_chat.db"
    old_db = os.environ.get("CHURN_DB")
    os.environ["CHURN_DB"] = str(db_path)
    try:
        flask_app = app_module.create_app()
        flask_app.config.update(TESTING=True)
        client = flask_app.test_client()

        # Trigger health check so before_request runs ensure_database once
        client.get("/api/health")

        # Now clear customer_churn table and mark db initialized so it won't re-seed
        flask_app.config["DB_INITIALIZED_PATHS"].add(str(db_path))
        conn = sqlite3.connect(db_path)
        conn.execute("DELETE FROM customer_churn")
        conn.commit()
        conn.close()

        res = client.post(
            "/api/chat",
            data=json.dumps({"message": "What is the churn risk?"}),
            content_type="application/json"
        )
        assert res.status_code == 400
        payload = res.get_json()
        assert payload["has_data"] is False
        assert "Dataset Data Required" in payload["error"]
    finally:
        if old_db is not None:
            os.environ["CHURN_DB"] = old_db
        elif "CHURN_DB" in os.environ:
            del os.environ["CHURN_DB"]

