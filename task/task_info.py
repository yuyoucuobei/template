
from logging import fatal
from settings import *
import json

class task_info():
    taskjson = None
    taskdata = None
    
    #taskid callid calltype caller callee display category recordpath callbackURL
    
    def __init__(self, taskjson):
        self.taskjson = taskjson
        self.taskdata = {'taskid':None,'callid':None,'calltype':None,'caller':None,'callee':None,'display':None,'category':None,'recordpath':None,'callbackURL':None}
        
        try:
            #parse json
            self.taskdata = json.loads(taskjson)
        except Exception as e:
            logging.error("task_info loads json fail")
            
        return
    
    def check_params(self):
        #check param is None
        if None == self.taskdata:
            return False
        
        if "taskid" not in self.taskdata or None == self.taskdata["taskid"] or 0 == len(self.taskdata["taskid"]):
            return False
        
        if "callid" not in self.taskdata or None == self.taskdata["callid"] or 0 == len(self.taskdata["callid"]):
            return False
        
        if "calltype" not in self.taskdata or None == self.taskdata["calltype"]:
            return False

        if "caller" not in self.taskdata or None == self.taskdata["caller"] or 0 == len(self.taskdata["caller"]):
            return False
        
        if "callee" not in self.taskdata or None == self.taskdata["callee"] or 0 == len(self.taskdata["callee"]):
            return False
        
        if "display" not in self.taskdata or None == self.taskdata["display"] or 0 == len(self.taskdata["display"]):
            self.taskdata["display"] = ""
        
        if "category" not in self.taskdata or None == self.taskdata["category"] or 0 == len(self.taskdata["category"]):
            return False
        
        if "recordpath" not in self.taskdata or None == self.taskdata["recordpath"] or 0 == len(self.taskdata["recordpath"]):
            return False
        
        if "callbackURL" not in self.taskdata or None == self.taskdata["callbackURL"] or 0 == len(self.taskdata["callbackURL"]):
            self.taskdata["callbackURL"] = ""

        return True
    
    
    