import yfinance as yf
import datetime as dt
from base.misc import *
from base.stock_type import Stock_Type

def get_ticker(STK:str)->yf.Ticker:
    return yf.Ticker(STK)

def get_ticker_info(STK:str):
    ticker:yf.Ticker = get_ticker(STK)
    if(ticker!=None):
        return ticker.info
    return None

def getStockType(stock_ticker)->Stock_Type:
    if(getDataFromDict(stock_ticker,'currentPrice')!=None):
        return Stock_Type.EQUITY
    elif(getDataFromDict(stock_ticker,'bid')!=None and getDataFromDict(stock_ticker,'ask')!=None):
        return Stock_Type.ETF