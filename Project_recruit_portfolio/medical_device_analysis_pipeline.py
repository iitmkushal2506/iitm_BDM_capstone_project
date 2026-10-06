"""
KK Surgicals — BDM Capstone Final Report
Chart Generation and Statistical Analysis Script

Author: Kushal Batra (24f2000859)
Purpose: Reproduces all 10 figures and the statistical test results (T-test,
ANOVA, correlation, ARIMA forecast, SPC control limits) used in the Final
Submission report. Reads directly from the raw primary-data Excel file.

Libraries used (all permitted under BDM guidelines):
    pandas, numpy, matplotlib, scipy, statsmodels

HOW TO USE:
    1. Place 'Raw_Data_K_K_Surgicals.xlsx' in the same folder as this script
       (or update RAW_DATA_PATH below).
    2. Run: python KK_Surgicals_Charts.py
    3. All charts are saved as PNG files inside a 'charts/' folder, and all
       statistical results are printed to the console.
"""

import os
import warnings

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # non-interactive backend so the script runs headless
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from scipy import stats
from statsmodels.tsa.arima.model import ARIMA

warnings.filterwarnings("ignore")  # suppress ARIMA convergence chatter

# ----------------------------------------------------------------------
# CONFIGURATION
# ----------------------------------------------------------------------
RAW_DATA_CANDIDATES = [
    "Medical_Device_Analytics_Workbook.xlsx",
    "Raw_Data_K_K_Surgicals.xlsx",
    "Raw_Data_K.K.Surgicals.xlsx"
]
OUTPUT_DIR = "charts"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Global plot styling — plain, black-and-white-friendly, no clutter
plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False


def savepath(filename):
    """Helper: build the full output path for a chart file."""
    return os.path.join(OUTPUT_DIR, filename)


# ----------------------------------------------------------------------
# 1. LOAD AND CLEAN DATA
# ----------------------------------------------------------------------
print("Loading raw dataset...")

def load_dataset():
    for path in RAW_DATA_CANDIDATES:
        if os.path.exists(path):
            try:
                xl = pd.ExcelFile(path)
                sheet = "Raw_Data" if "Raw_Data" in xl.sheet_names else xl.sheet_names[0]
                df_candidate = pd.read_excel(path, sheet_name=sheet)
                if "Units_Produced" not in df_candidate.columns:
                    for h in range(1, 5):
                        df_try = pd.read_excel(path, sheet_name=sheet, header=h)
                        if "Units_Produced" in df_try.columns:
                            return df_try, path
                else:
                    return df_candidate, path
            except Exception:
                continue
    raise FileNotFoundError(f"Could not find any of the candidate Excel files: {RAW_DATA_CANDIDATES}")

df, loaded_path = load_dataset()
print(f"Loaded dataset from: {loaded_path}")

# Convert month column to proper datetime for time-series operations
if "Months_date" not in df.columns and "Month" in df.columns:
    df["Months_date"] = pd.to_datetime(df["Month"], format="%b-%y", errors="coerce")
    if df["Months_date"].isnull().any():
        df["Months_date"] = pd.to_datetime(df["Month"], errors="coerce")
else:
    df["Months_date"] = pd.to_datetime(df["Months_date"])

# Derived variables used throughout the analysis
df["Defect_Rate"] = df["Units_Rejected"] / df["Units_Produced"] * 100
# COPQ = Rework Cost + Scrap Cost (unit-cost-of-rejects term intentionally
# excluded to avoid double-counting, since rejected units are already
# reflected in rework/scrap cost figures)
df["COPQ"] = df["Rework_Cost_INR"] + df["Scrap_Cost_INR"]

# Basic data-quality checks (see Section 3.1 of the report)
assert df.isnull().sum().drop(labels=["Stockout_Incident"], errors="ignore").sum() == 0, \
    "Unexpected missing values in core analytical columns"
assert (df["Units_Rejected"] <= df["Units_Produced"]).all(), \
    "Found rows where Units_Rejected exceeds Units_Produced"
print(f"Loaded {len(df)} rows, {df['Product'].nunique()} products, "
      f"{df['Months_date'].nunique()} months. Data checks passed.\n")


# ========================================================================
# FIGURE 1 — Monthly Overall Defect Rate Trend
# ========================================================================
print("Generating Figure 1: Monthly defect rate trend...")

# Pooled monthly defect rate = total rejected / total produced per month
# (NOT the mean of per-batch rates, which would treat every product equally
# regardless of production volume)
monthly_defect = df.groupby("Months_date").apply(
    lambda g: g["Units_Rejected"].sum() / g["Units_Produced"].sum() * 100,
    include_groups=False,
)

