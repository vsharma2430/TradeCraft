from base.stock_price import *
from data_scrape.read_raw import get_df_nse_etf

if(__name__ == '__main__'):
    df = get_df_nse_etf()
    etf_obj = df.to_dict('index')

    for key in etf_obj:
        etfX = etf_obj[key]
        print(f'{key} {etfX['NAME']}')

    index_no = input()
    stock_name = f'{etf_obj[int(index_no)]['SYMBOL']}.NS'
    print(get_stock_price_print(stock_name))