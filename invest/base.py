from os import listdir
from os.path import join
from pathlib import Path
from base.stock_base import convert_gfinToyfin
from base.stock_history import get_historical_data

stock_csv_folder = r'invest\stock_list'

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
        
        stocks = [{'SYMBOL': stock , 'HISTORY' :  get_historical_data(STK=stock,session=session)} for stock in stock_syms]
        stklist_stocks[id] = {'NAME' : id , 'FILE' : file_path , 'STOCK' : stocks }
    
    return stklist_stocks