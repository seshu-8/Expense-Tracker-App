# 🔧 Troubleshooting Guide — Expense Tracker App

---

## Error 1: ModuleNotFoundError

**Error:**
```
ModuleNotFoundError: No module named 'pandas'
```
**Fix:**
```bash
pip install -r requirements.txt
# Or individually:
pip install pandas numpy matplotlib seaborn openpyxl streamlit
```

---

## Error 2: FileNotFoundError for CSV

**Error:**
```
FileNotFoundError: data/expenses_raw.csv not found
```
**Fix:**
Run the generator first:
```bash
python src/data_generator.py
# Then run cleaning:
python src/data_cleaning.py
```
Or just run the complete pipeline:
```bash
python main.py
```

---

## Error 3: Streamlit not opening

**Error:**
```
streamlit: command not found
```
**Fix:**
```bash
pip install streamlit
# Then:
streamlit run dashboard.py
# If that fails:
python -m streamlit run dashboard.py
```

---

## Error 4: Matplotlib display error (Linux servers)

**Error:**
```
_tkinter.TclError: no display name and no $DISPLAY environment variable
```
**Fix:**
Add this at the top of visualization.py (already included):
```python
import matplotlib
matplotlib.use("Agg")
```

---

## Error 5: openpyxl error when saving Excel

**Error:**
```
ModuleNotFoundError: No module named 'openpyxl'
```
**Fix:**
```bash
pip install openpyxl
```

---

## Error 6: Jupyter kernel not found

**Error:**
```
No kernel found for Python 3
```
**Fix:**
```bash
pip install ipykernel
python -m ipykernel install --user --name=venv
```

---

## Error 7: Git push rejected

**Error:**
```
error: failed to push some refs to origin
```
**Fix:**
```bash
git pull origin main --rebase
git push
```

---

## Error 8: UnicodeEncodeError in report file

**Error:**
```
UnicodeEncodeError: 'charmap' codec can't encode character '₹'
```
**Fix:**
Already handled in report_generator.py with `encoding="utf-8"`.  
If it still fails on Windows:
```bash
# Set environment variable
set PYTHONIOENCODING=utf-8
python main.py
```

---

## Error 9: Virtual environment activation fails (Windows)

**Error:**
```
'venv\Scripts\activate' is not recognised
```
**Fix:**
```bash
# In PowerShell, first run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Then:
venv\Scripts\Activate.ps1
```

---

## Error 10: Seaborn version conflict

**Error:**
```
AttributeError: module 'seaborn' has no attribute 'set_theme'
```
**Fix:**
```bash
pip install --upgrade seaborn
```

---

> 💡 Always activate your virtual environment before running the project!
