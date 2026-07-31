# Qiplo Enterprise Compliance, Security & Privacy Framework

This document outlines Qiplo's global compliance alignment, privacy-by-design architecture, and security controls, establishing a trusted environment for commercial and enterprise scale deployment.

---

## 🇪🇺 1. GDPR (General Data Protection Regulation) Compliance
Qiplo is designed to act primarily as a **Local Data Processor** or **Self-Hosted Data Controller**.

- **Data Minimization (Article 5(1)(c))**: All personal telemetry features are optional. The system operates on de-identified customer keys.
- **Right to Erasure / Right to be Forgotten (Article 17)**: Deleting any data source via the Qiplo interface instantly and permanently purges all associated customer records, notes, predictions, and metadata from the database files via strict cascade SQL transactions.
- **Local Isolation (Article 25)**: No PII (Personally Identifiable Information) is uploaded to remote clouds by default. All data remains securely housed within your self-hosted SQLite instance.

---

## 🇺🇸 2. CCPA (California Consumer Privacy Act) Compliance
Qiplo supports all data sovereignty and consumer privacy rights:

- **No Sale of Personal Data**: Qiplo does not collect, monitor, monetize, or sell customer database records.
- **Access & Deletion Controls**: Users retain 100% control over their database files and can view, export, or delete records in real-time.

---

## 🔒 3. SOC2 Type II & ISO 27001 Readiness
For global cloud and enterprise software installations:

- **Network Segregation & Outbound Controls**: Outbound AI chat or search queries can be routed through a managed, authenticated **proxy pool** (configured in the *Settings* tab) to prevent direct IP leakage.
- **Encryption at Rest**: SQLite databases (`.db` files) can be encrypted using SQLCipher or standard block-level host encryption.
- **Encryption in Transit**: All endpoints enforce HTTPS protocols.

---

## 🏥 4. HIPAA (Health Insurance Portability and Accountability Act) Compliance
For healthcare analytics integrations:

- **PHI De-identification**: Qiplo's data importer automatically replaces original customer/account names with randomized identifier hashes (`CUST_XXXXX`) to prevent the exposure of Protected Health Information (PHI).

---

## ⚖️ 5. Global Export & Open Source License
Qiplo is distributed under the **MIT License**—permitting free, unrestricted modification, private use, distribution, and commercial reuse worldwide without licensing liabilities.
