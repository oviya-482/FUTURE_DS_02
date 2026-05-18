"""
Telco Customer Churn Analysis
==============================
A complete retention analysis pipeline covering:
  - Data cleaning & preparation
  - Churn rate by key segments
  - Customer lifetime value (CLV) estimation
  - Cohort survival by tenure group
  - Retention driver identification
  - Visual charts for stakeholder presentation

Requirements:
    pip install pandas matplotlib seaborn scikit-learn

Usage:
    python telco_churn_analysis.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from pathlib import Path

# ── 0. CONFIG ─────────────────────────────────────────────────────────────────
DATA_PATH = "Telco-Customer-Churn.csv"   # update if needed
OUTPUT_DIR = Path("churn_charts")
OUTPUT_DIR.mkdir(exist_ok=True)

BRAND_BLUE   = "#1a56db"
BRAND_RED    = "#e02424"
BRAND_GREEN  = "#057a55"
BRAND_AMBER  = "#d97706"
BRAND_GRAY   = "#6b7280"
NEUTRAL_BG   = "#f9fafb"

plt.rcParams.update({
    "font.family": "sans-serif",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.facecolor": NEUTRAL_BG,
    "axes.facecolor":   NEUTRAL_BG,
})

# ── 1. LOAD & CLEAN ───────────────────────────────────────────────────────────
print("Loading data …")
df = pd.read_csv(DATA_PATH)

# TotalCharges has some blank strings → coerce to NaN, then fill with MonthlyCharges
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df["TotalCharges"].fillna(df["MonthlyCharges"], inplace=True)

# Binary churn flag
df["Churned"] = (df["Churn"] == "Yes").astype(int)

# Customer Lifetime Value proxy
df["CLV"] = df["MonthlyCharges"] * df["tenure"]

# Tenure buckets
tenure_bins   = [0, 6, 12, 24, 36, 72]
tenure_labels = ["0–6 mo", "7–12 mo", "13–24 mo", "25–36 mo", "37–72 mo"]
df["TenureGroup"] = pd.cut(df["tenure"], bins=tenure_bins, labels=tenure_labels)

print(f"Loaded {len(df):,} customers | {df['Churned'].sum():,} churned")
print(f"Overall churn rate: {df['Churned'].mean()*100:.1f}%\n")

# ── 2. HELPER ─────────────────────────────────────────────────────────────────
def churn_rate(series):
    return series.mean() * 100

def save(fig, name):
    path = OUTPUT_DIR / f"{name}.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    print(f"  Saved → {path}")
    plt.close(fig)

# ── 3. OVERALL SUMMARY ───────────────────────────────────────────────────────
total          = len(df)
n_churned      = df["Churned"].sum()
n_retained     = total - n_churned
overall_rate   = churn_rate(df["Churned"])
monthly_loss   = df[df["Churned"]==1]["MonthlyCharges"].sum()
avg_clv_churn  = df[df["Churned"]==1]["CLV"].mean()
avg_clv_retain = df[df["Churned"]==0]["CLV"].mean()

print("=== SUMMARY ===")
print(f"  Total customers     : {total:,}")
print(f"  Churned             : {n_churned:,} ({overall_rate:.1f}%)")
print(f"  Retained            : {n_retained:,}")
print(f"  Monthly revenue lost: ${monthly_loss:,.0f}")
print(f"  Avg CLV – churned   : ${avg_clv_churn:,.0f}")
print(f"  Avg CLV – retained  : ${avg_clv_retain:,.0f}\n")

# ── 4. CHART 1 – Churn by Contract Type ──────────────────────────────────────
print("Generating charts …")

contract_churn = (
    df.groupby("Contract")["Churned"].mean().mul(100)
      .reset_index().rename(columns={"Churned": "ChurnRate"})
      .sort_values("ChurnRate", ascending=False)
)

fig, ax = plt.subplots(figsize=(7, 4))
colors = [BRAND_RED if r > 30 else BRAND_AMBER if r > 15 else BRAND_GREEN
          for r in contract_churn["ChurnRate"]]
bars = ax.barh(contract_churn["Contract"], contract_churn["ChurnRate"], color=colors, height=0.5)
ax.set_xlabel("Churn Rate (%)")
ax.set_title("Churn Rate by Contract Type", fontsize=13, fontweight="bold")
for bar, val in zip(bars, contract_churn["ChurnRate"]):
    ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
            f"{val:.1f}%", va="center", fontsize=10)
ax.set_xlim(0, 55)
ax.axvline(overall_rate, color=BRAND_GRAY, linestyle="--", linewidth=1, label=f"Overall avg {overall_rate:.1f}%")
ax.legend(fontsize=9)
save(fig, "01_churn_by_contract")

# ── 5. CHART 2 – Churn by Tenure Group ────────────────────────────────────────
tenure_churn = (
    df.groupby("TenureGroup", observed=True)["Churned"].mean().mul(100)
      .reset_index().rename(columns={"Churned": "ChurnRate"})
)

fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(tenure_churn["TenureGroup"], tenure_churn["ChurnRate"],
        marker="o", color=BRAND_BLUE, linewidth=2.5, markersize=8)
ax.fill_between(tenure_churn["TenureGroup"], tenure_churn["ChurnRate"],
                alpha=0.15, color=BRAND_BLUE)
for _, row in tenure_churn.iterrows():
    ax.text(row["TenureGroup"], row["ChurnRate"] + 1.2, f"{row['ChurnRate']:.1f}%",
            ha="center", fontsize=9, color=BRAND_BLUE, fontweight="bold")
ax.set_ylabel("Churn Rate (%)")
ax.set_title("Churn Rate by Customer Tenure", fontsize=13, fontweight="bold")
ax.set_ylim(0, 65)
ax.axhline(overall_rate, color=BRAND_GRAY, linestyle="--", linewidth=1, label=f"Overall avg {overall_rate:.1f}%")
ax.legend(fontsize=9)
save(fig, "02_churn_by_tenure")

# ── 6. CHART 3 – Churn by Internet Service ────────────────────────────────────
internet_churn = (
    df.groupby("InternetService")["Churned"].mean().mul(100)
      .reset_index().rename(columns={"Churned": "ChurnRate"})
      .sort_values("ChurnRate", ascending=False)
)

fig, ax = plt.subplots(figsize=(6, 4))
colors2 = [BRAND_RED if r > 35 else BRAND_AMBER if r > 15 else BRAND_GREEN
           for r in internet_churn["ChurnRate"]]
bars2 = ax.bar(internet_churn["InternetService"], internet_churn["ChurnRate"], color=colors2, width=0.5)
ax.set_ylabel("Churn Rate (%)")
ax.set_title("Churn Rate by Internet Service Type", fontsize=13, fontweight="bold")
for bar, val in zip(bars2, internet_churn["ChurnRate"]):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
            f"{val:.1f}%", ha="center", fontsize=10, fontweight="bold")
ax.set_ylim(0, 55)
ax.axhline(overall_rate, color=BRAND_GRAY, linestyle="--", linewidth=1, label=f"Overall avg {overall_rate:.1f}%")
ax.legend(fontsize=9)
save(fig, "03_churn_by_internet")

# ── 7. CHART 4 – Churn by Payment Method ─────────────────────────────────────
payment_churn = (
    df.groupby("PaymentMethod")["Churned"].mean().mul(100)
      .reset_index().rename(columns={"Churned": "ChurnRate"})
      .sort_values("ChurnRate", ascending=False)
)
payment_churn["PaymentMethod"] = payment_churn["PaymentMethod"].str.replace(" (automatic)", "\n(auto)", regex=False)

fig, ax = plt.subplots(figsize=(8, 4))
colors3 = [BRAND_RED if r > 35 else BRAND_AMBER if r > 20 else BRAND_GREEN
           for r in payment_churn["ChurnRate"]]
bars3 = ax.bar(payment_churn["PaymentMethod"], payment_churn["ChurnRate"], color=colors3, width=0.5)
ax.set_ylabel("Churn Rate (%)")
ax.set_title("Churn Rate by Payment Method", fontsize=13, fontweight="bold")
for bar, val in zip(bars3, payment_churn["ChurnRate"]):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
            f"{val:.1f}%", ha="center", fontsize=10, fontweight="bold")
ax.set_ylim(0, 58)
ax.axhline(overall_rate, color=BRAND_GRAY, linestyle="--", linewidth=1, label=f"Overall avg {overall_rate:.1f}%")
ax.legend(fontsize=9)
save(fig, "04_churn_by_payment")

# ── 8. CHART 5 – Retention Drivers (Add-ons) ─────────────────────────────────
addons = {
    "Online Security": df[df["OnlineSecurity"]=="Yes"]["Churned"].mean() * 100,
    "Tech Support":    df[df["TechSupport"]=="Yes"]["Churned"].mean() * 100,
    "Online Backup":   df[df["OnlineBackup"]=="Yes"]["Churned"].mean() * 100,
    "No Add-ons\n(Internet)": df[
        (df["OnlineSecurity"]=="No") & (df["TechSupport"]=="No") & (df["InternetService"]!="No")
    ]["Churned"].mean() * 100,
}
addon_df = pd.DataFrame(list(addons.items()), columns=["Service", "ChurnRate"])

fig, ax = plt.subplots(figsize=(7, 4))
bar_colors = [BRAND_GREEN if r < 20 else BRAND_RED for r in addon_df["ChurnRate"]]
bars4 = ax.barh(addon_df["Service"], addon_df["ChurnRate"], color=bar_colors, height=0.45)
ax.set_xlabel("Churn Rate (%)")
ax.set_title("Impact of Value-Added Services on Churn", fontsize=13, fontweight="bold")
for bar, val in zip(bars4, addon_df["ChurnRate"]):
    ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
            f"{val:.1f}%", va="center", fontsize=10)
ax.set_xlim(0, 55)
ax.axvline(overall_rate, color=BRAND_GRAY, linestyle="--", linewidth=1, label=f"Overall avg {overall_rate:.1f}%")
ax.legend(fontsize=9)
save(fig, "05_retention_drivers")

# ── 9. CHART 6 – Monthly Charges Distribution ────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 4))
df[df["Churn"]=="No"]["MonthlyCharges"].plot(kind="kde", ax=ax, color=BRAND_GREEN,
                                               linewidth=2, label="Retained")
df[df["Churn"]=="Yes"]["MonthlyCharges"].plot(kind="kde", ax=ax, color=BRAND_RED,
                                               linewidth=2, label="Churned")
ax.set_xlabel("Monthly Charges ($)")
ax.set_ylabel("Density")
ax.set_title("Monthly Charges Distribution: Churned vs Retained", fontsize=13, fontweight="bold")
ax.legend(fontsize=10)
ax.axvline(df[df["Churn"]=="No"]["MonthlyCharges"].mean(), color=BRAND_GREEN,
           linestyle=":", linewidth=1.5, label=f"Retained avg ${df[df['Churn']=='No']['MonthlyCharges'].mean():.0f}")
ax.axvline(df[df["Churn"]=="Yes"]["MonthlyCharges"].mean(), color=BRAND_RED,
           linestyle=":", linewidth=1.5, label=f"Churned avg ${df[df['Churn']=='Yes']['MonthlyCharges'].mean():.0f}")
ax.legend(fontsize=9)
save(fig, "06_monthly_charges_dist")

# ── 10. CHART 7 – High-Risk Customer Segment Heatmap ─────────────────────────
pivot = df.groupby(["Contract", "InternetService"])["Churned"].mean().mul(100).unstack()

fig, ax = plt.subplots(figsize=(7, 4))
sns.heatmap(pivot, annot=True, fmt=".1f", cmap="RdYlGn_r",
            linewidths=0.5, linecolor="white", ax=ax,
            cbar_kws={"label": "Churn Rate (%)"})
ax.set_title("Churn Rate Heatmap: Contract × Internet Service", fontsize=13, fontweight="bold")
ax.set_xlabel("Internet Service")
ax.set_ylabel("Contract Type")
save(fig, "07_heatmap_contract_internet")

print("\n✅  All charts saved to ./churn_charts/")

# ── 11. SEGMENT SUMMARY TABLE ─────────────────────────────────────────────────
print("\n=== HIGH-RISK SEGMENTS ===")
risk_segments = [
    ("Month-to-month + Fiber + E-check",
     df[(df["Contract"]=="Month-to-month") & (df["InternetService"]=="Fiber optic") &
        (df["PaymentMethod"]=="Electronic check")]),
    ("Month-to-month + No security",
     df[(df["Contract"]=="Month-to-month") & (df["OnlineSecurity"]=="No") &
        (df["InternetService"]!="No")]),
    ("Senior citizens, month-to-month",
     df[(df["SeniorCitizen"]==1) & (df["Contract"]=="Month-to-month")]),
    ("Tenure < 6 months",
     df[df["tenure"] <= 6]),
]

for label, seg in risk_segments:
    rate = seg["Churned"].mean() * 100
    count = len(seg)
    print(f"  {label}: {count:,} customers, {rate:.1f}% churn rate")

print("\n=== RETENTION LEVERS ===")
print(f"  Two-year contract:      {churn_rate(df[df['Contract']=='Two year']['Churned']):.1f}% churn")
print(f"  With online security:   {churn_rate(df[df['OnlineSecurity']=='Yes']['Churned']):.1f}% churn")
print(f"  With tech support:      {churn_rate(df[df['TechSupport']=='Yes']['Churned']):.1f}% churn")
print(f"  Auto payment methods:   {churn_rate(df[df['PaymentMethod'].isin(['Bank transfer (automatic)','Credit card (automatic)'])]['Churned']):.1f}% churn")
print(f"  No partner/dependents:  {churn_rate(df[(df['Partner']=='No') & (df['Dependents']=='No')]['Churned']):.1f}% churn")
