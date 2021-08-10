
from settings import *
from httpif.http_server import http_server

thread_http_server = None

def http_init(taskqueue):
    global thread_http_server
    thread_http_server = http_server(taskqueue)
    thread_http_server.start()
    
    return True

def http_uninit():
    global thread_http_server
    logging.info("http_uninit, wait for the end of thread_http_server")
    http_server.httpserver.shutdown()
    thread_http_server.join()
    
    return True


