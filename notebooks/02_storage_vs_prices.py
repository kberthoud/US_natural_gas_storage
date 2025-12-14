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


'''Save the raw HH price data '''
#raw_path = Path("../data/raw")
#raw_path.mkdir(parents=True, exist_ok=True)

#df_price.to_csv(
#    raw_path / "HH_front_month.csv",
#    index=False
#)


#df_storage["friday_after"] = df_storage["period"] + pd.Timedelta(days=0)
df_storage = df_storage.set_index("period").sort_index()

df_price = (
    df_price
    .set_index("date")
    .sort_index()
)

df_price.index = df_price.index.tz_localize(None)

hh_on_friday = df_price.reindex(
    df_storage.index,
    method="ffill"
)

df_final = pd.concat(
    [df_storage, hh_on_friday],
    axis=1
)

print(df_final)

'''Save the processed file with HH and storage data '''

df_final.to_csv(
    processed_path / "storage_with_HH_prices.csv",
    index=False
)




