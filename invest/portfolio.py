from base.misc import *
from base.stock_base import *

portfolio_etf = r'invest\portfolio\portfolio_etf.csv'
portfolio_stock = r'invest\portfolio\portfolio_stock.csv'

#HEADER - SYMBOL,DATE,OPERATION,PRICE,QTY

def get_portfolio_stocks(csv_file)->dict:
    data = read_csv(csv_file)
    stock_dict = {}
    for dataX in data:
        plain_stock = get_plain_stock(dataX['SYMBOL'])
        dataX['PLAIN_STK'] = plain_stock
        stock_dict[plain_stock]=dataX
    return stock_dict