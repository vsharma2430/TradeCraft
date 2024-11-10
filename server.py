from fastapi import FastAPI
from base.stock_history import *
import datetime as dt
import matplotlib.pyplot as plt
from data_scrape.read_raw import get_df_nse_etf
from invest.base import get_stock_list
from fastapi.responses import HTMLResponse

app = FastAPI()

# root

@app.get('/')
async def root():
    return {'message': 'Welcome to PyETF server!'}

@app.get('/etf/')
async def root():
    return {'message': 'etf main page'}

# today

@app.get('/etf/today/')
async def root():
    return {'message': 'today'}

@app.get('/etf/today/buy/')
async def root():
    return {'message': 'buy'}

@app.get('/etf/today/sell/')
async def root():
    return {'message': 'sell'}

# lists

@app.get('/etf/list/')
async def root():
    obj = get_stock_list()
    return obj

@app.get('/etf/list/{list_id}')
async def root(list_id):
    obj = get_stock_list()
    if(list_id in obj):
        return obj[list_id]
    return {'message': f' {list_id}) not present'}

# history 

@app.get('/etf/history/')
async def root():
    return {'message': 'history'}

@app.get('/etf/history/{stk_id}/')
async def read_item(stk_id):
    return HTMLResponse(get_historical_data(get_stock_symbol(stk_id)).to_html())
