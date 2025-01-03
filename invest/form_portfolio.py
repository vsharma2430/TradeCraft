import copy
import logging 
import pandas as pd
from datetime import datetime,timezone,timedelta
from statistics import mean
from invest.base import *
from base.misc import *
from invest.trade import *
from invest.investment_target import *

log_file = r'dump\std.log'
logging.basicConfig(filename=log_file, 
					format='%(asctime)s %(message)s', 
					filemode='w') 
logger=logging.getLogger() 
logger.setLevel(logging.DEBUG) 
logger.debug("Logging started") 

cache_stock_data_stock_wise = r'dump\stock_data_stock_wise.pkl'
cache_stock_data_date_wise = r'dump\stock_data_date_wise.pkl'

india_tz=timezone(timedelta(seconds=19800))
purchase_time = {'hour':15,'minute':25}
get_ticker_dt = lambda df : [datetime.fromisoformat(dd) for dd in df]
get_ticker_dates = lambda dts : sorted(list(set([dt.date() for dt in dts])))

def get_close_price(dt_dict:dict,dt:datetime): 
    try_dt = datetime(dt.year,dt.month,dt.day,tzinfo=india_tz)
    if(try_dt in dt_dict):
        return dt_dict[try_dt]['Close']
    else:
        return None
    
def get_close_price_previous_day(dt_dict:dict,dt:datetime): 
    for delta in range(1,7):
        try_dt = datetime(dt.year,dt.month,dt.day,tzinfo=india_tz)-timedelta(days=delta)
        if(try_dt in dt_dict):
            return dt_dict[try_dt]['Close']
    return None

def get_purchase_price_at_time(dt_dict,dt):
    final_dt = datetime(dt.year,dt.month,dt.day, purchase_time['hour'], purchase_time['minute'], tzinfo=india_tz)
    if(final_dt in dt_dict):
        return mean([dt_dict[final_dt]['High'],dt_dict[final_dt]['Close']])
    else:
        print(f'Data missing for {final_dt}')
        return 0

def get_decision_data_5m_stock(plain_stk:str):
    csv_file_1d = rf'invest\back_test\2024\1d\{plain_stk}.csv'
    csv_file_5m = rf'invest\back_test\2024\5m\{plain_stk}.csv'

    df_1d = pd.read_csv(csv_file_1d,index_col=0)
    raw_dict_1d = df_1d.to_dict(orient='index')
    dt_dict_1d = { datetime.fromisoformat(dd) : raw_dict_1d[dd] for dd in raw_dict_1d }

    df_5m = pd.read_csv(csv_file_5m,index_col=0)
    raw_dict_5m = df_5m.to_dict(orient='index')
    dt_dict_5m = { datetime.fromisoformat(dd) : raw_dict_5m[dd] for dd in raw_dict_5m }
    index_ticker_dates = get_ticker_dates(dt_dict_5m)

    data = {}
    form_data = lambda dtX,purchase=0,close=0 : {'dt':dtX,'purchase':purchase,'previous_close':close,'change':get_change(close,purchase)} 
    for dtX in index_ticker_dates:
        if(get_purchase_price_at_time(dt_dict_5m,dtX)==0):
            print(f'data missing for {plain_stk}')
        data[dtX] = form_data(dtX,purchase=get_purchase_price_at_time(dt_dict_5m,dtX),close=get_close_price_previous_day(dt_dict_1d,dtX))
    return data

def get_decision_data_1d_stock(plain_stk:str):
    csv_file_1d = rf'invest\back_test\2024\1d\{plain_stk}.csv'

    df_1d = pd.read_csv(csv_file_1d,index_col=0)
    raw_dict_1d = df_1d.to_dict(orient='index')
    dt_dict_1d = { datetime.fromisoformat(dd) : raw_dict_1d[dd] for dd in raw_dict_1d }
    index_ticker_dates = get_ticker_dates(dt_dict_1d)

    data = {}
    form_data = lambda dtX,purchase=0,close=0 : {'dt':dtX,'purchase':purchase,'previous_close':close,'change':get_change(close,purchase)} 
    
    for dtX in index_ticker_dates:
        data[dtX] = form_data(dtX,purchase=get_close_price(dt_dict_1d,dtX),close=get_close_price_previous_day(dt_dict_1d,dtX))
    
    return data

