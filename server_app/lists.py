from server_app import *

from fastapi import FastAPI, Request,Response
from fastapi.responses import HTMLResponse,JSONResponse,FileResponse

from base.stock_history import *
from base.stock_price import *
from base.misc import *
from invest.base import *
from invest.portfolio import *
from server_app.nav_bar import nav_context

# lists etf

get_list_context = lambda files_object,stk_type : {
            'title':f'{stk_type.upper()} LISTS',
            'list':[{ 'caption':str(key) , 'href' : f'/{stk_type}/list/{key}'} for key in files_object],
            **nav_context
            }

@app.get('/etf/list/',response_class=HTMLResponse)
async def root_etf_list(request: Request):
    files_object = get_file_stocks_object(folder_location=etf_csv_folder,exclude_all=True)
    
    print()

    return templates.TemplateResponse(
        request=request, 
        name=template_stock_list, 
        context=get_list_context(files_object=files_object,stk_type='etf')
    )

@app.get('/etf/list/{list_id}',response_class=HTMLResponse)
async def root_etf_list_list_id(request: Request,list_id:str):
    portfolio_object = get_portfolio_stocks_concise(csv_file=portfolio_etf)
    stock_download_list = get_stock_download_list(folder_location=etf_csv_folder,list_name=list_id)
    history_data = history_async(stock_download_list=stock_download_list,session=session,)
    current_data = current_async(stock_download_list=stock_download_list,stock_type=Stock_Type.ETF,session=session)
    stock_list_object = get_stock_list_object(portfolio_object=portfolio_object,
                                              stock_download_list=stock_download_list,
                                              list_name=list_id,
                                              history_data=history_data,
                                              current_data=current_data)
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
    files_object = get_file_stocks_object(folder_location=stock_csv_folder,exclude_all=True)
    return templates.TemplateResponse(
        request=request, 
        name=template_stock_list, 
        context=get_list_context(files_object=files_object,stk_type='stock')
    )

@app.get('/stock/list/{list_id}',response_class=HTMLResponse)
async def root_stock_list_list_id(request: Request,list_id:str):
    portfolio_object = get_portfolio_stocks_concise(csv_file=portfolio_stock)
    stock_download_list = get_stock_download_list(folder_location=stock_csv_folder,list_name=list_id)
    history_data = history_async(stock_download_list=stock_download_list,session=session,)
    current_data = current_async(stock_download_list=stock_download_list,stock_type=Stock_Type.EQUITY,session=session)
    stock_list_object = get_stock_list_object(portfolio_object=portfolio_object,
                                              stock_download_list = stock_download_list,
                                              list_name=list_id,
                                              history_data=history_data,
                                              current_data=current_data)
    context = get_stock_list_context(list_id=list_id,stock_list_object=stock_list_object,portfolio_object=portfolio_object)
    
    if(context['status'] == 'success'):
        return templates.TemplateResponse(
            request=request, 
            name=template_stock_list_stocks, 
            context=context
        )
    else:
        return JSONResponse(context)
