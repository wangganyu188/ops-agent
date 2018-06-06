#!/usr/bin/env python
#coding:utf-8
#author: moorewqk@163.com
#date:


import os, sys, time, datetime, commands
import requests
url = "http://127.0.0.1:54110/api/SendMail"
data = {
	"appname":"test",
	"subject":"电子发票",
	"text_body":"您的电子发票下载地址：http://www.fapiao.com/dzfp-web/pdf/download?request=P2jFLvnGWn5jD6wJm13QUQalFy1NAWolMtC7PW5KPps0Ov-oec2QaoDHnoyDebFSsrWsoq0uDJw_%5ECDHBaieHia",
	"recipients":"wangqiankun@eakay.cn"

}
r = requests.post(url=url,json=data,timeout=10)
print r.status_code
print r.json()

