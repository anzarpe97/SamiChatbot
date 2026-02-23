import requests

def get_exchange_rate(from_currency, to_currency):
    """
    Fetches the exchange rate between two currencies using a public API.
    """
    try:
        url = f"https://api.exchangerate-api.com/v4/latest/{from_currency.upper()}"
        response = requests.get(url)
        data = response.json()
        
        rates = data.get("rates", {})
        rate = rates.get(to_currency.upper())
        
        return rate
    except Exception as e:
        print(f"Error fetching exchange rate: {e}")
        return None
