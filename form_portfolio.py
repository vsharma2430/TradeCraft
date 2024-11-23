import pandas as pd
from datetime import datetime,timezone,timedelta
from statistics import mean
from invest.base import *
from base.misc import *

india_tz=timezone(timedelta(seconds=19800))
get_ticker_dt = lambda df : [datetime.fromisoformat(dd) for dd in df]
get_ticker_dates = lambda dts : sorted(list(set([dt.date() for dt in dts])))

def get_close_price(dt_dict,dt): 
    final_dt:datetime
    for delta in range(1,7):
        try_dt = datetime(dt.year,dt.month,dt.day,tzinfo=india_tz)-timedelta(days=delta)
        if(try_dt in dt_dict):
            final_dt = try_dt
            break
    return dt_dict[final_dt]['Close']

def get_purchase_price(dt_dict,dt):
    final_dt = datetime(dt.year,dt.month,dt.day, 15, 25, tzinfo=india_tz)
    if(final_dt in dt_dict):
        return mean([dt_dict[final_dt]['High'],dt_dict[final_dt]['Close']])
    else:
        print(f'Data missing for {final_dt}')
        return 0

def get_decision_data_stock(plain_stk:str):
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
        if(get_purchase_price(dt_dict_5m,dtX)==0):
            print(f'data missing for {plain_stk}')
        data[dtX] = form_data(dtX,purchase=get_purchase_price(dt_dict_5m,dtX),close=get_close_price(dt_dict_1d,dtX))
    return data

@timeit_concise_print
def get_stock_data():
    fire_list =[get_plain_stock(x) for x in get_file_stocks_object(folder_location=etf_csv_folder)['FIRE']]
    data = {}
    for stk in fire_list:
        data[stk] = get_decision_data_stock(plain_stk=stk)
    return data

@timeit_concise_print
def get_intersection_dates(data:dict):
    sets = []
    for dataX in data:
        sets.append(set(data[dataX].keys()))
    return sorted(list(set.intersection(*sets)))

if(__name__ == '__main__'):
    data = get_stock_data()
    print(get_intersection_dates(data))