import datetime as dt
from base.misc import *
from base.stock_base import *
from base.stock_price import *
    

def get_historical_data(STK:str,
                        start_date:dt.date = (dt.datetime.now()-dt.timedelta(days=60)).date(),
                        end_date:dt.date=dt.datetime.now().date()):
    
    STK = get_yfin_symbol(STK)
    stk_ticker= get_ticker(STK)
    stk_historical_df = stk_ticker.history(start=start_date, end=end_date)
    
    average_price = average([stk_historical_df['Open'].tail(20).mean() , stk_historical_df['Close'].tail(20).mean()])
    average_volume = stk_historical_df['Volume'].tail(20).mean()
    
    return {'df' : stk_historical_df ,
            'price' : average_price , 
            'start_date' : start_date , 
            'end_date' : end_date,
            'volume':average_volume
            } 

def get_history_context(stk_id:str):
    history_data = get_historical_data(stk_id)
    history_data_html = get_data_from_dict(history_data,'df').to_html().replace('dataframe','table')
    average_price = get_round(get_data_from_dict(history_data,'price'))
    average_volume =  get_format(get_round(get_data_from_dict(history_data,'volume')))
    current_stock_price = get_round(get_stock_price(stk_id))
    change = get_round(get_change(average_price,current_stock_price)*100)

    return {
            'title':f'Stock History : {stk_id}',
            'stock_id':stk_id,
            'cmp': f'{current_stock_price}',
            'dma_30':average_price,
            'dma':average_price,
            'change':f'{change}',
            'volume_30':average_volume,
            'volume_90':average_volume,
            'volume':average_volume,
            'history': history_data_html}