# Test whether the defect rate is trending up or down over time
x = np.arange(len(monthly_defect))
slope, intercept, r_value, p_value, std_err = stats.linregress(x, monthly_defect.values)
print(f"  Defect rate trend: slope={slope:.5f} pct-points/month, "
      f"p={p_value:.4f}, r^2={r_value**2:.4f}")
print(f"  {'Significant' if p_value < 0.05 else 'NOT significant'} at alpha=0.05")

fig, ax = plt.subplots(figsize=(9, 4.5))
ax.plot(monthly_defect.index, monthly_defect.values, marker="o",
        color="#8B3A3A", linewidth=1.5, markersize=4)
ax.axhline(monthly_defect.mean(), linestyle="--", color="gray", linewidth=1,
           label=f"Mean: {monthly_defect.mean():.2f}%")
ax.set_ylim(0, 2.0)
ax.set_ylabel("Defect Rate (%)")
ax.set_xlabel("Month")
ax.set_title("Figure 1: Monthly Overall Defect Rate — KK Surgicals (Jan 2025 – May 2026)")
ax.legend(loc="upper right", fontsize=8)
plt.xticks(rotation=45, ha="right", fontsize=7)
plt.tight_layout()
plt.savefig(savepath("fig1_defect_trend.png"), dpi=150)
plt.close()


# ========================================================================
# FIGURE 2 — Product-wise Defect Rate
# ========================================================================
print("Generating Figure 2: Product-wise defect rate...")

prod_defect = df.groupby("Product").agg(
    Produced=("Units_Produced", "sum"), Rejected=("Units_Rejected", "sum")
)
prod_defect["DefectRate"] = prod_defect["Rejected"] / prod_defect["Produced"] * 100
prod_defect = prod_defect.sort_values("DefectRate")

# ANOVA: does defect rate differ significantly across the 7 products?
groups = [df[df["Product"] == p]["Defect_Rate"] for p in df["Product"].unique()]
f_stat, p_anova = stats.f_oneway(*groups)
print(f"  ANOVA (defect rate across 7 products): F={f_stat:.2f}, p={p_anova:.6f}")

fig, ax = plt.subplots(figsize=(9, 4.5))
colors = plt.cm.tab10(np.linspace(0, 1, 7))
ax.barh(prod_defect.index, prod_defect["DefectRate"], color=colors)
ax.axvline(prod_defect["DefectRate"].mean(), color="red", linestyle="--",
           linewidth=1, label=f"Average: {prod_defect['DefectRate'].mean():.2f}%")
for i, (idx, val) in enumerate(prod_defect["DefectRate"].items()):
    ax.text(val + 0.02, i, f"{val:.2f}%", va="center", fontsize=9, fontweight="bold")
ax.set_xlabel("Defect Rate (%)")
ax.set_title("Figure 2: Product-wise Defect Rate — KK Surgicals (Jan 2025 – May 2026)")
ax.legend(fontsize=8)
plt.tight_layout()
plt.savefig(savepath("fig2_product_defect.png"), dpi=150)
plt.close()


# ========================================================================
# FIGURE 3 — Pareto Chart of Rejection Reasons
# ========================================================================
print("Generating Figure 3: Pareto chart of rejection reasons...")

reason_order = ["Surface Finish", "Thread Defect", "Dimension Variation",
                 "Burr Formation", "Material Defect", "Packaging Damage"]
counts = df["Rejection_Reason"].value_counts().reindex(reason_order)
cum_pct = counts.cumsum() / counts.sum() * 100

fig, ax1 = plt.subplots(figsize=(9, 4.5))
ax1.bar(counts.index, counts.values, color="#4C72B0")
for i, v in enumerate(counts.values):
    ax1.text(i, v + 0.3, str(v), ha="center", fontsize=9, fontweight="bold")
ax1.set_ylabel("Frequency (Number of Batches)", color="#4C72B0")
ax1.set_ylim(0, 24)
ax2 = ax1.twinx()
ax2.plot(counts.index, cum_pct.values, color="#C44E52", marker="o", linewidth=1.5)
ax2.set_ylabel("Cumulative %", color="#C44E52")
ax2.set_ylim(0, 105)
ax2.axhline(80, color="gray", linestyle=":", linewidth=1)
ax1.set_title("Figure 3: Pareto Chart — Rejection Reasons (Jan 2025 – May 2026)")
plt.xticks(rotation=20, ha="right", fontsize=8)
plt.tight_layout()
plt.savefig(savepath("fig3_pareto.png"), dpi=150)
plt.close()


