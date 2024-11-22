import os
import signal
from fastapi import FastAPI, Request,Response
from fastapi.responses import HTMLResponse,JSONResponse,FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI
from requests import Session
from requests_cache import CacheMixin, SQLiteCache
from requests_ratelimiter import LimiterMixin, MemoryQueueBucket
from pyrate_limiter import Duration, RequestRate, Limiter

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

template_stock_list = 'stock_list.html'
template_stock_list_stocks = 'stock_list_stocks.html'
template_stock_data = 'stock_data.html'
template_portfolio = 'portfolio_edit_table.html'

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

#start-stop
def start():
    return Response(status_code=200, content='Server started')

def shutdown():
    os.kill(os.getpid(), signal.SIGTERM)
    return Response(status_code=200, content='Server shutting down...')

@app.on_event('shutdown')
def on_shutdown():
    print('Server shutting down...')

app.add_api_route('/start', start, methods=['GET'])
app.add_api_route('/shutdown', shutdown, methods=['GET'])