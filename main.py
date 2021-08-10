#!/usr/bin/python3

from settings import *
from service.service import qcs_start

if __name__ == "__main__":
    print("qcs start!!!")
    print("SYS_BASE_PATH:%s" % SYS_BASE_PATH)
    qcs_start()

    print("qcs end!!!")

