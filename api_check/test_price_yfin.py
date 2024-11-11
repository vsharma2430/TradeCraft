import yfinance as yf
import datetime as dt

stock_data = yf.download('TATAMOTORS.NS', start=dt.date(2023,1,1), end=dt.date(2023,2,1))
print(stock_data)

stock_data = yf.download('NIFTYBEES.NS', start=dt.date(2023,1,1), end=dt.date(2023,2,1))
print(stock_data)

info = yf.Ticker('TATAMOTORS.NS').info
print(info)

info = yf.Ticker('NIFTYBEES.NS').info
print(info)

