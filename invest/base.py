from os import listdir
from os.path import join
from pathlib import Path
from base.stock_base import convert_gfinToyfin

stock_csv_folder = r'invest\stock_list'

def get_stock_list():
    
    stklist_stocks = {}
    array_files = listdir(stock_csv_folder)
    
    list_name : str
    for list_name in array_files:
        file_path= join(stock_csv_folder,list_name)
        id = Path(file_path).stem.upper()
        
        stocks : list = []
        with open(file_path) as f:
            stocks = [{'SYMBOL':convert_gfinToyfin(stock.strip())} for stock in f.readlines()]
        
        stklist_stocks[id] = {'NAME' : id , 'FILE' : file_path , 'STOCK' : stocks}
    
    return stklist_stocks