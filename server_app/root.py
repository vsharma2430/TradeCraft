from server_app import *

from fastapi import FastAPI, Request,Response
from fastapi.responses import HTMLResponse,JSONResponse,FileResponse

from base.stock_history import *
from base.stock_price import *
from base.misc import *
from invest.base import *
from invest.portfolio import *
from server_app.nav_bar import nav_context

# root

@app.get('/',response_class=HTMLResponse)
@app.get('/etf/',response_class=HTMLResponse)
@app.get('/stock/',response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name=template_home, 
        context=nav_context,
    )