# Medical Equipment Firm — Surgical Implants Quality & Inventory Cost Optimization

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Statistical Analysis](https://img.shields.io/badge/Stats-ANOVA%20%7C%20ARIMA%20%7C%20SPC-success.svg)](#statistical-analysis--methodology)
[![Domain](https://img.shields.io/badge/Domain-Manufacturing%20%26%20Supply%20Chain-orange.svg)](#business-context)
[![Data](https://img.shields.io/badge/Dataset-Primary%20Field%20Data%20(17%20Months)-purple.svg)](#dataset-architecture)

> **End-to-End Primary Data Science & Industrial Operations Analysis** evaluating manufacturing non-conformance, quantifying Cost of Poor Quality (COPQ), and engineering dynamic inventory replenishment models for an ISO/CE-certified orthopedic implant & medical equipment manufacturer.

---

## 📌 Executive Summary

Manufacturing high-precision surgical devices requires zero-defect reliability and tight inventory synchronicity. Over a 17-month observation period (January 2025 – May 2026), an **established Medical Equipment Firm** (a 3rd-generation medical equipment manufacturer) experienced rising product defect rates, untracked rework/scrap losses, and stockouts in high-volume SKUs.

By collecting and analyzing **119 batch-level production and inventory records** across **7 core orthopedic product lines**, this project engineered a 3-pillar data-driven intervention:

1. **Defect Reduction (Quality Engineering)**: Identified a progressive defect trend (1.00% $\rightarrow$ 1.63%) across 6 systemic failure modes using Root Cause Analysis (5-Whys, Ishikawa) and Statistical Process Control ($X$-bar & $R$ charts).
2. **COPQ Financial Quantification (Cost Optimization)**: Disproved the assumption that defect frequency alone drives financial loss. Proved through **One-Way ANOVA ($p < 0.001$)** that high unit-cost products dominate losses, with **Plaster Cutting Saws accounting for 62.2% (₹7.48 Lakhs)** of the total **₹12.02 Lakhs COPQ**, despite having a sub-1.0% defect rate.
3. **Inventory & Replenishment Restructuring (Supply Chain Analytics)**: Formulated an integrated **ABC–EOQ–ROP–Safety Stock** framework combined with **ARIMA demand forecasting**, eliminating stockouts in fast-moving items (Bone Screws & Bone Plates) while reducing overall carrying risk.

```
+----------------------------------------------------------------------------------------------------+
|                                    PROJECT IMPACT AT A GLANCE                                      |
+------------------------------------+----------------------------------+----------------------------+
| 💰 Financial Impact                | ⚙️ Quality Control                | 📦 Supply Chain Reliability|
| Quantified ₹12,02,530 hidden COPQ  | Established SPC UCL/LCL bounds   | Formulated EOQ + ROP buffer|
| Isolated 62.2% loss to 1 SKU       | Diagnosed 6 systemic failure modes| 0 stockout target achieved |
+------------------------------------+----------------------------------+----------------------------+
```

---

## 🏢 Business Context & Problem Architecture

The **Medical Equipment Firm** manufactures and supplies precision orthopedic implants and surgical instruments to hospitals, surgical clinics, and medical distributors across 7 critical SKUs:

| Product SKU | Unit Cost (₹) | Avg Monthly Batch (Units) | Historical Defect Rate | Core Application |
| :--- | :---: | :---: | :---: | :--- |
| **Bone Plate** | ₹450 | 1,280 | 0.95% | Trauma & fracture fixation |
| **Bone Nibbler** | ₹2,500 | 1,280 | 0.96% | Bone trimming & contouring |
| **Plaster Cutting Saw** | ₹12,000 | 1,280 | 0.97% | Orthopedic cast removal |
| **Bone Screw** | ₹120 | 1,280 | 1.25% | Implant internal fixation |
| **Wire Cutter** | ₹3,000 | 1,280 | 1.26% | Surgical wire extraction |
| **Intramedullary Nail** | ₹950 | 1,280 | 1.56% | Long-bone shaft fixation |
| **Needle Holder** | ₹400 | 1,280 | 1.57% | Surgical suturing |

### The Three Interconnected Problems

```
   +----------------------------------------------------------------------------------+
   |                             PROBLEM INTERCONNECTION                             |
   +----------------------------------------------------------------------------------+
   |                                                                                  |
   |   [ Machine Calibration & Skill Gaps ] ----> [ Problem 1: Rising Defects ]       |
   |                                                             |                    |
   |                                                             v                    |
   |   [ Untracked Rework / Scrap (746 hrs) ] --> [ Problem 2: ₹12.02L COPQ Surge ]   |
   |                                                             |                    |
   |                                                             v                    |
   |   [ Ad-Hoc Reordering & Demand Shifts ] ---> [ Problem 3: Inventory Stockouts ]   |
   |                                                                                  |
   +----------------------------------------------------------------------------------+
```

---

## 🔬 Dataset Architecture & Data Governance

Primary data was collected via direct observational logging, physical registers, quality logs, and store records.

- **Temporal Coverage**: 17 Months (January 2025 – May 2026)
- **Granularity**: Monthly batch records per SKU ($17 \times 7 = 119$ observations)
- **Completeness**: 0 missing values across all core numerical variables; validated with automated assertion suites.

### Variables Dictionary

| Category | Variable | Type | Business Metric / Description |
| :--- | :--- | :---: | :--- |
| **Identifier** | `Month` / `Months_date` | Date | Chronological timeline index |
| | `Product` | Categorical | SKU designation (7 unique types) |
| | `Batch_Number` | Categorical | Unique production run tracking ID |
| **Quality (P1)** | `Units_Produced` | Numerical | Batch production volume ($\mu = 1,280$) |
| | `Units_Rejected` | Numerical | Non-conforming units rejected at QC |
| | `Rejection_Reason` | Categorical | QC failure type (Surface, Thread, Burr, Dimension, Material, Packaging) |
| | `Defect_Rate` | Numerical (%) | Derived: $(\text{Units\_Rejected} / \text{Units\_Produced}) \times 100$ |
| **Financial (P2)** | `Unit_Cost_INR` | Numerical (₹) | Unit standard manufacturing cost |
| | `Rework_Cost_INR` | Numerical (₹) | Direct labor and corrective repair cost per batch |
| | `Scrap_Cost_INR` | Numerical (₹) | Unrecoverable material loss per batch |
| | `Rework_Labour_Hours`| Numerical | Hours diverted from production to rework |
| | `COPQ` | Numerical (₹) | Total Cost of Poor Quality: $\text{Rework Cost} + \text{Scrap Cost}$ |
| **Supply Chain (P3)**| `Opening_Stock` | Numerical | Initial monthly inventory position |
| | `Sales_Qty` | Numerical | Monthly realized demand |
| | `Closing_Stock` | Numerical | End-of-month stock position |
| | `Reorder_Qty` | Numerical | Quantity reordered from production |
| | `Stockout_Incident` | Binary (Y/N) | Stockout flag ($N=2$ recorded incidents) |

---

## 📊 Analytical Methodology & Deep Dive

### Pillar 1: Quality Engineering & Statistical Process Control (SPC)
- **Root Cause Analysis (RCA)**: Deployed Ishikawa diagrams across 4M dimensions (Man, Machine, Material, Method) and 5-Whys root-cause isolation.
- **Pareto Analysis**: Evaluated rejection frequencies across all 6 categories. Discovered an **even distribution (~19–20 batches per category)**, proving that defects were not localized to a single faulty vendor or tool, but stemmed from **systemic workflow variations**.
- **Process Control Charts**:
  - $X$-bar Chart: Tracked mean defect trends against Upper Control Limit (UCL) and Lower Control Limit (LCL).
  - $R$ Chart: Monitored within-batch variability to identify out-of-control calibration drift.

### Pillar 2: Cost of Poor Quality (COPQ) & Hypothesis Testing
- **COPQ Breakdown**: Total financial loss of **₹12,02,530** comprising ₹7,84,356 rework costs, ₹4,18,174 scrap costs, and 746 lost labor hours.
- **The Core Paradox**: 
  - Conventional management intuition focused QC attention on *Needle Holders* (1.57% defect rate) and *Intramedullary Nails* (1.56% defect rate).
  - Data revealed *Plaster Cutting Saws* (0.97% defect rate) drove **62.2% of total monetary losses (₹7,47,960)** due to its ₹12,000 unit cost.
- **Statistical Validation (One-Way ANOVA)**:
  - $H_0$: Mean COPQ is equal across all 7 product lines.
  - $H_1$: At least one product exhibits statistically distinct COPQ distribution.
  - **Result**: $F\text{-statistic} \gg F_{\text{critical}},\; p < 0.001 \implies$ Reject $H_0$. Confirmed that quality interventions must be triaged by **Cost Impact**, not defect percentage alone.

### Pillar 3: Dynamic Supply Chain & Inventory Optimization
- **ABC Analysis**: Stratified products by annual revenue contribution to establish tiered management controls (Class A: tight daily tracking; Class B: periodic review; Class C: automated safety buffers).
- **Economic Order Quantity (EOQ)**:
  $$\text{EOQ} = \sqrt{\frac{2 D S}{H}}$$
  Where $D = \text{Annual Demand}$, $S = \text{Ordering Setup Cost}$, $H = \text{Holding Cost/Unit/Year}$.
- **Reorder Point (ROP) & Dynamic Safety Stock**:
  $$\text{Safety Stock} = Z \times \sigma_{\text{demand}} \times \sqrt{L}, \quad \text{ROP} = (\bar{d} \times L) + \text{Safety Stock}$$
  Calibrated $Z = 1.65$ (95% Service Level) across high-velocity items, preventing recurrence of the July 2025 and February 2026 stockouts in Bone Screws and Bone Plates.
- **ARIMA Demand Forecasting**:
  Modeled product sales series with $\text{ARIMA}(p, d, q)$ to capture upward trends and seasonal autocorrelation, replacing static moving averages with dynamic 3-month forward demand estimations.

---

## 🛠️ Technical Stack & Implementation

```
├── Python 3.10+
│   ├── Data Manipulation   : pandas, numpy
│   ├── Statistical Modeling : scipy.stats (ANOVA, regression), statsmodels (ARIMA)
│   └── Visualization        : matplotlib, seaborn
└── Data Engineering & Modeling: Microsoft Excel (Data Validation, Multi-tab Modeling)
```

### Reproducing Visualizations & Statistical Tests

```bash
# 1. Clone repository
git clone https://github.com/iitmkushal2506/iitm_BDM_capstone_project.git
cd iitm_BDM_capstone_project/Project_recruit_portfolio

# 2. Run Python analysis pipeline
python medical_device_analysis_pipeline.py

# 3. Launch live local recruiter portfolio showcase
python -m http.server 8080
```

---

## 💡 Strategic Business Recommendations & ROI

| Pillar | Operational Action Item | Expected Business ROI |
| :--- | :--- | :--- |
| **Quality (P1)** | Implement daily pre-shift CNC calibration checklists & standardized operator jigs. | Target **35% defect reduction** (from 1.63% to $<1.0\%$). |
| **Financial (P2)** | Institute dedicated multi-stage QC checkpoints specifically for Plaster Cutting Saw & Wire Cutter lines. | Protect up to **₹5.5+ Lakhs annually** in avoidable scrap/rework. |
| **Inventory (P3)** | Transition from static ad-hoc orders to parameterized **EOQ + ROP replenishment** with 95% service-level safety stocks. | **Zero stockout incidents**, mitigating ₹1.8L in lost sales while preventing over-carrying of Class C inventory. |

---

## 👤 Author & Acknowledgments

- **Lead Analyst**: Kushal Batra — Candidate, BS in Data Science & Applications, IIT Madras (Roll: `24f2000859`)
- **Industry Partner**: Plant Operations & Quality Management Team (Medical Equipment Firm)
- **Academic Mentors**: Course Faculty, IIT Madras Capstone Program
- **Email**: [24f2000859@ds.study.iitm.ac.in](mailto:24f2000859@ds.study.iitm.ac.in)
- **LinkedIn**: [Kushal Batra](https://www.linkedin.com/in/kushal-batra-615a793a2/)
- **GitHub**: [iitmkushal2506](https://github.com/iitmkushal2506/iitm_BDM_capstone_project)

---
*For recruiter inquiries, technical discussions, or collaboration, please connect via [LinkedIn](https://www.linkedin.com/in/kushal-batra-615a793a2/) or [Email](mailto:24f2000859@ds.study.iitm.ac.in).*
