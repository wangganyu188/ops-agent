#!/usr/bin/env python
#coding:utf-8
#author: moorewqk@163.com
#date:


import os, sys, time, datetime, commands


MAIL_SETTINGS = {
		"MAIL_SERVER": "smtp.eakay.cn",
		"MAIL_PORT": 465,
		"MAIL_USE_SSL": True,
		"MAIL_DEFAULT_SENDER": ("monitor", "monitor@eakay.cn"),
		"MAIL_MAX_EMAILS": 10,
		"MAIL_USERNAME": "monitor@eakay.cn",
		"MAIL_PASSWORD": "Eakay2018"
	}


TASK_INFO = {
	"host":"10.30.60.12",
	"task_id":1,
	"task_status":0
}