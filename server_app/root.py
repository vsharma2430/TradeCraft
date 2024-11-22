from server_app import *

from fastapi import FastAPI, Request,Response
from fastapi.responses import HTMLResponse,JSONResponse,FileResponse

from base.stock_history import *
from base.stock_price import *
from base.misc import *
from invest.base import *
from invest.portfolio import *

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
    
stock_props = lambda stk_type : {'title':f'{stk_type.upper()}',
                                 'list':[{ 'caption': 'Lists' , 'href' : f'/{stk_type}/list/'},
                                         { 'caption': 'All Listed (NSE)' , 'href' : f'/{stk_type}/history/'},
                                         { 'caption': 'Portfolio' , 'href' : f'/{stk_type}/portfolio/'}],}

@app.get('/etf/',response_class=HTMLResponse)
async def root_etf(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name=template_stock_list, 
        context= stock_props(stk_type='etf')
    )

@app.get('/stock/')
async def root_stock(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name=template_stock_list, 
        context=stock_props(stk_type='stock')
    )
    

