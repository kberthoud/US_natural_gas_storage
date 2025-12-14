import requests
import pandas as pd

def fetch_eia_series(series_id: str, 
                     api_key: str, 
                     start: str = "2010-01-01") -> pd.DataFrame:
    """
    Fetch weekly natural gas data from the EIA v2 API.
    """
    
    # Construct URL and payload
    url = "https://api.eia.gov/v2/natural-gas/stor/wkly/data/"
    
    # API parameters
    params = {
        "api_key": api_key,
        "frequency": "weekly",
        "data[0]": "value",
        "facets[series][]": series_id,
        "start": start,
        "sort[0][column]": "period",
        "sort[0][direction]": "asc",
        "offset": 0,
        "length": 5000
    }
    
    # Make the GET request
    response = requests.get(url, params=params)
    
    # Check for HTTP errors
    response.raise_for_status()
    
    data = response.json()
    
    # Extract the data
    try:
        records = data['response']['data']
    except KeyError:
        raise ValueError("Unexpected response structure: ", data)
    
    # Convert to DataFrame
    df = pd.DataFrame(records)
    
    # Ensure period is datetime and value is numeric
    df['period'] = pd.to_datetime(df['period'])
    df['value'] = pd.to_numeric(df['value'])

    return df

