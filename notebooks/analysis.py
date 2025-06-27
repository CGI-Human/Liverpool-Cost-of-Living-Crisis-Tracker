import pandas as pd
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "liverpool_cost_living.db"
conn = sqlite3.connect(DB_PATH)

df_liverpool = pd.read_sql("SELECT * FROM ons_data", conn)
print(df_liverpool.head())
