"""
report_generator.py
-------------------
Generates a clean text + CSV summary report of expense analysis.
Saves to outputs/expense_report.txt and outputs/summary_tables.xlsx
"""

import os
import pandas as pd
from datetime import datetime
from analysis import run_full_analysis

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_text_report(results: dict) -> str:
    df       = results["df"]
    insights = results["insights"]
    budget   = results["budget"]
    cat      = results["category"]
    monthly  = results["monthly"]

    sep  = "=" * 65
    sep2 = "-" * 65

    lines = [
        sep,
        "         EXPENSE TRACKER APP – ANNUAL REPORT",
        f"         Generated : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        sep,
        "",
        "OVERVIEW",
        sep2,
        f"  Total Records     : {len(df):,}",
        f"  Date Range        : {df['Date'].min().date()}  →  {df['Date'].max().date()}",
        f"  Total Expenditure : ₹{df['Amount'].sum():>12,.2f}",
        f"  Average per Txn   : ₹{df['Amount'].mean():>12,.2f}",
        f"  Highest Txn       : ₹{df['Amount'].max():>12,.2f}",
        f"  Lowest  Txn       : ₹{df['Amount'].min():>12,.2f}",
        "",
        "CATEGORY-WISE SPENDING",
        sep2,
    ]

    for _, row in cat.iterrows():
        lines.append(
            f"  {row.name:<22} ₹{row['Total']:>10,.0f}   ({row['% Share']}%)"
        )

    lines += [
        "",
        "MONTHLY SUMMARY",
        sep2,
    ]
    for _, row in monthly.iterrows():
        chg = f"{row['MoM_Change_%']:+.1f}%" if pd.notna(row["MoM_Change_%"]) else "  N/A"
        lines.append(
            f"  {row['Month']:<12} ₹{row['Total']:>10,.0f}   Txns: {int(row['Transactions']):>3}   MoM: {chg}"
        )

    lines += [
        "",
        "BUDGET ANALYSIS  (Monthly Budget = ₹30,000)",
        sep2,
    ]
    for _, row in budget.iterrows():
        lines.append(
            f"  {row['Month']:<12} Spent ₹{row['Actual_Spend']:>9,.0f}   "
            f"Variance ₹{row['Variance']:>+9,.0f}   {row['Status']}"
        )

    lines += [
        "",
        "KEY INSIGHTS",
        sep2,
    ]
    for ins in insights:
        lines.append(f"  {ins}")

    lines += ["", sep, "  END OF REPORT", sep]

    report_text = "\n".join(lines)
    path = os.path.join(OUTPUT_DIR, "expense_report.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(report_text)
    print(f"📄  Text report saved → {path}")
    return path


def generate_excel_summary(results: dict) -> str:
    path = os.path.join(OUTPUT_DIR, "summary_tables.xlsx")
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        results["category"].to_excel(writer,   sheet_name="Category Analysis")
        results["monthly"].to_excel(writer,    sheet_name="Monthly Trends",   index=False)
        results["payment"].to_excel(writer,    sheet_name="Payment Methods")
        results["day_of_week"].to_excel(writer,sheet_name="Day of Week")
        results["top_txns"].to_excel(writer,   sheet_name="Top Transactions", index=False)
        results["budget"].to_excel(writer,     sheet_name="Budget Analysis",  index=False)
        results["pivot"].to_excel(writer,      sheet_name="Category x Month Pivot")
    print(f"📊  Excel report saved → {path}")
    return path


def run_reports(filepath: str = "data/expenses_cleaned.csv") -> None:
    results = run_full_analysis(filepath)
    generate_text_report(results)
    generate_excel_summary(results)
    print("\n✅  All reports generated.\n")


if __name__ == "__main__":
    run_reports()
