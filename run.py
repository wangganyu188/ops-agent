#!/usr/bin/env python
#coding:utf-8
#author:moorewqk@163.com
#date:



import os,sys

from flask_script import Manager,Server
from config import config
from config import appconfig,app

#管理启动脚本
manager = Manager(app)
manager.add_command("start",Server(
    host=config[appconfig].LOCALIP,port=config[appconfig].PORT
))


if __name__ == "__main__":
    manager.run()
