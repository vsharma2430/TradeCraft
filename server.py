from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from base.stock_history import *
from base.stock_price import *
from base.misc import *
from data_scrape.read_raw import get_df_nse_etf
from invest.base import get_stock_list

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')
template_stock_list = 'stock_list.html'
template_stock_data = 'stock_data.html'
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
async def root(request: Request):
    obj = get_stock_list()
    
    return templates.TemplateResponse(
        request=request, 
        name=template_stock_list, 
        context={
            'title':'STOCK LISTS',
            'list':[{ 'caption':str(key) , 'href' : f'/etf/list/{key}'} for key in obj],
            }
    )

@app.get('/etf/list/{list_id}')
async def root(request: Request,list_id:str):
    obj = get_stock_list()
    
    if(list_id in obj):
        
        return templates.TemplateResponse(
        request=request, 
        name=template_stock_list, 
        context={
            'title': f'STOCKS in {obj[list_id]['NAME']}',
            'list':[{ 'caption': key['SYMBOL'] , 'href' : f'/etf/history/{key['SYMBOL']}/'} for key in obj[list_id]['STOCK']],
            }
    )
    
    return {'message': f' ({list_id}) not present'}

# history 

@app.get('/etf/history/')
async def root(request: Request):
    return {'message': 'history'}

@app.get('/etf/history/{stk_id}/',response_class=HTMLResponse)
def stock_history(request: Request,stk_id:str):
    context = get_history_context(stk_id)
    return templates.TemplateResponse(
        request=request, 
        name=template_stock_data, 
        context=context
    )
