#!/usr/bin/env python
#coding:utf-8
#author: moorewqk@163.com
#date:


import os, sys, time, datetime, commands
import shutil
import socket
import requests



def checkDictValues(**kwargs):
    """
    检查字典是否有空值
    :param kwargs:
    :return:
    """
    if isinstance(kwargs,dict):
        for k,v in kwargs.items():
            if kwargs[k] is None:
                return False
        else:
            return True
    else:
        print "传入的字典类型不对"


def isCmdExits(shellpath=None):
    """
    判断shell命令是否存在
    :param shellpath:
    :return:
    """
    if os.access(shellpath,os.X_OK) == True:
        return True
    else:
        return False


def checkDir(dir):
    """
    检查目录不存的话,新创建
    :param dir:
    :return:
    """
    if not os.path.exists (dir):
        os.makedirs (dir)
        return True
    else:
        return True


def del_Dir(dirpath):
    """
    删除目录
    :param dirpath:
    :return:
    """
    if os.path.exists(dirpath):
        shutil.rmtree(dirpath,ignore_errors=True)
        return True
    else:
        print "%s目录不存在"%(dirpath)
        return False

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def send_mail(appname,subject,text_body,main_title,mailapi):
	maildict =  {
		"subject": None,
		"text_body": None,
		"html_body": None,
		"sender":None,
		"appname": None,
		"is_send": None
	}

	maildict["appname"] = appname
	maildict["subject"] = "%s%s"%(main_title,subject)
	maildict["recipients"] = "ops@eakay.cn"
	maildict["text_body"] = text_body
	r = requests.get(url=mailapi, params=maildict, timeout=20)
	if r.status_code == 200:
		return True
	else:
		print "邮件发送失败,请检查"
		return False