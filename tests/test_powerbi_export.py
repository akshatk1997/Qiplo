import io
import json
import zipfile
import pytest
import pandas as pd
from app import create_app
from powerbi_exporter import (
    build_star_schema,
    generate_powerbi_pbip_package,
    generate_fallback_package,
    generate_pbit_bytes,
    validate_powerbi_package,
    generate_theme_json,
    generate_dax_measures_text
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
            "payment_method": "Electronic check",
            "support_tickets": 3,
            "customer_satisfaction_score": 2.1
        },
        {
            "customer_id": "CUST-002",
            "MonthlyCharges": 45.00,
            "predicted_probability": 0.12,
            "churned": 0,
            "tenure_months": 36,
            "region": "EMEA",
            "contract_type": "Two year",
            "payment_method": "Credit card",
            "support_tickets": 0,
            "customer_satisfaction_score": 4.8
        }
    ])


def test_build_star_schema(sample_df):
    tables = build_star_schema(sample_df)
    assert "Fact" in tables
    assert "Customer" in tables
    assert "Date" in tables
    assert "Product" in tables
    assert "Region" in tables

    fact = tables["Fact"]
    cust = tables["Customer"]
    date_df = tables["Date"]
    prod = tables["Product"]
    reg = tables["Region"]

    # Check row counts
    assert len(fact) == len(sample_df)
    assert len(cust) == len(sample_df)

    # Check keys & relationships
    assert set(fact["CustomerID"]).issubset(set(cust["CustomerID"]))
    assert set(fact["Date"]).issubset(set(date_df["Date"]))
    assert set(fact["ProductID"]).issubset(set(prod["ProductID"]))
    assert set(fact["RegionID"]).issubset(set(reg["RegionID"]))

    # Check non-null keys
    assert not fact["CustomerID"].isnull().any()
    assert not fact["Date"].isnull().any()
    assert not fact["ProductID"].isnull().any()
    assert not fact["RegionID"].isnull().any()

    # Check required DAX measure fields
    assert "Revenue" in fact.columns
    assert "ChurnScore" in fact.columns
    assert "ChurnRisk" in fact.columns
    assert "Churned" in fact.columns


def test_generate_powerbi_pbip_package(sample_df):
    pkg_bytes = generate_powerbi_pbip_package(sample_df)
    assert pkg_bytes.startswith(b"PK")

    val = validate_powerbi_package(pkg_bytes, len(sample_df))
    assert val["ok"] is True

    z = zipfile.ZipFile(io.BytesIO(pkg_bytes), "r")
    names = z.namelist()

    # Checklist validation
    assert "QiploAnalytics.pbip" in names
    assert "QiploAnalytics.pbit" in names
    assert "data/Fact.csv" in names
    assert "data/DimCustomer.csv" in names
    assert "data/DimDate.csv" in names
    assert "data/DimProduct.csv" in names
    assert "data/DimRegion.csv" in names
    assert "QiploAnalytics.SemanticModel/definition.pbism" in names
    assert "QiploAnalytics.SemanticModel/model.bim" in names
    assert "QiploAnalytics.Report/definition.pbir" in names
    assert "QiploAnalytics.Report/report.json" in names
    assert "theme/qiplo-theme.json" in names
    assert "measures.dax" in names
    assert "README.txt" in names

    # TMDL files exist
    assert "QiploAnalytics.SemanticModel/definition/database.tmdl" in names
    assert "QiploAnalytics.SemanticModel/definition/model.tmdl" in names
    assert "QiploAnalytics.SemanticModel/definition/relationships.tmdl" in names
    assert "QiploAnalytics.SemanticModel/definition/tables/Fact.tmdl" in names

    # CSV has UTF-8 BOM
    fact_bytes = z.read("data/Fact.csv")
    assert fact_bytes.startswith(b"\xef\xbb\xbf")

    # DAX measures check
    dax_text = z.read("measures.dax").decode("utf-8")
    assert "Total Revenue = SUM(Fact[Revenue])" in dax_text
    assert "Customers = DISTINCTCOUNT(Fact[CustomerID])" in dax_text
    assert "Churn Rate = DIVIDE(CALCULATE(COUNTROWS(Fact), Fact[Churned]=TRUE()), COUNTROWS(Fact))" in dax_text
    assert "Revenue at Risk = CALCULATE([Total Revenue], Fact[ChurnRisk] >= 0.7)" in dax_text
    assert "Revenue MoM %" in dax_text
    assert "Revenue YTD = TOTALYTD([Total Revenue], 'Date'[Date])" in dax_text
    assert "Avg Churn Score = AVERAGE(Fact[ChurnScore])" in dax_text

    # Theme JSON is valid
    theme_obj = json.loads(z.read("theme/qiplo-theme.json").decode("utf-8"))
    assert "#00F5FF" in theme_obj["dataColors"]
    assert "#FF007F" in theme_obj["dataColors"]


def test_powerbi_api_endpoints():
    app = create_app()
    client = app.test_client()

    # 1. Default PBIP export
    res_default = client.get("/api/export/powerbi")
    assert res_default.status_code == 200
    assert res_default.content_type == "application/zip"
    assert res_default.data.startswith(b"PK")
    assert "qiplo-powerbi-" in res_default.headers.get("Content-Disposition", "")

    # 2. PBIDS export
    res_pbids = client.get("/api/export/powerbi?type=pbids")
    assert res_pbids.status_code == 200
    assert "json" in res_pbids.content_type
    assert b"connections" in res_pbids.data

    # 3. PBIT export
    res_pbit = client.get("/api/export/powerbi?type=pbit")
    assert res_pbit.status_code == 200
    assert res_pbit.data.startswith(b"PK")

    # 4. Fallback export
    res_fallback = client.get("/api/export/powerbi?type=fallback")
    assert res_fallback.status_code == 200
    assert res_fallback.data.startswith(b"PK")

    # 5. REST Status
    res_status = client.get("/api/export/powerbi/status")
    assert res_status.status_code == 200
    assert "configured" in res_status.json

    # 6. REST Push error structure
    res_push = client.post("/api/export/powerbi/push")
    assert res_push.status_code == 400
    data = res_push.json
    assert data["ok"] is False
    assert "stage" in data
    assert "message" in data
    assert "fix" in data
