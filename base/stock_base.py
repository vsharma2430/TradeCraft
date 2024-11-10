import yfinance as yf
import datetime as dt
from base.misc import *
from base.stock_type import *

def get_ticker(STK:str)->yf.Ticker:
    return yf.Ticker(STK)

def get_ticker_info(STK:str):
    ticker:yf.Ticker = get_ticker(STK)
    if(ticker!=None):
        return ticker.info
    return None

def get_stock_exchange(exchange:str)->Stock_Exchange:
    if(exchange.startswith('NS')):
        return Stock_Exchange.NSE
    elif (exchange.startswith('BS') or exchange.startswith('BE')):
        return Stock_Exchange.BSE

def get_stocktype_from_ticker(stock_ticker:yf.Ticker)->Stock_Type:
    if(getDataFromDict(stock_ticker,'currentPrice')!=None):
        return Stock_Type.EQUITY
    elif(getDataFromDict(stock_ticker,'bid')!=None and getDataFromDict(stock_ticker,'ask')!=None):
        return Stock_Type.ETF
    
def get_stock_symboltype(stock:str)->Stock_Symbol:
    if(':' in stock):
        return Stock_Symbol.GFIN
    elif('.' in stock):
        return Stock_Symbol.YFIN
    else:
        return Stock_Symbol.PLAIN
    
def get_plain_stock(stock:str,s_stype:Stock_Type=Stock_Symbol.YFIN)->str:
    
    if(s_stype == None):
        s_stype = get_stock_symboltype(stock)
    
    if(s_stype == Stock_Symbol.PLAIN):
        return stock
    elif(s_stype == Stock_Symbol.GFIN):
        return stock.split(':')[-1]
    elif (s_stype == Stock_Symbol.YFIN):
        return stock.split('.')[0]
    
def get_stock_symbol(stock:str,stock_exchange:Stock_Exchange=Stock_Exchange.NSE)->str:
    if(stock_exchange == Stock_Exchange.NSE):
        return f'{stock}.NS'
    elif(stock_exchange == Stock_Exchange.BSE):
        return f'{stock}.BO'
    
def convert_gfinToyfin(stock:str)->str:
    stock_st = get_stock_symboltype(stock)

    if(stock_st == Stock_Symbol.GFIN):
        data = stock.split(':')
        data_se = get_stock_exchange(data[0])
        data_stk = get_plain_stock(stock,stock_st)
        
        return get_stock_symbol(data_stk,data_se)
    
    return stock