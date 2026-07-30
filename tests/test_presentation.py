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
        assert len(slides) == 5

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

        # Check Slide 4: Prescriptive Playbook
        assert slides[3]["layout"] == "prescriptive_playbook"
        assert "playbook" in slides[3]
        assert len(slides[3]["playbook"]) == 4

        # Check Slide 5: Journey workflow
        assert slides[4]["layout"] == "journey_workflow"
        assert "steps" in slides[4]
        assert len(slides[4]["steps"]) == 4
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
        assert pbi_payload["connections"][0]["type"] == "Web"
    finally:
        if old_db is not None:
            os.environ["CHURN_DB"] = old_db
        elif "CHURN_DB" in os.environ:
            del os.environ["CHURN_DB"]


def test_custom_slide_count_presentation(tmp_path):
    db_path = tmp_path / "custom_presentation_test.db"
    old_db = os.environ.get("CHURN_DB")
    os.environ["CHURN_DB"] = str(db_path)
    try:
        flask_app = app_module.create_app()
        flask_app.config.update(TESTING=True)
        client = flask_app.test_client()

        response = client.post("/api/presentation", json={"num_slides": 8})
        assert response.status_code == 200
        payload = response.get_json()
        assert len(payload["slides"]) == 8

        response12 = client.post("/api/presentation", json={"num_slides": 12})
        assert response12.status_code == 200
        payload12 = response12.get_json()
        assert len(payload12["slides"]) == 12
    finally:
        if old_db is not None:
            os.environ["CHURN_DB"] = old_db
        elif "CHURN_DB" in os.environ:
            del os.environ["CHURN_DB"]
