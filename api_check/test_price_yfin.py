import yfinance as yf
import datetime as dt

yf.set_tz_cache_location(r'cache\yfin')

# end date data is excluded 
stock_data = yf.download('TATAMOTORS.NS', start=dt.date(2023,1,1), end=dt.date(2023,2,1))
print(stock_data)

info = yf.Ticker('TATAMOTORS.NS').info
print(info['sharesOutstanding'], info['floatShares'], info['currentPrice'])

info = yf.Ticker('NIFTYBEES.NS').info
print(info)

stock_data = yf.download('NIFTYBEES.NS', start=dt.date(2023,1,1), end=dt.date(2023,2,1))
print(stock_data)