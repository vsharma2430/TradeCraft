from os import listdir
from os.path import join
from pathlib import Path
from base.stock_base import convert_gfinToyfin
from base.stock_history import *
from base.misc import *
from invest.investment_target import *

stock_csv_folder = r'invest\stock_list'

def get_file_stocks_object(folder_location = stock_csv_folder):
    array_files = listdir(folder_location)
    
    list_name : str
    file_stocks = {}
    
    for list_name in array_files:
        file_path= join(stock_csv_folder,list_name)
        id = Path(file_path).stem.upper()
        
        with open(file_path) as f:
            stock_syms = [convert_gfinToyfin(stock.strip()) for stock in f.readlines()]
        
        file_stocks[id] = stock_syms

    return file_stocks

@timeit
def get_stock_list_object(portfolio_object:dict,session=None,list_name=None,buy_count:int=10,sell_count:int=10):
    stock_list_object = {}
    stock_download_list:list = []
    file_stocks = get_file_stocks_object()
    
    if(list_name != None and list_name in file_stocks):
        stock_download_list = file_stocks[list_name]
    
    logger.info(f'Fetching data for {len(stock_download_list)} symbols')
    stocks = []
    count = 1
    for stock in stock_download_list:
        history = get_historical_data(STK=stock,session=session)
        current = get_current_data(STK=stock)
        open_current_change  = get_open_current_change(current_data=current)
        current_stock_price = get_round(get_data_from_dict(current,'current_stock_price'))
        units = 0 if current_stock_price == 0 else round(order_price / current_stock_price)
        stocks.append({
                    'RANK' : count,
                    'SYMBOL': stock , 
                    'HISTORY' : history,
                    'CURRENT' : current,
                    'CHANGE' : get_round(open_current_change),
                    'PRICE' : current_stock_price,
                    'UNITS' : units,
                    'DESC': get_data_from_dict(current['ticker'],'longName')
                    })
        count = count + 1
            
    stocks.sort(key = lambda x:x['CHANGE'])
    stocks_buy = stocks
    stocks_sell = list(reversed(stocks))
        
    stock_list_object = {'NAME' : list_name , 
                         'STOCKS' : stocks , 
                         'STOCK_BUY' : stocks_buy[:buy_count] , 
                         'STOCK_SELL' : stocks_sell[:sell_count]
                        }
    
    return { list_name:stock_list_object} 

def get_stock_list_context(list_id:str,stock_list_object:dict,portfolio_object:dict):

    n_stocks_buy = len(stock_list_object[list_id]['STOCK_BUY'])
    n_stocks_sell = len(stock_list_object[list_id]['STOCK_SELL'])
    n_stocks_total = len(stock_list_object[list_id]['STOCKS'])

    get_key : dict = lambda key : {'rank':key['RANK'], 
                            'caption': key['SYMBOL'], 
                            'change' : key['CHANGE'] , 
                            'price' : key['PRICE'] , 
                            'units' : key['UNITS'] , 
                            'desc':key['DESC'],
                            'href' : f'/etf/history/{key['SYMBOL']}/'} 
    
    get_table : list = lambda table_key,n_stocks : [ get_key(key) for key in stock_list_object[list_id][table_key][:n_stocks]]

    return {
            'status':'success',
            'title': f'STOCKS in {stock_list_object[list_id]['NAME']}',
            'settings' : get_settings() ,
            'list_buy': 
            {
                'table_head':'BUY',
                'table' : get_table('STOCK_BUY',n_stocks_buy),    
            },
            'list_sell':
            {
                'table_head':'SELL',
                'table' : get_table('STOCK_SELL',n_stocks_sell),    
            },
            'list':
            {
                'table_head':'LIST',
                'table' : get_table('STOCKS',n_stocks_total),    
            },
            'portfolio':
            {
                'table_head':'PORTFOLIO',
                'table' : [{'caption':portfolio_object[symbol]['SYMBOL'],'rank':(index+1),'href' : f'/etf/history/{portfolio_object[symbol]['SYMBOL']}/'} for index,symbol in enumerate(portfolio_object)],    
            }
        }
    
