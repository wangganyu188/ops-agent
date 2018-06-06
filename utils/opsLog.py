#!/usr/bin/env python
#coding:utf-8
#author: moorewqk@163.com
#date:


import os, sys, time, datetime, commands
import logging
import logging.config
from config.logConfig import LOGGING
from functools import wraps
reload(sys)
sys.setdefaultencoding("utf-8")

logging.config.dictConfig(LOGGING)
logger = logging.getLogger('default')

def Loging(func):
    @wraps(func)
    def warpper(*args,**kwargs):
        logger.info("start time:[%s] %s"%(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),func.func_name))
        res = func(*args,**kwargs)
        logger.info("end time:[%s] %s" % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), func.func_name))
        return res
    return warpper