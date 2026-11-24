"""
Tests for Corporate Presentation Skill (Qiplo)
Verifies corporate-presentation/SKILL.md specification and implementation:
- Core principles (Code numbers, Deck JSON schema, Patch engine, Action titles)
- Accuracy guardrails validation
- Native PPTX chart and table rendering with 16:9 widescreen layout
- Flask API endpoints
"""

import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["TESTING"] = "True"

from pathlib import Path
import pytest
from pptx import Presentation

import app as app_module
import corporate_presentation as cp


@pytest.fixture
def client():
    flask_app = app_module.create_app()
    flask_app.config.update(TESTING=True)
    return flask_app.test_client()


def test_skill_markdown_exists():
    """Verify corporate-presentation/SKILL.md exists and contains the required spec."""
    skill_path = Path("corporate-presentation/SKILL.md")
    assert skill_path.exists(), "corporate-presentation/SKILL.md must exist in root"
    content = skill_path.read_text(encoding="utf-8")
    assert "name: corporate-presentation" in content
    assert "NUMBERS COME FROM CODE, NEVER FROM THE LLM" in content
    assert "ONE SOURCE OF TRUTH" in content
    assert "EVERY CHANGE IS A PATCH" in content
    assert "ACTION TITLES" in content
    assert "Deck JSON schema" in content


def test_compute_dataset_bindings():
    """Verify deterministic binding computation from dataset."""
    bindings = cp.compute_dataset_bindings()
    assert "revenue.total" in bindings
    assert "revenue.at_risk" in bindings
    assert "revenue.preserved" in bindings
    assert "customers.total" in bindings
    assert "churn.rate" in bindings
    assert "model.roc_auc" in bindings
    assert "drivers.top_1" in bindings
    # Check that counts reconcile
    assert bindings["customers.total_raw"] > 0


def test_generate_corporate_deck_json():
    """Verify Deck JSON schema, slide count, and action titles."""
    deck = cp.generate_corporate_deck_json(audience="board", num_slides=9)
    assert "meta" in deck
    assert "theme" in deck
    assert "slides" in deck
    assert len(deck["slides"]) == 9

    # Verify action titles stating conclusion
    for slide in deck["slides"]:
        assert "title" in slide
        title = slide["title"]
        assert len(title) > 10
        # Assert no unresolved placeholders in titles
        assert "{{" not in title and "}}" not in title
        assert "layout" in slide
        assert "notes" in slide


def test_accuracy_guardrails_validation():
    """Verify guardrails validator on clean vs corrupted decks."""
    bindings = cp.compute_dataset_bindings()
    deck = cp.generate_corporate_deck_json()

    # Valid deck should pass
    val_res = cp.validate_accuracy_guardrails(deck, bindings)
    assert val_res["ok"] is True
    assert len(val_res["errors"]) == 0

    # Deck with unresolved placeholder must fail
    corrupt_deck = dict(deck)
    corrupt_deck["slides"] = list(deck["slides"])
    corrupt_deck["slides"][0] = dict(corrupt_deck["slides"][0])
    corrupt_deck["slides"][0]["title"] = "Title with {{unknown_unresolved_metric}}"

    fail_res = cp.validate_accuracy_guardrails(corrupt_deck, bindings)
    assert fail_res["ok"] is False
    assert any("unknown_unresolved_metric" in err for err in fail_res["errors"])


def test_deck_patch_operations_and_locked_enforcement():
    """Verify JSON patch engine applies replacements, moves, and blocks locked slides."""
    deck = cp.generate_corporate_deck_json()
    
    # 1. Successful replace operation
    patches = [
        {"op": "replace", "path": "/slides/0/title", "value": "Approved Strategy by Executive Board"}
    ]
    res = cp.apply_deck_patch(deck, patches)
    assert res["ok"] is True
    assert res["deck"]["slides"][0]["title"] == "Approved Strategy by Executive Board"

    # 2. Lock Slide 0
    lock_patches = [
        {"op": "replace", "path": "/slides/0/locked", "value": True}
    ]
    locked_res = cp.apply_deck_patch(res["deck"], lock_patches)
    assert locked_res["ok"] is True
    assert locked_res["deck"]["slides"][0]["locked"] is True

    # 3. Attempt to modify locked slide -> must be rejected
    illegal_patch = [
        {"op": "replace", "path": "/slides/0/title", "value": "Unapproved Change"}
    ]
    fail_res = cp.apply_deck_patch(locked_res["deck"], illegal_patch)
    assert fail_res["ok"] is False
    assert "locked" in fail_res["message"]


def test_export_native_pptx_with_open_test(tmp_path):
    """Verify export to native 16:9 PPTX with native charts, tables, notes, and open-test."""
    deck = cp.generate_corporate_deck_json(num_slides=5)
    out_file = tmp_path / "corporate_deck.pptx"

    exported_path = cp.export_corporate_deck_to_pptx(deck, str(out_file), palette_name="classic_blue")
    assert Path(exported_path).exists()

    # Re-parse to verify 16:9 widescreen dimensions and slide count
    prs = Presentation(exported_path)
    assert len(prs.slides) == 5
    assert abs(prs.slide_width.inches - 13.333) < 0.05
    assert abs(prs.slide_height.inches - 7.5) < 0.05

    # Verify speaker notes are injected
    first_slide = prs.slides[0]
    assert first_slide.notes_slide.notes_text_frame.text != ""


def test_api_corporate_presentation_endpoints(client):
    """Verify Flask API endpoints for corporate presentations."""
    # 1. Generate endpoint
    gen_res = client.post("/api/corporate-presentation/generate", json={"audience": "board", "num_slides": 7})
    assert gen_res.status_code == 200
    gen_data = gen_res.get_json()
    assert gen_data["status"] == "ok"
    assert gen_data["slides_count"] == 7
    deck = gen_data["deck"]

    # 2. Validate endpoint
    val_res = client.post("/api/corporate-presentation/validate", json={"deck": deck})
    assert val_res.status_code == 200
    val_data = val_res.get_json()
    assert val_data["ok"] is True

    # 3. Patch endpoint
    patch_res = client.post("/api/corporate-presentation/patch", json={
        "deck": deck,
        "patches": [{"op": "replace", "path": "/meta/title", "value": "Board Strategy Deck Q1"}]
    })
    assert patch_res.status_code == 200
    patch_data = patch_res.get_json()
    assert patch_data["ok"] is True
    assert patch_data["deck"]["meta"]["title"] == "Board Strategy Deck Q1"

    # 4. Export PPTX endpoint
    export_res = client.post("/api/corporate-presentation/export-pptx", json={"deck": deck})
    assert export_res.status_code == 200
    export_data = export_res.get_json()
    assert export_data["status"] == "ok"
    assert "download_url" in export_data
