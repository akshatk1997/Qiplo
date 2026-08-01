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
