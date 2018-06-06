#!/usr/bin/env python
#coding:utf-8
#author: moorewqk@163.com
#date:


import os, sys, time, datetime, commands


d = datetime.datetime.now ()


def day_get(d):
	oneday = datetime.timedelta (days=1)
	day = d - oneday
	date_from = datetime.datetime (day.year, day.month, day.day, 0, 0, 0)
	date_to = datetime.datetime (day.year, day.month, day.day, 23, 59, 59)
	print '---'.join ([str (date_from), str (date_to)])
	return str(date_from).split()[0].replace('-','')

def week_get(d):
	dayscount = datetime.timedelta (days=d.isoweekday ())
	dayto = d - dayscount
	sixdays = datetime.timedelta (days=6)
	dayfrom = dayto - sixdays
	date_from = datetime.datetime (dayfrom.year, dayfrom.month, dayfrom.day, 0, 0, 0)
	date_to = datetime.datetime (dayto.year, dayto.month, dayto.day, 23, 59, 59)
	print '---'.join ([str (date_from), str (date_to)])
	return str(date_from).split()[0].replace("-",'')

def month_get(d):
	dayscount = datetime.timedelta (days=d.day)
	dayto = d - dayscount
	date_from = datetime.datetime (dayto.year, dayto.month, 1, 0, 0, 0)
	date_to = datetime.datetime (dayto.year, dayto.month, dayto.day, 23, 59, 59)
	print '---'.join ([str (date_from), str (date_to)])
	return str(date_from).split()[0].replace('-','')
	
if __name__ == "__main__":
	
	print "上月",month_get(d)
	print "上周", week_get (d)
	print "上一天", day_get(d)