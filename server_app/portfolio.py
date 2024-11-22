from server_app import *

from fastapi import FastAPI, Request,Response
from fastapi.responses import HTMLResponse,JSONResponse,FileResponse

from base.stock_history import *
from base.stock_price import *
from base.misc import *
from invest.base import *
from invest.portfolio import *

# portfolio etf
@app.get('/etf/portfolio/',response_class=HTMLResponse)
async def root_etf(request: Request):
    portfolio_object = get_portfolio_stocks_concise(csv_file=portfolio_etf)
    return templates.TemplateResponse(
        request=request, 
        name=template_portfolio, 
        context={
            'title':'ETF Portfolio',
            'portfolio':portfolio_object
            }
    )
    
# portfolio stock
@app.get('/stock/portfolio/',response_class=HTMLResponse)
async def root_etf(request: Request):
    portfolio_object = get_portfolio_stocks_concise(csv_file=portfolio_stock)
    return templates.TemplateResponse(
        request=request, 
        name=template_portfolio, 
        context={
            'title':'ETF Portfolio',
            'portfolio':portfolio_object
            }
    )
