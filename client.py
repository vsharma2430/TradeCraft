import uvicorn
from multiprocessing import cpu_count

if (__name__ == '__main__'):
    uvicorn.run('server_app.list_server:app', host='0.0.0.0', port=8005,workers=cpu_count()*2+1)