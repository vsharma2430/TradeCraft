from server_app import *

from fastapi import FastAPI, Request,Response
from fastapi.responses import HTMLResponse,JSONResponse,FileResponse

from base.stock_history import *
from base.stock_price import *
from base.misc import *
from invest.base import *
from invest.portfolio import *


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
async def root_etf_history_id(request: Request,stk_id:str,stock_data:int=2,chart:int=1,exchange:int=1):
    context = get_history_context(STK=stk_id,stock_exchange=Stock_Exchange(exchange),stock_type=Stock_Type.ETF,session=session,chart_type=Chart_Type(chart),stock_data_display=Stock_Page(stock_data))
    add_chart_context(context=context,chart=Chart_Type(chart))

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
async def root_stock_history_id(request: Request,stk_id:str,stock_data:int=1,chart:int=1,exchange:int=1):
    context = get_history_context(STK=stk_id,stock_exchange=Stock_Exchange(exchange),stock_type=Stock_Type.EQUITY,session=session,chart_type=Chart_Type(chart),stock_data_display=Stock_Page(stock_data))
    add_chart_context(context=context,chart=Chart_Type(chart))
    
    return templates.TemplateResponse(
        request=request, 
        name=template_stock_data, 
        context=context
    )




