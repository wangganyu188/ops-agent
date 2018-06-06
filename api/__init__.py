#!/usr/bin/env python
#coding:utf-8
#author: moorewqk@163.com
#date:


import os, sys, time, datetime, commands
from os.path import dirname, basename, isfile
import glob


all_list = list()
for f in glob.glob(os.path.dirname(__file__)+"/*.py"):
    # print "py ffffff",f
    if os.path.isfile(f) and not os.path.basename(f).startswith('_') and not os.path.basename(f).startswith('views'):
        all_list.append(os.path.basename(f)[:-3])

__all__ = all_list