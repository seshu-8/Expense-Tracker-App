"""
data_cleaning.py
----------------
Cleans raw expense data:
  • removes duplicates
  • handles missing values
  • fixes negative amounts
  • validates date formats
  • adds derived columns
"""

import pandas as pd
import numpy as np
import os


def load_raw_data(filepath: str) -> pd.DataFrame:
    """Load raw CSV and show basic info."""
    df = pd.read_csv(filepath, parse_dates=["Date"])
    print(f"📂  Loaded  : {filepath}")
    print(f"    Shape  : {df.shape}")
    print(f"    Columns: {list(df.columns)}\n")
    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    before = len(df)
    df = df.drop_duplicates()
    removed = before - len(df)
    print(f"🔁  Duplicates removed : {removed}")
    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    before = df["Amount"].isna().sum()
    # Fill missing amounts with category median
    df["Amount"] = df.groupby("Category")["Amount"].transform(
        lambda x: x.fillna(x.median())
    )
    print(f"❓  Missing amounts fixed : {before}")
    return df


def fix_negative_amounts(df: pd.DataFrame) -> pd.DataFrame:
    mask  = df["Amount"] < 0
    count = mask.sum()
    df.loc[mask, "Amount"] = df.loc[mask, "Amount"].abs()
    print(f"⚠️   Negative amounts corrected : {count}")
    return df


def validate_and_enrich(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure correct dtypes and add derived columns."""
    df["Date"]       = pd.to_datetime(df["Date"])
    df["Amount"]     = df["Amount"].astype(float).round(2)
    df["Month"]      = df["Date"].dt.strftime("%B")
    df["Month_Num"]  = df["Date"].dt.month
    df["Year"]       = df["Date"].dt.year
    df["Quarter"]    = df["Date"].dt.quarter
    df["Week"]       = df["Date"].dt.isocalendar().week.astype(int)
    df["Day_of_Week"]= df["Date"].dt.strftime("%A")
    df["Is_Weekend"] = df["Date"].dt.dayofweek >= 5

    # Budget flag – example monthly budget ₹30,000
    MONTHLY_BUDGET = 30_000
    monthly_totals = df.groupby(["Year", "Month_Num"])["Amount"].transform("sum")
    df["Over_Budget"] = monthly_totals > MONTHLY_BUDGET

    # Amount bins
    df["Spend_Level"] = pd.cut(
        df["Amount"],
        bins   = [0, 500, 2000, 5000, np.inf],
        labels = ["Low", "Medium", "High", "Very High"],
    )

    print("✅  Enrichment columns added.")
    return df


def generate_quality_report(raw: pd.DataFrame, clean: pd.DataFrame) -> None:
    print("\n" + "=" * 50)
    print("       DATA QUALITY REPORT")
    print("=" * 50)
    print(f"  Raw rows         : {len(raw)}")
    print(f"  Clean rows       : {len(clean)}")
    print(f"  Rows removed     : {len(raw) - len(clean)}")
    print(f"  Null values left : {clean.isnull().sum().sum()}")
    print(f"  Amount range     : ₹{clean['Amount'].min():,.2f}  –  ₹{clean['Amount'].max():,.2f}")
    print(f"  Date range       : {clean['Date'].min().date()}  →  {clean['Date'].max().date()}")
    print("=" * 50 + "\n")


def clean_pipeline(raw_path: str, output_path: str) -> pd.DataFrame:
    raw   = load_raw_data(raw_path)
    df    = raw.copy()
    df    = remove_duplicates(df)
    df    = handle_missing_values(df)
    df    = fix_negative_amounts(df)
    df    = validate_and_enrich(df)
    generate_quality_report(raw, df)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"💾  Cleaned data saved → {output_path}\n")
    return df


if __name__ == "__main__":
    clean_pipeline(
        raw_path    = "data/expenses_raw.csv",
        output_path = "data/expenses_cleaned.csv",
    )
