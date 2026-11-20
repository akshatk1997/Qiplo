import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["TESTING"] = "True"

import pytest
import app as app_module
from app import THEME_PALETTES, build_gamma_pptx

@pytest.fixture
def client():
    flask_app = app_module.create_app()
    flask_app.config.update(TESTING=True)
    return flask_app.test_client()

def test_pptx_skill_theme_palettes_count():
    assert len(THEME_PALETTES) >= 30
    skill_palettes = [
        "classic_blue", "teal_coral", "bold_red", "warm_blush",
        "burgundy_luxury", "deep_purple_emerald", "cream_forest",
        "pink_purple", "lime_plum", "black_gold", "sage_terracotta",
        "charcoal_red", "vibrant_orange", "forest_green",
        "retro_rainbow", "vintage_earthy", "coastal_rose", "orange_turquoise"
    ]
    for p in skill_palettes:
        assert p in THEME_PALETTES
        assert "bg" in THEME_PALETTES[p]
        assert "surface" in THEME_PALETTES[p]
        assert "accent" in THEME_PALETTES[p]
        assert "text" in THEME_PALETTES[p]

def test_pptx_build_gamma_deck():
    slides = [
        {"layout": "title", "title": "Hero Title", "subtitle": "Executive Briefing"},
        {"layout": "clv_quadrants", "title": "CLV 4-Quadrant Matrix", "protect_cnt": 15, "protect_mrr": 2500},
        {"layout": "friction_telemetry", "title": "Friction Signals", "high_tickets_cnt": 10},
        {"layout": "recovery_scenarios", "title": "ARR Preservation Scenarios", "conserv_arr": "$15,000 Saved ARR"},
        {"layout": "split_metrics", "title": "Key Indicators", "bullets": ["Signal 1", "Signal 2"]},
        {"layout": "segment_comparison", "title": "Comparison", "bullets": ["A", "B", "C", "D"]},
        {"layout": "prescriptive_playbook", "title": "Playbook", "playbook": [{"title": "Action", "desc": "Desc"}]},
        {"layout": "journey_workflow", "title": "Timeline", "steps": [{"title": "Stage", "description": "Desc"}]},
        {"layout": "quote", "quote": "Excellence in customer retention.", "attribution": "Qiplo AI"},
        {"layout": "closing", "title": "Next Steps", "subtitle": "Start today"}
    ]
    prs = build_gamma_pptx(slides, palette_name="classic_blue")
    assert len(prs.slides) == 10

def test_presentation_api_custom_prompts(client):
    # Prompt 1: CLV Strategy
    res1 = client.post("/api/presentation/generate", json={"custom_prompt": "Customer Lifetime Value (CLV) & Revenue Risk 4-Quadrant Strategy Deck", "num_slides": 5})
    assert res1.status_code == 200
    data1 = res1.get_json()
    assert "slides" in data1
    layouts1 = [s["layout"] for s in data1["slides"]]
    assert "clv_quadrants" in layouts1

    # Prompt 2: Support Friction
    res2 = client.post("/api/presentation/generate", json={"custom_prompt": "Customer Friction Telemetry & Support Escalation Audit with CSAT and SLA Exposure", "num_slides": 5})
    assert res2.status_code == 200
    data2 = res2.get_json()
    assert "slides" in data2
    layouts2 = [s["layout"] for s in data2["slides"]]
    assert "friction_telemetry" in layouts2

    # Prompt 3: Financial ARR Recovery
    res3 = client.post("/api/presentation/generate", json={"custom_prompt": "Financial ARR Recovery Scenarios & ROI Payback Executive Forecast", "num_slides": 5})
    assert res3.status_code == 200
    data3 = res3.get_json()
    assert "slides" in data3
    layouts3 = [s["layout"] for s in data3["slides"]]
    assert "recovery_scenarios" in layouts3

def test_download_presentation_pptx_endpoint(client):
    # Generate deck then download pptx
    res = client.post("/api/presentation/generate", json={"num_slides": 8})
    assert res.status_code == 200
    deck = res.get_json()["slides"]
    
    download_res = client.post("/api/presentation/download-pptx", json={"slides": deck, "theme": "black_gold"})
    assert download_res.status_code == 200
    download_data = download_res.get_json()
    assert download_data["status"] == "ok"
    assert "download_url" in download_data
