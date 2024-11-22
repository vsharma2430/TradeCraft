from base.misc import *
from base.stock_base import *
from base.stock_enum import Stock_Type

logger = getLogger('uvicorn.error')

@timeit
def get_ticker_price_server(STK:str):
    return get_ticker_info_price_server(STK=STK)

def get_price_server_stock_current_price(stock_ticker,stock_type:Stock_Type=None)->tuple[float,Market_Open]:
    if(stock_ticker!=None):
        
        if(stock_type == None):
            stock_type = get_stocktype_from_ticker(stock_ticker)

        if(stock_type == Stock_Type.EQUITY):
            if('currentPrice' in stock_ticker):
                return get_float(get_data_from_dict(stock_ticker,'currentPrice')),Market_Open.OPEN
            elif('previousClose' in  stock_ticker):
                return get_float(get_data_from_dict(stock_ticker,'previousClose')),Market_Open.CLOSE
        
        elif(stock_type == Stock_Type.ETF):
            if('bid' in stock_ticker and 'ask' in stock_ticker):
                return get_float(average([get_data_from_dict(stock_ticker,'bid'),get_data_from_dict(stock_ticker,'ask')])),Market_Open.OPEN
            elif('previousClose' in  stock_ticker):
                return get_float(get_data_from_dict(stock_ticker,'previousClose')),Market_Open.CLOSE

def get_price_server_stock_previous_close(stock_ticker)->float:
    if(stock_ticker!=None):
        return get_float(get_data_from_dict(stock_ticker,'previousClose'))

@timeit
def get_stock_price(STK:str,stock_type:Stock_Type=None,session=None)->float:
    stock_ticker = get_ticker_info(STK=STK,session=session)
    
    if(stock_ticker!=None):
        
        if(stock_type == None):
            stock_type = get_stocktype_from_ticker(stock_ticker)

        if(stock_type == Stock_Type.EQUITY):
            if('currentPrice' in stock_ticker):
                return get_float(get_data_from_dict(stock_ticker,'currentPrice'))
            else:
                return get_float(get_data_from_dict(stock_ticker,'previousClose'))
        
        elif(stock_type == Stock_Type.ETF):
            if('bid' in stock_ticker and 'ask' in stock_ticker):
                return get_float(average([get_data_from_dict(stock_ticker,'bid'),get_data_from_dict(stock_ticker,'ask')]))
            else:
                return get_float(get_data_from_dict(stock_ticker,'previousClose'))
    
def get_stock_price_print(STK:str,stock_type:Stock_Type=None)->str:
    stock_ticker = get_ticker_info(STK)
    
    if(stock_ticker!=None):
        
        if(stock_type == None):
            stock_type = get_stocktype_from_ticker(stock_ticker)

        if(stock_type == Stock_Type.EQUITY):
            return f'{get_data_from_dict(stock_ticker,'currentPrice')}'
        elif(stock_type == Stock_Type.ETF):
            return f'{get_data_from_dict(stock_ticker,'bid')} - {get_data_from_dict(stock_ticker,'ask')}'
