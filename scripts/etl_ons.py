import pandas as pd
import sqlite3
from pathlib import Path

# 1) Define paths
ROOT = Path(__file__).parent.parent    # project root: C:/Users/prashant/Desktop/project 1
RAW_DIR = ROOT / "data" / "data_raw"
DB_PATH = ROOT / "data" / "liverpool_cost_living.db"

# 2) Read the Liverpool Excel file (all sheets)
df_liv = pd.read_excel(RAW_DIR / "liverpool data.xlsx", sheet_name=None)

# 3) Load the London CSV, skipping metadata rows so we get real headers and data
london_csv_path = RAW_DIR / "london and nearby data.csv"
df_lon = pd.read_csv(london_csv_path, skiprows=5)
print("\nLondon data shape:", df_lon.shape)
print(df_lon.head())

# 4) Quick check on Liverpool sheets
print("✅ Liverpool sheets:", list(df_liv.keys()))
for sheet_name, df in df_liv.items():
    print(f"  - {sheet_name}: {df.shape}")

# 5) Load everything into SQLite
with sqlite3.connect(DB_PATH) as conn:
    # Write each Liverpool sheet as its own table
    for sheet_name, df in df_liv.items():
        table = f"ons_{sheet_name.lower().replace(' ', '_')}"
        df.to_sql(table, conn, if_exists="replace", index=False)
        print(f"  • Wrote {table} ({df.shape[0]} rows)")
    # Write the cleaned London data
    df_lon.to_sql("london_data", conn, if_exists="replace", index=False)
    print(f"  • Wrote london_data ({df_lon.shape[0]} rows)")

print(f"\n🎉 All data loaded into {DB_PATH}")
