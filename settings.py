
import os
import sys
import logging

#global settings of qcs process
#system config
SYS_BASE_PATH = os.path.dirname(os.path.abspath(__file__))
SYS_THREAD_MAX = 100
SYS_QUEUE_SIZE = 1024
SYS_SLEEP_SECOND = 60
SYS_DEFAULT_CALLBACK_URL = "http://10.9.0.70:8080/qccallback"

#http server
HTTP_IP = "10.9.0.70"
HTTP_PORT = 8080

#log config
LOG_FILE = "D:\\TEST\\python\\template\\log\\main.log"
LOG_LEVEL = logging.DEBUG

#record config
RECORD_PATH = "D:\\TEST\\python\\template\\record\\remote\\"
RECORD_WORK_PATH = "D:\\TEST\\python\\template\\record\\local\\"

#asr config
ASR_THREAD_MAX = 50

#NLU config
NLU_URL = "http://127.0.0.1:8080/nlu"

#mongodb config
MONGODB_IP = "10.0.33.54"
MONGODB_PORT = 27017
MONGODB_USER = "test"
MONGODB_PWD = "test"
MONGODB_DATABASE = "qcs"

##########global config, DO NOT MODIFY##################
if not os.access(LOG_FILE, os.F_OK):
    with open(LOG_FILE, mode='a') as ff:
        ff.close()
LOG_FORMAT= "%(asctime)s %(name)s %(levelname)s %(pathname)s %(message)s"
logging.basicConfig(filename = LOG_FILE,
                    level = LOG_LEVEL,
                    format = LOG_FORMAT
                    )


