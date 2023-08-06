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

# import os
# import requests
# from dotenv import load_dotenv

# # Load variables from .env file
# load_dotenv()

# # Read the AlphaVantage API key from the environment variable
# api_key = os.getenv("ALPHAVANTAGE_API_KEY")

# if api_key is None:
#     print("Error: AlphaVantage API key not found. Please check your .env file.")
#     exit(1)

# print(f"AlphaVantage API Key: {api_key}") # Check if the API key has been read properly