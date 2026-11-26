"""
Tests for Curated Presentation Themes and Authentic Deck Layouts
Verifies the 6 analyzed presentation themes:
1. Next-Gen Creative Agency (Forest Green & Lime, Stepped Staircase Growth)
2. Mejor Exporta Global Trade (Royal Cobalt & Azure, Connected Capsule Roadmap)
3. Endorf Artisanal Luxury (Midnight Navy & Terracotta, Product Catalog Matrix)
4. Weskout Vibrant SaaS (Hyper Cobalt & Ripple Lines, Action Statement)
5. MyTemp Minimalist Enterprise (Slate Teal & Amber Gold, Service Pillars)
6. Ell.co Neo-Glass Hub (Electric Indigo-Violet, Radial Constellation Hub)
"""

import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["TESTING"] = "True"

import pytest
import app as app_module
from app import THEME_PALETTES, build_gamma_pptx, _generate_prompt_driven_gamma_deck
import corporate_presentation as cp


@pytest.fixture
def client():
    flask_app = app_module.create_app()
    flask_app.config.update(TESTING=True)
    return flask_app.test_client()


def test_curated_themes_exist_in_palettes():
    """Verify all 6 curated themes are registered in palettes."""
    curated_themes = [
        "creative_agency",
        "global_export",
        "artisan_luxury",
        "tech_weskout",
        "minimal_mytemp",
        "radial_glass"
    ]
    for th in curated_themes:
        assert th in THEME_PALETTES, f"{th} must be in app.THEME_PALETTES"
        assert th in cp.CORPORATE_PALETTES, f"{th} must be in cp.CORPORATE_PALETTES"
        pal = THEME_PALETTES[th]
        assert "bg" in pal
        assert "surface" in pal
        assert "accent" in pal
        assert "text" in pal


def test_generate_curated_theme_decks():
    """Verify prompt synthesis for each of the 6 themes produces authentic layouts."""
    theme_prompts = [
        ("Next-Gen Creative Agency Growth", ["stepped_growth", "what_makes_different", "kpi_split_cards"]),
        ("Mejor Exporta Global Trade", ["capsule_roadmap", "what_makes_different"]),
        ("Endorf Artisanal Luxury Portfolio", ["catalog_matrix", "kpi_split_cards"]),
        ("Weskout Vibrant SaaS Momentum", ["statement_ripple", "kpi_split_cards"]),
        ("MyTemp Minimalist Enterprise", ["what_makes_different", "kpi_split_cards"]),
        ("Ell.co Neo-Glass Constellation Hub", ["radial_hub", "kpi_split_cards"])
    ]

    for prompt, expected_layouts in theme_prompts:
        slides = _generate_prompt_driven_gamma_deck(prompt, num_slides=5, total_cust=250, avg_risk=0.268)
        assert len(slides) >= 3, f"Prompt '{prompt}' should yield at least 3 slides"
        layouts = [s.get("layout") for s in slides]
        for exp in expected_layouts:
            assert exp in layouts, f"Expected layout '{exp}' in slides for prompt '{prompt}', got: {layouts}"


def test_build_pptx_for_all_curated_themes(tmp_path):
    """Verify building and exporting native PPTX for each curated theme."""
    curated_themes = [
        "creative_agency",
        "global_export",
        "artisan_luxury",
        "tech_weskout",
        "minimal_mytemp",
        "radial_glass"
    ]

    slides = [
        {"layout": "title", "title": "Executive Presentation", "subtitle": "Board Briefing"},
        {"layout": "stepped_growth", "title": "Annual Growth", "badge_pct": "95%"},
        {"layout": "what_makes_different", "title": "Core Advantage", "subtitle": "Autonomous Intelligence"},
        {"layout": "kpi_split_cards", "title": "Key Benchmarks"},
        {"layout": "capsule_roadmap", "title": "Operational Roadmap"},
        {"layout": "radial_hub", "title": "Constellation Network"},
        {"layout": "catalog_matrix", "title": "Portfolio Matrix"},
        {"layout": "statement_ripple", "action_word": "Grow.", "statement": "Scale retention seamlessly."},
        {"layout": "quote_tab", "quote": "Retention is growth.", "attribution": "Executive Leadership"},
        {"layout": "closing", "title": "Next Steps", "subtitle": "Get started today."}
    ]

    for th in curated_themes:
        prs = build_gamma_pptx(slides, palette_name=th)
        assert len(prs.slides) == 10, f"Deck for {th} should have 10 slides"
        out_file = tmp_path / f"test_deck_{th}.pptx"
        prs.save(str(out_file))
        assert out_file.exists()
        assert out_file.stat().st_size > 1000, f"PPTX file for {th} should be > 1KB"


def test_api_download_pptx_curated_themes(client):
    """Verify API endpoint handles PPTX download requests for the curated themes."""
    payload = {
        "title": "Board Briefing Deck",
        "theme": "creative_agency",
        "slides": [
            {"layout": "title", "title": "Creative Agency Growth", "subtitle": "Q1 2026 Audit"},
            {"layout": "stepped_growth", "title": "ARR Expansion"},
            {"layout": "what_makes_different", "title": "What Makes Us Different"},
            {"layout": "kpi_split_cards", "title": "Performance Scorecard"}
        ]
    }
    res = client.post("/api/presentation/download-pptx", json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "ok"
    assert "download_url" in data
