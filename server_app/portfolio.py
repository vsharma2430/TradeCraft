from server_app import *

from fastapi import FastAPI, Request,Response
from fastapi.responses import HTMLResponse,JSONResponse,FileResponse

from base.stock_history import *
from base.stock_price import *
from base.misc import *
from invest.base import *
from invest.portfolio import *
from server_app.nav_bar import nav_context

get_portfolio_context = lambda stk_type,portfolio_object : {
            'title':f'{stk_type.upper()} Portfolio',
            'portfolio':portfolio_object,
            **nav_context
            }

# portfolio etf
@app.get('/etf/portfolio/',response_class=HTMLResponse)
async def root_etf(request: Request):
    portfolio_object = get_portfolio_stocks_concise(csv_file=portfolio_etf)
    return templates.TemplateResponse(
        request=request, 
        name=template_portfolio, 
        context=get_portfolio_context(stk_type='etf',portfolio_object=portfolio_object)
    )
    
# portfolio stock
@app.get('/stock/portfolio/',response_class=HTMLResponse)
async def root_etf(request: Request):
    portfolio_object = get_portfolio_stocks_concise(csv_file=portfolio_stock)
    return templates.TemplateResponse(
        request=request, 
        name=template_portfolio, 
        context=get_portfolio_context(stk_type='stock',portfolio_object=portfolio_object)
    )
