from os import listdir
from os.path import join
from pathlib import Path
from base.stock_base import convert_gfinToyfin
from base.stock_history import *
from base.misc import *
from invest.investment_target import *
from invest.trade import *
from server_app.nav_bar import nav_context

etf_csv_folder = r'invest\stock_list\ETF'
stock_csv_folder = r'invest\stock_list\stock'
us_stocks_csv = r'invest\stock_list\US'

def get_file_stocks_object(folder_location:str,exclude_all:bool=False):
    array_files = listdir(folder_location)
    
    list_name : str
    file_stocks = {}
    stock_header = ''

    for list_name in array_files:
        file_path= join(folder_location,list_name)
        id = Path(file_path).stem.upper()
        
        if(id.startswith('ALL') and 'NSE' in id and exclude_all):
            continue
        
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

def get_stock_download_list(folder_location:str,list_name=None):
    stock_download_list:list = []
    file_stocks = get_file_stocks_object(folder_location=folder_location)
    
    if(list_name != None and list_name in file_stocks):
        stock_download_list = file_stocks[list_name]
    return stock_download_list

@timeit_concise
def history_async(stock_download_list:list,session=None):
    logger.info(f'Fetching history data for {len(stock_download_list)} symbols')

    history_stks = {}
    for stock in stock_download_list:
        history_stks[stock] = get_historical_data(STK=stock,session=session)

    return history_stks

@timeit_concise
def current_async(stock_download_list:list,stock_type:Stock_Type,session=None):
    logger.info(f'Fetching current data for {len(stock_download_list)} symbols')

    current_stks = {}
    for stock in stock_download_list:
        current_stks[stock] = get_current_data(STK=stock,stock_type=stock_type)

    return current_stks

def get_stock_list_object(portfolio_object:dict,
                          stock_download_list:list,list_name:str,
                          history_data:dict,current_data:dict,
                          buy_count:int=10,sell_count:int=10):
    stocks = []
    portfolio_stocks = set([get_plain_stock(x) for x in portfolio_object])
    
    for index,stock in enumerate(stock_download_list):
        plain_stock_sym = get_plain_stock(stock)
        history_data_stk = history_data[stock]
        current_data_stk = current_data[stock]
        open_current_change  = get_open_current_change(current_data=current_data_stk,history_data=history_data_stk['df'])
        current_stock_price = get_round(get_data_from_dict(current_data_stk,'current_stock_price'))
        units = 0 if current_stock_price == 0 else round(order_price / current_stock_price)

        portfolio_stk_object : Trade = get_data_from_dict(portfolio_object,plain_stock_sym)
        if(portfolio_stk_object is not None):
            portfolio_price = portfolio_stk_object.price
            portfolio_change = get_change(portfolio_price,current_stock_price)
            portfolio_stk_object.pl = portfolio_change
        
        stocks.append({
                    'RANK' : index+1,
                    'SYMBOL': stock , 
                    'PLAIN_STK' : plain_stock_sym,
                    'HISTORY' : history_data_stk,
                    'CURRENT' : current_data_stk,
                    'CHANGE' : get_round(open_current_change),
                    'PRICE' : current_stock_price,
                    'UNITS' : units,
                    'DESC': get_data_from_dict(current_data_stk['ticker'],'longName'),
                    'PL' : portfolio_stk_object.pl if portfolio_stk_object is not None else 0
                    })
    
    stocks.sort(key = lambda x:x['CHANGE'])
    stocks_buy = stocks
    stocks_sell = list(reversed(stocks))
    
    stocks_buy_person = [x if x['PLAIN_STK'] not in portfolio_stocks else None for x in stocks_buy]
    stocks_sell_person = [x if (x['PLAIN_STK'] in portfolio_stocks and x['PL']>=sell_target) else None for x in stocks_sell]
    stocks_buy_person = clean_list(stocks_buy_person)
    stocks_sell_person = clean_list(stocks_sell_person)

    return { list_name:{ 'NAME' : list_name , 
                         'STOCKS' : stocks , 
                         'STOCK_BUY' : stocks_buy_person[:buy_count] , 
                         'STOCK_SELL' : stocks_sell_person[:sell_count]
                        }} 

def get_stock_list_context(list_id:str,stock_list_object:dict,portfolio_object:dict):

    n_stocks_buy = len(stock_list_object[list_id]['STOCK_BUY'])
    n_stocks_sell = len(stock_list_object[list_id]['STOCK_SELL'])
    n_stocks_total = len(stock_list_object[list_id]['STOCKS'])
    
    stocks_syms = [x['SYMBOL'] for x in stock_list_object[list_id]['STOCKS']]

    get_buy_stock_key : dict = lambda key : {'rank': get_data_from_dict(key,'RANK'), 
                                        'caption': get_data_from_dict(key,'SYMBOL'),
                                        'change' : get_data_from_dict(key,'CHANGE'), 
                                        'price' : get_data_from_dict(key,'PRICE'),
                                        'units' : get_data_from_dict(key,'UNITS'),
                                        'desc': get_data_from_dict(key,'DESC'),
                                        'href' : f'/etf/history/{get_data_from_dict(key,'SYMBOL')}/'} 
    
    get_sell_stock_key : dict = lambda key : {'rank': get_data_from_dict(key,'RANK'), 
                                        'caption': get_data_from_dict(key,'SYMBOL'),
                                        'change' : get_percentage_format(get_data_from_dict(key,'PL')), 
                                        'price' : get_data_from_dict(key,'PRICE'),
                                        'desc': get_data_from_dict(key,'DESC'),
                                        'href' : f'/etf/history/{get_data_from_dict(key,'SYMBOL')}/'} 
    
    get_table : list = lambda fn=get_buy_stock_key,table_key=None,n_stocks=len(stock_list_object) : [ fn(key) for key in stock_list_object[list_id][table_key][:n_stocks]]

    get_portfolio_key :dict = lambda index,portfolio : {
                                                        'caption': portfolio.symbol,
                                                        'rank': (index+1),
                                                        'change': get_percentage_format(portfolio.pl), 
                                                        'price':portfolio.price,
                                                        'units':portfolio.quantity,
                                                        'href' : f'/etf/history/{portfolio.symbol}/'
                                                        } if (portfolio.symbol in stocks_syms) else None
    
    get_portfolio : list = lambda portfolio : [get_portfolio_key(index,portfolio[symbol]) for index,symbol in enumerate(portfolio)]

    return {
            'status':'success',
            'title': f'STOCKS in {stock_list_object[list_id]['NAME']}',
            'settings' : get_settings() ,
            'list_buy': 
            {
                'table_head':'BUY',
                'table' : get_table(get_buy_stock_key,'STOCK_BUY',n_stocks_buy),    
            },
            'list_sell':
            {
                'table_head':'SELL',
                'table' : get_table(get_sell_stock_key,'STOCK_SELL',n_stocks_sell),    
            },
            'list':
            {
                'table_head':'LIST',
                'table' : get_table(get_buy_stock_key,'STOCKS',n_stocks_total),    
            },
            'portfolio':
            {
                'table_head':'PORTFOLIO',
                'table' : clean_list(get_portfolio(portfolio_object)),    
            },
            **nav_context
        }
    
