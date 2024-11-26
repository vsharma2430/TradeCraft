from invest.history_csv import *
from invest.form_portfolio import *

if(__name__ == '__main__'):

    prompt = input('Download stock data ?  (y/n) (default:n) ')
    download_data = True if prompt == 'y' else False

    if(download_data):
        download_csv_interday()

    perform_simulation()
    