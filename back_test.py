from invest.history_csv import *
from invest.form_portfolio import *

if(__name__ == '__main__'):
    download_csv_interday(stock_list_id='ALL_ETF_NSE')
    perform_simulation('FIRE1YR')
    