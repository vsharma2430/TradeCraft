from os import listdir
from os.path import join
from pathlib import Path
from base.stock_base import convert_gfinToyfin
from base.stock_history import *
from base.misc import *

stock_csv_folder = r'invest\stock_list'

@timeit
def get_stock_list(session=None):
    
    stklist_stocks = {}
    array_files = listdir(stock_csv_folder)
    
    list_name : str
    for list_name in array_files:
        file_path= join(stock_csv_folder,list_name)
        id = Path(file_path).stem.upper()
        
        stocks : list = []
        with open(file_path) as f:
            stock_syms = [convert_gfinToyfin(stock.strip()) for stock in f.readlines()]

        count = 1
        for stock in stock_syms:
            history = get_historical_data(STK=stock,session=session)
            current = get_current_data(STK=stock,session=session)
            change  = get_dma_change(history_data=history,current_data=current)
            stocks.append({
                        'RANK' : count,
                        'SYMBOL': stock , 
                        'HISTORY' : get_historical_data(STK=stock,session=session),
                        'CURRENT' : get_current_data(STK=stock,session=session),
                        'CHANGE' : get_round(change),
                        })
            count = count + 1
            
        stocks.sort(key = lambda x:x['CHANGE'])
        stocks_buy = stocks
        stocks_sell = list(reversed(stocks))
        
        stklist_stocks[id] = {'NAME' : id , 'FILE' : file_path , 'STOCKS' : stocks , 'STOCK_BUY' : stocks_buy , 'STOCK_SELL' : stocks_sell }
    
    return stklist_stocks

def get_stock_list_context(list_id:str,stock_list_object:dict,n_stocks:int=10):
    
    if(n_stocks == None):
        n_stocks = len(stock_list_object[list_id]['STOCK_BUY'])
        
    return {
            'title': f'STOCKS in {stock_list_object[list_id]['NAME']}',
            'list_buy': 
            {
                'table_head':'BUY',
                'table' : [{'rank':key['RANK'], 'caption': key['SYMBOL'], 'change' : key['CHANGE'] , 'href' : f'/etf/history/{key['SYMBOL']}/'} 
                for key in stock_list_object[list_id]['STOCK_BUY'][0:n_stocks]],    
            },
            'list_sell':
            {
                'table_head':'SELL',
                'table' : [{'rank':key['RANK'], 'caption': key['SYMBOL'], 'change' : key['CHANGE'] , 'href' : f'/etf/history/{key['SYMBOL']}/'} 
                for key in stock_list_object[list_id]['STOCK_SELL'][0:n_stocks]],    
            },
            'list':
            {
                'table_head':'LIST',
                'table' : [{'rank':key['RANK'], 'caption': key['SYMBOL'], 'change' : key['CHANGE'] , 'href' : f'/etf/history/{key['SYMBOL']}/'} 
                for key in stock_list_object[list_id]['STOCKS']],    
            }
        }
    
