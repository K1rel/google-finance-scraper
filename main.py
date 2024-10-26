from dataclasses import dataclass
import requests as r
from bs4 import BeautifulSoup

@dataclass
class Stock:
    ticker: str
    exchange: str
    price: float = 0
    currency: str = "EUR"
    eur_price: float = 0

    def __post_init__(self):
        price_info = get_price_info(self.ticker, self.exchange)
       
        if price_info["ticker"] == self.ticker: 
            self.price = price_info["price"]
            self.currency = price_info["currency"]
            self.eur_price = price_info["eur_price"]




def getEuroRate(currency):
    url = f"https://www.google.com/finance/quote/{currency}-EUR"
    resp = r.get(url)
    soup = BeautifulSoup(resp.content, "html.parser")

    return float(soup.find("div", attrs={"data-last-price": True})["data-last-price"])

def get_price_info(ticker,exchange):
    url = f"https://www.google.com/finance/quote/{ticker}:{exchange}"
    resp = r.get(url)
    soup = BeautifulSoup(resp.content, "html.parser")

    price_div = soup.find("div", attrs={"data-last-price": True})
    
    price = float(price_div["data-last-price"])
    currency = price_div["data-currency-code"]
    eurPrice = price
    if currency != "EUR":
        rate = getEuroRate(currency)
        eurPrice = round(price*rate,2)



    return {
        "ticker": ticker,
        "exchange": exchange,
        "price": price,
        "currency": currency,
        "eurPrice": eurPrice
    }


if __name__ == "__main__":
    print(Stock("SHOP","TSE"))