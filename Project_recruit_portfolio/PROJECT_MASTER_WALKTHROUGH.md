# 🧭 Master Guide: Project Breakdown & Recruiter Showcase Strategy

**Candidate:** Kushal Batra (IIT Madras BS in Data Science & Applications)  
**Project:** Precision Medical Equipment — Quality, Cost & Supply Chain Optimization

---

## 🎯 1. WHAT ARE WE DOING? (The Big Picture)

### The Objective
We are taking your completed academic BDM capstone project and **packaging it as a professional industrial case study** for recruiters, engineering managers, and hiring leads.

### Why do this?
- Most student projects use clean, artificial Kaggle datasets (e.g., Titanic, Iris, Housing Prices). Recruiters often ignore these.
- **Your big differentiator**: You collected **real primary data directly from the factory floor** of an active manufacturing enterprise over 17 months.
- By packaging this properly, you demonstrate:
  1. **Business Acumen**: Understanding profit, manufacturing costs, and hospital supply chains.
  2. **Data Science & Statistics**: ANOVA hypothesis testing, ARIMA forecasting, SPC control charts.
  3. **Operational Rigor**: Inventory optimization (EOQ, Safety Stock, Reorder Points).
  4. **Data Privacy & Ethics**: Anonymizing proprietary enterprise data professionally.

---

## ⚙️ 2. HOW DID WE DO THAT? (Methodology & Technical Execution)

Here is the exact step-by-step breakdown of how the analysis was conducted from factory floor to Python models:

```
+---------------------------------------------------------------------------------------------------------+
|                                    STEP-BY-STEP METHODOLOGY FLOW                                        |
+---------------------------------------------------------------------------------------------------------+
|                                                                                                         |
|  [ Step 1: On-Site Data Collection ]                                                                    |
|  • 3 plant visits auditing handwritten production logs, rejection registers & cost sheets.             |
|  • Compiled 119 monthly batch records across 7 products (Jan 2025 – May 2026).                         |
|                                     │                                                                   |
|                                     ▼                                                                   |
|  [ Step 2: Quality Analysis (Problem 1) ]                                                               |
|  • Defect Rate Calculation: (Units Rejected / Units Produced) × 100                                     |
|  • Statistical Process Control (SPC): X-bar (mean) and R-charts (range) with 3-sigma UCL/LCL bounds.    |
|  • Root Cause Analysis (RCA): 4M Ishikawa (Man, Machine, Material, Method) + 5-Whys.                    |
|  • Pareto Analysis: Found defects spread equally (~20 batches each) across all 6 failure modes.         |
|                                     │                                                                   |
|                                     ▼                                                                   |
|  [ Step 3: Financial Modeling & Hypothesis Testing (Problem 2) ]                                        |
|  • COPQ Equation: Rework Cost + Scrap Cost (₹12,02,530 total across 746 lost labor hours).              |
|  • The Discovery: Plaster Saw (0.97% defect) drove 62.2% of COPQ due to its ₹12,000 unit cost.          |
|  • One-Way ANOVA: Statistically proved COPQ variance across SKUs is non-random (p < 0.001).             |
|                                     │                                                                   |
|                                     ▼                                                                   |
|  [ Step 4: Supply Chain & Demand Forecasting (Problem 3) ]                                              |
|  • ABC Stratification: Ranked SKUs by annual revenue velocity.                                          |
|  • ARIMA Time-Series: Modeled growth trends with differencing (d=1) to forecast 3-month demand.         |
|  • EOQ & ROP Formula: Calibrated batch sizes and safety buffers (Z=1.65 for 95% service level).         |
|                                     │                                                                   |
|                                     ▼                                                                   |
|  [ Step 5: Strategic Business ROI ]                                                                     |
|  • 35% Defect Reduction target, ₹5.5L+ Annual Quality Savings, 0 Stockout Resiliency.                   |
|                                                                                                         |
+---------------------------------------------------------------------------------------------------------+
```

---

## 🏗️ 3. STRUCTURE OF YOUR RECRUITER DEMONSTRATION

We have set up a 4-layer demonstration system so you have the right asset for every stage of your job hunt:

