import yfinance as yf
import datetime as dt

def getHistoricalData(STK:str,start_date:dt.date,end_date:dt.date):
    stk_ticker= yf.Ticker(STK)
    stk_historical_df = stk_ticker.history(start=start_date, end=end_date)
    return stk_historical_df

if(__name__ == '__main__'):
    print(getHistoricalData('aapl',dt.date(2020,1,1),dt.date(2020,2,1)))