from dataclasses import dataclass
import requests as r
from bs4 import BeautifulSoup
from tabulate import tabulate

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


@dataclass
class Position:
    stock: Stock
    quantity: int

@dataclass
class Portfolio:
    positions: list[Position]
    
    def get_total_value(self):
        total_value = 0
        for position in self.positions:
            total_value += position.quantity * position.stock.eur_price

        return round(total_value, 2)

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
        "eur_price": eurPrice
    }


def display_portfolio_summary(portfolio):
    if not isinstance(portfolio,Portfolio):
        raise TypeError("Please provide a instance of the Portfolio type")

    portfolio_value = portfolio.get_total_value()
    
    position_data = []

    for position in sorted(portfolio.positions, key = lambda x : x.quantity * x.stock.eur_price, reverse=True): 
        position_data.append([position.stock.ticker, 
        position.stock.exchange, 
        position.quantity, 
        position.stock.eur_price,
         position.quantity * position.stock.eur_price,
          position.quantity * position.stock.eur_price / portfolio_value * 100])

    print(tabulate(position_data, 
                    headers=["Ticker", "Exchange", "Quantity", "Price", "Market Value" , "% Allocation"],
                    tablefmt="psql",
                    floatfmt=".2f"))
    print(f"Total portfolio value: {portfolio_value: ,.2f}.")


if __name__ == "__main__":
    shopify = Stock("SHOP","TSE")
    msft = Stock("MSFT","NASDAQ")
    googl = Stock("GOOGL","NASDAQ")


    portfolio = Portfolio([Position(shopify,100), Position(msft,10), Position(googl,30)])

    display_portfolio_summary(portfolio)