```
                      ┌────────────────────────────────────────┐
                      │        LAYER 1: ATTRACT & HOOK         │
                      │  • LinkedIn Viral Post                 │
                      │  • LinkedIn "Featured Project" Entry   │
                      └──────────────────┬─────────────────────┘
                                         │
                                         ▼
                      ┌────────────────────────────────────────┐
                      │        LAYER 2: RESUME IMPACT          │
                      │  • Google XYZ Format Bullet Points     │
                      │  • Tailored for 4 distinct job roles   │
                      └──────────────────┬─────────────────────┘
                                         │
                                         ▼
                      ┌────────────────────────────────────────┐
                      │     LAYER 3: TECHNICAL PROOF (REPO)    │
                      │  • GitHub README (README_PORTFOLIO.md) │
                      │  • Clean Code, Architecture & Math     │
                      └──────────────────┬─────────────────────┘
                                         │
                                         ▼
                      ┌────────────────────────────────────────┐
                      │        LAYER 4: INTERVIEW MASTERY      │
                      │  • 90-Second Elevator Pitch            │
                      │  • 5 Technical Deep-Dive Defenses      │
                      └────────────────────────────────────────┘
```

---

## 📂 4. GUIDE TO YOUR WORKSPACE ASSETS

Here is where each document lives and how to use it:

| File in Your Folder | What it is | How you should use it |
| :--- | :--- | :--- |
| **[`README_PORTFOLIO.md`](file:///c:/Users/kusha/Desktop/ANTIGRAVITY/BDM_JUN26/README_PORTFOLIO.md)** | The complete GitHub Repository `README.md` | Copy the text of this file and make it the `README.md` of your public GitHub repo. It gives recruiters a world-class repo overview. |
| **[`RESUME_AND_INTERVIEW_GUIDE.md`](file:///c:/Users/kusha/Desktop/ANTIGRAVITY/BDM_JUN26/RESUME_AND_INTERVIEW_GUIDE.md)** | Resume bullets & Interview answers | Copy the bullet points into your resume. Read Section 2 & 3 before interviews to master the 90-second pitch and technical Q&As. |
| **[`LINKEDIN_AND_PORTFOLIO_POSTS.md`](file:///c:/Users/kusha/Desktop/ANTIGRAVITY/BDM_JUN26/LINKEDIN_AND_PORTFOLIO_POSTS.md)** | LinkedIn post & Featured snippet | Post the viral storytelling piece on LinkedIn with a couple of your chart PNGs. Add the featured project snippet to your LinkedIn profile. |
| **[`PROJECT_MASTER_WALKTHROUGH.md`](file:///c:/Users/kusha/Desktop/ANTIGRAVITY/BDM_JUN26/PROJECT_MASTER_WALKTHROUGH.md)** | This document (Your Master Blueprint) | Keep this open as your reference guide whenever you are preparing for applications or interviews. |

---

## 💬 5. HOW TO TALK ABOUT THIS IN AN INTERVIEW (The 3 Golden Rules)

### Rule 1: Always highlight that it's PRIMARY DATA
- Say: *"I conducted 3 on-site plant visits to collect handwritten production and QC logs rather than using synthetic benchmark datasets."*
- **Why**: Recruiters love candidates who can handle raw, messy, real-world data collection and validation.

### Rule 2: Deliver the Counter-Intuitive Twist
- Say: *"Management was focusing on Needle Holders because of their 1.57% defect rate, but my ANOVA analysis revealed that Plaster Cutting Saws—with only a 0.97% defect rate—caused 62.2% of the ₹12 Lakhs total financial loss due to unit replacement cost."*
- **Why**: This proves you think like a business owner, not just a code monkey.

### Rule 3: Bridge the Gap from Insights to Action
- Say: *"Data analysis without action is useless. I didn't stop at charting defects; I built an EOQ + ROP inventory replenishment model with ARIMA demand forecasting to prevent stockouts and protect ₹5.5 Lakhs in annual quality costs."*
- **Why**: This proves you deliver measurable ROI and end-to-end solutions.
