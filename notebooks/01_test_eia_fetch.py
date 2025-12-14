import os
import sys
from pathlib import Path
import pandas as pd

#make sure /src is in my path
PROJECT_ROOT = Path.cwd().parent
sys.path.append(str(PROJECT_ROOT / "src"))

from eia_api import fetch_eia_series

series_id = "NW2_EPG0_SWO_R48_BCF"

EIA_KEY = os.environ.get("EIA_API_KEY")

if EIA_KEY is None:
    raise RuntimeError("EIA_API_KEY is not set")

df_storage = fetch_eia_series(series_id, EIA_KEY)
#print(df_storage.head())

#data_raw_path = Path("../data/raw")
#df_storage.to_csv(data_raw_path / "lower48_storage_weekly.csv", index=False)


#Calculating the five-year average storage levels

df = df_storage.copy()
df['week'] = df['period'].dt.isocalendar().week
df['year'] = df['period'].dt.year

five_year_avg = (
    df.groupby('week')['value']
    .rolling(5, min_periods=5).mean()
    .reset_index(level=0, drop=True)
)

df['5yr_avg'] = five_year_avg
df['diff'] = df['value'] - df['5yr_avg']

#print(df.tail())
#Save this new processed file with 5 yr avg

df_processed = df[
    ['period', 'value', '5yr_avg', 'diff']
].copy()

processed_path = Path("../data/processed")
processed_path.mkdir(parents=True, exist_ok=True)

df_processed.to_csv(
    processed_path / "lower48_storage_with_5yr_diff.csv",
    index=False
)

