"""
analysis.py
-----------
Core analytics for the Expense Tracker:
  • Category-wise spending
  • Monthly trends
  • Payment method distribution
  • Day-of-week patterns
  • Top transactions
  • Budget analysis
  • Correlation & statistical summary
"""

import pandas as pd
import numpy as np


def load_clean_data(filepath: str = "data/expenses_cleaned.csv") -> pd.DataFrame:
    df = pd.read_csv(filepath, parse_dates=["Date"])
    print(f"✅  Data loaded : {df.shape[0]} records\n")
    return df


# ── 1. Summary Statistics ──────────────────────────────────────────────────────
def summary_stats(df: pd.DataFrame) -> pd.DataFrame:
    stats = df["Amount"].describe().rename("Value").to_frame()
    stats.loc["Total Spend"] = df["Amount"].sum()
    stats.loc["Median Spend"] = df["Amount"].median()
    print("📊  Summary Statistics:")
    print(stats.to_string(), "\n")
    return stats


# ── 2. Category Analysis ───────────────────────────────────────────────────────
def category_analysis(df: pd.DataFrame) -> pd.DataFrame:
    cat = (
        df.groupby("Category")["Amount"]
        .agg(Total="sum", Count="count", Average="mean", Max="max")
        .sort_values("Total", ascending=False)
        .round(2)
    )
    cat["% Share"] = (cat["Total"] / cat["Total"].sum() * 100).round(1)
    print("📊  Category-wise Spending:")
    print(cat.to_string(), "\n")
    return cat


# ── 3. Monthly Trends ──────────────────────────────────────────────────────────
def monthly_trends(df: pd.DataFrame) -> pd.DataFrame:
    monthly = (
        df.groupby(["Year", "Month_Num", "Month"])["Amount"]
        .agg(Total="sum", Transactions="count", Avg_Per_Txn="mean")
        .round(2)
        .reset_index()
        .sort_values(["Year", "Month_Num"])
    )
    monthly["MoM_Change_%"] = monthly["Total"].pct_change().mul(100).round(2)
    print("📊  Monthly Trends:")
    print(monthly[["Month", "Total", "Transactions", "MoM_Change_%"]].to_string(index=False), "\n")
    return monthly


# ── 4. Payment Method Analysis ─────────────────────────────────────────────────
def payment_analysis(df: pd.DataFrame) -> pd.DataFrame:
    pay = (
        df.groupby("Payment_Method")["Amount"]
        .agg(Total="sum", Count="count", Avg="mean")
        .sort_values("Total", ascending=False)
        .round(2)
    )
    pay["% Usage"] = (pay["Count"] / pay["Count"].sum() * 100).round(1)
    print("📊  Payment Method Analysis:")
    print(pay.to_string(), "\n")
    return pay


# ── 5. Day-of-Week Spending ────────────────────────────────────────────────────
def day_of_week_analysis(df: pd.DataFrame) -> pd.DataFrame:
    order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    day = (
        df.groupby("Day_of_Week")["Amount"]
        .agg(Total="sum", Count="count", Avg="mean")
        .reindex(order)
        .round(2)
    )
    print("📊  Day-of-Week Spending:")
    print(day.to_string(), "\n")
    return day


# ── 6. Top 10 Transactions ─────────────────────────────────────────────────────
def top_transactions(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    top = (
        df[["Date","Category","Description","Amount","Payment_Method"]]
        .nlargest(n, "Amount")
        .reset_index(drop=True)
    )
    print(f"📊  Top {n} Transactions:")
    print(top.to_string(index=False), "\n")
    return top


# ── 7. Monthly Budget Analysis ────────────────────────────────────────────────
def budget_analysis(df: pd.DataFrame, monthly_budget: float = 30_000) -> pd.DataFrame:
    monthly = df.groupby(["Year","Month_Num","Month"])["Amount"].sum().reset_index()
    monthly.columns = ["Year","Month_Num","Month","Actual_Spend"]
    monthly["Budget"]     = monthly_budget
    monthly["Variance"]   = monthly["Budget"] - monthly["Actual_Spend"]
    monthly["% Used"]     = (monthly["Actual_Spend"] / monthly["Budget"] * 100).round(1)
    monthly["Status"]     = monthly["Variance"].apply(
        lambda v: "✅ Under Budget" if v >= 0 else "❌ Over Budget"
    )
    monthly = monthly.sort_values(["Year","Month_Num"]).reset_index(drop=True)
    print(f"📊  Budget Analysis (Monthly Budget = ₹{monthly_budget:,.0f}):")
    print(monthly[["Month","Actual_Spend","Budget","Variance","% Used","Status"]].to_string(index=False), "\n")
    return monthly


# ── 8. Category × Month Pivot ─────────────────────────────────────────────────
def category_monthly_pivot(df: pd.DataFrame) -> pd.DataFrame:
    pivot = df.pivot_table(
        index="Category", columns="Month_Num", values="Amount", aggfunc="sum"
    ).fillna(0).round(2)
    pivot.columns = [f"Month-{c}" for c in pivot.columns]
    print("📊  Category × Month Pivot (first 5 rows):")
    print(pivot.head().to_string(), "\n")
    return pivot


# ── 9. Insights Generator ─────────────────────────────────────────────────────
def generate_insights(df: pd.DataFrame, monthly_budget: float = 30_000) -> list:
    insights = []

    top_cat    = df.groupby("Category")["Amount"].sum().idxmax()
    top_amount = df.groupby("Category")["Amount"].sum().max()
    insights.append(f"💡 Highest spending category: {top_cat} (₹{top_amount:,.0f})")

    top_month  = df.groupby("Month")["Amount"].sum().idxmax()
    insights.append(f"💡 Most expensive month: {top_month}")

    top_day    = df.groupby("Day_of_Week")["Amount"].sum().idxmax()
    insights.append(f"💡 Most spending day: {top_day}")

    top_pay    = df.groupby("Payment_Method")["Amount"].sum().idxmax()
    insights.append(f"💡 Most used payment method by value: {top_pay}")

    avg_daily  = df.groupby("Date")["Amount"].sum().mean()
    insights.append(f"💡 Average daily spend: ₹{avg_daily:,.2f}")

    monthly_totals = df.groupby("Month_Num")["Amount"].sum()
    over_budget    = (monthly_totals > monthly_budget).sum()
    insights.append(f"💡 Months over budget: {over_budget} out of {len(monthly_totals)}")

    weekend = df[df["Is_Weekend"]]["Amount"].mean()
    weekday = df[~df["Is_Weekend"]]["Amount"].mean()
    if weekend > weekday:
        insights.append(f"💡 You spend more on weekends (₹{weekend:,.0f} avg) vs weekdays (₹{weekday:,.0f} avg)")
    else:
        insights.append(f"💡 Weekday spending (₹{weekday:,.0f}) exceeds weekend (₹{weekend:,.0f})")

    print("🔍  Key Insights:")
    for i in insights:
        print(f"   {i}")
    print()
    return insights


# ── Run All ────────────────────────────────────────────────────────────────────
def run_full_analysis(filepath: str = "data/expenses_cleaned.csv") -> dict:
    df = load_clean_data(filepath)
    return {
        "df":             df,
        "summary":        summary_stats(df),
        "category":       category_analysis(df),
        "monthly":        monthly_trends(df),
        "payment":        payment_analysis(df),
        "day_of_week":    day_of_week_analysis(df),
        "top_txns":       top_transactions(df),
        "budget":         budget_analysis(df),
        "pivot":          category_monthly_pivot(df),
        "insights":       generate_insights(df),
    }


if __name__ == "__main__":
    results = run_full_analysis()