def get_stock_wise_stock_data(func,list_name:str=''):
    fire_list =[get_plain_stock(x) for x in get_file_stocks_object(folder_location=etf_csv_folder)[list_name]]
    data = {}
    for stk in fire_list:
        #func -> get_decision_data_1d_stock or get_decision_data_5m_stock
        data[stk] = func(plain_stk=stk)
    return data

def get_intersection_dates(data:dict):
    sets = []
    for dataX in data:
        sets.append(set(data[dataX].keys()))
    return sorted(list(set.intersection(*sets)))

@timeit_concise_print
def get_date_wise_stock_data(stock_wise_stock_data):
    trade_dates = get_intersection_dates(stock_wise_stock_data)
    trade_stocks = stock_wise_stock_data.keys()
    
    date_wise_stock_dict = {}
    for dateX in trade_dates:
        date_wise_stock_dict[dateX] = []
        for stockX in trade_stocks:
            date_wise_stock_dict[dateX].append({'stock':stockX,'purchase':stock_wise_stock_data[stockX][dateX]['purchase'],'change':stock_wise_stock_data[stockX][dateX]['change']})
        date_wise_stock_dict[dateX].sort(key=lambda x:x['change'])      
    
    return date_wise_stock_dict

def get_buy_trades(date:datetime.date,date_wise_stock_data:dict,portfolio={})->list[Trade]:
    count = 0
    trades = []
    
    today_list=date_wise_stock_data[date]
    
    for stockX in today_list:
        if(stockX['stock'] not in portfolio):
            price = stockX['purchase']
            if(price!=0):
                qty = round(order_price/price)
                trades.append(Trade(date=date,symbol=stockX['stock'],operation=Stock_Trade.BUY,price=price,quantity=qty))
                count = count + 1
                
        if(count == 5):
            break
        
    return trades

def get_sell_trades(date:datetime.date,stock_wise_stock_data:dict,portfolio:dict={},on_target:bool=False)->list[Trade]:
    trades = []
    
    for portfolio_stk in  portfolio:
        trade_obj : Trade
        trade_obj = portfolio[portfolio_stk]
        current_price = stock_wise_stock_data[trade_obj.symbol][date]['purchase']
        pl = get_change(trade_obj.price,current_price)
        if(pl>sell_target or on_target):
            trade_sell_obj = copy.deepcopy(trade_obj)
            trade_sell_obj.date = date
            trade_sell_obj.price = current_price
            trade_sell_obj.operation = Stock_Trade.SELL
            trade_sell_obj.pl = (current_price-trade_obj.price)*trade_obj.quantity
            trades.append(trade_sell_obj)
            
    return trades

def update_portfolio(portfolio:dict={},trades=[]):
    tradeX : Trade
    for tradeX in trades:
        if (tradeX.operation == Stock_Trade.SELL):
            portfolio.pop(tradeX.symbol,None)
        elif(tradeX.operation == Stock_Trade.BUY):
            portfolio[tradeX.symbol] = tradeX
    
