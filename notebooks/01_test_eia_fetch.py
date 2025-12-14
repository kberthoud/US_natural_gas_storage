import os
import sys
from pathlib import Path


#make sure /src is in my path
PROJECT_ROOT = Path.cwd().parent
sys.path.append(str(PROJECT_ROOT / "src"))

from eia_api import fetch_eia_series

series_id = "NW2_EPG0_SWO_R48_BCF"

EIA_KEY = os.environ.get("EIA_API_KEY")

if EIA_KEY is None:
    raise RuntimeError("EIA_API_KEY is not set")

df_storage = fetch_eia_series(series_id, EIA_KEY)
print(df_storage.head())

data_raw_path = Path("../data/raw")
df_storage.to_csv(data_raw_path / "lower48_storage_weekly.csv", index=False)