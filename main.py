"""
main.py
-------
Entry point for the Expense Tracker App.
Runs the full pipeline in order:
  1. Generate synthetic data
  2. Clean data
  3. Analyse
  4. Visualise
  5. Generate reports

Usage:
    python main.py
"""

import sys
import os

# Ensure src/ is on the path when run from project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from src.data_generator  import generate_expense_data, introduce_quality_issues
from src.data_cleaning   import clean_pipeline
from src.analysis        import run_full_analysis
from src.visualization   import generate_all_charts
from src.report_generator import run_reports


BANNER = """
╔══════════════════════════════════════════════════════╗
║           EXPENSE TRACKER APP – DATA SCIENCE         ║
║          Built for Placements & Internships          ║
╚══════════════════════════════════════════════════════╝
"""


def main():
    print(BANNER)

    # ── Step 1 : Generate data ────────────────────────────────────────────────
    print("━" * 55)
    print("  STEP 1 │ Generating Synthetic Expense Data")
    print("━" * 55)
    os.makedirs("data", exist_ok=True)
    df_clean = generate_expense_data(num_records=500)
    df_dirty = introduce_quality_issues(df_clean)
    df_clean.to_csv("data/expenses_clean.csv",  index=False)
    df_dirty.to_csv("data/expenses_raw.csv",    index=False)
    print(f"  ✅  Clean : {len(df_clean)} rows  |  Raw : {len(df_dirty)} rows\n")

    # ── Step 2 : Clean data ───────────────────────────────────────────────────
    print("━" * 55)
    print("  STEP 2 │ Cleaning & Enriching Data")
    print("━" * 55)
    df = clean_pipeline(
        raw_path    = "data/expenses_raw.csv",
        output_path = "data/expenses_cleaned.csv",
    )

    # ── Step 3 : Analyse ──────────────────────────────────────────────────────
    print("━" * 55)
    print("  STEP 3 │ Running Analysis")
    print("━" * 55)
    results = run_full_analysis("data/expenses_cleaned.csv")

    # ── Step 4 : Visualise ────────────────────────────────────────────────────
    print("━" * 55)
    print("  STEP 4 │ Generating Charts")
    print("━" * 55)
    generate_all_charts("data/expenses_cleaned.csv")

    # ── Step 5 : Reports ──────────────────────────────────────────────────────
    print("━" * 55)
    print("  STEP 5 │ Generating Reports")
    print("━" * 55)
    run_reports("data/expenses_cleaned.csv")

    # ── Done ──────────────────────────────────────────────────────────────────
    print("━" * 55)
    print("  ✅  PROJECT COMPLETE!")
    print("  📁  Check the following folders for outputs:")
    print("       data/       → CSV datasets")
    print("       outputs/    → charts (.png) + reports (.txt, .xlsx)")
    print("━" * 55)


if __name__ == "__main__":
    main()
