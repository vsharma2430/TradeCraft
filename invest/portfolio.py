from base.misc import *
from base.stock_base import *
from invest.trade import *

portfolio_etf = r'invest\portfolio\portfolio_etf.csv'
portfolio_stock = r'invest\portfolio\portfolio_stock.csv'

#HEADER - SYMBOL,DATE,OPERATION,PRICE,QTY

def add_stock_data(a:Trade,b:Trade):
    return a

def get_portfolio_stocks_concise(csv_file)->dict:
    data = read_csv(csv_file)
    stock_dict = {}
    for dataX in data:
        plain_stock = get_plain_stock(dataX['SYMBOL'])
        stock_dict[plain_stock]= Trade(symbol= dataX['SYMBOL'],
                                       price=get_float(dataX['PRICE']),
                                       quantity=get_float(dataX['QTY']),
                                       date=get_datetime(dataX['DATE']),
                                       operation=Stock_Trade.BUY if 'buy' in dataX['OPERATION'].lower() else Stock_Trade.SELL)

    return stock_dict