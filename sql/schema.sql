CREATE TABLE IF NOT EXISTS data_sources (
    source_id TEXT PRIMARY KEY,
    filename TEXT NOT NULL,
    row_count INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    is_active INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS customer_churn (
    customer_id TEXT PRIMARY KEY,
    source_id TEXT,
    tenure_months INTEGER,
    monthly_charges REAL,
    total_charges REAL,
    contract_type TEXT,
    internet_service TEXT,
    payment_method TEXT,
    region TEXT,
    support_tickets INTEGER,
    payment_delays INTEGER,
    product_usage REAL,
    complaint_count INTEGER,
    customer_satisfaction_score REAL,
    churned INTEGER
);

CREATE TABLE IF NOT EXISTS churn_predictions (
    customer_id TEXT PRIMARY KEY,
    predicted_probability REAL NOT NULL,
    prediction_label TEXT NOT NULL,
    risk_drivers TEXT DEFAULT '[]',
    ci_lower REAL DEFAULT 0.0,
    ci_upper REAL DEFAULT 0.0,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS user_notes (
    note_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS crm_integrations (
    integration_id TEXT PRIMARY KEY,
    platform TEXT NOT NULL,
    api_key TEXT,
    connected_at TEXT NOT NULL,
    status TEXT DEFAULT 'active'
);

CREATE TABLE IF NOT EXISTS risk_history (
    history_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id TEXT NOT NULL,
    predicted_probability REAL NOT NULL,
    prediction_label TEXT NOT NULL,
    recorded_date TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS audit_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_role TEXT NOT NULL,
    action TEXT NOT NULL,
    target_customer TEXT,
    timestamp TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS scheduled_reports (
    report_id TEXT PRIMARY KEY,
    recipient_email TEXT NOT NULL,
    frequency TEXT NOT NULL,
    format TEXT NOT NULL,
    last_sent TEXT
);

CREATE TABLE IF NOT EXISTS ab_tests (
    campaign_id INTEGER PRIMARY KEY AUTOINCREMENT,
    campaign_name TEXT NOT NULL,
    predicted_churn_rate REAL NOT NULL,
    actual_churn_rate REAL NOT NULL,
    sample_size INTEGER NOT NULL,
    outcome TEXT NOT NULL,
    start_date TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS account_assignments (
    customer_id TEXT PRIMARY KEY,
    csm_name TEXT,
    status TEXT DEFAULT 'unassigned',
    notes TEXT,
    last_updated TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS integrations_webhooks (
    webhook_id TEXT PRIMARY KEY,
    platform TEXT NOT NULL,
    webhook_url TEXT NOT NULL,
    is_active INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS email_templates (
    template_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    subject TEXT NOT NULL,
    body_html TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS email_campaigns (
    campaign_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    template_id TEXT NOT NULL,
    recipient_segment TEXT NOT NULL DEFAULT 'all',
    scheduled_at TEXT,
    sent_at TEXT,
    status TEXT DEFAULT 'draft',
    total_recipients INTEGER DEFAULT 0,
    sent_count INTEGER DEFAULT 0,
    opened_count INTEGER DEFAULT 0,
    clicked_count INTEGER DEFAULT 0,
    bounced_count INTEGER DEFAULT 0,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS email_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    campaign_id INTEGER NOT NULL,
    recipient_email TEXT NOT NULL,
    customer_id TEXT,
    subject TEXT NOT NULL,
    status TEXT DEFAULT 'queued',
    sent_at TEXT,
    opened_at TEXT,
    clicked_at TEXT,
    error_message TEXT,
    tracking_token TEXT UNIQUE,
    FOREIGN KEY (campaign_id) REFERENCES email_campaigns(campaign_id)
);
