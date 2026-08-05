import os
import re
import smtplib
import ssl
import threading
import time
import uuid
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from pathlib import Path
from typing import Optional

import sqlite3


BASE_DIR = Path(__file__).resolve().parent
TRACKING_DOMAIN = os.environ.get("TRACKING_DOMAIN", "http://localhost:5000")


def get_db_path() -> Path:
    if "CHURN_DB" in os.environ:
        return Path(os.environ["CHURN_DB"])
    return BASE_DIR / "churn_analysis.db"


def get_connection() -> sqlite3.Connection:
    db_p = get_db_path()
    conn = sqlite3.connect(db_p, timeout=30.0)
    conn.row_factory = sqlite3.Row
    return conn


def generate_tracking_token() -> str:
    return uuid.uuid4().hex + uuid.uuid4().hex[:8]


def render_template_html(template_body: str, customer: dict, company_name: str = "Qiplo Analytics") -> str:
    body = template_body
    body = re.sub(r"\{\{customer_name\}\}", customer.get("customer_name", "Valued Customer"), body, flags=re.IGNORECASE)
    body = re.sub(r"\{\{company_name\}\}", company_name, body, flags=re.IGNORECASE)
    body = re.sub(r"\{\{risk_label\}\}", customer.get("prediction_label", "stable").replace("_", " ").title(), body, flags=re.IGNORECASE)
    body = re.sub(r"\{\{risk_score\}\}", f"{round((customer.get('predicted_probability') or 0) * 100, 1)}%", body, flags=re.IGNORECASE)
    body = re.sub(r"\{\{contract_type\}\}", customer.get("contract_type", "N/A"), body, flags=re.IGNORECASE)
    body = re.sub(r"\{\{monthly_charges\}\}", f"${customer.get('monthly_charges', 0):.2f}", body, flags=re.IGNORECASE)
    body = re.sub(r"\{\{tenure_months\}\}", str(customer.get("tenure_months", "N/A")), body, flags=re.IGNORECASE)
    body = re.sub(r"\{\{support_tickets\}\}", str(customer.get("support_tickets", 0)), body, flags=re.IGNORECASE)
    body = re.sub(r"\{\{customer_id\}\}", str(customer.get("customer_id", "")), body, flags=re.IGNORECASE)
    return body


def get_smtp_config() -> Optional[dict]:
    return {
        "host": os.environ.get("SMTP_HOST", ""),
        "port": int(os.environ.get("SMTP_PORT", 587)),
        "username": os.environ.get("SMTP_USERNAME", ""),
        "password": os.environ.get("SMTP_PASSWORD", ""),
        "from_email": os.environ.get("SMTP_FROM_EMAIL", ""),
        "from_name": os.environ.get("SMTP_FROM_NAME", "Qiplo Analytics"),
    }


def get_recipients_for_segment(segment: str) -> list:
    conn = get_connection()
    cursor = conn.cursor()
    if segment == "high_risk":
        rows = cursor.execute("""
            SELECT cp.customer_id, cp.predicted_probability, cp.prediction_label,
                   cc.monthly_charges, cc.contract_type, cc.tenure_months,
                   cc.support_tickets, cc.payment_delays
            FROM churn_predictions cp
            LEFT JOIN customer_churn cc ON cp.customer_id = cc.customer_id
            JOIN data_sources ds ON cc.source_id = ds.source_id
            WHERE ds.is_active = 1 AND cp.prediction_label = 'high_risk'
            ORDER BY cp.predicted_probability DESC
        """).fetchall()
    elif segment == "low_risk":
        rows = cursor.execute("""
            SELECT cp.customer_id, cp.predicted_probability, cp.prediction_label,
                   cc.monthly_charges, cc.contract_type, cc.tenure_months,
                   cc.support_tickets, cc.payment_delays
            FROM churn_predictions cp
            LEFT JOIN customer_churn cc ON cp.customer_id = cc.customer_id
            JOIN data_sources ds ON cc.source_id = ds.source_id
            WHERE ds.is_active = 1 AND cp.prediction_label = 'low_risk'
            ORDER BY cp.predicted_probability DESC
        """).fetchall()
    else:
        rows = cursor.execute("""
            SELECT cp.customer_id, cp.predicted_probability, cp.prediction_label,
                   cc.monthly_charges, cc.contract_type, cc.tenure_months,
                   cc.support_tickets, cc.payment_delays
            FROM churn_predictions cp
            LEFT JOIN customer_churn cc ON cp.customer_id = cc.customer_id
            JOIN data_sources ds ON cc.source_id = ds.source_id
            WHERE ds.is_active = 1
            ORDER BY cp.predicted_probability DESC
        """).fetchall()
    conn.close()
    result = []
    for r in rows:
        result.append({
            "customer_id": r["customer_id"],
            "predicted_probability": r["predicted_probability"] or 0,
            "prediction_label": r["prediction_label"] or "low_risk",
            "monthly_charges": r["monthly_charges"] or 0,
            "contract_type": r["contract_type"] or "N/A",
            "tenure_months": r["tenure_months"] or 0,
            "support_tickets": r["support_tickets"] or 0,
            "payment_delays": r["payment_delays"] or 0,
            "email": f"{r['customer_id'].lower()}@example.com",
        })
    return result


