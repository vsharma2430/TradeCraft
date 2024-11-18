from base.misc import *

portfolio_etf = r'invest\portfolio\portfolio_etf.csv'
portfolio_stock = r'invest\portfolio\portfolio_stock.csv'

#HEADER - SYMBOL,DATE,OPERATION,PRICE,QTY

def get_portfolio_stocks(csv_file)->dict:
    data = read_csv(csv_file)
    stock_dict = {}
    for dataX in data:
        stock_dict[dataX['SYMBOL']]=dataX
    return stock_dict