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
    
stock_props = lambda stk : {'title':f'{stk.upper()}',
                                 'list':[{ 'caption': 'Lists' , 'href' : f'/{stk}/list/'},
                                         { 'caption': 'All Listed (NSE)' , 'href' : f'/{stk}/history/'},
                                         { 'caption': 'Portfolio' , 'href' : f'/{stk}/portfolio/'},
                                         { 'caption': 'Backtest' , 'href' : f'/{stk}/backtest/'} if stk == 'etf' else None,
                                         ],}

@app.get('/etf/',response_class=HTMLResponse)
async def root_etf(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name=template_stock_list, 
        context= stock_props(stk='etf')
    )

@app.get('/stock/')
async def root_stock(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name=template_stock_list, 
        context=stock_props(stk='stock')
    )
    

