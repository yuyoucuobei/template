
from settings import *
from task.thread_dispatch import thread_dispatch

thread_task_dispatch = None

def task_init(taskqueue):
    global thread_task_dispatch
    #create new thread of dispatch
    thread_task_dispatch = thread_dispatch(taskqueue)
    thread_task_dispatch.start()
    
    return True

def task_uninit():
    global thread_task_dispatch
    logging.info("task_uninit, wait for the end of thread_task_dispatch")
    thread_dispatch.exit_flag = 1
    thread_task_dispatch.join()
    return True
