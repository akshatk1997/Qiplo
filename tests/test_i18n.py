import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest
import app as app_module
from i18n_backend import (
    SUPPORTED_LANGUAGES,
    normalize_language,
    generate_sandbox_recommendations,
    get_localized_presentation_deck,
    format_localized_chat_response,
    enhance_system_instruction_with_language
)

def test_supported_languages_and_normalization():
    assert len(SUPPORTED_LANGUAGES) == 10
    expected_codes = ["en", "es", "fr", "de", "zh", "ja", "pt", "ar", "hi", "ru"]
    for code in expected_codes:
        assert code in SUPPORTED_LANGUAGES
        assert normalize_language(code) == code
        assert "name" in SUPPORTED_LANGUAGES[code]
        assert "native" in SUPPORTED_LANGUAGES[code]
    
    # Test normalization fallback
    assert normalize_language("invalid_lang") == "en"
    assert normalize_language(None) == "en"
    assert normalize_language("ES") == "es"
    assert normalize_language("  ZH  ") == "zh"

def test_sandbox_recommendations_multilingual():
    # High risk in English
    recs_en = generate_sandbox_recommendations(0.85, 0.6, tickets=3, satisfaction=1, delays=4, language="en")
    assert any("HIGH CHURN RISK" in r for r in recs_en)
    assert any("Resolve Support Issues" in r for r in recs_en)
    
    # High risk in Spanish
    recs_es = generate_sandbox_recommendations(0.85, 0.6, tickets=3, satisfaction=1, delays=4, language="es")
    assert any("ALTO RIESGO DE CANCELACIÓN" in r for r in recs_es)
    assert any("Resolver problemas de soporte" in r for r in recs_es)

    # Low risk in French
    recs_fr = generate_sandbox_recommendations(0.20, 0.6, tickets=0, satisfaction=5, delays=0, language="fr")
    assert any("FAIBLE RISQUE DE DÉSABONNEMENT" in r for r in recs_fr)

    # Low risk in German
    recs_de = generate_sandbox_recommendations(0.20, 0.6, tickets=0, satisfaction=5, delays=0, language="de")
    assert any("GERINGES ABWANDERUNGSRISIKO" in r for r in recs_de)

    # High risk in Chinese
    recs_zh = generate_sandbox_recommendations(0.85, 0.6, tickets=2, satisfaction=1, delays=3, language="zh")
    assert any("高流失风险" in r for r in recs_zh)

    # High risk in Japanese
    recs_ja = generate_sandbox_recommendations(0.85, 0.6, tickets=2, satisfaction=1, delays=3, language="ja")
    assert any("高解約リスク" in r for r in recs_ja)

    # High risk in Portuguese
    recs_pt = generate_sandbox_recommendations(0.85, 0.6, tickets=2, satisfaction=1, delays=3, language="pt")
    assert any("ALTO RISCO DE CHURN" in r for r in recs_pt)

    # High risk in Arabic
    recs_ar = generate_sandbox_recommendations(0.85, 0.6, tickets=2, satisfaction=1, delays=3, language="ar")
    assert any("مستوى مخاطر تسرب مرتفع" in r for r in recs_ar)

    # High risk in Hindi
    recs_hi = generate_sandbox_recommendations(0.85, 0.6, tickets=2, satisfaction=1, delays=3, language="hi")
    assert any("उच्च ग्राहक मंथन जोखिम" in r for r in recs_hi)

    # High risk in Russian
    recs_ru = generate_sandbox_recommendations(0.85, 0.6, tickets=2, satisfaction=1, delays=3, language="ru")
    assert any("ВЫСОКИЙ РИСК ОТТОКА" in r for r in recs_ru)

def test_presentation_deck_multilingual():
    top_segs = [{"dimension": "Contract", "value": "Month-to-month", "expected_loss": 5000.0}]
    
    # English Deck
    deck_en = get_localized_presentation_deck(1000, 0.35, top_segs, language="en")
    assert len(deck_en) == 5
    assert "Qiplo Executive Presentation" in deck_en[0]["title"]

    # Spanish Deck
    deck_es = get_localized_presentation_deck(1000, 0.35, top_segs, language="es")
    assert len(deck_es) == 5
    assert "Presentación Ejecutiva Qiplo" in deck_es[0]["title"]

    # French Deck
    deck_fr = get_localized_presentation_deck(1000, 0.35, top_segs, language="fr")
    assert len(deck_fr) == 5
    assert "Présentation Exécutive Qiplo" in deck_fr[0]["title"]

    # German Deck
    deck_de = get_localized_presentation_deck(1000, 0.35, top_segs, language="de")
    assert len(deck_de) == 5
    assert "Qiplo Management-Präsentation" in deck_de[0]["title"]

    # Chinese Deck
    deck_zh = get_localized_presentation_deck(1000, 0.35, top_segs, language="zh")
    assert len(deck_zh) == 5
    assert "Qiplo 高管决策汇报演示" in deck_zh[0]["title"]

    # Japanese Deck
    deck_ja = get_localized_presentation_deck(1000, 0.35, top_segs, language="ja")
    assert len(deck_ja) == 5
    assert "Qiplo エグゼクティブ プレゼンテーション" in deck_ja[0]["title"]

    # Russian Deck
    deck_ru = get_localized_presentation_deck(1000, 0.35, top_segs, language="ru")
    assert len(deck_ru) == 5
    assert "Исполнительная презентация Qiplo" in deck_ru[0]["title"]

