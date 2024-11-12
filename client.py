import os
import signal
import fastapi
import uvicorn
from list_server import list_app

def start():
    return fastapi.Response(status_code=200, content='Server started')

def shutdown():
    os.kill(os.getpid(), signal.SIGTERM)
    return fastapi.Response(status_code=200, content='Server shutting down...')

@list_app.on_event('shutdown')
def on_shutdown():
    print('Server shutting down...')

list_app.add_api_route('/start', start, methods=['GET'])
list_app.add_api_route('/shutdown', shutdown, methods=['GET'])

if __name__ == '__main__':
    uvicorn.run(list_app, host='localhost', port=8005)