def send_single_email(smtp_config: dict, recipient_email: str, subject: str, html_body: str, tracking_token: str, company_name: str) -> tuple:
    try:
        msg = MIMEMultipart("related")
        msg["Subject"] = subject
        msg["From"] = f"{smtp_config['from_name']} <{smtp_config['from_email']}>"
        msg["To"] = recipient_email

        alt = MIMEMultipart("alternative")
        msg.attach(alt)

        text_body = re.sub(r"<[^>]+>", "", html_body)
        alt.attach(MIMEText(text_body, "plain"))

        combined_html = html_body
        tracking_pixel_url = f"{TRACKING_DOMAIN}/api/email/track/open/{tracking_token}"
        pixel_html = f'<img src="{tracking_pixel_url}" width="1" height="1" alt="" style="display:none;" />'
        combined_html += pixel_html
        alt.attach(MIMEText(combined_html, "html"))

        context = ssl._create_unverified_context()
        with smtplib.SMTP(smtp_config["host"], smtp_config["port"]) as server:
            server.starttls(context=context)
            server.login(smtp_config["username"], smtp_config["password"])
            server.send_message(msg)

        return True, None
    except Exception as e:
        return False, str(e)


def send_campaign_emails(campaign_id: int, recipients: list, template_subject: str, template_body: str, company_name: str = "Qiplo Analytics"):
    smtp_config = get_smtp_config()
    if not smtp_config["host"] or not smtp_config["from_email"]:
        conn = get_connection()
        conn.execute("UPDATE email_campaigns SET status = 'error' WHERE campaign_id = ?", (campaign_id,))
        conn.commit()
        conn.close()
        return

    conn = get_connection()
    now = datetime.now().isoformat()
    conn.execute("UPDATE email_campaigns SET status = 'sending', sent_at = ? WHERE campaign_id = ?", (now, campaign_id))
    conn.commit()

    batch_size = 10
    delay_seconds = 2

    for i in range(0, len(recipients), batch_size):
        batch = recipients[i:i + batch_size]
        for customer in batch:
            token = generate_tracking_token()
            personalized_subject = render_template_html(template_subject, customer, company_name)
            personalized_body = render_template_html(template_body, customer, company_name)

            log_id = None
            try:
                cursor = conn.execute(
                    "INSERT INTO email_logs (campaign_id, recipient_email, customer_id, subject, status, tracking_token) VALUES (?, ?, ?, ?, 'queued', ?)",
                    (campaign_id, customer["email"], customer.get("customer_id"), personalized_subject, token)
                )
                log_id = cursor.lastrowid
                conn.commit()
            except Exception:
                continue

            sent_ok, error_msg = send_single_email(smtp_config, customer["email"], personalized_subject, personalized_body, token, company_name)
            now = datetime.now().isoformat()
            if sent_ok:
                conn.execute("UPDATE email_logs SET status = 'sent', sent_at = ? WHERE log_id = ?", (now, log_id))
                conn.execute("UPDATE email_campaigns SET sent_count = sent_count + 1 WHERE campaign_id = ?", (campaign_id,))
            else:
                conn.execute("UPDATE email_logs SET status = 'failed', error_message = ? WHERE log_id = ?", (error_msg, log_id))
                conn.execute("UPDATE email_campaigns SET bounced_count = bounced_count + 1 WHERE campaign_id = ?", (campaign_id,))
            conn.commit()

        if i + batch_size < len(recipients):
            time.sleep(delay_seconds)

    conn.execute("UPDATE email_campaigns SET status = 'completed' WHERE campaign_id = ? AND status = 'sending'", (campaign_id,))
    conn.commit()
    conn.close()


def start_campaign_send(campaign_id: int, recipients: list, template_subject: str, template_body: str, company_name: str = "Qiplo Analytics"):
    thread = threading.Thread(
        target=send_campaign_emails,
        args=(campaign_id, recipients, template_subject, template_body, company_name),
        daemon=True
    )
    thread.start()
    return thread
