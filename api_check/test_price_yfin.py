import yfinance as yf

# end date data is excluded 
stock_data = yf.download('TATAMOTORS.NS', start='2023-01-01', end='2023-01-06')
print(stock_data)

info = yf.Ticker('TATAMOTORS.NS').info
print(info['sharesOutstanding'], info['floatShares'], info['currentPrice'])

info = yf.Ticker('NIFTYBEES.NS').info
print(info)