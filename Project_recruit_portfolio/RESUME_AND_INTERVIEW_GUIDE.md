# Medical Equipment Firm Case Study: Resume Bullets & Recruiter Interview Playbook
**Author:** Kushal Batra | **Project:** Surgical Implants Quality & Inventory Cost Analysis

---

## 📄 Section 1: Tailored Resume Bullet Points

Use the bullet points below tailored to the specific role you are targeting. These are formulated using the gold-standard **Google XYZ formula**: *"Accomplished [X] as measured by [Y], by doing [Z]"* and the **STAR method**.

### Option A: For Data Analyst / BI Analyst Roles
- **Analyzed 17 months of batch-level production & inventory data (119 records, 7 SKUs)** for an ISO/CE-certified surgical equipment manufacturer using Python (Pandas, SciPy, Statsmodels) and advanced Excel modeling.
- **Quantified ₹12.02 Lakhs in hidden Cost of Poor Quality (COPQ)** across 746 wasted rework hours; conducted **One-Way ANOVA ($p < 0.001$)** proving high-unit-cost SKUs drove **62.2% of total financial losses** despite having low defect frequency (<1%).
- **Engineered dynamic inventory optimization models (ABC, EOQ, Reorder Point, Safety Stock)** and time-series demand forecasting (**ARIMA**), eliminating recurring stockouts in high-volume SKUs while preserving a 95% service level.
- **Designed 10+ publication-ready statistical visualizations** (SPC $X$-bar/$R$ control charts, Pareto, stacked financial breakdowns, ARIMA confidence bands) to present actionable insights to executive leadership.

---

### Option B: For Supply Chain & Operations Analyst Roles
- **Spearheaded an end-to-end operational audit** of surgical implant manufacturing, gathering primary field data across 3 on-site plant visits to evaluate defect rates, machine drift, and carrying costs.
- **Formulated an integrated ABC–EOQ–ROP inventory replenishment framework** with calibrated safety buffers ($Z=1.65$) and ARIMA sales forecasting, resolving stockout vulnerabilities in fast-moving items (Bone Screws and Plates).
- **Implemented Statistical Process Control (SPC)** and 4M Ishikawa Root Cause Analysis across 6 failure modes, identifying systemic calibration drift and structuring standard operating procedures to reduce defect rates by a projected 35%.
- **Benchmarked carrying vs. ordering cost trade-offs** across ₹120 to ₹12,000 unit-cost categories, optimizing batch sizing ($1,280$ avg units) to streamline working capital allocation.

---

### Option C: For Business Analyst / Strategy & Consulting Roles
- **Partnered with plant executive leadership** of a precision medical device enterprise to translate unstructured shop-floor logs into an institutionalized data-driven decision framework.
- **Disproved core operational assumptions** regarding defect impact by isolating financial risk: proved that low-defect, high-value SKUs accounted for >79% of COPQ (₹9.55 Lakhs), pivoting management focus to high-leverage quality gates.
- **Synthesized multi-dimensional operational metrics** across quality, cost, and logistics into strategic C-suite recommendations projected to save ₹5.5+ Lakhs annually in scrap/rework.
- **Authored comprehensive 20-page executive analysis** and delivered technical defense covering statistical validation, hypothesis testing, and operational roadmaps.

---

