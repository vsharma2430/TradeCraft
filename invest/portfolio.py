from base.misc import *

def get_portfolio_stocks(csv_file='invest\portfolio\portfolio.csv')->dict:
    data = read_csv(csv_file)
    stock_dict = {}
    for dataX in data:
        stock_dict[dataX['SYMBOL']]=dataX
    return stock_dict