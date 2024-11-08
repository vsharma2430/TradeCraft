from base.stock_history import *
import datetime as dt
import matplotlib.pyplot as plt
from data_scrape.read_raw import get_df_nse_etf

if(__name__ == '__main__'):
    df = get_df_nse_etf()
    etf_obj = df.to_dict('index')

    for key in etf_obj:
        etfX = etf_obj[key]
        print(f'{key} {etfX['NAME']}')
    
    index_no = input()
    stock_name = f'{etf_obj[int(index_no)]['SYMBOL']}.NS'

    df = getHistoricalData(stock_name)
    df.columns = df.columns.str.replace(' ', '') 
    print(df)

    df.plot(kind='line',x='Date',y='Close')
    plt.show()