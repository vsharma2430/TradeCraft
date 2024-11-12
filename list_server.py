from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI
from requests import Session
from requests_cache import CacheMixin, SQLiteCache
from requests_ratelimiter import LimiterMixin, MemoryQueueBucket
from pyrate_limiter import Duration, RequestRate, Limiter

from base.stock_history import *
from base.stock_price import *
from base.misc import *
from invest.base import *

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')
template_stock_list = 'stock_list.html'
template_stock_list_stocks = 'stock_list_stocks.html'
template_stock_data = 'stock_data.html'

class CachedLimiterSession(CacheMixin, LimiterMixin, Session):
    pass
session = CachedLimiterSession(
    limiter=Limiter(RequestRate(2, Duration.SECOND*5)),  # max 2 requests per 5 seconds
    bucket_class=MemoryQueueBucket,
    backend=SQLiteCache(r"cache\yfinance.cache"),
)

# root

@app.get('/')
async def root():
    return {'message': 'Welcome to PyETF server!'}

@app.get('/etf/')
async def root():
    return {'message': 'etf main page'}

#price

@app.get('/etf/price/{stk_id}/',response_class=JSONResponse)
def stock_price(request: Request,stk_id:str):
    return {'price': get_stock_price(STK=stk_id,session=None)}

# lists

@app.get('/etf/list/')
async def root(request: Request):
    files_object = get_file_stocks_object()
    
    return templates.TemplateResponse(
        request=request, 
        name=template_stock_list, 
        context={
            'title':'STOCK LISTS',
            'list':[{ 'caption':str(key) , 'href' : f'/etf/list/{key}'} for key in files_object],
            }
    )

@app.get('/etf/list/{list_id}')
async def root(request: Request,list_id:str):
    stock_list_object = get_stock_list_data(session=session,file_name=list_id)
    context = get_stock_list_context(list_id=list_id,stock_list_object=stock_list_object)
    
    if(context['status'] == 'success'):
        return templates.TemplateResponse(
            request=request, 
            name=template_stock_list_stocks, 
            context=context
        )
    else:
        return JSONResponse(context)

# history 

@app.get('/etf/history/')
async def root(request: Request):
    return {'message': 'history'}

@app.get('/etf/history/{stk_id}/',response_class=HTMLResponse)
def stock_history(request: Request,stk_id:str):
    context = get_history_context(STK=stk_id,session=session)
    return templates.TemplateResponse(
        request=request, 
        name=template_stock_data, 
        context=context
    )

