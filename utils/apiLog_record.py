#!/usr/bin/env python
#coding:utf-8
#author: moorewqk@163.com
#date:


import os, sys, time, datetime, commands



def recordToFile(apiname,level,msg):
    """
    记录接口操作日志到本地/tmp目录
    :param apiname:
    :param level:
    :param msg:
    :return:
    """

    with open("/tmp/{apiname}_{level}_{dt}.log".format(apiname=apiname,level=level,dt=datetime.datetime.now().strftime("%Y%m%d%H")),'w') as arf:
        arf.write("{msg}\n".format(msg=msg))
