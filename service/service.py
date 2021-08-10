    
from settings import *
from record.record import record_init
from asr.asr import asr_init
from nlu.nlu import nlu_init
from mongodb.mongodb import mongodb_init
from task.task import task_init, task_uninit
from httpif.httpif import http_init, http_uninit
import signal
import queue
import time


def qcs_start():
    logging.info("qcs service start")
    
    #NAS check
    #record path check
    if not record_init():
        logging.error("record_init fail, return")
        return
    logging.info("record_init success")
    
    #ASR check
    if not asr_init():
        logging.error("asr_init fail, return")
        return
    logging.info("asr_init success")
    
    #NLU check
    if not nlu_init():
        logging.error("nlu_init fail, return")
        return
    logging.info("nlu_init success")
    
    #mysql check
    
    #mongodb check
    if not mongodb_init():
        logging.error("mongodb_init fail, return")
        return
    logging.info("mongodb_init success")
    
    #create task queue
    taskqueue = queue.Queue(SYS_QUEUE_SIZE)
    
    #create thread of task dispatch
    if not task_init(taskqueue):
        logging.error("task_init fail, return")
        return
    logging.info("task_init success")
    
    #create thread of http service
    if not http_init(taskqueue):
        logging.error("http_init fail, return")
        return
    logging.info("http_init success")
    
    #register signal of exit
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    #sleep
    # signal.pause()
    
    #flow of exit
    time.sleep(SYS_SLEEP_SECOND)
    qcs_stop()
    
    return 
    
def qcs_stop():
    logging.info("qcs service stopping")
    #stop http service
    http_uninit()
    
    #check task queue, clear task  
    #send quit msg to queue    
    #wait thread of task dispatch
    task_uninit()
    
    #service stop    
    logging.info("qcs service end")
    return
    
def signal_handler(signum, frame):
    # print('service received: ', signum)
    return

