# 💰 Expense Tracker App — Data Science Project

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)](https://python.org)
[![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458?logo=pandas)](https://pandas.pydata.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

> **A complete, placement-ready Data Science project** that tracks, analyses, and visualises personal/business expenses using synthetic data, Pandas, Matplotlib, Seaborn, and an interactive Streamlit dashboard.

---

## 📌 Table of Contents
- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Solution](#solution)
- [Project Architecture](#project-architecture)
- [Tech Stack](#tech-stack)
- [Folder Structure](#folder-structure)
- [Installation](#installation)
- [How to Run](#how-to-run)
- [Features](#features)
- [Charts & Outputs](#charts--outputs)
- [Key Insights Generated](#key-insights-generated)
- [Future Improvements](#future-improvements)
- [Interview Q&A](#interview-qa)

---

## 📖 Overview

The **Expense Tracker App** is a data-science project that simulates one year of personal expenses across 10 categories. It demonstrates the full analytics pipeline:

```
Data Generation → Cleaning → EDA → Feature Engineering → Visualisation → Insights → Dashboard
```

It is designed to be **beginner-friendly but professional**—ideal for Data Analyst, Business Analyst, and Financial Analyst placement portfolios.

---

## ❓ Problem Statement

- People and businesses often lose track of where money is being spent.
- Without analysis, overspending goes undetected until it is too late.
- Manual spreadsheets are error-prone and give no visual insights.

---

## ✅ Solution

An automated Python pipeline that:
1. **Generates** 500 synthetic expense records with realistic patterns.
2. **Cleans** data (removes duplicates, fixes nulls & negatives).
3. **Analyses** spending by category, month, day, and payment method.
4. **Visualises** results with 10 professional charts.
5. **Detects** budget overruns and generates text insights.
6. **Displays** everything in an interactive Streamlit dashboard.

---

## 🏗️ Project Architecture

```
Raw Data (CSV)
      │
      ▼
Data Cleaning & Enrichment
  - Remove duplicates
  - Fill missing values (category median)
  - Fix negative amounts
  - Add: Quarter, Week, Is_Weekend, Spend_Level
      │
      ▼
Exploratory Data Analysis
  - Summary statistics
  - Category / Monthly / Day-of-Week breakdowns
  - Budget vs Actual comparison
  - Pivot tables
      │
      ▼
Visualisation (10 Charts)
  - Pie, Bar, Line, Heatmap, Box, Donut
      │
      ▼
Reports & Dashboard
  - expense_report.txt
  - summary_tables.xlsx
  - Streamlit interactive dashboard
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.9+ | Core language |
| Pandas | Data manipulation |
| NumPy | Numerical operations |
| Matplotlib | Static charts |
| Seaborn | Statistical visualisations |
| Streamlit | Interactive dashboard |
| OpenPyXL | Excel report generation |
| Jupyter | Notebook-based EDA |

---

## 📁 Folder Structure

```
Expense-Tracker-App/
│
├── data/
│   ├── expenses_clean.csv       ← Original synthetic data
│   ├── expenses_raw.csv         ← Data with quality issues (for demo)
│   └── expenses_cleaned.csv     ← Final cleaned dataset
│
├── notebooks/
│   └── expense_eda.ipynb        ← Full EDA notebook
│
├── src/
│   ├── data_generator.py        ← Synthetic data creation
│   ├── data_cleaning.py         ← Cleaning pipeline
│   ├── analysis.py              ← All analytics functions
│   ├── visualization.py         ← Chart generation
│   └── report_generator.py      ← Text + Excel reports
│
├── outputs/
│   ├── 01_category_pie.png
│   ├── 02_monthly_bar.png
│   ├── 03_category_bar.png
│   ├── 04_monthly_trend_line.png
│   ├── 05_category_month_heatmap.png
│   ├── 06_payment_donut.png
│   ├── 07_boxplot_category.png
│   ├── 08_day_of_week.png
│   ├── 09_budget_vs_actual.png
│   ├── 10_cumulative_spend.png
│   ├── expense_report.txt
│   └── summary_tables.xlsx
│
├── images/                      ← Screenshots for README
├── dashboard.py                 ← Streamlit dashboard
├── main.py                      ← One-click pipeline runner
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/Expense-Tracker-App.git
cd Expense-Tracker-App
```

### 2. Create a virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## ▶️ How to Run

### Option A — Full pipeline (one command)
```bash
python main.py
```
This generates data, cleans it, runs analysis, creates all 10 charts, and writes reports.

### Option B — Step by step
```bash
# 1. Generate data
python src/data_generator.py

# 2. Clean data
python src/data_cleaning.py

# 3. Analyse
python src/analysis.py

# 4. Visualise
python src/visualization.py

# 5. Reports
python src/report_generator.py
```

### Option C — Streamlit Dashboard
```bash
streamlit run dashboard.py
```
Opens at `http://localhost:8501` in your browser.

### Option D — Jupyter Notebook
```bash
jupyter notebook notebooks/expense_eda.ipynb
```

---

## 🌟 Features

| Feature | Description |
|---|---|
| 🎲 Synthetic Data | 500 realistic expense records across 10 categories |
| 🧹 Data Cleaning | Handles duplicates, nulls, and negative values |
| 📊 10 Charts | Pie, Bar, Line, Heatmap, Box, Donut, Cumulative |
| 🎯 Budget Alerts | Flags months that exceed ₹30,000 budget |
| 💡 Auto Insights | Generates 7+ text insights automatically |
| 📄 Reports | Text report + multi-sheet Excel workbook |
| 📱 Dashboard | Interactive Streamlit app with sidebar filters |
| 📓 EDA Notebook | Step-by-step Jupyter analysis notebook |

---

## 📈 Charts & Outputs

| # | Chart | What it shows |
|---|---|---|
| 1 | Category Pie | Spending share by category |
| 2 | Monthly Bar | Month-wise totals with budget line |
| 3 | Category Bar (H) | Horizontal ranking of categories |
| 4 | Monthly Line | Trend over 12 months |
| 5 | Heatmap | Category × Month matrix |
| 6 | Payment Donut | How money was paid |
| 7 | Box Plot | Spending distribution per category |
| 8 | Day of Week | Weekday vs weekend patterns |
| 9 | Budget vs Actual | Side-by-side monthly comparison |
| 10 | Cumulative | Running total throughout the year |

---

## 💡 Key Insights Generated

- Highest spending category identified automatically
- Most expensive month detected
- Months exceeding budget flagged
- Weekend vs weekday spending compared
- Top payment method by transaction value
- Average daily spending calculated
- Month-over-Month change tracked

---

## 🚀 Future Improvements

- [ ] Mobile app (Flutter / React Native)
- [ ] Real-time expense entry (Google Sheets API)
- [ ] AI-based spending prediction (LSTM / Prophet)
- [ ] Smart budget alerts (email / SMS notifications)
- [ ] Financial goal tracker
- [ ] Multi-user / family expense splitting
- [ ] Bank statement PDF parser

---

## 🎤 Interview Q&A

**Q1: What is this project about?**  
A: It tracks and analyses personal expenses using Python and Data Science. It generates synthetic data, cleans it, performs EDA, visualises spending patterns, and provides actionable financial insights.

**Q2: Why synthetic data?**  
A: Real financial data is private. Synthetic data lets us simulate realistic scenarios with full control—useful for learning and demonstration.

**Q3: How does data cleaning work?**  
A: We remove duplicates, fill missing amounts with category medians, and convert negative amounts to positive (data-entry errors).

**Q4: Which chart did you find most insightful?**  
A: The Category × Month Heatmap—it immediately shows seasonal spending spikes, such as Travel in festival months and Shopping during Diwali.

**Q5: How would you extend this for a real company?**  
A: Connect it to a live database, add role-based access, implement anomaly detection for fraud, and integrate with ERP systems like SAP or Tally.

---

## 📄 License

MIT License — free to use, modify, and share.

---

## 👤 Author

**KONIJETI VENKATA SESHU BABU**   
[LinkedIn](https://www.linkedin.com/in/seshu-babu-konijeti-74968b2b9?utm_source=share_via&utm_content=profile&utm_medium=member_android) · 

---

