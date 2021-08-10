
from settings import *

def record_init():
    #check record params
    if not os.access(RECORD_PATH, os.R_OK):
        logging.error("record path is not readable, %s" % RECORD_PATH)
        return False
    
    #check local record path, deal with legacy files
    if not os.access(RECORD_WORK_PATH, os.F_OK):
        #create path
        os.makedirs(RECORD_WORK_PATH)
    else:
        #check legacy files, clear record files
        pass
    
    return True

def record_get(recordpath):
    return True