### Option D: For Junior Data Scientist / Quantitative Analyst Roles
- **Developed statistical hypotheses and executed parametric tests (One-Way ANOVA, Student's t-test, linear trend regression)** in Python (SciPy) to rigorously validate variance in manufacturing cost drivers ($p < 0.001, R^2 = 0.81$).
- **Built univariate ARIMA $(p, d, q)$ time-series forecasting models** (Statsmodels) with rolling AIC optimization to project SKU-level monthly demand and generate 95% confidence intervals under non-stationary trends.
- **Constructed Statistical Process Control algorithms** to establish Upper and Lower Control Limits ($3\sigma$ bounds) on production batches, separating random noise from assignable causes.
- **Built end-to-end data pipeline** with automated validation assertions and zero-loss handling for 15 operational variables.

---

## 🎙️ Section 2: Recruiter & Hiring Manager Pitch Playbook

### 1. The 90-Second Elevator Pitch ("Walk me through this project")
> *"For my major capstone project, I wanted to work on a real-world problem rather than a synthetic Kaggle dataset. I partnered with an established **medical equipment and surgical device manufacturing firm**. Over 17 months of primary batch data, they were facing three coupled issues: rising product defects, surging rework/scrap expenses, and unpredictable stockouts in key surgical items.*
>
> *I built an end-to-end analytics framework covering quality, finance, and supply chain. First, using Statistical Process Control and Root Cause Analysis, I discovered that defects were systemic across all 6 rejection reasons rather than isolated to one vendor. Second, through financial modeling and ANOVA hypothesis testing, I uncovered a counter-intuitive insight: management assumed high-defect products were their biggest cost driver, but data proved that the Plaster Cutting Saw—which had a low defect rate of 0.97%—drove **62.2% of their ₹12 Lakhs total Cost of Poor Quality** purely due to its ₹12,000 unit cost.*
>
> *Finally, I built an integrated ABC-EOQ-ROP replenishment model combined with ARIMA demand forecasting to eliminate their stockouts. The project delivered a clear roadmap projected to save over ₹5.5 Lakhs annually in quality costs and stabilize inventory at a 95% service level."*

---

## 🧠 Section 3: Technical Interview Deep Dive Q&A

### Q1: "How did you gather and clean this dataset? Why primary data?"
**Answer:**
> *"I conducted three in-person field visits to the manufacturing facility, interviewing the Operations Manager and auditing physical production registers, QC rejection logs, store issue records, and cost sheets. I synthesized this into a 119-record monthly batch dataset across 7 SKUs and 15 variables covering Jan 2025 to May 2026.
>
> To ensure data integrity, I implemented automated Python assertion suites verifying that rejected units never exceeded produced units, cross-validated closing stock balance equations ($\text{Closing} = \text{Opening} + \text{Produced} - \text{Sales}$), and audited consistency in COPQ derivations."*

---

### Q2: "Why did you use One-Way ANOVA instead of multiple t-tests for COPQ?"
**Answer:**
> *"We were comparing the mean Cost of Poor Quality across 7 distinct product lines. If I had used pairwise Student's t-tests, evaluating 7 groups requires $\binom{7}{2} = 21$ individual comparisons.
>
> Conducting 21 separate t-tests at an alpha level of $\alpha = 0.05$ compounds the **Family-Wise Error Rate (FWER)**:
> $$\text{FWER} = 1 - (1 - \alpha)^k = 1 - (0.95)^{21} \approx 65.9\%$$
> This means there would be an unacceptably high ~66% chance of at least one false positive (Type I error). One-Way ANOVA allowed us to test the omnibus null hypothesis that all product COPQ means are equal simultaneously with a single controlled test statistic ($F$-statistic), which yielded $p < 0.001$, confirming highly significant variance."*

---

### Q3: "Why choose ARIMA forecasting over simple Moving Averages or Exponential Smoothing?"
**Answer:**
> *"Moving Averages and Simple Exponential Smoothing assume a mean-reverting stationary series and suffer from lag when demand has strong directional momentum. In the firm's sales data, all 7 products showed a statistically significant upward growth trajectory over the 17-month period ($r^2 \approx 0.74–0.86$).
>
> Moving averages systematically underestimated future demand during growth periods, directly causing the stockout incidents in Bone Screws and Bone Plates. ARIMA explicitly handles non-stationarity through differencing ($d=1$), models autocorrelation in demand shocks through autoregressive terms ($p$), and smooths noise via moving average residuals ($q$). This dynamic forecast fed directly into our Reorder Point (ROP) equation."*

---

### Q4: "What was the most surprising or non-obvious business insight from your analysis?"
**Answer:**
> *"The biggest insight was the **decoupling of defect rate from financial impact**.
>
> Intuitively, plant supervisors were spending the majority of their QC bandwidth firefighting Needle Holders and Intramedullary Nails because they had the highest defect rates (~1.57%). However, because those units cost only ₹400–₹950, their combined COPQ was only ~₹1.04 Lakhs.
>
> In contrast, the Plaster Cutting Saw had one of the lowest defect rates in the factory (0.97%), but because each unit costs ₹12,000 to manufacture, each scrapped or reworked batch was massively expensive. Plaster Cutting Saws generated ₹7.48 Lakhs (62.2% of the entire factory's COPQ). We redirected managerial priority to institute pre-machining inspections on high-unit-value lines, generating immediate high-leverage cost savings."*

---

### Q5: "How did you balance the trade-off between holding cost and stockout risk in your inventory model?"
**Answer:**
> *"We used an integrated two-tier model:
> 1. **EOQ for Sizing**: Minimized total annual inventory costs by finding the mathematical equilibrium between ordering setup costs and per-unit holding costs ($H = 20\%$ of unit cost/year).
> 2. **Safety Stock & ROP for Risk Buffering**: Calculated dynamic safety stock using:
>    $$\text{Safety Stock} = Z \times \sigma_{\text{demand}} \times \sqrt{L}$$
>    Setting $Z = 1.65$ guaranteed a 95% cycle service level against lead-time demand variability ($\sigma_{\text{demand}} = 79.09$).
> 3. **ABC Stratification**: For high-cost Class A items (Plaster Cutting Saw), we held lean safety stocks with frequent weekly review, whereas for low-cost Class C items (Bone Screws/Plates where stockouts previously occurred), we held wider safety buffers because holding costs were negligible (₹24/unit/yr) compared to the disruption of losing a hospital client."*

---

## 🎯 Section 4: Key Numerical Soundbites to Memorize

| Metric | Exact Value | Context / Story |
| :--- | :--- | :--- |
| **Total COPQ** | **₹12,02,530** | Quantified 17-month financial loss from rework & scrap |
| **Plaster Saw COPQ Share** | **62.2% (₹7.48 Lakhs)** | Single SKU responsible for majority of quality loss |
| **Overall Defect Rate** | **1.22%** | Rose from 1.00% (Jan 2025) to 1.63% (May 2026) |
| **Rework Labour Wasted** | **746 Hours** | Lost manufacturing capacity over 17 months |
| **Stockouts** | **2 Incidents** | Bone Screw (Jul 2025) & Bone Plate (Feb 2026) |
| **Dataset Size** | **119 rows, 15 variables** | 17 months $\times$ 7 products, primary factory records |
