import yfinance_cache as yf


info1 = yf.Ticker('TATAMOTORS.NS').info
info2 = yf.Ticker('NIFTYBEES.NS').info

print(info1)
print(info2)

print(info1['currentPrice'])
print(info2['bid'],info2['ask'])

