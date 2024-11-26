from os.path import join,getctime,getmtime
from time import ctime
from datetime import datetime

from base.stock_history import *
from base.stock_price import *
from base.misc import *
from invest.base import *
from invest.portfolio import *

def modification_date(filename):
    if(path.exists(filename)):
        t = getmtime(filename)
        return datetime.fromtimestamp(t).date()
    return None

def creation_date(filename):
    if(path.exists(filename)):
        t = getctime(filename)
        return datetime.fromtimestamp(t).date()
    return None

def get_stock_download_list(folder_location=etf_csv_folder,stock_list_id = 'FIRE',year=datetime.now().year,interval:str='1m'):
    stock_folder_stocks = get_file_stocks_object(folder_location=folder_location,exclude_all=False)
    csv_save_location = rf'.\invest\back_test\{year}\{interval}'
    return stock_folder_stocks[stock_list_id],csv_save_location

def download_csv_interday(folder_location=etf_csv_folder,stock_list_id = 'FIRE'):
    stock_download_list,csv_save_location = get_stock_download_list(folder_location=folder_location,stock_list_id=stock_list_id,interval='1d')
    for stock in stock_download_list:
        plain_stk = get_plain_stock(stock=stock)
        csv_save_path = join(csv_save_location,f'{plain_stk}.csv')
        date_today = datetime.now().date()
        if(creation_date(csv_save_path) == date_today or modification_date(csv_save_path) == date_today):
            print(f'Skipped downloading for {stock}.')
            continue
        else:
            df:DataFrame = get_historical_data(start_date= (dt.datetime.now()-dt.timedelta(days=365*10)).date(),STK=stock)['df']
            df.to_csv(path_or_buf=csv_save_path, encoding='utf-8')
            print(f'Downloaded data for {stock} to {csv_save_path}.')
            
        
def download_csv_intraday(folder_location=etf_csv_folder,stock_list_id = 'FIRE',interval:str='1m'):
    stock_download_list,csv_save_location = get_stock_download_list(folder_location=folder_location,stock_list_id=stock_list_id)
    for stock in stock_download_list:
        dfs = []
        plain_stk = get_plain_stock(stock=stock)
        
        for i in range(29):
            df:DataFrame = get_historical_data_interval(STK=stock,
                                                        days_delta_start=(i+1),
                                                        days_delta_end=i,
                                                        interval=interval)['df']
            if(type(df)!=type(None)):
                print(f'Downloaded df for start/end delta {i+1}-{i}')
                dfs.append(df)
        
        df=pd.concat(dfs,sort=True)
        location = join(csv_save_location,f'{plain_stk}.csv')
        df.to_csv(path_or_buf=location, encoding='utf-8')
            
        print(f'Downloaded data for {stock}')