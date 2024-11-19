from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse,JSONResponse,FileResponse
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
from invest.portfolio import *

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
    backend=SQLiteCache(r'cache\yfinance.cache'),
)

#favicon
favicon_path = f'static/images/favicon.ico'
@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)

# root

@app.get('/',response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name=template_stock_list, 
        context={
            'title':'TRADE CRAFT - Home',
            'list':[{ 'caption': 'ETF' , 'href' : f'/etf/'},
                { 'caption': 'Stock' , 'href' : f'/stock/'}],
            }
    )

@app.get('/etf/',response_class=HTMLResponse)
async def root_etf(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name=template_stock_list, 
        context={
            'title':'ETF',
            'list':[{ 'caption': 'Lists' , 'href' : f'/etf/list/'},
                    { 'caption': 'All Listed (NSE)' , 'href' : f'/etf/history/'},
                    { 'caption': 'Portfolio' , 'href' : f'/etf/portfolio/'}],
            }
    )

@app.get('/stock/')
async def root_stock(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name=template_stock_list, 
        context={
            'title':'Stock',
            'list':[
                { 'caption': 'Lists' , 'href' : f'/stock/list/'},
                { 'caption': 'All Listed (NSE)' , 'href' : f'/stock/history/'},
                { 'caption': 'Portfolio' , 'href' : f'/stock/portfolio/'}],
            }
    )

# lists etf

@app.get('/etf/list/',response_class=HTMLResponse)
async def root_etf_list(request: Request):
    files_object = get_file_stocks_object(folder_location=etf_csv_folder)
    return templates.TemplateResponse(
        request=request, 
        name=template_stock_list, 
        context={
            'title':'ETF LISTS',
            'list':[{ 'caption':str(key) , 'href' : f'/etf/list/{key}'} for key in files_object],
            }
    )

@app.get('/etf/list/{list_id}',response_class=HTMLResponse)
async def root_etf_list_list_id(request: Request,list_id:str):
    portfolio_object = get_portfolio_stocks_concise(csv_file=portfolio_etf)
    stock_list_object = get_stock_list_object(portfolio_object=portfolio_object,stock_type=Stock_Type.ETF,folder_location=etf_csv_folder,session=session,list_name=list_id)
    context = get_stock_list_context(list_id=list_id,stock_list_object=stock_list_object,portfolio_object=portfolio_object)
    
    if(context['status'] == 'success'):
        return templates.TemplateResponse(
            request=request, 
            name=template_stock_list_stocks, 
            context=context
        )
    else:
        return JSONResponse(context)

# lists stock

@app.get('/stock/list/',response_class=HTMLResponse)
async def root_stock_list(request: Request):
    files_object = get_file_stocks_object(folder_location=stock_csv_folder)
    return templates.TemplateResponse(
        request=request, 
        name=template_stock_list, 
        context={
            'title':'STOCK LISTS',
            'list':[{ 'caption':str(key) , 'href' : f'/stock/list/{key}'} for key in files_object],
            }
    )

@app.get('/stock/list/{list_id}',response_class=HTMLResponse)
async def root_stock_list_list_id(request: Request,list_id:str):
    portfolio_object = get_portfolio_stocks_concise(csv_file=portfolio_stock)
    stock_list_object = get_stock_list_object(portfolio_object=portfolio_object,stock_type=Stock_Type.EQUITY,folder_location=stock_csv_folder,session=session,list_name=list_id)
    context = get_stock_list_context(list_id=list_id,stock_list_object=stock_list_object,portfolio_object=portfolio_object)
    
    if(context['status'] == 'success'):
        return templates.TemplateResponse(
            request=request, 
            name=template_stock_list_stocks, 
            context=context
        )
    else:
        return JSONResponse(context)


# history etf

@app.get('/etf/history/',response_class=HTMLResponse)
async def root_etf_history(request: Request):
    files_object = get_file_stocks_object(etf_csv_folder)
    stocks = []
    for file in files_object:
        stocks.extend(files_object[file])

    stocks = list(set(stocks))
    stocks.sort()
    return templates.TemplateResponse(
        request=request, 
        name=template_stock_list, 
        context={
            'title':'ETFs',
            'list':[{ 'caption': get_plain_stock(str(key)) , 'href' : f'/etf/history/{key}'} for key in stocks],
            }
    )

@app.get('/etf/history/{stk_id}/',response_class=HTMLResponse)
async def root_etf_history_id(request: Request,stk_id:str,chart:int=0):
    context = get_history_context(STK=stk_id,stock_type=Stock_Type.ETF,session=session,simple= True if chart == 0 else False,chart_type=chart)
    add_chart_context(context=context,chart=chart)
    
    return templates.TemplateResponse(
        request=request, 
        name=template_stock_data, 
        context=context
    )

# history stock

@app.get('/stock/history/',response_class=HTMLResponse)
async def root_stock_history(request: Request):
    files_object = get_file_stocks_object(stock_csv_folder)
    stocks = []
    for file in files_object:
        stocks.extend(files_object[file])

    stocks = list(set(stocks))
    stocks.sort()
    return templates.TemplateResponse(
        request=request, 
        name=template_stock_list, 
        context={
            'title':'Stocks',
            'list':[{ 'caption': get_plain_stock(str(key)) , 'href' : f'/stock/history/{key}'} for key in stocks],
            }
    )

@app.get('/stock/history/{stk_id}/',response_class=HTMLResponse)
async def root_stock_history_id(request: Request,stk_id:str,chart:int=0):
    context = get_history_context(STK=stk_id,stock_type=Stock_Type.EQUITY,session=session,simple= True if chart == 0 else False)
    add_chart_context(context=context,chart=chart)
    
    return templates.TemplateResponse(
        request=request, 
        name=template_stock_data, 
        context=context
    )


# ticker and price query

@app.get('/etf/ticker/{stk_id}/',response_class=JSONResponse)
@app.get('/stock/ticker/{stk_id}/',response_class=JSONResponse)
async def root_ticker(request: Request,stk_id:str):
    return {'ticker': get_ticker_info(STK=stk_id,session=session)}

@app.get('/etf/query/{stk_id}/{variable}',response_class=JSONResponse)
@app.get('/stock/query/{stk_id}/{variable}',response_class=JSONResponse)
async def root_query(request: Request,stk_id:str,variable:str):
    ticker = get_ticker_info(STK=stk_id,session=session)
    return {f'{variable}': get_data_from_dict(ticker,variable) }

@app.get('/etf/query/{stk_id}/price',response_class=JSONResponse)
async def root_etf_price(request: Request,stk_id:str):
    return {'price': get_stock_price(STK=stk_id,stock_type=Stock_Type.ETF,session=session)}

@app.get('/stock/query/{stk_id}/price',response_class=JSONResponse)
async def root_stock_price(request: Request,stk_id:str):
    return {'price': get_stock_price(STK=stk_id,stock_type=Stock_Type.EQUITY,session=session)}