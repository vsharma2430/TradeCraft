import pandas as pd

def get_df_nse_etf()->pd.DataFrame:
    return pd.read_csv(r'data_scrape\raw\etf_all_nse.csv')

def get_df_icom_etf()->pd.DataFrame:
    return pd.read_html(r'data_scrape\raw\investing_com_all_etf.html', header=0)[0]

if(__name__ == '__main__'):
    df = get_df_icom_etf()
    pd.DataFrame({"Symbol": df['Symbol'].tolist(), "Name": df['Name'].tolist()}).to_csv(r'data_scrape\output\etf_all.csv')
    
    df = get_df_nse_etf()
    pd.DataFrame({"Symbol": df['SYMBOL'].tolist(), "Name": df['NAME'].tolist()}).to_csv(r'data_scrape\output\etf.csv')