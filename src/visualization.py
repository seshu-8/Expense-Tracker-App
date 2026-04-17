"""
visualization.py
----------------
Generates and saves all charts for the Expense Tracker project.
Charts saved in outputs/ folder for GitHub proof.
"""

import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")          # headless – no display required
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

# ── Style ──────────────────────────────────────────────────────────────────────
sns.set_theme(style="whitegrid", palette="muted")
PALETTE   = "Set2"
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

MONTH_ORDER = [
    "January","February","March","April","May","June",
    "July","August","September","October","November","December",
]

rupee_fmt = mticker.FuncFormatter(lambda x, _: f"₹{x:,.0f}")


def _save(fig: plt.Figure, name: str) -> str:
    path = os.path.join(OUTPUT_DIR, name)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  💾  Saved → {path}")
    return path


# ── 1. Category Pie Chart ──────────────────────────────────────────────────────
def plot_category_pie(df: pd.DataFrame) -> str:
    cat_totals = df.groupby("Category")["Amount"].sum().sort_values(ascending=False)
    fig, ax    = plt.subplots(figsize=(9, 9))
    wedges, texts, autotexts = ax.pie(
        cat_totals,
        labels     = cat_totals.index,
        autopct    = "%1.1f%%",
        startangle = 140,
        colors     = sns.color_palette(PALETTE, len(cat_totals)),
        pctdistance= 0.82,
    )
    for at in autotexts:
        at.set_fontsize(9)
    ax.set_title("Category-wise Expense Distribution", fontsize=16, fontweight="bold", pad=20)
    return _save(fig, "01_category_pie.png")


# ── 2. Monthly Bar Chart ───────────────────────────────────────────────────────
def plot_monthly_bar(df: pd.DataFrame) -> str:
    monthly = (
        df.groupby("Month")["Amount"].sum()
        .reindex(MONTH_ORDER)
        .dropna()
        .reset_index()
    )
    monthly.columns = ["Month", "Total"]
    fig, ax = plt.subplots(figsize=(14, 6))
    bars    = ax.bar(monthly["Month"], monthly["Total"],
                     color=sns.color_palette("Blues_d", len(monthly)))
    ax.set_title("Monthly Total Expenses", fontsize=16, fontweight="bold")
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Amount (₹)")
    ax.yaxis.set_major_formatter(rupee_fmt)
    ax.tick_params(axis="x", rotation=45)
    # Value labels
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 200,
                f"₹{h:,.0f}", ha="center", va="bottom", fontsize=8)
    # Budget line
    BUDGET = 30_000
    ax.axhline(BUDGET, color="red", linestyle="--", linewidth=1.5, label=f"Budget ₹{BUDGET:,}")
    ax.legend()
    return _save(fig, "02_monthly_bar.png")


# ── 3. Category Bar Chart ─────────────────────────────────────────────────────
def plot_category_bar(df: pd.DataFrame) -> str:
    cat = df.groupby("Category")["Amount"].sum().sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.barh(cat.index, cat.values,
            color=sns.color_palette("Set3", len(cat)))
    ax.set_title("Category-wise Total Spending", fontsize=16, fontweight="bold")
    ax.set_xlabel("Total Amount (₹)")
    ax.xaxis.set_major_formatter(rupee_fmt)
    for i, (idx, val) in enumerate(cat.items()):
        ax.text(val + 200, i, f"₹{val:,.0f}", va="center", fontsize=9)
    return _save(fig, "03_category_bar.png")


# ── 4. Line Chart – Monthly Trend ─────────────────────────────────────────────
def plot_monthly_trend_line(df: pd.DataFrame) -> str:
    monthly = (
        df.groupby(["Month_Num", "Month"])["Amount"].sum()
        .reset_index()
        .sort_values("Month_Num")
    )
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(monthly["Month"], monthly["Amount"], marker="o", linewidth=2.5,
            color="#2196F3", markersize=8, label="Monthly Spend")
    ax.fill_between(monthly["Month"], monthly["Amount"], alpha=0.15, color="#2196F3")
    ax.axhline(30_000, color="red", linestyle="--", linewidth=1.5, label="Budget ₹30,000")
    ax.set_title("Monthly Expense Trend", fontsize=16, fontweight="bold")
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Amount (₹)")
    ax.yaxis.set_major_formatter(rupee_fmt)
    ax.tick_params(axis="x", rotation=45)
    ax.legend()
    return _save(fig, "04_monthly_trend_line.png")


# ── 5. Heatmap – Category × Month ────────────────────────────────────────────
def plot_category_month_heatmap(df: pd.DataFrame) -> str:
    pivot = df.pivot_table(
        index="Category", columns="Month_Num", values="Amount", aggfunc="sum"
    ).fillna(0)
    pivot.columns = [f"M{c}" for c in pivot.columns]
    fig, ax = plt.subplots(figsize=(16, 7))
    sns.heatmap(
        pivot, ax=ax, annot=True, fmt=".0f",
        cmap="YlOrRd", linewidths=0.5, linecolor="white",
        cbar_kws={"format": rupee_fmt},
    )
    ax.set_title("Category × Month Spending Heatmap", fontsize=16, fontweight="bold")
    ax.set_xlabel("Month Number")
    ax.set_ylabel("Category")
    return _save(fig, "05_category_month_heatmap.png")


