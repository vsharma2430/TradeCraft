from os import listdir
from os.path import join
from pathlib import Path
from base.stock_base import convert_gfinToyfin
from base.stock_history import *
from base.misc import *
from invest.investment_target import *

etf_csv_folder = r'invest\stock_list\ETF'
stock_csv_folder = r'invest\stock_list\stock'

def get_file_stocks_object(folder_location:str):
    array_files = listdir(folder_location)
    
    list_name : str
    file_stocks = {}
    stock_header = ''

    for list_name in array_files:
        file_path= join(folder_location,list_name)
        id = Path(file_path).stem.upper()
        
        data = read_csv(file_path)
        with open(file_path) as f:
            if(len(data)>0):
                if('SYMBOL' in data[0]):
                    stock_header = 'SYMBOL'
                elif('Symbol' in data[0]):
                    stock_header = 'Symbol'
                elif('SYM' in data[0]):
                    stock_header = 'SYM'

                stock_syms = [get_yfin_symbol(dataX[stock_header]) for dataX in data]
                file_stocks[id] = stock_syms

    return file_stocks

@timeit
def get_stock_list_object(portfolio_object:dict,folder_location:str,stock_type:Stock_Type,session=None,list_name=None,buy_count:int=10,sell_count:int=10):
    stock_list_object = {}
    stock_download_list:list = []
    file_stocks = get_file_stocks_object(folder_location=folder_location)
    
    if(list_name != None and list_name in file_stocks):
        stock_download_list = file_stocks[list_name]
    
    logger.info(f'Fetching data for {len(stock_download_list)} symbols')
    stocks = []
    count = 1
    
    portfolio_stocks = set([get_plain_stock(x) for x in portfolio_object])
    
    for stock in stock_download_list:
        plain_stock_sym = get_plain_stock(stock)
        history = get_historical_data(STK=stock,session=session)
        current = get_current_data(STK=stock,stock_type=stock_type)
        open_current_change  = get_open_current_change(current_data=current)
        current_stock_price = get_round(get_data_from_dict(current,'current_stock_price'))
        units = 0 if current_stock_price == 0 else round(order_price / current_stock_price)
        portfolio_stk_object = get_data_from_dict(portfolio_object,plain_stock_sym)
        portfolio_price = get_float(get_data_from_dict(portfolio_stk_object,'PRICE'))
        portfolio_change = get_change(portfolio_price,current_stock_price)
        if(portfolio_stk_object is not None):
            portfolio_stk_object['PL'] = portfolio_change
        
        stocks.append({
                    'RANK' : count,
                    'SYMBOL': stock , 
                    'PLAIN_STK' : plain_stock_sym,
                    'HISTORY' : history,
                    'CURRENT' : current,
                    'CHANGE' : get_round(open_current_change),
                    'PRICE' : current_stock_price,
                    'UNITS' : units,
                    'DESC': get_data_from_dict(current['ticker'],'longName'),
                    'PL' : portfolio_change
                    })
        count = count + 1
    
    stocks.sort(key = lambda x:x['CHANGE'])
    stocks_buy = stocks
    stocks_sell = list(reversed(stocks))
    
    stocks_buy_person = [x if x['PLAIN_STK'] not in portfolio_stocks else None for x in stocks_buy]
    stocks_sell_person = [x if (x['PLAIN_STK'] in portfolio_stocks and x['PL']>=sell_target) else None for x in stocks_sell]
    stocks_buy_person = clean_list(stocks_buy_person)
    stocks_sell_person = clean_list(stocks_sell_person)

    stock_list_object = {'NAME' : list_name , 
                         'STOCKS' : stocks , 
                         'STOCK_BUY' : stocks_buy_person[:buy_count] , 
                         'STOCK_SELL' : stocks_sell_person[:sell_count]
                        }
    
    return { list_name:stock_list_object} 

def get_stock_list_context(list_id:str,stock_list_object:dict,portfolio_object:dict):

    n_stocks_buy = len(stock_list_object[list_id]['STOCK_BUY'])
    n_stocks_sell = len(stock_list_object[list_id]['STOCK_SELL'])
    n_stocks_total = len(stock_list_object[list_id]['STOCKS'])

    get_stock_key : dict = lambda key : {'rank': get_data_from_dict(key,'RANK'), 
                                        'caption': get_data_from_dict(key,'SYMBOL'),
                                        'change' : get_data_from_dict(key,'CHANGE'), 
                                        'price' : get_data_from_dict(key,'PRICE'),
                                        'units' : get_data_from_dict(key,'UNITS'),
                                        'desc': get_data_from_dict(key,'DESC'),
                                        'href' : f'/etf/history/{get_data_from_dict(key,'SYMBOL')}/'} 
    
    get_table : list = lambda table_key,n_stocks : [ get_stock_key(key) for key in stock_list_object[list_id][table_key][:n_stocks]]

    get_portfolio_key :dict = lambda index,portfolio : {
                                                        'caption': get_data_from_dict(portfolio,'SYMBOL'),
                                                        'rank': (index+1),
                                                        'change': get_percentage_format(get_data_from_dict(portfolio,'PL')), 
                                                        'href' : f'/etf/history/{get_data_from_dict(portfolio,'SYMBOL')}/'} 
    
    get_portfolio : list = lambda portfolio : [get_portfolio_key(index,portfolio[symbol]) for index,symbol in enumerate(portfolio)]

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
                'table' : get_portfolio(portfolio_object),    
            }
        }
    