@timeit_concise_print
def perform_simulation(list_name:str='FIRE',cache:bool = False) -> list:

    stock_wise_stock_data = None
    date_wise_stock_data = None 

    if(cache):
        stock_wise_stock_data = get_cached_fun_data(func=get_stock_wise_stock_data,args=[get_decision_data_1d_stock,list_name],cache_file=cache_stock_data_stock_wise)
        date_wise_stock_data = get_cached_fun_data(func=get_date_wise_stock_data,args=[stock_wise_stock_data],cache_file=cache_stock_data_date_wise)
    else:
        stock_wise_stock_data = get_stock_wise_stock_data(get_decision_data_1d_stock,list_name)
        date_wise_stock_data = get_date_wise_stock_data(stock_wise_stock_data)
    
    portfolio_dict = {}
    trade_dates = list(date_wise_stock_data.keys())
    
    date_wise_operations = {}    
    for dateX in trade_dates:
        buy_trades = get_buy_trades(date=dateX,date_wise_stock_data=date_wise_stock_data,portfolio=portfolio_dict)
        update_portfolio(portfolio=portfolio_dict,trades=buy_trades)
        
        sell_trades = get_sell_trades(date=dateX,stock_wise_stock_data=stock_wise_stock_data,portfolio=portfolio_dict)
        update_portfolio(portfolio=portfolio_dict,trades=sell_trades)
        
        date_wise_operations[dateX] = {'buy':buy_trades,'sell':sell_trades}
        
        if(len(buy_trades)>0):
            logger.info(f'Date : {dateX} BUY')
            for buyX in buy_trades:
                logger.info(buyX)
        if(len(sell_trades)>0):
            logger.info(f'Date : {dateX} SELL')
            for sellX in sell_trades:
                logger.info(sellX)
        if(len(buy_trades)>0 or len(sell_trades)>0):
            logger.info(f'Date : {dateX} PORTFOLIO')
            for stkX in portfolio_dict:
                    logger.info(portfolio_dict[stkX])
    
    last_date = trade_dates[-1]
    final_sell_trades = get_sell_trades(date=last_date,stock_wise_stock_data=stock_wise_stock_data,portfolio=portfolio_dict,on_target=True)
    update_portfolio(portfolio=portfolio_dict,trades=final_sell_trades)
    date_wise_operations[last_date]['sell'].extend(final_sell_trades)
    
    logger.info(f'Final sell on {last_date}')
    for sellX in final_sell_trades:
        logger.info(sellX)

    logger.info(f'Final portfolio : {portfolio_dict}')

    pl = {}
    for dateX in date_wise_operations:
        pl_marker = f'{dateX.month}-{dateX.year}'
        if(pl_marker not in pl):
            pl[pl_marker] = 0

        for tradeX in date_wise_operations[dateX]['sell']:
            if hasattr(tradeX, 'pl'):
                pl[pl_marker] = pl[pl_marker] + tradeX.pl
            else:
                print(dateX,tradeX)
    
    for dtX in pl:
        pl[dtX] = round(pl[dtX],1)

    result = {
        'Stock List' : f'{list_name}',
        'Timeline' : f'{trade_dates[1]} to {trade_dates[-1]} -> ({(trade_dates[-1]-trade_dates[1]).days}) days or  ({ round((trade_dates[-1]-trade_dates[1]).days/30,1)}) months',
        'Capital' : f'₹ {get_comma_format(capital)}',
        'Sell target' : f'{get_percentage_format(sell_target)}',
        'Trade time' : f'{purchase_time["hour"]}:{purchase_time["minute"]}',
        'P/L and Returns' :{'Net P/L (Excluding this month)' : f'₹ {get_comma_format(round(sum([pl[dtX] for dtX in list(pl.keys())[:-1]])))}',
                            'Returns (Excluding this month)' : f'{get_percentage_format(round(sum([pl[dtX] for dtX in list(pl.keys())[:-1]]))/capital)}',
                            'Net P/L (Including this month)' : f'₹ {get_comma_format(round(sum([pl[dtX] for dtX in pl])))}',
                            'Returns (Including this month)' : f'{get_percentage_format(round(sum([pl[dtX] for dtX in pl]))/capital)}',},
        'Month-wise P/L' : pl
        }

    for key in result:
        logger.info(f'{key} : {result[key]}')
        
    return result

