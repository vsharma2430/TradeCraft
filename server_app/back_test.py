from server_app import *

from fastapi import FastAPI, Request,Response
from fastapi.responses import HTMLResponse,JSONResponse,FileResponse

from base.stock_history import *
from base.stock_price import *
from base.misc import *
from invest.base import *
from invest.portfolio import *
from invest.form_portfolio import *
from invest.history_csv import *

@app.get('/etf/backtest/',response_class=HTMLResponse)
async def root_etf_list(request: Request):
    files_object = get_file_stocks_object(folder_location=etf_csv_folder,exclude_all=True)
    return templates.TemplateResponse(
        request=request, 
        name=template_stock_list, 
        context={
            'title':'ETF LISTS BACKTESTING',
            'list':[{ 'caption':str(key) , 'href' : f'/etf/backtest/{key}'} for key in files_object],
            }
    )

@app.get('/etf/backtest/{list_id}',response_class=HTMLResponse)
async def root_etf_history(request: Request,list_id:str):
    download_csv_interday(stock_list_id=list_id)
    result = perform_simulation(list_name=list_id)
    return templates.TemplateResponse(
        request=request, 
        name=template_backtest, 
        context={
            'title':f'BACKTEST FOR {list_id}',
            'result': result,
            }
    )