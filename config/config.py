#!/usr/bin/env python
#coding:utf-8
#author: moorewqk@163.com
#date:


import os, sys, time, datetime, commands
from utils import get_ipaddr


class Config (object):
	DEBUG = False
	TESTING = False
	PORT = 5000
	BASE_DIR = os.path.abspath (os.path.dirname (os.path.dirname ('__file__')))
	LOCALIP = get_ipaddr.get_local_ip()
	SECRET_KEY = os.environ.get ('SECRET_KEY') or 'eakay201706021518'
	LOG_PATH = os.path.join (BASE_DIR, 'logs')



class DevConfig(Config):
	DEBUG = os.environ.get('DEBUG', 'true').lower() == 'true'
	LOCALIP = "0.0.0.0"

class PrdConfig (Config):
	DEBUG = os.environ.get ('DEBUG', 'true').lower () == 'true'


config = {
	'dev': DevConfig,
	'prd': PrdConfig,
	'default': PrdConfig,
}