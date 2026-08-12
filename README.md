# Qiplo — Never Lose a Customer Again ⚡

> **"Business Decision Intelligence Platform"**

**Qiplo** is a 100% free, open-source, and claims-free Business Decision Intelligence Platform designed for high-growth enterprises and modern customer success teams. Powered by a custom state-of-the-art **Tabular Hybrid Attention Transformer Classifier**, Qiplo maps unstructured database inputs, identifies revenue-at-risk, and generates recovery playbooks with zero latency.

---

## 🌐 Live URLs & Links
* **Vercel Live Production App**: [https://qiplo.vercel.app](https://qiplo.vercel.app)
* **Official GitHub Repository**: [https://github.com/akshatk1997/Qiplo](https://github.com/akshatk1997/Qiplo)

---

## 🌟 Key Features & A to Z Dashboard Details

* **Business Decision Intelligence Modules**:
  Qiplo operates as a centralized decision suite, segmenting operations into four specialized core modules:
  * **Qiplo Finance (CashFlow)**: Evaluates outstanding Receivables, DSO collection delays, upcoming Payables commitments, and Working Capital cycle efficiency. Includes real-time DSO cash simulation.
  * **Qiplo Operations (Supply Chain)**: Evaluates Supplier Risk Score, regional safety stock Inventory Capital allocation, logistics delay offsets, and active line tool anomalies.
  * **Qiplo Sales (Revenue)**: Tracks ML-driven churn rate, monthly Revenue Leakage, next-month sales forecasting, and enterprise customer segments.
  * **Qiplo Product (Product)**: Tracks week-over-week user Retention Index, feature adoption rates, Day 7 funnel attrition, and RICE feature backlog prioritization.

* **Real-time Telemetry Synchronization Engine (`reloadData()`)**:
  Features a header sync control that refreshes all dashboard calculations dynamically without hard reload caching. It automatically uses column alias resolution helpers (`getRowCharges`, `getRowTickets`, `getRowUsage`) to scan arbitrary client uploads for synonyms (such as `adr` in travel data or `spend` in financial records), ensuring exact real-time calculations.

* **Enhanced Executive Analysis Audit Report**:
  Generates a print-optimized, multi-page HTML audit report. Incorporates:
  1. Detailed tables for **Regional Churn Risk Concentrations** and **Billing/Payment Method Exposure**.
  2. Financial risk mitigation forecasts mapping out 15% (Tactical CSM), 30% (Migration Offer), and 50% (VIP Onboarding) retention recovery scenarios.
  3. Interactive Visual Analytics curves matching the active database profiles.

* **SOTA Tabular Hybrid Attention Transformer Classifier**:
  Qiplo features a custom self-attention classification architecture built in NumPy that uses scale projections to capture inter-feature correlations dynamically:
  $$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$
  Optimized for tabular customer parameters (tenure, charges, support tickets, CSAT, billing delays), it operates as the absolute single-source classifier engine.
  
* **Interactive What-If Simulation Sandbox**:
  A professional playground allowing customer success managers to adjust account sliders (billing, support tickets, CSAT, complaints) and observe simulated churn risk changes in real time, accompanied by an interactive SVG circular risk dial and prescriptive recovery recipes.

* **Smart PowerPoint & HTML Slide Deck Builder**:
  Generates fully styled slideshow presentation decks from active analytics datasets, customizable by theme colors, typography pairings, and layout counts. Includes standard PowerPoint (`.pptx`) deck downloads.

* **Client-Side Text-To-Speech Audio Narration**:
  Features a built-in vocal player inside the slides dashboard utilizing the browser's native HTML5 `SpeechSynthesis` Web API to read slide summaries, bullets, and playbook steps with professional pacing.

* **Passcode-Free Instant Role Switcher**:
  Bypasses passcode dialog prompts entirely, allowing instant navigation across `EXECUTIVE`, `MANAGER`, `SALES`, and `SUPPORT` permission layers.

* **High-Performance Dark Mode**:
  Replaced heavy backdrop-filter blur rendering layers with paint-optimized solid surface overlays to eliminate browser repaint lags and maximize frame rates in dark mode.

* **Secure Gated Seeding & Fresh Production State**:
  Gates mock dataset seeding to testing environments (`pytest` or `TESTING=True` contexts). On standard production runs, it initializes with a completely fresh, empty database.

---

## 🚀 Quick Setup & Installation

### 1. Install dependencies
```bash
# Clone the repository
git clone https://github.com/akshatk1997/Qiplo.git
cd Qiplo

# Install requirements
pip install -r requirements.txt
```

### 2. Run local web server
```bash
python app.py
```
Open **http://127.0.0.1:5000/** in your browser.

---

## 🧪 Automated Testing & Verifications

Qiplo includes an end-to-end integration verifier and a complete pytest suite.

### Run A-to-Z Integration Verifications
Simulates user sessions over all endpoints:
```bash
python verify.py
```

### Run Pytest Suite
Runs all 21 automated validation test cases:
```bash
pytest
```

---

## 📄 License & Credits
Released under the permissive **[MIT License](LICENSE)**.

Developed by **Akshat Kumar** and pairs. Confidentially compiled for enterprise customer success alignment.
