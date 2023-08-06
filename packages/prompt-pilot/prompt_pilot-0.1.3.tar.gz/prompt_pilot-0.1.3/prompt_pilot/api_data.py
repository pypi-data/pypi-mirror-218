import requests

def alpha_vantage_intraday(api_key:str="", symbol:str=""):

    url = "https://alpha-vantage.p.rapidapi.com/query"

    querystring = {
        "interval": "1min",
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "datatype": "json",
        "output_size": "compact"
    }

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "alpha-vantage.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()