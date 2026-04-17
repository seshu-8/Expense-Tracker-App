# 📤 GitHub Upload Guide — Expense Tracker App

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Fill in:
   - **Repository name:** `Expense-Tracker-App`
   - **Description:** `💰 A Data Science project for tracking, analysing, and visualising expenses using Python, Pandas, Matplotlib, Seaborn & Streamlit.`
   - **Visibility:** Public
   - **DO NOT** initialise with README (we have our own)
3. Click **Create repository**

---

## Step 2: Initialise Git Locally

```bash
# Navigate to project folder
cd Expense-Tracker-App

# Initialise git
git init

# Add all files
git add .

# First commit
git commit -m "🎉 Initial commit: Complete Expense Tracker Data Science project"
```

---

## Step 3: Connect & Push

```bash
# Connect to GitHub (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/Expense-Tracker-App.git

# Push
git branch -M main
git push -u origin main
```

---

## Step 4: Create .gitignore

Create a `.gitignore` file:

```
__pycache__/
*.pyc
.env
venv/
.venv/
*.egg-info/
.DS_Store
```

---

## Step 5: Day-wise Commit Plan (for proof)

### Day 1 — Setup
```bash
git add requirements.txt README.md
git commit -m "📦 Day 1: Project setup, requirements, README"
git push
```

### Day 2 — Data
```bash
git add src/data_generator.py data/
git commit -m "🎲 Day 2: Synthetic data generator (500 records, 10 categories)"
git push
```

### Day 3 — Cleaning + Analysis
```bash
git add src/data_cleaning.py src/analysis.py
git commit -m "🧹 Day 3: Data cleaning pipeline + full analysis module"
git push
```

### Day 4 — Visualisation + Reports
```bash
git add src/visualization.py src/report_generator.py outputs/
git commit -m "📊 Day 4: 10 charts, text report, Excel summary"
git push
```

### Day 5 — Dashboard + Final
```bash
git add dashboard.py notebooks/ main.py
git commit -m "🚀 Day 5: Streamlit dashboard + EDA notebook + main pipeline"
git push
```

---

## Step 6: Add Repository Topics (Tags)

In GitHub repo → ⚙️ Settings → Topics, add:
```
python, data-science, pandas, matplotlib, seaborn, streamlit,
expense-tracker, data-analysis, financial-analysis, portfolio-project,
data-visualization, eda, synthetic-data, placement-project
```

---

## Step 7: Pin the Repository

Go to your GitHub profile → Click "Customize your pins" → Add `Expense-Tracker-App`.

---

## Proof Checklist ✅

- [ ] Repo is public and visible
- [ ] README has badges, screenshots, and usage guide
- [ ] At least 5 meaningful commits with descriptive messages
- [ ] outputs/ folder has all 10 charts (PNG files)
- [ ] Notebook (expense_eda.ipynb) is viewable on GitHub
- [ ] Topics/tags added
- [ ] Repo pinned to profile

---

## Screenshots to Take & Upload to images/

| Screenshot | What to capture |
|---|---|
| `01_dataset_preview.png` | Terminal output showing first 5 rows of CSV |
| `02_cleaning_report.png` | Data quality report printed in terminal |
| `03_insights.png` | Insights section from terminal output |
| `04_dashboard.png` | Full Streamlit dashboard in browser |
| `05_heatmap.png` | Category × Month heatmap |
| `06_budget_analysis.png` | Budget vs Actual bar chart |

---

> Keep your commit history clean — recruiters and interviewers look at it!
