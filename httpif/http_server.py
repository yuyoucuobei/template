
from settings import *
import threading

from http.server import BaseHTTPRequestHandler, HTTPServer

from task.task_info import task_info

class post_handler(BaseHTTPRequestHandler):
    def do_POST(self):
        #path parse
        # parsed_path = parse.urlparse(self.path)   
        if self.path == "/qctask":
            self.qctask()
        else:
            self.send_error(404)
            return 
        
        return 
        
    def qctask(self):
        #parse post body
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data 

        logging.info("POST request, path:%s, from %s, body:%s",
                str(self.path), str(self.client_address), post_data.decode('utf-8'))

        #check post data is valid
        taskinfo = task_info(post_data)
        if not taskinfo.check_params():
            logging.warning("post body is invalid, return 400")
            self.send_error(400)
            return
        
        #put task into queue
        if http_server.taskqueue.full():
            logging.warning("task queue is full, return 503")
            self.send_error(503)
            return
        else:
            http_server.taskqueue.put_nowait(taskinfo)
            
        #send response
        self.send_response(202)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.end_headers()
        return

class http_server(threading.Thread):
    taskqueue = None
    httpserver = None
    
    def __init__(self, taskqueue):
        threading.Thread.__init__(self)
        http_server.taskqueue = taskqueue
    
    def run(self):
        #create http server, listen port
        http_server.httpserver = HTTPServer((HTTP_IP, HTTP_PORT), post_handler)
        http_server.httpserver.serve_forever()
    
    