# ========================================================================
# FIGURE 4 — Monthly COPQ Trend
# ========================================================================
print("Generating Figure 4: Monthly COPQ trend...")

monthly_copq = df.groupby("Months_date").agg(
    Rework=("Rework_Cost_INR", "sum"), Scrap=("Scrap_Cost_INR", "sum")
)
monthly_copq["Total"] = monthly_copq["Rework"] + monthly_copq["Scrap"]

# Test whether COPQ is trending up over time (unlike the flat defect rate)
x2 = np.arange(len(monthly_copq))
slope2, intercept2, r2, p2, se2 = stats.linregress(x2, monthly_copq["Total"].values)
print(f"  COPQ trend: slope={slope2:.1f} INR/month, p={p2:.6f}, r^2={r2**2:.4f}")

fig, ax = plt.subplots(figsize=(9, 4.5))
ax.bar(monthly_copq.index, monthly_copq["Rework"], width=20,
       label="Rework Cost", color="#4C72B0")
ax.bar(monthly_copq.index, monthly_copq["Scrap"], width=20,
       bottom=monthly_copq["Rework"], label="Scrap Cost", color="#C44E52")
ax.plot(monthly_copq.index, monthly_copq["Total"], color="#DDAA33",
        marker="o", linewidth=1.5, label="Total COPQ")
ax.set_ylabel("Cost (INR)")
ax.set_title("Figure 4: Monthly Cost of Poor Quality (COPQ) — KK Surgicals (Jan 2025 – May 2026)")
ax.legend(fontsize=8)
plt.xticks(rotation=45, ha="right", fontsize=7)
plt.tight_layout()
plt.savefig(savepath("fig4_copq_trend.png"), dpi=150)
plt.close()


# ========================================================================
# FIGURE 5 — Product-wise COPQ Breakdown
# ========================================================================
print("Generating Figure 5: Product-wise COPQ breakdown...")

copq_prod = df.groupby("Product").agg(
    Rework=("Rework_Cost_INR", "sum"), Scrap=("Scrap_Cost_INR", "sum")
)
copq_prod["Total"] = copq_prod["Rework"] + copq_prod["Scrap"]
copq_prod["Pct"] = copq_prod["Total"] / copq_prod["Total"].sum() * 100
copq_prod = copq_prod.sort_values("Total")

fig, ax = plt.subplots(figsize=(9, 4.5))
ax.barh(copq_prod.index, copq_prod["Rework"], color="#4C72B0", label="Rework Cost")
ax.barh(copq_prod.index, copq_prod["Scrap"], left=copq_prod["Rework"],
        color="#C44E52", label="Scrap Cost")
for i, (idx, row) in enumerate(copq_prod.iterrows()):
    ax.text(row["Total"] + 8000, i, f"\u20b9{row['Total']:,.0f}",
            va="center", fontsize=8, fontweight="bold")
ax.set_xlabel("Total COPQ (INR)")
ax.set_title("Figure 5: Product-wise COPQ Breakdown — KK Surgicals (Jan 2025 – May 2026)")
ax.legend(fontsize=8)
plt.tight_layout()
plt.savefig(savepath("fig5_copq_product.png"), dpi=150)
plt.close()

# --- Key hypothesis tests behind Figure 5's interpretation ---
# Does COPQ correlate more with unit cost or with defect rate?
r_cost, p_cost = stats.pearsonr(df["Unit_Cost_INR"], df["COPQ"])
r_defect, p_defect = stats.pearsonr(df["Defect_Rate"], df["COPQ"])
print(f"  Correlation COPQ vs Unit Cost:   r={r_cost:.3f}, p={p_cost:.6f}")
print(f"  Correlation COPQ vs Defect Rate: r={r_defect:.3f}, p={p_defect:.6f}")

# T-test: COPQ in the 3 highest-unit-cost products vs the remaining 4
high_cost_products = ["Plaster Cutting Saw", "Wire Cutter", "Bone Nibbler"]
grp_high = df[df["Product"].isin(high_cost_products)]["COPQ"]
grp_low = df[~df["Product"].isin(high_cost_products)]["COPQ"]
t_stat, p_ttest = stats.ttest_ind(grp_high, grp_low, equal_var=False)
print(f"  T-test (high-cost vs low-cost products' COPQ): t={t_stat:.3f}, p={p_ttest:.6f}")

