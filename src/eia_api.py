import requests
import pandas as pd

def fetch_eia_series(series_id: str, api_key: str) -> pd.DataFrame:
    '''Function to take the name of an EIA data series and an API key
    to return a pandas data frame.'''
    
    url = "https://api.eia.gov/series"
    params = {
        "api_key": api_key,
        "series_id": series_id
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    payload = response.json()
    series = payload["series"][0]
    data = series["data"]

    df = pd.DataFrame(data, columns=["date", "value"])

    #parse date from str to datetime
    df["date"] = pd.to_datetime(df["date"], format="%Y%m%d")

    #sort with oldest first
    df = df.sort_values("date").reset_index(drop=True)

    return df