import yfinance as yf
import datetime as dt

def getHistoricalData(STK:str,start_date:dt.date,end_date:dt.date):
    stk_ticker= yf.Ticker(STK)
    stk_historical_df = stk_ticker.history(start=start_date, end=end_date)
    return stk_historical_df

def getHistoricalData1m(STK:str,
                        start_date:dt.date=(dt.datetime.now()-dt.timedelta(days=59)).date(),
                        end_date:dt.date=dt.datetime.now().date()):
    stk_ticker= yf.Ticker(STK)
    stk_historical_df = stk_ticker.history(start=start_date,end=end_date,interval='5m')
    return stk_historical_df

if(__name__ == '__main__'):
    '''
    print(getHistoricalData('aapl',dt.date(2020,1,1),dt.date(2020,2,1)))

    print(yf.download('TATAMOTORS.NS', start=dt.date(2023,1,1), end=dt.date(2023,2,1)))

    print(yf.download('NIFTYBEES.NS', start=dt.date(2023,1,1), end=dt.date(2023,2,1)))
    '''
    print(getHistoricalData1m('NIFTYBEES.NS'))
    