# ANOVA: COPQ across all 7 products
groups_copq = [df[df["Product"] == p]["COPQ"] for p in df["Product"].unique()]
f_copq, p_copq = stats.f_oneway(*groups_copq)
print(f"  ANOVA (COPQ across 7 products): F={f_copq:.2f}, p={p_copq:.6f}\n")


# ========================================================================
# FIGURE 6 — Monthly Sales Trend (All Products)
# ========================================================================
print("Generating Figure 6: Monthly sales trend...")

fig, ax = plt.subplots(figsize=(9, 4.5))
colors = plt.cm.tab10(np.linspace(0, 1, 7))
for i, product in enumerate(df["Product"].unique()):
    sub = df[df["Product"] == product].sort_values("Months_date")
    ax.plot(sub["Months_date"], sub["Sales_Qty"], marker="o", markersize=3,
            linewidth=1.3, label=product, color=colors[i])
ax.set_ylabel("Units Sold")
ax.set_xlabel("Month")
ax.set_title("Figure 6: Monthly Sales Trend — All 7 Products (Jan 2025 – May 2026)")
ax.legend(fontsize=7, loc="upper left", ncol=2)
plt.xticks(rotation=45, ha="right", fontsize=7)
plt.tight_layout()
plt.savefig(savepath("fig6_sales_trend.png"), dpi=150)
plt.close()


# ========================================================================
# FIGURE 7 — Average vs Minimum Closing Stock (Stockouts Marked)
# ========================================================================
print("Generating Figure 7: Average vs minimum closing stock...")

stock = df.groupby("Product").agg(
    AvgClosing=("Closing_Stock", "mean"), MinClosing=("Closing_Stock", "min")
)
stockout_products = df[df["Stockout_Incident"] == "Yes"]["Product"].unique()
stock = stock.sort_values("AvgClosing")

fig, ax = plt.subplots(figsize=(9, 4.5))
x_pos = np.arange(len(stock))
ax.bar(x_pos, stock["AvgClosing"], color="#4C72B0", label="Avg Closing Stock", width=0.6)
ax.scatter(x_pos, stock["MinClosing"], color="#C44E52", zorder=5,
           label="Min Closing Stock", s=40)
for i, prod in enumerate(stock.index):
    if prod in stockout_products:
        ax.annotate("\u26a0 Stockout", (i, stock["MinClosing"].iloc[i]),
                    textcoords="offset points", xytext=(0, -18), ha="center",
                    fontsize=8, color="#C44E52", fontweight="bold")
ax.set_xticks(x_pos)
ax.set_xticklabels(stock.index, rotation=25, ha="right", fontsize=8)
ax.set_ylabel("Stock Units")
ax.set_title("Figure 7: Average vs Minimum Closing Stock by Product (Jan 2025 – May 2026)")
ax.legend(fontsize=8)
plt.tight_layout()
plt.savefig(savepath("fig7_stock.png"), dpi=150)
plt.close()


# ========================================================================
# FIGURE 8 — ABC Classification Pie Chart
# ========================================================================
print("Generating Figure 8: ABC classification...")

prod_sales = df.groupby("Product").agg(
    AvgMonthlySales=("Sales_Qty", "mean"), UnitCost=("Unit_Cost_INR", "first")
)
# Annualise monthly average sales, then compute annual consumption value
prod_sales["AnnualDemand"] = prod_sales["AvgMonthlySales"] * 12
prod_sales["AnnualValue"] = prod_sales["AnnualDemand"] * prod_sales["UnitCost"]
prod_sales = prod_sales.sort_values("AnnualValue", ascending=False)
prod_sales["PctValue"] = prod_sales["AnnualValue"] / prod_sales["AnnualValue"].sum() * 100
prod_sales["CumPct"] = prod_sales["PctValue"].cumsum()


def abc_class(cum_pct):
    """Standard ABC thresholds: A <= 70% cum. value, B <= 90%, C = rest."""
    if cum_pct <= 70:
        return "A"
    elif cum_pct <= 90:
        return "B"
    return "C"


prod_sales["Class"] = prod_sales["CumPct"].apply(abc_class)
print("  ABC classification:")
print(prod_sales[["AnnualValue", "PctValue", "CumPct", "Class"]].round(1))

class_colors = {"A": "#C44E52", "B": "#DDAA33", "C": "#4C72B0"}
pie_colors = [class_colors[c] for c in prod_sales["Class"]]

