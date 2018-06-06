#!/usr/bin/env python
#coding:utf-8
#author: moorewqk@163.com
#date:


import os, sys, time, datetime, commands
import glob
import json
reload(sys)
from flask import jsonify,Blueprint
from flask_restful import Api
from config.ApiConfig import loadApiConfig
from api import *


# 初始化接口蓝图
apis = Blueprint("api", __name__)
api = Api(apis)

if len(loadApiConfig()) > 0:

    for apiconfig in loadApiConfig():
        # print apiconfig
        api.add_resource(eval(apiconfig["func"]),
                         "/{url}".format(url=apiconfig["url"].encode())
                         )

else:
    print "ApiConfig.json配置不能为空"



