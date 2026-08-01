from pathlib import Path
import sqlite3
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import churn_analysis


def test_train_and_predict(tmp_path):
    db_path = tmp_path / "test_churn.db"
    schema_path = Path(__file__).resolve().parents[1] / "sql" / "schema.sql"
    model_path = tmp_path / "model.pkl"

    churn_analysis.ensure_database(db_path, schema_path)
    result = churn_analysis.train_model(db_path, model_path)

    assert result["accuracy"] >= 0.5
    assert model_path.exists()

    conn = sqlite3.connect(db_path)
    count = conn.execute("SELECT COUNT(*) FROM churn_predictions").fetchone()[0]
    conn.close()
    assert count > 0

def test_xgboost_pipeline(tmp_path):
    db_path = tmp_path / "test_xgb.db"
    schema_path = Path(__file__).resolve().parents[1] / "sql" / "schema.sql"
    model_path = tmp_path / "model_xgb.pkl"
    
    churn_analysis.ensure_database(db_path, schema_path)
    config = {"model_engine": "xgboost"}
    result = churn_analysis.train_model(db_path, model_path, config=config)
    
    assert result["accuracy"] >= 0.5
    assert model_path.exists()
    
    conn = sqlite3.connect(db_path)
    count = conn.execute("SELECT COUNT(*) FROM churn_predictions").fetchone()[0]
    conn.close()
    assert count > 0
