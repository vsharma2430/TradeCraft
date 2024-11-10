import datetime as dt
from base.misc import *
from base.stock_base import *
    
def get_historical_data(STK:str,
                        start_date:dt.date = (dt.datetime.now()-dt.timedelta(days=30)).date(),
                        end_date:dt.date=dt.datetime.now().date()):
    
    s_stype = get_stock_symboltype(STK)
    
    if(s_stype == Stock_Symbol.PLAIN):
        STK = get_stock_symbol(STK)
    elif (s_stype == Stock_Symbol.GFIN):
        STK = convert_gfinToyfin(STK)
            
    stk_ticker= get_ticker(STK)
    stk_historical_df = stk_ticker.history(start=start_date, end=end_date)
    
    average_price = average([stk_historical_df['Open'].mean() , stk_historical_df['Close'].mean()])
    average_volume = stk_historical_df['Volume'].mean()
    
    return {'df' : stk_historical_df ,
            'price' : average_price , 
            'start_date' : start_date , 
            'end_date' : end_date,
            'volume':average_volume
            } 