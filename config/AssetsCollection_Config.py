#!/usr/bin/env python
#coding:utf-8
#author: moorewqk@163.com
#date:


import os, sys, time, datetime, commands

ASSETSCOLLECTION_SETTINGT = {
    "dev":{
        "username":"admin",
        "password":"eakay2015",
        "apitoken":"http://127.0.0.1:8000/api/token/",
        "apiassetsreport":"http://127.0.0.1:8000/api/assets_report/",
        "apiserver":"http://127.0.0.1:8000/api/server/"
    },
    "pro":{
        "username":"opsadmin",
        "password":"opsadmineakayops-manager20171023173434KZHzuKW2lLUs++Sh",
        "apitoken":"http://172.168.1.20:8000/api/token/",
        "apiassetsreport":"http://172.168.1.20:8000/api/assets_report/",
        "apiserver":"http://172.168.1.20:8000/api/server/"
    }

}