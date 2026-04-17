"""
dashboard.py
------------
Interactive Streamlit dashboard for the Expense Tracker App.

Run:
    streamlit run dashboard.py
"""

import sys, os
sys.path.insert(0, "src")

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

from src.data_generator import generate_expense_data, introduce_quality_issues
from src.data_cleaning  import clean_pipeline

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="💰 Expense Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

sns.set_theme(style="whitegrid")
MONTH_ORDER = ["January","February","March","April","May","June",
               "July","August","September","October","November","December"]

# ── Data loader (cached) ───────────────────────────────────────────────────────
@st.cache_data
def load_data():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists("data/expenses_cleaned.csv"):
        df_clean = generate_expense_data(num_records=500)
        df_dirty = introduce_quality_issues(df_clean)
        df_clean.to_csv("data/expenses_clean.csv", index=False)
        df_dirty.to_csv("data/expenses_raw.csv",   index=False)
        df = clean_pipeline("data/expenses_raw.csv", "data/expenses_cleaned.csv")
    else:
        df = pd.read_csv("data/expenses_cleaned.csv", parse_dates=["Date"])
    return df

df_full = load_data()

# ── Sidebar filters ────────────────────────────────────────────────────────────
st.sidebar.title("🔧 Filters")

months = st.sidebar.multiselect(
    "Select Month(s)",
    options  = MONTH_ORDER,
    default  = MONTH_ORDER,
)
categories = st.sidebar.multiselect(
    "Select Category(s)",
    options = df_full["Category"].unique().tolist(),
    default = df_full["Category"].unique().tolist(),
)
payment_methods = st.sidebar.multiselect(
    "Payment Method(s)",
    options = df_full["Payment_Method"].unique().tolist(),
    default = df_full["Payment_Method"].unique().tolist(),
)
budget = st.sidebar.number_input("Monthly Budget (₹)", value=30_000, step=1000)

# Apply filters
df = df_full[
    df_full["Month"].isin(months) &
    df_full["Category"].isin(categories) &
    df_full["Payment_Method"].isin(payment_methods)
]

# ── Header ─────────────────────────────────────────────────────────────────────
st.title("💰 Expense Tracker App – Data Science Dashboard")
st.caption("Built with Python · Pandas · Matplotlib · Seaborn · Streamlit")
st.markdown("---")

# ── KPI Cards ──────────────────────────────────────────────────────────────────
total   = df["Amount"].sum()
avg_txn = df["Amount"].mean()
max_txn = df["Amount"].max()
num_txn = len(df)

k1, k2, k3, k4 = st.columns(4)
k1.metric("💸 Total Spend",    f"₹{total:,.0f}")
k2.metric("📋 Transactions",   f"{num_txn:,}")
k3.metric("📊 Avg per Txn",   f"₹{avg_txn:,.0f}")
k4.metric("🔝 Highest Txn",   f"₹{max_txn:,.0f}")

st.markdown("---")

# ── Row 1: Category Pie + Monthly Bar ─────────────────────────────────────────
c1, c2 = st.columns(2)

with c1:
    st.subheader("📊 Category-wise Distribution")
    cat_totals = df.groupby("Category")["Amount"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(cat_totals, labels=cat_totals.index, autopct="%1.1f%%",
           startangle=140, colors=sns.color_palette("Set2", len(cat_totals)))
    ax.set_title("Expense Share by Category")
    st.pyplot(fig)
    plt.close()

with c2:
    st.subheader("📅 Monthly Spending")
    monthly = df.groupby("Month")["Amount"].sum().reindex(MONTH_ORDER).dropna()
    fig, ax = plt.subplots(figsize=(9, 7))
    bars = ax.bar(monthly.index, monthly.values, color=sns.color_palette("Blues_d", len(monthly)))
    ax.axhline(budget, color="red", linestyle="--", linewidth=1.5, label=f"Budget ₹{budget:,}")
    ax.set_title("Monthly Total Expenses")
    ax.tick_params(axis="x", rotation=45)
    ax.legend()
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 100, f"₹{h:,.0f}",
                ha="center", va="bottom", fontsize=7)
    st.pyplot(fig)
    plt.close()

# ── Row 2: Heatmap ─────────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("🗺️ Spending Heatmap – Category × Month")
pivot = df.pivot_table(index="Category", columns="Month_Num", values="Amount", aggfunc="sum").fillna(0)
pivot.columns = [f"M{c}" for c in pivot.columns]
fig, ax = plt.subplots(figsize=(16, 6))
sns.heatmap(pivot, ax=ax, annot=True, fmt=".0f", cmap="YlOrRd", linewidths=0.5)
ax.set_title("Category × Month Heatmap")
st.pyplot(fig)
plt.close()

# ── Row 3: Payment + Day of Week ───────────────────────────────────────────────
st.markdown("---")
c3, c4 = st.columns(2)

with c3:
    st.subheader("💳 Payment Method")
    pay = df.groupby("Payment_Method")["Amount"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(pay, labels=pay.index, autopct="%1.1f%%", startangle=90,
           colors=sns.color_palette("Pastel1", len(pay)), wedgeprops={"width": 0.5})
    ax.set_title("Payment Method Distribution")
    st.pyplot(fig)
    plt.close()

with c4:
    st.subheader("📆 Day-of-Week Spending")
    DOW    = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    day    = df.groupby("Day_of_Week")["Amount"].sum().reindex(DOW)
    colors = ["#FF7043" if d in ["Saturday","Sunday"] else "#42A5F5" for d in DOW]
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(day.index, day.values, color=colors)
    ax.set_title("Spending by Day of Week")
    ax.tick_params(axis="x", rotation=30)
    st.pyplot(fig)
    plt.close()

# ── Budget Analysis ────────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("🎯 Budget Analysis")
mdf = df.groupby(["Month_Num","Month"])["Amount"].sum().reset_index().sort_values("Month_Num")
mdf["Status"] = mdf["Amount"].apply(lambda x: "❌ Over" if x > budget else "✅ Under")
mdf["Variance"] = budget - mdf["Amount"]
mdf = mdf.rename(columns={"Amount":"Actual Spend"})
st.dataframe(mdf[["Month","Actual Spend","Variance","Status"]].style.format(
    {"Actual Spend": "₹{:,.0f}", "Variance": "₹{:,.0f}"}
), use_container_width=True)

# ── Top Transactions ───────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("🔝 Top 10 Transactions")
top = df[["Date","Category","Description","Amount","Payment_Method"]].nlargest(10, "Amount")
st.dataframe(top.style.format({"Amount": "₹{:,.2f}"}), use_container_width=True)

# ── Insights ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("💡 Key Insights")
top_cat    = df.groupby("Category")["Amount"].sum().idxmax()
top_month  = df.groupby("Month")["Amount"].sum().idxmax()
top_pay    = df.groupby("Payment_Method")["Amount"].sum().idxmax()
avg_daily  = df.groupby("Date")["Amount"].sum().mean()

st.info(f"🔵 Highest spending category: **{top_cat}**")
st.info(f"🔵 Most expensive month: **{top_month}**")
st.info(f"🔵 Top payment method: **{top_pay}**")
st.info(f"🔵 Average daily spend: **₹{avg_daily:,.2f}**")

over_months = (df.groupby("Month_Num")["Amount"].sum() > budget).sum()
if over_months > 0:
    st.warning(f"⚠️ {over_months} month(s) exceeded the ₹{budget:,} budget!")
else:
    st.success("✅ All months are within budget!")

st.markdown("---")
st.caption("Expense Tracker App · Built with ❤️ for Placements & Internships")
