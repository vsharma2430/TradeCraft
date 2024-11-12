from os import listdir
from os.path import join
from pathlib import Path
from base.stock_base import convert_gfinToyfin
from base.stock_history import *
from base.misc import *
from invest.investment_target import *

stock_csv_folder = r'invest\stock_list'

def get_file_stocks_object():
    array_files = listdir(stock_csv_folder)
    
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
def get_stock_list_data(session=None,file_name=None,buy_count:int=10,sell_count:int=10):
    stock_list_object = {}
    stock_download_list:list = []
    file_stocks = get_file_stocks_object()
    
    if(file_name != None and file_name in file_stocks):
        stock_download_list = file_stocks[file_name]
    
    logger.info(stock_download_list)
    stocks = []
    count = 1
    for stock in stock_download_list:
        history = get_historical_data(STK=stock,session=session)
        current = get_current_data(STK=stock,session=session)
        change  = get_dma_change(history_data=history,current_data=current)
        current_stock_price = get_round(get_data_from_dict(current,'current_stock_price'))
        units = 0 if current_stock_price == 0 else round(order_price / current_stock_price)
        stocks.append({
                    'RANK' : count,
                    'SYMBOL': stock , 
                    'HISTORY' : get_historical_data(STK=stock,session=session),
                    'CURRENT' : get_current_data(STK=stock,session=session),
                    'CHANGE' : get_round(change),
                    'PRICE' : current_stock_price,
                    'UNITS' : units
                    })
        count = count + 1
            
    stocks.sort(key = lambda x:x['CHANGE'])
    stocks_buy = stocks
    stocks_sell = list(reversed(stocks))
        
    stock_list_object = {'NAME' : file_name , 
                         'STOCKS' : stocks , 
                         'STOCK_BUY' : stocks_buy[:buy_count] , 
                         'STOCK_SELL' : stocks_sell[:sell_count]
                        }
    
    return { file_name:stock_list_object} 

def get_stock_list_context(list_id:str,stock_list_object:dict):
    
    n_stocks = len(stock_list_object[list_id]['STOCK_BUY'])
        
    return {
            'status':'success',
            'title': f'STOCKS in {stock_list_object[list_id]['NAME']}',
            'settings' : get_settings() ,
            'list_buy': 
            {
                'table_head':'BUY',
                'table' : [{'rank':key['RANK'], 'caption': key['SYMBOL'], 'change' : key['CHANGE'] , 'price' : key['PRICE'] , 'units' : key['UNITS'] , 'href' : f'/etf/history/{key['SYMBOL']}/'} 
                for key in stock_list_object[list_id]['STOCK_BUY'][0:n_stocks]],    
            },
            'list_sell':
            {
                'table_head':'SELL',
                'table' : [{'rank':key['RANK'], 'caption': key['SYMBOL'], 'change' : key['CHANGE'] , 'price' : key['PRICE'] , 'units' : key['UNITS'] , 'href' : f'/etf/history/{key['SYMBOL']}/'} 
                for key in stock_list_object[list_id]['STOCK_SELL'][0:n_stocks]],    
            },
            'list':
            {
                'table_head':'LIST',
                'table' : [{'rank':key['RANK'], 'caption': key['SYMBOL'], 'change' : key['CHANGE'] , 'price' : key['PRICE'] , 'units' : key['UNITS'] , 'href' : f'/etf/history/{key['SYMBOL']}/'} 
                for key in stock_list_object[list_id]['STOCKS']],    
            }
        }
    
