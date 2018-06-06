#!/usr/bin/env python
#coding:utf-8
#author: moorewqk@163.com
#date:

import os,sys
sys.path.append(os.path.abspath(os.path.dirname('__file__')))
from flask import Flask,Blueprint
from config import config

#初始化Flask实例
app = Flask(__name__)

def init_env(path):
    if os.path.exists(path):
        return
    else:
        os.makedirs(path)

#app配置初始化
def create_app(config_name):
    #主配置文件
    app.config.from_object(config[config_name])
    #各模块配置文件
    app.config['JSON_AS_ASCII'] = False

    #初始化日志路径
    init_env(config[config_name].LOG_PATH)

    # api视图路由
    from api.views import apis as api_blueprint
    app.register_blueprint(api_blueprint,url_prefix='/api')
    return app

#主配置引用
appconfig = os.getenv('config') or 'dev'
app = create_app(appconfig)

