# Liverpool Cost of Living Crisis Tracker

This project helps track how the cost of living in Liverpool has changed from 2015 to 2024. I wanted to see how stuff like rent, bills, and income really impacts people in the city, especially with all the news about rising prices. The idea is to make a dashboard and share my findings in a way that's actually useful, not just academic.

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Status](https://img.shields.io/badge/status-active-brightgreen)

---

## What’s in this project?

- Cleaned data for Liverpool and London (so you don’t have to mess with raw files)
- Python scripts for ETL (extract, transform, load) and analysis
- Notebooks for all the analysis and visualizations
- Dashboard (coming soon) to make everything interactive
- All code is organized and easy to follow

---

## Folder Structure

```
data/           # Cleaned CSVs & database files  
data_raw/       # Original files as downloaded (not touched)  
notebooks/      # Jupyter notebooks for analysis and plotting  
scripts/        # Python scripts for ETL and automation  
dashboard/      # Dashboard code (Streamlit or Power BI)  
viz/            # Plots, screenshots, or images for report/README  
README.md       # This file!  
requirements.txt# All Python dependencies  
``` 

## Example ETL Script

This is just a preview. Full code is in `scripts/etl_ons.py`.

```python
import pandas as pd
import sqlite3
from pathlib import Path

# 1) Define paths
ROOT = Path(__file__).parent.parent    # project root
RAW_DIR = ROOT / "data" / "data_raw"
DB_PATH = ROOT / "data" / "liverpool_cost_living.db"

# 2) Read the raw files
df_liv = pd.read_excel(RAW_DIR / "liverpool data.xlsx", sheet_name=None)
df_lon = pd.read_csv(RAW_DIR / "london and nearby data.csv", skiprows=5)

# 3) Quick check
print("✅ Liverpool sheets:", list(df_liv.keys()))
print("✅ London rows:", len(df_lon))

# 4) Load into SQLite
with sqlite3.connect(DB_PATH) as conn:
    for sheet_name, df in df_liv.items():
        table = f"ons_{sheet_name.lower().replace(' ', '_')}"
        df.to_sql(table, conn, if_exists="replace", index=False)
    df_lon.to_sql("london_data", conn, if_exists="replace", index=False)

print(f"\n🎉 All data loaded into {DB_PATH}")

---

## How to Run

1. **Clone the repo**
2. **Set up your environment**
3. **Run the ETL script:**

4. **Explore the data** in Jupyter or with DB Browser

---

## License

MIT License – you’re free to use this for your own learning or projects.

---

*Made with Python, caffeine, and a little frustration when Windows paths break things.*


