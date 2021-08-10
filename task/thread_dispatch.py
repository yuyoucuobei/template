
from settings import *
import queue
import threading
import time
from task.thread_task import thread_task
from httpif.http_callback import http_callback

class thread_dispatch(threading.Thread):
    exit_flag = 0
    
    def __init__(self, taskqueue):
        threading.Thread.__init__(self)
        self.taskqueue = taskqueue
    
    def run(self):
        #listen queue, task dispatch
        while not thread_dispatch.exit_flag:
            try:
                taskinfo = self.taskqueue.get(timeout=2)

                #check current task threads number, is gt max
                while SYS_THREAD_MAX <= len(thread_task.threads):
                    time.sleep(1)
                
                #check the number of task thread state with ASR, is gt max
                while ASR_THREAD_MAX <= thread_task.count_asr:
                    time.sleep(1)
                
                #create new thread of task, and run 
                newtask = thread_task(taskinfo)
                newtask.start()
                continue
                
            except Exception as e:
                continue
        
        #clear task queue, return error report
        while not self.taskqueue.empty():
            try:
                taskinfo = self.taskqueue.get(timeout=1)

                #return error report
                http_callback(taskinfo, 1, "service is stopping", [], [])
                continue
                
            except Exception as e:
                continue
        
        #exit flow, wait the task thread 
        logging.info("thread_dispatch, wait for the end of thread_tasks")
        # print("len(thread_task.threads)=%d" % len(thread_task.threads))
        for t in thread_task.threads:
            try:
                t.join()
            except:
                continue
            
    
    
