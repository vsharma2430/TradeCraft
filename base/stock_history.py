import datetime as dt
from base.misc import *
from base.stock_base import *
from base.stock_price import *
from logging import getLogger
from pandas import DataFrame
from base.stock_chart import *
from base.stock_candle_stick_pattern import *

logger = getLogger('uvicorn.error')

@timeit
def get_historical_data_interval(STK:str,
                        start_date:dt.date = (dt.datetime.now()-dt.timedelta(days=59)).date(),
                        end_date:dt.date=dt.datetime.now().date(),
                        stock_exchange:Stock_Exchange = Stock_Exchange.NSE,
                        interval='5m',
                        days_delta_start = None,
                        days_delta_end = None,
                        session=None):
        
        if(days_delta_start!=None):
                start_date:dt.date = (dt.datetime.now()-dt.timedelta(days=days_delta_start)).date()
                
        if(days_delta_end!=None):
                end_date:dt.date = (dt.datetime.now()-dt.timedelta(days=days_delta_end)).date()

        STK = get_yfin_symbol(stock=STK,stock_exchange=stock_exchange)
        stk_ticker= get_ticker(STK=STK,session=session)
        stk_historical_df = stk_ticker.history(start=start_date, end=end_date,interval=interval)
        
        return {'df' : stk_historical_df}

@timeit
def get_historical_data(STK:str,
                        start_date:dt.date = (dt.datetime.now()-dt.timedelta(days=365)).date(),
                        end_date:dt.date=dt.datetime.now().date(),
                        stock_exchange:Stock_Exchange = Stock_Exchange.NSE,
                        session=None):

	STK = get_yfin_symbol(stock=STK,stock_exchange=stock_exchange)
	
	stk_ticker= get_ticker(STK=STK,session=session)
	stk_historical_df = stk_ticker.history(start=start_date, end=end_date)
	candle_dict = candle_df(stk_historical_df)
	stk_historical_df = candle_dict['candle_df']
	
	average_price_30 = stk_historical_df['Close'].tail(20).mean()
	average_price_90 = stk_historical_df['Close'].tail(90).mean()
	average_price_365 = stk_historical_df['Close'].mean()

	average_volume_30 = stk_historical_df['Volume'].tail(20).mean()
	average_volume_90 = stk_historical_df['Volume'].tail(60).mean()
	average_volume_365 = stk_historical_df['Volume'].mean()
	
	return {'df' : stk_historical_df ,
		'start_date' : start_date , 
		'end_date' : end_date,
		'dma_30' : average_price_30 , 
		'dma_90' : average_price_90 , 
		'dma_365' : average_price_365 , 
		'volume_30':average_volume_30,
		'volume_90':average_volume_90,
		'volume_365':average_volume_365,
		} 

def get_current_data(STK:str,stock_type:Stock_Type):
        ticker = get_ticker_price_server(STK=STK)
        price,open = get_price_server_stock_current_price(stock_ticker=ticker,stock_type=stock_type)
        return  {
                'current_stock_price' : get_round(price),
                'previous_close' : get_round(get_price_server_stock_previous_close(ticker)),
                'market':open,
                'ticker' : ticker
        }

def get_dma_change(history_data:dict,current_data:dict):
        average_price = get_round(get_data_from_dict(history_data,'dma_30'))
        current_stock_price = get_data_from_dict(current_data,'current_stock_price')
        return get_change_percentage(average_price,current_stock_price)

def get_open_current_change(current_data:dict,history_data:DataFrame=None):
        previous_close_price = get_data_from_dict(current_data,'previous_close')
        current_stock_price = get_data_from_dict(current_data,'current_stock_price')

        if(type(history_data) == type(None)):
                return get_change_percentage(previous_close_price,current_stock_price)
        else:
                close_minus_1 = history_data.iloc[-1]['Close']
                close_minus_2 = history_data.iloc[-2]['Close']

                if(current_stock_price!=0 and current_data['market'] == Market_Open.OPEN):
                        return get_change_percentage(previous_close_price,current_stock_price)
                else:
                        return get_change_percentage(close_minus_1,close_minus_2)

def get_history_context(STK:str,
                        stock_type:Stock_Type,
                        stock_exchange:Stock_Exchange = Stock_Exchange.NSE,
                        stock_data_display=Stock_Page.CLASSIC,
                        chart_type=Chart_Type.CLASSIC,
                        session=None,
                        ):
        
        history_data = get_historical_data(STK=STK,stock_exchange=stock_exchange,session=session)
        current_data = get_current_data(STK=STK,stock_type=stock_type)
        
        history_data_df : DataFrame = get_data_from_dict(history_data,'df')
        history_data_html = history_data_df[::-1].to_html().replace('dataframe','table') # table-fixed
        current_stock_price = get_data_from_dict(current_data,'current_stock_price')
        previous_close_stock_price = get_data_from_dict(current_data,'previous_close')
        
        open_current_change = get_open_current_change(current_data,history_data_df)

        return {
                'title':f'Stock History : {STK}',
                'stock_id':STK,
                'stock_data_display':stock_data_display.value,
                'chart_type':chart_type,
                'previous_close': f'{previous_close_stock_price}',
                'cmp': f'{current_stock_price}',
                'start_date':f'{get_data_from_dict(history_data,'start_date')}',
                'end_date':f'{get_data_from_dict(history_data,'end_date')}',
                'dma_30':get_round(get_data_from_dict(history_data,'dma_30')),
                'dma_90':get_round(get_data_from_dict(history_data,'dma_90')),
                'dma_365':get_round(get_data_from_dict(history_data,'dma_365')),
                'change':f'{open_current_change}',
                'volume_30':get_format(get_round(get_data_from_dict(history_data,'volume_30'))),
                'volume_90':get_format(get_round(get_data_from_dict(history_data,'volume_90'))),
                'volume_365':get_format(get_round(get_data_from_dict(history_data,'volume_365'))),
                'history': history_data_html,
                'chart': get_chart(history_data_df=history_data_df,chart_type=chart_type) ,
                'current_data':current_data['ticker']
                }