import uvicorn
import click
from multiprocessing import cpu_count

@click.command
@click.option('--cpu',default=cpu_count()*2+1)
@click.option('--host',default='0.0.0.0')
@click.option('--port',default=8005)
@click.option('--dev',default=False)
def uvicorn_app(host,port,cpu,dev):
    uvicorn.run('server_app.list_server:app', host=host, port=port,workers=cpu,reload=dev)

if (__name__ == '__main__'):
    uvicorn_app()