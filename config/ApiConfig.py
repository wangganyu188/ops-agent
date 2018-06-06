#!/usr/bin/env python
#coding:utf-8
#author: moorewqk@163.com
#date:


import os, sys, time, datetime, commands
import json
from . import config,appconfig
from utils.opsLog import logger,Loging

def loadApiConfig():
    configPath="{basedir}/config/ApiConfig.json".format(basedir=config[appconfig].BASE_DIR)
    with open(configPath,'r') as cf:
        configdict = json.load(cf)
        if configdict:
            return configdict
        else:
            logger.info("配置加载失败,请检查配置")
