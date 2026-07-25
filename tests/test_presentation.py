import sys
from pathlib import Path
import json
import os

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import app as app_module
import churn_analysis


def test_presentation_api_generation(tmp_path):
    db_path = tmp_path / "presentation_test.db"
    old_db = os.environ.get("CHURN_DB")
    os.environ["CHURN_DB"] = str(db_path)
    try:
        flask_app = app_module.create_app()
        flask_app.config.update(TESTING=True)
        client = flask_app.test_client()

        response = client.post("/api/presentation", json={})
        assert response.status_code == 200
        payload = response.get_json()

        assert "slides" in payload
        slides = payload["slides"]
        assert len(slides) == 4

        # Check Slide 1: Title
        assert slides[0]["layout"] == "title"
        assert "title" in slides[0]
        assert "subtitle" in slides[0]

        # Check Slide 2: Split columns
        assert slides[1]["layout"] == "split_metrics"
        assert "bullets" in slides[1]
        assert len(slides[1]["bullets"]) == 3

        # Check Slide 3: Segment comparison
        assert slides[2]["layout"] == "segment_comparison"
        assert "bullets" in slides[2]

        # Check Slide 4: Journey workflow
        assert slides[3]["layout"] == "journey_workflow"
        assert "steps" in slides[3]
        assert len(slides[3]["steps"]) == 4
    finally:
        if old_db is not None:
            os.environ["CHURN_DB"] = old_db
        elif "CHURN_DB" in os.environ:
            del os.environ["CHURN_DB"]


def test_bi_exports(tmp_path):
    db_path = tmp_path / "bi_exports_test.db"
    old_db = os.environ.get("CHURN_DB")
    os.environ["CHURN_DB"] = str(db_path)
    try:
        flask_app = app_module.create_app()
        flask_app.config.update(TESTING=True)
        client = flask_app.test_client()

        # Test Tableau Export
        tab_res = client.get("/api/export/tableau")
        assert tab_res.status_code == 200
        assert "xml" in tab_res.content_type
        assert b"<workbook" in tab_res.data

        # Test Power BI Export
        pbi_res = client.get("/api/export/powerbi")
        assert pbi_res.status_code == 200
        assert "json" in pbi_res.content_type
        pbi_payload = json.loads(pbi_res.data)
        assert "connections" in pbi_payload
        assert pbi_payload["connections"][0]["type"] == "Sqlite"
    finally:
        if old_db is not None:
            os.environ["CHURN_DB"] = old_db
        elif "CHURN_DB" in os.environ:
            del os.environ["CHURN_DB"]
