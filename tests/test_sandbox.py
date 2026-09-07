import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import app as app_module

def test_sandbox_predict():
    flask_app = app_module.create_app()
    flask_app.config.update(TESTING=True)
    client = flask_app.test_client()

    simulated_data = {
        "tenure_months": 12,
        "monthly_charges": 85.5,
        "support_tickets": 4,
        "customer_satisfaction_score": 2,
        "payment_delays": 5,
        "product_usage": 10.0,
        "complaint_count": 2
    }

    response = client.post(
        "/api/sandbox/predict",
        data=json.dumps(simulated_data),
        content_type="application/json"
    )

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["status"] == "ok"
    assert "probability" in payload
    assert "label" in payload
    assert "recommendations" in payload
    assert len(payload["recommendations"]) > 0


def test_sandbox_predict_no_data(tmp_path):
    import os
    import sqlite3
    db_path = tmp_path / "empty_sandbox.db"
    old_db = os.environ.get("CHURN_DB")
    os.environ["CHURN_DB"] = str(db_path)
    try:
        flask_app = app_module.create_app()
        flask_app.config.update(TESTING=True)
        client = flask_app.test_client()

        # Trigger initial request so before_request runs ensure_database once
        client.get("/api/health")

        # Now clear customer_churn table and mark db initialized so it won't re-seed
        flask_app.config["DB_INITIALIZED_PATHS"].add(str(db_path))
        conn = sqlite3.connect(db_path)
        conn.execute("DELETE FROM customer_churn")
        conn.commit()
        conn.close()

        res = client.post(
            "/api/sandbox/predict",
            data=json.dumps({"tenure_months": 12}),
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

