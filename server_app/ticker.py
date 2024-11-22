from server_app import *

from fastapi import FastAPI, Request,Response
from fastapi.responses import HTMLResponse,JSONResponse,FileResponse

from base.stock_history import *
from base.stock_price import *
from base.misc import *
from invest.base import *
from invest.portfolio import *

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