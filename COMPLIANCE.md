# Qiplo Privacy-by-Design, Security & Deployment Guide

This document outlines Qiplo's technical design, privacy-first data flow, and on-premises security controls. Qiplo is built to assist engineering and data teams in adhering to security best practices and compliance frameworks.

---

## 🇪🇺 1. GDPR & CCPA Data Sovereignty Readiness
Qiplo is architected to operate strictly as an **On-Premises / Self-Hosted Data Processor**.

- **Local Isolation**: Customer data never leaves your environment. All model training and predictions run locally inside the host SQLite database.
- **Data Minimization**: The analytical pipeline requires no personal customer identifiers (names, emails, SSNs are ignored). It is designed to work solely on anonymized cohort keys.
- **Permanent Purges (Right to Erasure / Article 17)**: The "Delete Source" interface triggers a cascading SQL purge, deleting all corresponding rows, predictive outputs, and activity logs instantly from the SQLite database file.

---

## 🔒 2. Enterprise Host Security Alignment (SOC 2 & ISO 27001)
As a self-hosted platform, Qiplo provides tooling to align your deployment with security protocols:

- **IP Masking & Network Segregation**: To shield host servers from IP leaks during outbound AI queries, Qiplo includes a managed **Proxy Pool Manager** (configured in the *Settings* dashboard) supporting SOCKS5 and HTTP/HTTPS authenticated gateways.
- **Transport Security**: All API routes and client interfaces are bound to local or containerized HTTPS port mappings.
- **Database Hardening**: Developers can configure the SQLite database files to use SQLCipher or block-level cloud volume encryption.

---

## 🏥 3. HIPAA Protected Health Information (PHI) De-identification
For healthcare retention use-cases:

- **Identifier Hashing**: If source CSV or Excel files lack a dedicated customer key, the data importer automatically maps records to generalized hashes (`CUST_00001`, `CUST_00002`) and drops original names. This aligns your storage pattern with HIPAA's Safe Harbor de-identification rules.

---

## ⚖️ 4. MIT Licensing & Commercial Usage
Qiplo is distributed under the permissive **MIT License**. It is 100% free and open-source for public, private, academic, commercial, and enterprise-wide application without hidden licensing costs or royalties.
