
from settings import *
import threading
import time
import os

from httpif.http_callback import http_callback
from mongodb.mongodb import *
from asr.asr import asr_transfer
from nlu.nlu import nlu_label
from record.record import record_get

class thread_task(threading.Thread):
    count_asr = 0 #static, count of ASR state thread
    threads = [] #static, list of task thread
    
    def __init__(self, taskinfo):
        threading.Thread.__init__(self)
        self.taskinfo = taskinfo
        self.result = 0
        self.errdsc = "success"
        self.category_label = []
        self.content_label = []
        
        self.record_local = ""
        
        thread_task.threads.append(self)
        # print("__init__, len(thread_task.threads)=%d" % len(thread_task.threads))
        return 
            
    def run(self):
        # time.sleep(5)
        # return
        
        logging.info("thread_task start, taskid=%s, callid=%s" % (self.taskinfo.taskdata['taskid'], self.taskinfo.taskdata['callid']))
        #get record file
        if not self.get_record():
            logging.warning("get_record fail, taskid=%s, callid=%s" % (self.taskinfo.taskdata['taskid'], self.taskinfo.taskdata['callid']))
            self.result = 2
            self.errdsc = "get record file fail"
            self.mongodb_flow()
            self.result_report()
            thread_task.threads.remove(self)
            return
        
        #asr flow
        if not self.asr_flow():
            logging.warning("asr_flow fail, taskid=%s, callid=%s" % (self.taskinfo.taskdata['taskid'], self.taskinfo.taskdata['callid']))
            self.result = 3
            self.errdsc = "asr flow fail"
            self.mongodb_flow()
            self.result_report()
            thread_task.threads.remove(self)
            return
        
        #nlu flow
        if not self.nlu_flow():
            logging.warning("nlu_flow fail, taskid=%s, callid=%s" % (self.taskinfo.taskdata['taskid'], self.taskinfo.taskdata['callid']))
            self.result = 4
            self.errdsc = "nlu flow fail"
            self.mongodb_flow()
            self.result_report()
            thread_task.threads.remove(self)
            return
        
        #success flow
        #write result to mongodb
        self.mongodb_flow()
        
        #set result, return report
        self.result_report()
        
        #remove self from threads
        thread_task.threads.remove(self)
        
        logging.info("thread_task end, taskid=%s, callid=%s" % (self.taskinfo.taskdata['taskid'], self.taskinfo.taskdata['callid']))
        return 
            
    def get_record(self):
        if not record_get(self.taskinfo.taskdata['recordpath']):
            logging.error("get_record fail")
            return False
        
        #asign record_local 
        self.record_local = RECORD_WORK_PATH + os.path.basename(self.taskinfo.taskdata['recordpath'])
        
        return True
    
    def asr_flow(self):
        if not asr_transfer(self.record_local, self.content_label):
            logging.error("asr_flow fail")
            return False
        
        return True
    
    def nlu_flow(self):
        if not nlu_label(self.content_label, self.category_label):
            logging.error("nlu_flow fail")
            return False
        
        return True
    
    def mongodb_flow(self):
        #get json string from result
        mongo_value = ""
        
        #mongodb insert value
        if not mongodb_insert(mongo_value):
            logging.error("mongodb_flow fail")
            return False
        return True
    
    def result_report(self):
        if not http_callback(self.taskinfo, self.result, self.errdsc, self.category_label, self.content_label):
            logging.error("result_report fail")
            return False
            
        return True
    