fig, ax = plt.subplots(figsize=(7, 6))
ax.pie(prod_sales["AnnualValue"], labels=prod_sales.index, autopct="%1.1f%%",
       colors=pie_colors, startangle=90, textprops={"fontsize": 8})
ax.set_title("Figure 8: ABC Classification by Annual Consumption Value")
legend_elems = [Patch(facecolor=class_colors[c], label=f"Class {c}") for c in "ABC"]
ax.legend(handles=legend_elems, loc="lower left", fontsize=8)
plt.tight_layout()
plt.savefig(savepath("fig8_abc_pie.png"), dpi=150)
plt.close()

# --- EOQ / ROP / Safety Stock calculations (see report Section 3.4 for assumptions) ---
S = 500        # ordering cost per order (INR) — assumed
H_RATE = 0.20  # holding cost as a fraction of unit cost per year — assumed
Z = 1.65       # service level factor for 95% service level — assumed
LEAD_TIME_DAYS = 15

prod_sales["H"] = prod_sales["UnitCost"] * H_RATE
prod_sales["EOQ"] = np.sqrt(2 * prod_sales["AnnualDemand"] * S / prod_sales["H"])
daily_demand = prod_sales["AnnualDemand"] / 365
prod_sales["LeadTimeDemand"] = daily_demand * LEAD_TIME_DAYS
# Convert monthly std dev of sales to a daily std dev, then apply the
# standard safety-stock formula: Z * sigma_daily * sqrt(lead time in days)
monthly_std = df.groupby("Product")["Sales_Qty"].std()
daily_std = monthly_std / np.sqrt(30)
prod_sales["SafetyStock"] = Z * daily_std.reindex(prod_sales.index) * np.sqrt(LEAD_TIME_DAYS)
prod_sales["ROP"] = prod_sales["LeadTimeDemand"] + prod_sales["SafetyStock"]

print("\n  EOQ / ROP / Safety Stock (rounded):")
print(prod_sales[["EOQ", "LeadTimeDemand", "SafetyStock", "ROP"]].round(0))


# ========================================================================
# FIGURE 9 — ARIMA Sales Forecast (Bone Plate & Bone Screw)
# ========================================================================
print("\nGenerating Figure 9: ARIMA forecast (Bone Plate & Bone Screw)...")

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
for ax, product in zip(axes, ["Bone Plate", "Bone Screw"]):
    sub = df[df["Product"] == product].sort_values("Months_date")
    series = pd.Series(sub["Sales_Qty"].values,
                        index=pd.DatetimeIndex(sub["Months_date"].values, freq="MS"))
    fit = ARIMA(series, order=(2, 1, 0)).fit()
    forecast = fit.get_forecast(steps=3)
    mean_fc = forecast.predicted_mean
    ci = forecast.conf_int(alpha=0.05)

    ax.plot(series.index, series.values, marker="o", markersize=3,
            color="#4C72B0", label="Actual Sales")
    ax.plot(mean_fc.index, mean_fc.values, marker="o", markersize=4,
            color="#C44E52", linestyle="--", label="ARIMA Forecast")
    ax.fill_between(mean_fc.index, ci.iloc[:, 0], ci.iloc[:, 1],
                     color="#C44E52", alpha=0.2, label="95% CI")
    ax.set_title(product, fontsize=10)
    ax.legend(fontsize=7)
    ax.tick_params(axis="x", rotation=45, labelsize=6)

fig.suptitle("Figure 9: ARIMA(2,1,0) Sales Forecast — Bone Plate & Bone Screw (Jun–Aug 2026)",
             fontsize=11)
plt.tight_layout()
plt.savefig(savepath("fig9_arima.png"), dpi=150)
plt.close()

# --- Full 3-month ARIMA forecast for all 7 products, order chosen by lowest AIC ---
print("  ARIMA 3-month forecast for all products (order selected by lowest AIC):")
candidate_orders = [(1, 1, 0), (0, 1, 1), (1, 1, 1), (2, 1, 0)]
for product in df["Product"].unique():
    sub = df[df["Product"] == product].sort_values("Months_date")
    series = pd.Series(sub["Sales_Qty"].values,
                        index=pd.DatetimeIndex(sub["Months_date"].values, freq="MS"))
    best_aic, best_order, best_fit = None, None, None
    for order in candidate_orders:
        try:
            candidate_fit = ARIMA(series, order=order).fit()
            if best_aic is None or candidate_fit.aic < best_aic:
                best_aic, best_order, best_fit = candidate_fit.aic, order, candidate_fit
        except Exception:
            continue
    fc = best_fit.get_forecast(steps=3).predicted_mean.round(0).values
    print(f"    {product}: order={best_order}, forecast(Jun,Jul,Aug-26)={fc}")