def test_chat_offline_responses_multilingual():
    ctx = {
        "total_cust": 1200,
        "high_risk": 240,
        "high_risk_pct": 20.0,
        "risk_mrr": 18500.0,
        "avg_risk": 28.5
    }
    
    # Spanish welcome
    resp_es = format_localized_chat_response("welcome_header", ctx, language="es")
    assert "¡Bienvenido a Qiplo" in resp_es
    assert "1,200" in resp_es or "1200" in resp_es

    # French welcome
    resp_fr = format_localized_chat_response("welcome_header", ctx, language="fr")
    assert "Bienvenue sur Qiplo" in resp_fr

    # German welcome
    resp_de = format_localized_chat_response("welcome_header", ctx, language="de")
    assert "Willkommen bei Qiplo" in resp_de

    # Chinese welcome
    resp_zh = format_localized_chat_response("welcome_header", ctx, language="zh")
    assert "欢迎使用 Qiplo" in resp_zh

    # Japanese welcome
    resp_ja = format_localized_chat_response("welcome_header", ctx, language="ja")
    assert "Qiplo へようこそ" in resp_ja

    # Arabic welcome
    resp_ar = format_localized_chat_response("welcome_header", ctx, language="ar")
    assert "مرحبًا بك في Qiplo" in resp_ar

    # Hindi welcome
    resp_hi = format_localized_chat_response("welcome_header", ctx, language="hi")
    assert "Qiplo में आपका स्वागत है" in resp_hi

    # Russian welcome
    resp_ru = format_localized_chat_response("welcome_header", ctx, language="ru")
    assert "Добро пожаловать в Qiplo" in resp_ru

def test_enhance_system_instruction():
    base = "You are a customer retention expert."
    res_en = enhance_system_instruction_with_language(base, "en")
    assert res_en == base

    res_es = enhance_system_instruction_with_language(base, "es")
    assert "MULTILINGUAL MANDATE" in res_es
    assert "Español" in res_es

    res_zh = enhance_system_instruction_with_language(base, "zh")
    assert "MULTILINGUAL MANDATE" in res_zh
    assert "简体中文" in res_zh

def test_api_endpoints_with_language():
    flask_app = app_module.create_app()
    flask_app.config.update(TESTING=True)
    client = flask_app.test_client()
    # 1. Test GET / contains language selector elements
    res = client.get("/")
    assert res.status_code == 200
    html = res.get_data(as_text=True)
    assert 'id="langSelectBtn"' in html
    assert 'id="langDropdownMenu"' in html
    assert 'data-lang="es"' in html
    assert 'data-lang="fr"' in html
    assert 'data-lang="zh"' in html
    assert 'data-lang="ja"' in html
    assert 'mobile-lang-grid' in html
    assert 'static/i18n.js' in html

    # 2. Test POST /api/sandbox/predict with language="es"
    sim_data = {
        "tenure_months": 2,
        "monthly_charges": 110.0,
        "support_tickets": 4,
        "customer_satisfaction_score": 1,
        "payment_delays": 5,
        "language": "es"
    }
    res_sim = client.post("/api/sandbox/predict", data=json.dumps(sim_data), content_type="application/json")
    assert res_sim.status_code == 200
    sim_resp = res_sim.get_json()
    assert "recommendations" in sim_resp
    assert any("ALTO RIESGO" in r or "BAJO RIESGO" in r for r in sim_resp["recommendations"])

    # 3. Test POST /api/presentation/generate with language="fr"
    pres_data = {
        "num_slides": 5,
        "language": "fr"
    }
    res_pres = client.post("/api/presentation/generate", data=json.dumps(pres_data), content_type="application/json")
    assert res_pres.status_code == 200
    pres_resp = res_pres.get_json()
    assert "slides" in pres_resp
    assert len(pres_resp["slides"]) > 0
    assert "Présentation Exécutive" in pres_resp["slides"][0]["title"]

    # 4. Test POST /api/chat with language="de"
    chat_data = {
        "message": "hello",
        "language": "de"
    }
    res_chat = client.post("/api/chat", data=json.dumps(chat_data), content_type="application/json")
    assert res_chat.status_code == 200
    chat_resp = res_chat.get_json()
    assert "response" in chat_resp
    assert "Willkommen bei Qiplo" in chat_resp["response"]
