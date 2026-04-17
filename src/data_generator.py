"""
data_generator.py
-----------------
Generates synthetic expense data for the Expense Tracker App.
Simulates 12 months of realistic personal/business expenses.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# ── Reproducibility ────────────────────────────────────────────────────────────
np.random.seed(42)
random.seed(42)

# ── Configuration ──────────────────────────────────────────────────────────────
CATEGORIES = {
    "Food & Dining":   {"min": 200,  "max": 800,  "freq": 20},
    "Transportation":  {"min": 100,  "max": 500,  "freq": 15},
    "Rent & Housing":  {"min": 8000, "max": 15000, "freq": 1},
    "Shopping":        {"min": 500,  "max": 3000, "freq": 8},
    "Entertainment":   {"min": 200,  "max": 1500, "freq": 6},
    "Healthcare":      {"min": 300,  "max": 2000, "freq": 3},
    "Education":       {"min": 500,  "max": 5000, "freq": 2},
    "Utilities":       {"min": 500,  "max": 2000, "freq": 4},
    "Travel":          {"min": 2000, "max": 20000, "freq": 2},
    "Miscellaneous":   {"min": 100,  "max": 1000, "freq": 5},
}

PAYMENT_METHODS = ["Credit Card", "Debit Card", "UPI", "Cash", "Net Banking"]

DESCRIPTIONS = {
    "Food & Dining":   ["Zomato order", "Restaurant dinner", "Grocery shopping",
                        "Coffee shop", "Swiggy delivery", "Supermarket"],
    "Transportation":  ["Uber ride", "Ola cab", "Metro card recharge",
                        "Petrol", "Auto rickshaw", "Bus pass"],
    "Rent & Housing":  ["Monthly rent", "Maintenance charges", "Electricity bill",
                        "Broadband bill", "Water charges"],
    "Shopping":        ["Amazon purchase", "Flipkart order", "Clothing store",
                        "Electronics", "Home decor", "Books"],
    "Entertainment":   ["Netflix subscription", "Movie tickets", "Spotify",
                        "Gaming", "OTT platform", "Concert"],
    "Healthcare":      ["Doctor consultation", "Medicine purchase", "Lab test",
                        "Gym membership", "Pharmacy", "Health insurance"],
    "Education":       ["Online course", "Books & stationery", "Coaching fees",
                        "Udemy course", "Certification exam"],
    "Utilities":       ["Mobile recharge", "DTH recharge", "Gas cylinder",
                        "Internet bill", "Electricity"],
    "Travel":          ["Flight tickets", "Hotel booking", "Train tickets",
                        "Cab booking", "Travel insurance", "Sightseeing"],
    "Miscellaneous":   ["Charity donation", "Gift purchase", "Bank charges",
                        "ATM withdrawal", "Other expense"],
}


def generate_expense_data(
    start_date: str = "2024-01-01",
    end_date: str = "2024-12-31",
    num_records: int = 500,
) -> pd.DataFrame:
    """Generate a synthetic expense DataFrame."""

    start = datetime.strptime(start_date, "%Y-%m-%d")
    end   = datetime.strptime(end_date,   "%Y-%m-%d")
    total_days = (end - start).days

    records = []
    for _ in range(num_records):
        # Random date within range
        rand_days = random.randint(0, total_days)
        date = start + timedelta(days=rand_days)

        # Weighted category selection (higher freq → more likely)
        cats   = list(CATEGORIES.keys())
        weights = [CATEGORIES[c]["freq"] for c in cats]
        cat    = random.choices(cats, weights=weights, k=1)[0]

        cfg    = CATEGORIES[cat]
        amount = round(random.uniform(cfg["min"], cfg["max"]), 2)

        # Add seasonal spikes
        month = date.month
        if cat == "Travel" and month in [4, 5, 10, 11, 12]:
            amount = round(amount * random.uniform(1.3, 2.0), 2)
        if cat == "Shopping" and month in [10, 11]:         # Festive season
            amount = round(amount * random.uniform(1.5, 2.5), 2)
        if cat == "Entertainment" and month in [12, 1]:
            amount = round(amount * random.uniform(1.2, 1.8), 2)

        payment = random.choice(PAYMENT_METHODS)
        desc    = random.choice(DESCRIPTIONS[cat])

        records.append({
            "Date":           date.strftime("%Y-%m-%d"),
            "Category":       cat,
            "Description":    desc,
            "Amount":         amount,
            "Payment_Method": payment,
            "Month":          date.strftime("%B"),
            "Month_Num":      date.month,
            "Year":           date.year,
            "Day_of_Week":    date.strftime("%A"),
        })

    df = pd.DataFrame(records).sort_values("Date").reset_index(drop=True)
    df.index = df.index + 1  # 1-based index
    return df


def introduce_quality_issues(df: pd.DataFrame) -> pd.DataFrame:
    """Introduce minor data-quality issues for cleaning demo."""
    df_dirty = df.copy()
    n = len(df_dirty)

    # ~3 % missing amounts
    missing_idx = random.sample(range(n), k=int(n * 0.03))
    df_dirty.loc[missing_idx, "Amount"] = np.nan

    # ~2 % duplicate rows
    dup_idx = random.sample(range(n), k=int(n * 0.02))
    dups    = df_dirty.iloc[dup_idx]
    df_dirty = pd.concat([df_dirty, dups], ignore_index=True)

    # ~1 % negative amounts (data-entry errors)
    neg_idx = random.sample(range(len(df_dirty)), k=int(n * 0.01))
    df_dirty.loc[neg_idx, "Amount"] = df_dirty.loc[neg_idx, "Amount"].apply(
        lambda x: -abs(x) if pd.notna(x) else x
    )

    return df_dirty.sample(frac=1, random_state=42).reset_index(drop=True)


if __name__ == "__main__":
    # Generate clean data
    df_clean = generate_expense_data(num_records=500)

    # Generate dirty version for cleaning demonstration
    df_dirty = introduce_quality_issues(df_clean)

    # Save both
    os.makedirs("data", exist_ok=True)
    df_clean.to_csv("data/expenses_clean.csv", index=False)
    df_dirty.to_csv("data/expenses_raw.csv",   index=False)

    print(f"✅  Clean dataset : {len(df_clean)} rows  → data/expenses_clean.csv")
    print(f"✅  Raw   dataset : {len(df_dirty)} rows  → data/expenses_raw.csv")
    print("\nSample records:")
    print(df_clean.head(5).to_string())
