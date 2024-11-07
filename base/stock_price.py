import yfinance as yf

def getStockPrice(STK:str):
    Share = yf.Ticker(STK).info
    market_price = Share['currentPrice']
    return market_price,Share

if(__name__ == '__main__'):
    print(getStockPrice('MSFT'))