import yfinance as yf
import pandas as pd

HH_front_month = yf.download("NG=F", start="2010-01-01", interval ="1d")

HH_front_month.to_csv("../data/raw/HH_front_month_prices.csv")