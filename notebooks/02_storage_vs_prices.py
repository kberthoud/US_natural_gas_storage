import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import yfinance as yf

processed_path = Path("../data/processed")

df_storage = pd.read_csv(
    processed_path / "lower48_storage_with_5yr_diff.csv",
    parse_dates=["period"]
)

#print(df_storage.head(), df_storage.tail())

#fetch HH front month prices
hh = yf.download(
    "NG=F",
    start=df_storage["period"].min(),
    progress=False
)

df_price = (
    hh[["Close"]]
    .reset_index()
    .rename(columns={"Date": "date", "Close": "hh_price"})
)

df_price["report_period"] = (
    df_price["date"]
    .dt.to_period("W-THU")
    .dt.start_time
)

df_price_weekly = (
    df_price
    .groupby("report_period")["hh_price"]
    .mean()
    .rename("hh_price")
    .to_frame()
    .sort_index()
)

df_storage = df_storage.set_index("period").sort_index()

df_final = pd.concat(
    [df_storage, df_price_weekly],
    axis=1
)



print(df_final)