# ========================================================================
# FIGURE 10 — SPC X-bar and R Charts
# ========================================================================
print("\nGenerating Figure 10: SPC X-bar and R charts...")

# SPC constants for subgroup size n = 7 (7 products sampled per month)
A2, D3, D4 = 0.419, 0.076, 1.924

spc_monthly = df.groupby("Months_date")["Units_Rejected"].agg(["mean", "max", "min"])
spc_monthly["range"] = spc_monthly["max"] - spc_monthly["min"]

xbar_grand = spc_monthly["mean"].mean()   # X-double-bar: centre line for X-bar chart
rbar = spc_monthly["range"].mean()        # R-bar: centre line for R chart

UCL_x = xbar_grand + A2 * rbar
LCL_x = max(0, xbar_grand - A2 * rbar)
UCL_r = D4 * rbar
LCL_r = D3 * rbar

out_of_control_x = spc_monthly[(spc_monthly["mean"] > UCL_x) | (spc_monthly["mean"] < LCL_x)]
out_of_control_r = spc_monthly[(spc_monthly["range"] > UCL_r) | (spc_monthly["range"] < LCL_r)]
print(f"  X-bar chart: CL={xbar_grand:.2f}, UCL={UCL_x:.2f}, LCL={LCL_x:.2f}, "
      f"out-of-control points={len(out_of_control_x)}")
print(f"  R chart:     CL={rbar:.2f}, UCL={UCL_r:.2f}, LCL={LCL_r:.2f}, "
      f"out-of-control points={len(out_of_control_r)}")

fig, axes = plt.subplots(2, 1, figsize=(9, 7), sharex=True)

axes[0].plot(spc_monthly.index, spc_monthly["mean"], marker="o", color="#4C72B0", linewidth=1.3)
axes[0].axhline(xbar_grand, color="green", linestyle="-", linewidth=1, label=f"CL: {xbar_grand:.2f}")
axes[0].axhline(UCL_x, color="red", linestyle="--", linewidth=1, label=f"UCL: {UCL_x:.2f}")
axes[0].axhline(LCL_x, color="red", linestyle="--", linewidth=1, label=f"LCL: {LCL_x:.2f}")
axes[0].set_ylabel("Mean Units Rejected")
axes[0].set_title("X-bar Chart — Average Units Rejected per Batch (Monthly Subgroup, n=7 Products)")
axes[0].legend(fontsize=7, loc="upper left", ncol=3)

axes[1].plot(spc_monthly.index, spc_monthly["range"], marker="o", color="#C44E52", linewidth=1.3)
axes[1].axhline(rbar, color="green", linestyle="-", linewidth=1, label=f"CL: {rbar:.2f}")
axes[1].axhline(UCL_r, color="red", linestyle="--", linewidth=1, label=f"UCL: {UCL_r:.2f}")
axes[1].axhline(LCL_r, color="red", linestyle="--", linewidth=1, label=f"LCL: {LCL_r:.2f}")
axes[1].set_ylabel("Range (Units Rejected)")
axes[1].set_xlabel("Month")
axes[1].set_title("R Chart — Range of Units Rejected within Monthly Subgroup")
axes[1].legend(fontsize=7, loc="upper left", ncol=3)

plt.xticks(rotation=45, ha="right", fontsize=7)
plt.tight_layout()
plt.savefig(savepath("fig10_spc.png"), dpi=150)
plt.close()


# ========================================================================
# DESCRIPTIVE STATISTICS SUMMARY (Appendix A.3 of the report)
# ========================================================================
print("\nDescriptive statistics summary:")
desc_vars = {
    "Units_Produced": "units", "Units_Rejected": "units", "Defect_Rate": "%",
    "Unit_Cost_INR": "INR", "Rework_Cost_INR": "INR", "Scrap_Cost_INR": "INR",
    "Rework_Labour_Hours": "hours", "Opening_Stock": "units", "Sales_Qty": "units",
    "Closing_Stock": "units", "COPQ": "INR",
}
for col, unit in desc_vars.items():
    s = df[col]
    print(f"  {col:<22} [{unit:<5}]  mean={s.mean():>10.2f}  median={s.median():>10.2f}  "
          f"std={s.std():>10.2f}  min={s.min():>8.2f}  max={s.max():>10.2f}")

print(f"\nAll charts saved to '{OUTPUT_DIR}/' — done.")