# ── 6. Payment Method Donut ────────────────────────────────────────────────────
def plot_payment_donut(df: pd.DataFrame) -> str:
    pay = df.groupby("Payment_Method")["Amount"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(
        pay, labels=pay.index, autopct="%1.1f%%", startangle=90,
        colors=sns.color_palette("Pastel1", len(pay)),
        wedgeprops={"width": 0.5},
    )
    for at in autotexts:
        at.set_fontsize(10)
    ax.set_title("Payment Method Distribution", fontsize=16, fontweight="bold")
    return _save(fig, "06_payment_donut.png")


# ── 7. Box Plot – Amount by Category ─────────────────────────────────────────
def plot_boxplot_category(df: pd.DataFrame) -> str:
    order = df.groupby("Category")["Amount"].median().sort_values(ascending=False).index
    fig, ax = plt.subplots(figsize=(14, 7))
    sns.boxplot(data=df, x="Category", y="Amount", order=order,
                palette=PALETTE, ax=ax)
    ax.set_title("Spending Distribution per Category", fontsize=16, fontweight="bold")
    ax.set_xlabel("Category")
    ax.set_ylabel("Amount (₹)")
    ax.yaxis.set_major_formatter(rupee_fmt)
    ax.tick_params(axis="x", rotation=45)
    return _save(fig, "07_boxplot_category.png")


# ── 8. Day-of-Week Bar ────────────────────────────────────────────────────────
def plot_day_of_week(df: pd.DataFrame) -> str:
    order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    day   = df.groupby("Day_of_Week")["Amount"].sum().reindex(order)
    colors = ["#FF7043" if d in ["Saturday","Sunday"] else "#42A5F5" for d in order]
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(day.index, day.values, color=colors)
    ax.set_title("Spending by Day of Week", fontsize=16, fontweight="bold")
    ax.set_ylabel("Total Amount (₹)")
    ax.yaxis.set_major_formatter(rupee_fmt)
    from matplotlib.patches import Patch
    legend = [Patch(facecolor="#42A5F5", label="Weekday"),
              Patch(facecolor="#FF7043", label="Weekend")]
    ax.legend(handles=legend)
    return _save(fig, "08_day_of_week.png")


# ── 9. Budget vs Actual Bar ───────────────────────────────────────────────────
def plot_budget_vs_actual(df: pd.DataFrame, budget: float = 30_000) -> str:
    monthly = (
        df.groupby(["Month_Num", "Month"])["Amount"].sum()
        .reset_index().sort_values("Month_Num")
    )
    x   = np.arange(len(monthly))
    w   = 0.35
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.bar(x - w/2, [budget]*len(monthly), w, label="Budget", color="#66BB6A", alpha=0.85)
    ax.bar(x + w/2, monthly["Amount"],      w, label="Actual",
           color=["#EF5350" if a > budget else "#42A5F5" for a in monthly["Amount"]])
    ax.set_xticks(x)
    ax.set_xticklabels(monthly["Month"], rotation=45)
    ax.set_title("Budget vs Actual Monthly Spending", fontsize=16, fontweight="bold")
    ax.set_ylabel("Amount (₹)")
    ax.yaxis.set_major_formatter(rupee_fmt)
    ax.legend()
    return _save(fig, "09_budget_vs_actual.png")


# ── 10. Cumulative Spend ──────────────────────────────────────────────────────
def plot_cumulative_spend(df: pd.DataFrame) -> str:
    daily = df.groupby("Date")["Amount"].sum().sort_index().cumsum()
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(daily.index, daily.values, linewidth=2.5, color="#AB47BC")
    ax.fill_between(daily.index, daily.values, alpha=0.2, color="#AB47BC")
    ax.set_title("Cumulative Expense Over the Year", fontsize=16, fontweight="bold")
    ax.set_xlabel("Date")
    ax.set_ylabel("Cumulative Amount (₹)")
    ax.yaxis.set_major_formatter(rupee_fmt)
    return _save(fig, "10_cumulative_spend.png")


# ── Generate All ──────────────────────────────────────────────────────────────
def generate_all_charts(filepath: str = "data/expenses_cleaned.csv") -> None:
    df = pd.read_csv(filepath, parse_dates=["Date"])
    print("\n🎨  Generating all charts …\n")
    plot_category_pie(df)
    plot_monthly_bar(df)
    plot_category_bar(df)
    plot_monthly_trend_line(df)
    plot_category_month_heatmap(df)
    plot_payment_donut(df)
    plot_boxplot_category(df)
    plot_day_of_week(df)
    plot_budget_vs_actual(df)
    plot_cumulative_spend(df)
    print(f"\n✅  All charts saved in '{OUTPUT_DIR}/' folder.\n")


if __name__ == "__main__":
    generate_all_charts()
