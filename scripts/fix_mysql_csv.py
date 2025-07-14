# scripts/fix_mysql_csv.py

import pandas as pd

# ─── CONFIG ────────────────────────────────────────────────
INFILE = 'liverpool_for_mysql.csv'             # your raw CSV
OUTFILE = 'liverpool_for_mysql_clean.csv'      # final MySQL-ready CSV

# Mapping from original headers → SQL-friendly snake_case
COL_MAP = {
    "Date": "date",
    "Employment rate - aged 16-64": "employment_rate_16_64",
    "% aged 16-64 who are employees": "percent_employees_16_64",
    "% aged 16-64 who are self employed": "percent_self_employed_16_64",
    "Unemployment rate - aged 16+": "unemployment_rate_16_plus",
    "% who are economically inactive - aged 16-64": "percent_econ_inactive_16_64",
    "% of economically inactive who want a job": "percent_econ_inactive_want_job",
    "% all in employment who are - 1: managers, directors and senior officials (SOC2020)": "soc1_managers",
    "% all in employment who are - 2: professional occupations (SOC2020)": "soc2_professional",
    "% all in employment who are - 3: associate professional occupations (SOC2020)": "soc3_associate_prof",
    "% all in employment who are - 4: administrative and secretarial occupations (SOC2020)": "soc4_admin_secretarial",
    "% all in employment who are - 5: skilled trades occupations (SOC2020)": "soc5_skilled_trades",
    "% all in employment who are - 6: caring, leisure and other service occupations (SOC2020)": "soc6_caring_leisure_other",
    "% all in employment who are - 7: sales and customer service occupations (SOC2020)": "soc7_sales_customer_service",
    "% all in employment who are - 8: process, plant and machine operatives (SOC2020)": "soc8_process_plant_machine",
    "% all in employment who are - 9: elementary occupations (SOC2020)": "soc9_elementary",
    "16+ unemployment rate - ethnic minority": "unemployment_rate_ethnic_minority_16_plus",
    "% with RQF4+ - aged 16-64": "percent_rqf4_plus_16_64",
    "% with RQF3+ - aged 16-64": "percent_rqf3_plus_16_64",
    "% with RQF2+ - aged 16-64": "percent_rqf2_plus_16_64",
}

def main():
    # 1. Load everything as strings
    df = pd.read_csv(INFILE, dtype=str)
    print(f"🔍 Loaded {INFILE} with shape {df.shape}")

    # 2. Rename headers & keep only the mapped columns in order
    df = df.rename(columns=COL_MAP)[list(COL_MAP.values())]
    print("✏️  Renamed columns to SQL-friendly names.")

    # 3. Clean numeric columns: strip commas/spaces → coerce to float
    num_cols = df.columns.difference(['date'])
    for col in num_cols:
        df[col] = (
            df[col]
              .str.replace(',', '', regex=False)
              .str.strip()
              .pipe(pd.to_numeric, errors='coerce')
        )
    print(f"🧹 Cleaned numeric columns: {num_cols.tolist()}")

    # 4. Drop rows with no numeric data (all NaN except `date`)
    before = df.shape[0]
    df = df.dropna(subset=num_cols, how='all')
    dropped = before - df.shape[0]
    print(f"🗑  Dropped {dropped} empty rows (if any).")

    # 5. Save final CSV
    df.to_csv(OUTFILE, index=False)
    print(f"✅ Saved clean file as {OUTFILE}")
    print(f"📊 Final shape: {df.shape}")
    print("📝 Columns:", df.columns.tolist())
    print("\n✨ Preview:")
    print(df.head(3).to_string(index=False))

if __name__ == "__main__":
    main()
