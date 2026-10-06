# Surgical Implants Quality & Inventory Cost Optimization
## IIT Madras BS in Data Science & Applications — BDM Capstone Project

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Statistical Analysis](https://img.shields.io/badge/Stats-ANOVA%20%7C%20ARIMA%20%7C%20SPC-success.svg)](#-analytical-methodology--deep-dive)
[![Domain](https://img.shields.io/badge/Domain-Industrial%20Data%20Science%20%26%20Operations-orange.svg)](#-business-context--problem-architecture)
[![Dataset](https://img.shields.io/badge/Dataset-17%20Months%20(119%20Batches)-purple.svg)](#-dataset-architecture--data-governance)
[![Live Showcase](https://img.shields.io/badge/Web%20Showcase-Interactive%20Portfolio-green.svg)](Project_recruit_portfolio/index.html)

> **An End-to-End Primary Field Analytics & Operations Research Case Study** evaluating manufacturing non-conformance, resolving a ₹12.02 Lakhs Cost of Poor Quality (COPQ) paradox via One-Way ANOVA, and engineering dynamic ARIMA + EOQ + ROP inventory replenishment policies for an ISO/CE-certified medical equipment manufacturing firm.

---

## 📌 Executive Summary

Manufacturing high-precision surgical devices requires zero-defect reliability and tight inventory synchronicity. Over a 17-month observation period (January 2025 – May 2026), an **established Medical Equipment Firm** experienced rising product defect rates, untracked rework/scrap losses, and stockouts in high-volume SKUs.

By collecting and analyzing **119 batch-level production and inventory records** across **7 core orthopedic product lines**, this project engineered a 3-pillar data-driven intervention:

1. **Defect Reduction (Quality Engineering)**: Diagnosed 6 systemic failure modes using Root Cause Analysis (4M Ishikawa, 5-Whys) and Statistical Process Control ($X$-bar & $R$ charts).
2. **COPQ Financial Quantification (Cost Optimization)**: Disproved the assumption that defect frequency alone drives financial loss. Proved through **One-Way ANOVA ($F = 38.42, p = 1.48 \times 10^{-24}$)** that high unit-cost products dominate losses, with **Plaster Cutting Saws accounting for 62.2% (₹7.48 Lakhs)** of the total **₹12.02 Lakhs COPQ**, despite having a sub-1.0% defect rate.
3. **Inventory Restructuring (Supply Chain Analytics)**: Formulated an integrated **ABC–EOQ–ROP–Safety Stock** framework combined with **ARIMA(2,1,0) demand forecasting**, eliminating stockouts in fast-moving items (Bone Screws & Bone Plates) while reducing annual holding capital by 18.4%.

```
+----------------------------------------------------------------------------------------------------+
|                                    PROJECT IMPACT AT A GLANCE                                      |
+------------------------------------+----------------------------------+----------------------------+
| 💰 Financial Impact                | ⚙️ Quality Control                | 📦 Supply Chain Reliability|
| Quantified ₹12,02,530 hidden COPQ  | Established SPC UCL/LCL bounds   | Formulated EOQ + ROP buffer|
| Isolated 62.2% loss to 1 SKU       | Diagnosed 6 systemic failure modes| 0 stockout target achieved |
| ₹5.1L projected annual recovery    | UCL drift caught in early 2026   | 95% cycle service level    |
+------------------------------------+----------------------------------+----------------------------+
```

---

## 🏢 Business Context & Problem Architecture

The firm manufactures and supplies precision orthopedic implants and surgical instruments across 7 critical SKUs:

| Product SKU | Unit Cost (₹) | Avg Monthly Batch | Historical Defect Rate | Core Clinical Application |
| :--- | :---: | :---: | :---: | :--- |
| **Bone Plate** | ₹450 | 1,280 | 0.95% | Trauma & fracture internal fixation |
| **Bone Nibbler** | ₹2,500 | 1,280 | 0.96% | Bone trimming & contouring |
| **Plaster Cutting Saw** | ₹18,500 | 1,280 | 0.92% | Orthopedic cast removal |
| **Bone Screw** | ₹120 | 1,280 | 1.25% | Implant internal compression fixation |
| **Wire Cutter** | ₹3,000 | 1,280 | 1.26% | Surgical pin & wire extraction |
| **Intramedullary Nail** | ₹950 | 1,280 | 1.56% | Long-bone shaft fracture fixation |
| **Needle Holder** | ₹400 | 1,280 | 1.57% | Precision surgical suturing |

---

## 🔬 Dataset Architecture & Data Governance

Primary data was audited directly from physical registers, production batch cards, and store ledgers:

- **Temporal Coverage**: 17 Months (January 2025 – May 2026)
- **Granularity**: Monthly batch records per SKU ($17 \times 7 = 119$ observations)
- **Data Integrity**: 100% complete records with zero missing entries.
- **Privacy & Governance**: All legal entities, physical addresses, proprietary tool IDs, and client hospital identities have been strictly anonymized under NDA guidelines.

---

## 📊 Analytical Methodology & Deep Dive

### 1. Pillar 1: Root Cause Analysis & Statistical Process Control (SPC)
- **4M Ishikawa & 5-Whys**: Isolated tool wear concentricity runout ($>0.015\text{mm}$) on CNC collets and dry-running thermal expansion during setup.
- **SPC Limits ($n=7$)**:
  $$\text{UCL}_{\bar{X}} = \bar{\bar{X}} + A_2 \bar{R} = 20.03, \quad \text{LCL}_{\bar{X}} = 11.31, \quad \text{UCL}_R = D_4 \bar{R} = 20.03$$
  Early 2026 batches systematically breached $\text{UCL}$, confirming machine tool wear drift.

### 2. Pillar 2: Cost of Poor Quality (COPQ) & ANOVA Econometrics
- **COPQ Breakdown**: Total financial loss of **₹12,02,530** (₹7,73,810 rework, ₹4,28,720 scrap, 746 lost labor hours).
- **The Core Paradox**: Plaster Saw had the lowest defect rate (0.92%) but accounted for **62.2% of total COPQ (₹7.48 Lakhs)** due to its ₹18,500 unit cost.
- **One-Way ANOVA & FWER Defense**:
  $$F = \frac{\text{MS}_{\text{between}}}{\text{MS}_{\text{within}}} = 38.42 \quad (p = 1.48 \times 10^{-24})$$
  $$\text{FWER} = 1 - (1 - 0.05)^{21} \approx 65.9\%$$
  ANOVA successfully defended against severe Type I error inflation from 21 pairwise tests.

### 3. Pillar 3: Dynamic Supply Chain & Inventory Optimization
- **ABC Classification**: Stratified items by value velocity (Class A: Plaster Saw $\rightarrow$ 62.2% value; Class C: Bone Plates & Screws $\rightarrow$ high volume).
- **EOQ & Safety Stock Formulation**:
  $$\text{EOQ} = \sqrt{\frac{2 D S}{H}}, \quad \text{SS} = Z \cdot \sigma_{\text{daily}} \sqrt{L}, \quad \text{ROP} = (\bar{d} \cdot L) + \text{SS}$$
- **ARIMA(2,1,0) Demand Forecasting**: First-order differencing ($d=1$) captured growth momentum, overcoming 3-month rolling moving averages that lagged demand by 60 days and caused stockouts.

---

## 💻 Project Structure

```
├── Project_recruit_portfolio/             # Interactive Recruiter Showcase Suite
│   ├── index.html                         # Interactive Showcase Web App
│   ├── style.css                          # Dark/Light Slate Editorial Design System
│   ├── app.js                             # Simulators, Data Grid, AI Chatbot & Math Engine
│   ├── Medical_Device_Analytics_Workbook.xlsx # 119-Record Primary Dataset & Models
│   ├── medical_device_analysis_pipeline.py    # Complete Python 3 Statistical Pipeline
│   ├── medical_device_charts_notebook.ipynb   # Jupyter / Google Colab Reproduction Notebook
│   ├── chart1_monthly_defect_rate.png     # Figure 1: Defect Rate Trend
│   ├── chart2_defect_rate_by_product.png  # Figure 2: SKU Defect Rates
│   ├── chart3_pareto_rejection.png        # Figure 3: Defect Reason Pareto
│   ├── chart4_monthly_copq.png            # Figure 4: Monthly COPQ Stacked
│   ├── chart5_copq_by_product.png         # Figure 5: Product COPQ (62.2% Plaster Saw)
│   ├── chart6_sales_trend.png             # Figure 6: Upward Sales Trajectory
│   ├── chart7_inventory_stock.png         # Figure 7: Stockout Incidents vs Safety Buffer
│   ├── songs/                             # Background Score Audio Collection
│   ├── PROJECT_MASTER_WALKTHROUGH.md      # Comprehensive Recruiter Technical Walkthrough
│   ├── RESUME_AND_INTERVIEW_GUIDE.md      # Bullet Points & Defense Q&A for Interviews
│   └── HOW_TO_SHOWCASE_TO_RECRUITERS.md   # Presentation Strategy & Pitch Deck Guide
└── README.md                              # Main GitHub Landing Page
```

---

## 🚀 Quick Start & Reproduction

```bash
# 1. Clone repository
git clone https://github.com/iitmkushal2506/iitm_BDM_capstone_project.git
cd iitm_BDM_capstone_project

# 2. Run Python statistical pipeline
python Project_recruit_portfolio/medical_device_analysis_pipeline.py

# 3. Launch the live interactive recruiter web application
python -m http.server 8080 --directory Project_recruit_portfolio
```

Visit **`http://localhost:8080/index.html`** in your browser.

---

## 👤 Author & Credentials

- **Lead Analyst**: **Kushal Batra**
- **Degree Program**: Candidate, BS in Data Science & Applications — **IIT Madras** (Roll: `24f2000859`)
- **Email**: [24f2000859@ds.study.iitm.ac.in](mailto:24f2000859@ds.study.iitm.ac.in)
- **LinkedIn**: [linkedin.com/in/kushal-batra-615a793a2](https://www.linkedin.com/in/kushal-batra-615a793a2/)
- **GitHub**: [github.com/iitmkushal2506/iitm_BDM_capstone_project](https://github.com/iitmkushal2506/iitm_BDM_capstone_project)

---
*Developed as part of the Business Data Management (BDM) Capstone Project, Indian Institute of Technology Madras (IIT Madras).*
