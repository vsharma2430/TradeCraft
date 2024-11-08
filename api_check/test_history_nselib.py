import pandas as pd
from nselib import capital_market

from_date_str = '05-05-2021'
to_date_str = '03-05-2024'

time_periods = [('06-05-2019', '04-05-2021'), ('05-05-2021', '03-05-2024')]
index_data = pd.DataFrame()

for (from_date_str, to_date_str) in time_periods:
    temp_index_data = capital_market.index_data(index='Nifty Midcap 150', from_date=from_date_str, to_date=to_date_str)
    temp_index_data['TIMESTAMP'] = pd.to_datetime(temp_index_data['TIMESTAMP'], format='%d-%m-%Y')
    index_data = pd.concat([index_data, temp_index_data])
    
index_data = index_data.sort_values('TIMESTAMP').reset_index(drop=True)

print(index_data)