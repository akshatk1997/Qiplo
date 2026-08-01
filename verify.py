import json
import os
import sys
from pathlib import Path
from io import BytesIO

# Reconfigure stdout to use UTF-8 encoding on Windows to prevent UnicodeEncodeError
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Insert project path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import app as app_module
import churn_analysis

def run_atoz_verification():
    print("======================================================================")
    print("[START] STARTING A-TO-Z SYSTEM & DASHBOARD INTEGRITY VERIFICATION")
    print("======================================================================\n")

    flask_app = app_module.create_app()
    flask_app.config.update(TESTING=True)
    client = flask_app.test_client()

    success = True

    # 1. Test HTML loading routes
    print("[INFO] Testing HTML Loading Routes...")
    routes = ["/", "/dashboard", "/actions", "/business", "/presentation", "/guide"]
    for r in routes:
        res = client.get(r)
        if res.status_code == 200:
            print(f"  [OK] GET {r} -> 200 OK")
        else:
            print(f"  [ERROR] GET {r} -> FAILED ({res.status_code})")
            success = False

    # 2. Test Health Route
    print("\n[INFO] Testing System Health Endpoint...")
    res = client.get("/api/health")
    if res.status_code == 200:
        data = res.get_json()
        print(f"  [OK] GET /api/health -> 200 OK (Status: {data.get('status')})")
    else:
        print(f"  [ERROR] GET /api/health -> FAILED ({res.status_code})")
        success = False

    # 3. Test Dashboard State Route
    print("\n[INFO] Testing Dashboard State Endpoint...")
    res = client.get("/api/dashboard-state?role=manager")
    if res.status_code == 200:
        data = res.get_json()
        print(f"  [OK] GET /api/dashboard-state -> 200 OK")
        print(f"     - Summary Items: {data.get('summary', [])}")
        print(f"     - Total predictions loaded: {len(data.get('predictions', []))}")
        print(f"     - Active Model Engine: {data.get('branding', {}).get('model_engine_name')}")
    else:
        print(f"  [ERROR] GET /api/dashboard-state -> FAILED ({res.status_code})")
        success = False

    # 4. Test Predictions List Endpoint
    print("\n[INFO] Testing Customer Predictions List Endpoint...")
    res = client.get("/api/predictions")
    if res.status_code == 200:
        data = res.get_json()
        print(f"  [OK] GET /api/predictions -> 200 OK (Loaded {len(data.get('predictions', []))} records)")
    else:
        print(f"  [ERROR] GET /api/predictions -> FAILED ({res.status_code})")
        success = False

    # 5. Test Sandbox What-If Simulator
    print("\n[INFO] Testing Sandbox Simulation Endpoint...")
    sandbox_input = {
        "tenure_months": 24,
        "monthly_charges": 75.0,
        "support_tickets": 2,
        "customer_satisfaction_score": 3,
        "payment_delays": 1,
        "product_usage": 20.0,
        "complaint_count": 1
    }
    res = client.post("/api/sandbox/predict", data=json.dumps(sandbox_input), content_type="application/json")
    if res.status_code == 200:
        data = res.get_json()
        print(f"  [OK] POST /api/sandbox/predict -> 200 OK")
        print(f"     - Simulated Churn Prob: {data.get('probability'):.3f}")
        print(f"     - Assigned Class: {data.get('label')}")
        print(f"     - Recommendations: {data.get('recommendations')}")
    else:
        print(f"  [ERROR] POST /api/sandbox/predict -> FAILED ({res.status_code})")
        success = False

    # 6. Test Model Engine API (Read-only API lock checks)
    print("\n[INFO] Testing Model Engine Configuration Endpoint...")
    res = client.get("/api/model/engine")
    if res.status_code == 200:
        data = res.get_json()
        print(f"  [OK] GET /api/model/engine -> 200 OK (Engine: {data.get('model_engine_name')})")
    else:
        print(f"  [ERROR] GET /api/model/engine -> FAILED ({res.status_code})")
        success = False

    # 7. Test Alerts Configuration Endpoint
    print("\n[INFO] Testing SLA Alerts Config Endpoint...")
    res = client.get("/api/alerts/config")
    if res.status_code == 200:
        print(f"  [OK] GET /api/alerts/config -> 200 OK")
        # Save updates
        save_data = {
            "slack_webhook_url": "https://hooks.slack.com/services/test/web",
            "alert_email_recipient": "csm@company.com"
        }
        res2 = client.post("/api/alerts/config?role=executive", data=json.dumps(save_data), content_type="application/json")
        if res2.status_code == 200:
            print("  [OK] POST /api/alerts/config -> 200 OK (Successfully saved configurations)")
        else:
            print(f"  [ERROR] POST /api/alerts/config -> FAILED ({res2.status_code})")
            success = False
    else:
        print(f"  [ERROR] GET /api/alerts/config -> FAILED ({res.status_code})")
        success = False

    # 8. Test Compliance Audit Logs Endpoints
    print("\n[INFO] Testing Compliance Reporting & Audit Logs Endpoint...")
    res = client.get("/api/compliance/audit/logs")
    if res.status_code == 200:
        data = res.get_json()
        print(f"  [OK] GET /api/compliance/audit/logs -> 200 OK (Fetched {len(data.get('logs', []))} audit events)")
    else:
        print(f"  [ERROR] GET /api/compliance/audit/logs -> FAILED ({res.status_code})")
        success = False

    res = client.get("/api/compliance/audit/export?role=manager")
    if res.status_code == 200:
        print(f"  [OK] GET /api/compliance/audit/export -> 200 OK (Mimetype: {res.mimetype})")
    else:
        print(f"  [ERROR] GET /api/compliance/audit/export -> FAILED ({res.status_code})")
        success = False

    # 9. Test NotebookLM Integration Notes Endpoints
    print("\n[INFO] Testing NotebookLM Corporate Extensions Endpoints...")
    res = client.get("/api/notes")
    if res.status_code == 200:
        print(f"  [OK] GET /api/notes -> 200 OK")
        # Save note
        note_data = {
            "title": "Verified Integration Note",
            "content": "A-to-Z sanity test successfully completed notes checklist."
        }
        res2 = client.post("/api/notes", data=json.dumps(note_data), content_type="application/json")
        if res2.status_code == 200:
            print("  [OK] POST /api/notes -> 200 OK (Note saved successfully)")
        else:
            print(f"  [ERROR] POST /api/notes -> FAILED ({res2.status_code})")
            success = False
    else:
        print(f"  [ERROR] GET /api/notes -> FAILED ({res.status_code})")
        success = False

    # 10. Test Presentation Slides Generation Engine
    print("\n[INFO] Testing PowerPoint Deck Compilation Engine...")
    pres_payload = {
        "num_slides": 5,
        "theme": "indigo",
        "font_pairing": "inter_mono",
        "transition": "fade",
        "custom_prompt": "Standard Corporate Retention Analysis",
        "presentation_title": "Enterprise Churn Review"
    }
    res = client.post("/api/presentation/generate", data=json.dumps(pres_payload), content_type="application/json")
    if res.status_code == 200:
        data = res.get_json()
        print(f"  [OK] POST /api/presentation/generate -> 200 OK (Generated {len(data.get('slides', []))} slides)")
    else:
        print(f"  [ERROR] POST /api/presentation/generate -> FAILED ({res.status_code})")
        success = False

    # 11. Test Custom Data Ingestion / CSV File Upload
    print("\n[INFO] Testing Custom CSV Dataset Ingestion Upload...")
    csv_content = (
        "customer_id,tenure_months,monthly_charges,support_tickets,customer_satisfaction_score,payment_delays,product_usage,complaint_count,churned\n"
        "CUST_99001,15,65.0,1,4,2,12.5,0,0\n"
        "CUST_99002,3,95.0,4,1,6,8.0,2,1\n"
    )
    res = client.post(
        "/api/upload",
        data={"file": (BytesIO(csv_content.encode("utf-8")), "custom_verification.csv")},
        content_type="multipart/form-data"
    )
    if res.status_code == 200:
        data = res.get_json()
        print(f"  [OK] POST /api/upload -> 200 OK (Ingested {data.get('rows')} rows, Warnings: {data.get('warnings')})")
    else:
        print(f"  [ERROR] POST /api/upload -> FAILED ({res.status_code}, Response: {res.get_data(as_text=True)})")
        success = False

    # 12. Test Copilot consultation session endpoint
    print("\n[INFO] Testing AI Advisor Copilot Session endpoint...")
    chat_payload = {"message": "Suggest customer retention strategies for customers experiencing billing payment delays."}
    res = client.post("/api/chat", data=json.dumps(chat_payload), content_type="application/json")
    if res.status_code == 200:
        data = res.get_json()
        print(f"  [OK] POST /api/chat -> 200 OK")
        print(f"     - Copilot Consultation response: \"{data.get('response')[:100]}...\"")
    else:
        print(f"  [ERROR] POST /api/chat -> FAILED ({res.status_code})")
        success = False

    print("\n======================================================================")
    if success:
        print("[SUCCESS] SUCCESS: ALL A-TO-Z ENDPOINTS AND WORKFLOW CHECKS PASSED 100%!")
    else:
        print("[FAILURE] FAILURE: ONE OR MORE ENDPOINTS RETURNED ERRORS during hard testing.")
    print("======================================================================\n")
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    run_atoz_verification()