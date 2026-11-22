import io
import zipfile
import xml.etree.ElementTree as ET
import pytest
import pandas as pd
from app import create_app
from tableau_exporter import (
    build_tableau_dataset,
    generate_tableau_twb_xml,
    generate_tableau_twbx_package,
    generate_tableau_fallback_package,
    validate_tableau_package,
    publish_to_tableau_server,
)


@pytest.fixture
def sample_df():
    return pd.DataFrame([
        {
            "customer_id": "CUST-001",
            "MonthlyCharges": 85.50,
            "predicted_probability": 0.82,
            "churned": 1,
            "tenure_months": 4,
            "region": "North America",
            "contract_type": "Month-to-month",
            "support_tickets": 3,
            "customer_satisfaction_score": 2.1
        },
        {
            "customer_id": "CUST-002",
            "MonthlyCharges": 45.00,
            "predicted_probability": 0.12,
            "churned": 0,
            "tenure_months": 36,
            "region": "Europe",
            "contract_type": "Two year",
            "support_tickets": 0,
            "customer_satisfaction_score": 4.8
        }
    ])


def test_build_tableau_dataset(sample_df):
    tab_df = build_tableau_dataset(sample_df)
    assert len(tab_df) == 2

    expected_cols = [
        "CustomerID", "CustomerName", "Date", "Segment", "Region",
        "ContractType", "Revenue", "ChurnScore", "ChurnRisk", "Churned",
        "TenureMonths", "SupportTickets", "CSAT", "PaymentDelayDays",
        "RiskTier", "RecommendedAction"
    ]
    for col in expected_cols:
        assert col in tab_df.columns, f"Missing column: {col}"

    assert tab_df["Churned"].dtype == bool
    assert tab_df["Revenue"].iloc[0] > 0
    assert tab_df["ChurnScore"].iloc[0] == 82.0


def test_generate_tableau_twb_xml(sample_df):
    tab_df = build_tableau_dataset(sample_df)
    twb_xml = generate_tableau_twb_xml(tab_df)

    # Valid XML test via ElementTree
    tree = ET.fromstring(twb_xml)
    assert tree.tag == "workbook"
    assert tree.attrib.get("version") == "2023.1"

    # Connection check
    conn = tree.find(".//connection")
    assert conn is not None
    assert conn.attrib.get("class") == "textscan"
    assert conn.attrib.get("directory") == "Data"
    assert conn.attrib.get("filename") == "CustomerIntelligence.csv"

    # Calculated fields check
    calcs = tree.findall(".//calculation")
    assert len(calcs) >= 3
    formulas = [c.attrib.get("formula", "") for c in calcs]
    assert any("Churned" in f for f in formulas)
    assert any("ChurnScore" in f for f in formulas)
    assert any("LOOKUP" in f for f in formulas)

    # Worksheets check
    worksheets = [ws.attrib.get("name") for ws in tree.findall(".//worksheet")]
    assert "KPI Revenue" in worksheets
    assert "KPI Churn" in worksheets
    assert "Revenue Trend" in worksheets
    assert "Churn by Segment" in worksheets
    assert "Risk Table" in worksheets
    assert "Region Bar" in worksheets

    # Dashboard check
    dashboard = tree.find(".//dashboard[@name='Executive Overview']")
    assert dashboard is not None
    size = dashboard.find("size")
    assert size is not None
    assert size.attrib.get("maxwidth") == "1200"
    assert size.attrib.get("maxheight") == "800"


def test_generate_tableau_twbx_package(sample_df):
    twbx_bytes = generate_tableau_twbx_package(sample_df)
    assert len(twbx_bytes) > 0
    assert twbx_bytes.startswith(b"PK")  # ZIP signature

    zf = zipfile.ZipFile(io.BytesIO(twbx_bytes), "r")
    names = set(zf.namelist())

    assert "workbook.twb" in names
    assert "Data/CustomerIntelligence.csv" in names
    assert "README.txt" in names

    # Validation checklist
    val = validate_tableau_package(twbx_bytes, len(sample_df))
    assert val.get("ok") is True, f"Validation failed: {val}"


def test_tableau_api_endpoints():
    app = create_app()
    client = app.test_client()

    # 1. Default .twbx export
    res_twbx = client.get("/api/export/tableau")
    assert res_twbx.status_code == 200
    assert res_twbx.content_type == "application/vnd.tableau.twbx"
    assert res_twbx.data.startswith(b"PK")
    assert "qiplo-tableau-" in res_twbx.headers.get("Content-Disposition", "")

    # 2. Raw .twb XML export
    res_twb = client.get("/api/export/tableau?type=twb")
    assert res_twb.status_code == 200
    assert "xml" in res_twb.content_type
    assert b"<workbook" in res_twb.data

    # 3. Fallback package export
    res_fallback = client.get("/api/export/tableau?type=fallback")
    assert res_fallback.status_code == 200
    assert res_fallback.data.startswith(b"PK")

    # 4. Status endpoint
    res_status = client.get("/api/export/tableau/status")
    assert res_status.status_code == 200
    assert "configured" in res_status.json

    # 5. REST publish failure handling
    res_publish = client.post("/api/export/tableau/publish")
    assert res_publish.status_code == 400
    p_data = res_publish.json
    assert p_data["ok"] is False
    assert "stage" in p_data
    assert "message" in p_data
    assert "fix" in p_data

    # 6. Preview telemetry API
    res_preview = client.get("/api/export/tableau/preview")
    assert res_preview.status_code == 200
    prev_data = res_preview.json
    assert prev_data["ok"] is True
    assert "kpis" in prev_data
    assert "calculated_fields" in prev_data
    assert len(prev_data["calculated_fields"]) == 3
    assert "worksheets" in prev_data
    assert len(prev_data["worksheets"]) == 6
    assert prev_data["dashboard"]["name"] == "Executive Overview"
