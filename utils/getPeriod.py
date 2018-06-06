#!/usr/bin/env python
#coding:utf-8
#author: moorewqk@163.com
#date:


import os, sys, time, datetime, commands
from BeautifulSoup import BeautifulSoup
import requests
import time,json
from utils import serializable_datetime


#本函数处理把table表里的数据生成dict类型

def TimeFormat(strtime):
    """

    :param strtime:
    :return:
    """
    restime = time.strftime("%Y-%m-%d",time.strptime(strtime,"%B  %d, %Y"))
    return restime



def HtmlToDict(html):
    """

    :param html:
    :param tableTag:
    :return:
    """
    datadict = {}
    soup = BeautifulSoup(html)
    #print soup("table")
    datadict["server_type"]="warranty"
    datadict["start_time"] = TimeFormat(soup('table')[1]("td")[1].text.encode("utf-8"))
    datadict["expires_date"] = TimeFormat(soup('table')[1]("td")[2].text.encode("utf-8"))

    return datadict



def GetData(sn):
    """

    :param url:
    :return:
    """
    geturl = "http://www.dell.com/support/home/ph/en/phbsd1/product-support/servicetag/%s/warranty?ref=captchaseen&lwp=rt"%(sn)
    #print geturl
    rs = requests.get(url=geturl)
    #print rs.text
    return rs.text.encode("utf-8")




def periodDate(sn):
    if sn:
        try:
            delldict = {}
            html = GetData(sn)
            #print html
            delldict["manufacturer"] = "dell"
            if HtmlToDict(html=html):
                delldict["buy_info"] = json.loads(json.dumps(HtmlToDict(html=html),cls=serializable_datetime.DateEncoder))
                return delldict
            else:
                print "非dell服务器"
                return False
        except Exception,e:
            return False
    else:
        print "sn不能为空"


if __name__ == "__main__":
    periodDate("3L8ZL82")




