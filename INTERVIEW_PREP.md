# 🎤 Interview Preparation — Expense Tracker App

---

## ✅ How to Introduce This Project (HR Round)

> "I built an **Expense Tracker App using Data Science** in Python.
> The project covers the full data pipeline—from generating realistic synthetic data
> to cleaning, analysing, and visualising expenses.
> It includes 10 charts, an automated insights engine, and an interactive
> Streamlit dashboard. I designed it to demonstrate skills relevant to
> Data Analyst, Business Analyst, and Financial Analyst roles."

---

## Q&A: 15 Interview Questions with Answers

---

### Q1. What is this project about? (HR)
**Answer:**
This is a personal finance analytics project. It simulates one year of expenses across categories like Food, Rent, Travel, and Shopping. Using Python and Data Science libraries, I clean the data, run analysis, and generate charts and insights—just like what a financial analyst would do for a company's expense report.

---

### Q2. Why did you use synthetic data? (Technical)
**Answer:**
Real financial data is private and unavailable to students. Synthetic data lets us control the size, quality, and patterns of the dataset. I used `numpy.random` with seeded random numbers for reproducibility, and added realistic features like seasonal spikes (Travel peaks in vacation months, Shopping spikes during Diwali season).

---

### Q3. Explain your data cleaning steps. (Technical)
**Answer:**
Three main steps:
1. **Remove duplicates** — `df.drop_duplicates()`
2. **Fill missing amounts** — Used category median via `groupby().transform()` to preserve category-specific context rather than a global mean
3. **Fix negatives** — Data-entry errors converted to positive via `.abs()`

---

### Q4. What is EDA? How did you perform it? (Technical)
**Answer:**
EDA = Exploratory Data Analysis. It means understanding your data before modelling. I performed:
- Shape, dtypes, null counts
- Summary statistics (mean, std, min, max)
- Category-wise and monthly aggregations
- Heatmaps to spot seasonal patterns
- Box plots to detect outliers in each category

---

### Q5. Which Pandas functions did you use most? (Technical)
**Answer:**
- `groupby()` with `agg()` — for category and monthly aggregations
- `pivot_table()` — for the Category × Month heatmap
- `pct_change()` — for Month-over-Month growth
- `pd.cut()` — to bin amounts into Low/Medium/High/Very High
- `transform()` — to apply group-level operations without losing rows

---

### Q6. What insights did you generate? (Technical + Business)
**Answer:**
- Highest spending category
- Most expensive month
- Months that exceeded the ₹30,000 budget
- Weekend vs weekday spending comparison
- Average daily spend
- Most used payment method by transaction value
- Month-over-Month change tracking

---

### Q7. How did you detect overspending? (Business Analyst angle)
**Answer:**
I set a monthly budget of ₹30,000. I aggregated spending per month, then compared it against the budget. I flagged months where actual > budget with a red bar in the Budget vs Actual chart and added a status column (✅ Under Budget / ❌ Over Budget) in the summary table.

---

### Q8. What is a heatmap and why did you use it? (Technical)
**Answer:**
A heatmap visualises a matrix using colour intensity. I used a Category × Month pivot table where each cell shows spending for that combination. Darker colours = higher spending. It instantly reveals seasonal patterns—e.g., Travel spiking in October–December, Shopping spiking in November (Diwali).

---

### Q9. What is the difference between `mean()` and `median()` for filling nulls? (Technical)
**Answer:**
- `mean()` is sensitive to outliers. A ₹50,000 rent transaction would inflate the mean.
- `median()` is robust to outliers. For expense data with wide ranges, median is more representative.
I used **category-level median** so that missing Food amounts are filled with the Food median, not the global median.

---

### Q10. How would you scale this for a real company? (Business + Technical)
**Answer:**
1. Connect to a real database (PostgreSQL, MySQL) instead of CSV
2. Use an ETL pipeline (Apache Airflow or AWS Glue)
3. Add role-based access so each department sees only its expenses
4. Implement anomaly detection using Z-score or Isolation Forest
5. Add email/Slack alerts when spending exceeds budget
6. Integrate with ERP systems like SAP or Tally

---

### Q11. What does Streamlit do? (Technical)
**Answer:**
Streamlit is a Python library that turns scripts into interactive web apps without HTML/CSS/JavaScript knowledge. It lets users filter data via sidebar widgets and see charts update in real time. For this project, users can filter by month, category, and payment method to explore their spending dynamically.

---

### Q12. What is feature engineering? Give examples from your project. (Technical)
**Answer:**
Feature engineering = creating new columns from existing data to improve analysis:
- `Quarter` — from date (for quarterly reports)
- `Is_Weekend` — True/False (spending pattern difference)
- `Spend_Level` — binned category (Low/Medium/High/Very High)
- `Over_Budget` — Boolean flag per month
- `MoM_Change_%` — Month-over-Month percentage change

---

### Q13. What charts did you create and why? (Technical + Presentation)
**Answer:**
10 charts total:
- **Pie chart** → proportion of each category
- **Bar chart (monthly)** → easy month comparison with budget line
- **Horizontal bar** → ranked category spending
- **Line chart** → trend over time
- **Heatmap** → category vs month patterns
- **Donut chart** → payment method mix
- **Box plot** → spending distribution and outliers per category
- **Day-of-week bar** → weekday vs weekend behaviour
- **Budget vs Actual** → financial health check
- **Cumulative line** → year-to-date spending

---

### Q14. How do you ensure reproducibility in your project? (Technical)
**Answer:**
I set `np.random.seed(42)` and `random.seed(42)` at the start of the data generator. This ensures that every run produces identical data, making charts and insights consistent—important for demos and version control.

---

### Q15. What would you add as your next version? (Future thinking)
**Answer:**
- **AI prediction** using Facebook Prophet or LSTM to forecast next month's spending
- **Receipt scanner** using OCR (Tesseract) to auto-enter expenses from photos
- **Budget alerts** via email using SMTP when category exceeds threshold
- **Goal tracker** (e.g., "Save ₹50,000 in 6 months")
- **Mobile app** using Flutter with a Python FastAPI backend

---

## 🏷️ GitHub Tags to Add to Your Profile

- `expense-tracker`
- `data-science-project`
- `python-analytics`
- `financial-analysis`
- `pandas-matplotlib`
- `streamlit-dashboard`
- `portfolio-project`

---

> 💡 TIP: When presenting this project, open the Streamlit dashboard live in your browser and change the filters while explaining. This makes a strong impression in virtual interviews.
