
from settings import *
from pymongo import MongoClient
from urllib.parse import quote_plus

def mongodb_init():
    #check mongodb params
    
    #check mongodb server is OK
    try:
        uri = "mongodb://%s:%s@%s:%d" % (quote_plus(MONGODB_USER), quote_plus(MONGODB_PWD), MONGODB_IP, MONGODB_PORT)
        myclient = MongoClient(uri)
        mydb = myclient[MONGODB_DATABASE]
        mycol = mydb["voice_quality_check"]
        x = mycol.find_one()
        logging.debug("mongodb test:%s" % str(x))
        
    except Exception as e:
        logging.error("exception when connect mongodb %s, %s, %s" % (MONGODB_DATABASE, uri, str(e)))
        return False
 
    return True

def mongodb_insert(value):
    return True

def mongodb_delete(key):
    return True

def mongodb_update(key, value):
    return True

def mongodb_find(key):
    return True