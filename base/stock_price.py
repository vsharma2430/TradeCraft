from base.misc import *
from base.stock_base import *
from base.stock_type import Stock_Type

def get_stock_price(STK:str,stock_type:Stock_Type=None)->float:
    stock_ticker = get_ticker_info(STK)
    
    if(stock_ticker!=None):
        
        if(stock_type == None):
            stock_type = get_stocktype_from_ticker(stock_ticker)

        if(stock_type == Stock_Type.EQUITY):
            return float(get_data_from_dict(stock_ticker,'currentPrice'))
        elif(stock_type == Stock_Type.ETF):
            return float(average([get_data_from_dict(stock_ticker,'bid'),get_data_from_dict(stock_ticker,'ask')]))
    
def get_stock_price_print(STK:str,stock_type:Stock_Type=None)->str:
    stock_ticker = get_ticker_info(STK)
    
    if(stock_ticker!=None):
        
        if(stock_type == None):
            stock_type = get_stocktype_from_ticker(stock_ticker)

        if(stock_type == Stock_Type.EQUITY):
            return f'{get_data_from_dict(stock_ticker,'currentPrice')}'
        elif(stock_type == Stock_Type.ETF):
            return f'{get_data_from_dict(stock_ticker,'bid')} - {get_data_from_dict(stock_ticker,'ask')}'
