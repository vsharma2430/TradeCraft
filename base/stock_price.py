import yfinance as yf
import datetime as dt
from base.misc import *
from base.stock_base import *
from base.stock_type import Stock_Type
    
def getStockPrice(STK:str,stock_type:Stock_Type=None)->str:
    stock_ticker = get_ticker_info(STK)
    
    if(stock_ticker!=None):
        
        if(stock_type == None):
            stock_type = get_stocktype_from_ticker(stock_ticker)

        if(stock_type == Stock_Type.EQUITY):
            return f'{getDataFromDict(stock_ticker,'currentPrice')}'
        elif(stock_type == Stock_Type.ETF):
            return f'{getDataFromDict(stock_ticker,'bid')} - {getDataFromDict(stock_ticker,'ask')}'
