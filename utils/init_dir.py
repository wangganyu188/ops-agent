#!/usr/bin/env python
#coding:utf-8
#author: moorewqk@163.com
#date:


import os, sys, time, datetime, commands

def Init_Dir(dir):
	if not os.path.exists (dir):
		os.makedirs (dir)
		
