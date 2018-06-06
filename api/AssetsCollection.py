#!/usr/bin/env python
#coding:utf-8
#author: moorewqk@163.com
#date:


import datetime
import hashlib
import json
import socket
from subprocess import Popen,PIPE

import requests
from flask_restful import Resource
from flask import jsonify
from utils import getPeriod
from config.AssetsCollection_Config import ASSETSCOLLECTION_SETTINGT
from utils.opsLog import logger,LOGGING

config = ASSETSCOLLECTION_SETTINGT["pro"]

#增加配置

def get_header():
	"""
	生成token信息返回
	:return:
	"""
	try:
		logger.info("get token")
		r = requests.post (url=config["apitoken"], data={"username":config["username"],"password":config["password"]})
		token = json.loads (r.text)['token']
		header = {"Authorization": "JWT %s"%token}
		return header
	except Exception,e:
		print "生成token失败",e

#随机生成临时资产编号
def number():
	logger.info("随机产生编号")
	nowtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	m = hashlib.md5()
	m.update("%s%s"%(get_host_ip(),nowtime))
	return m.hexdigest()[:-20]

def GetDmi():
    info = Popen(['dmidecode'],stdout=PIPE)
    data = info.stdout.read()
    return data

def parseData(data):
    parsed_data = []
    new_line = ''
    data = [i for i in data.split('\n') if i]
    for line in data:
        if line[0].strip():
            parsed_data.append(new_line)
            new_line = line + '\n'
        else:
            new_line += line + '\n'
    parsed_data.append(new_line)
    return [i for i in parsed_data if i]


def parseDmi(parsed_data):

	dic = {}
	logger.info("get资产信息,并处理成dict")
	parsed_data = [i for i in parsed_data if i.startswith('System Information')]
	parsed_data = [i for i in parsed_data[0].split('\n')[1:] if i]
	dmi_dic = dict([i.strip().split(':') for i in parsed_data])
	dic['manufacturer'] = dmi_dic['Manufacturer'].strip()
	dic['model'] = dmi_dic['Product Name'].strip()
	dic['sn'] = dmi_dic['Serial Number'].strip()
	return dic



#get服务器IP地址
def get_host_ip():
	try:
		logger.info("get本地ip地址")
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(('8.8.8.8', 80))
		ip = s.getsockname()[0]
	finally:
		s.close()
	return ip

#向服务器端提交资产信息
def post_assets_report(putdata):

	logger.info("向服务端提交资产数据")
	p = requests.post(url=config["apiassetsreport"],data=putdata,headers=get_header())
	if p.status_code == 201:
		print "资产信息汇报成功"
	else:
		print "资产信息汇报失败",p.status_code


#客户端向/api/assets/接口汇报IP
#新版接口功能:采集本地主机资产信息
class AssetsMain(Resource):

	def get(self):
		"""
		往资产接口上传数据
		:return:
		"""
		data = GetDmi()
		# print "datatatata",data
		parsed_data_dmi = parseData(data)
		# print "papapapa",parsed_data_dmi
		dmi = parseDmi(parsed_data_dmi)
		#采购时间需要做异常处理(只处理物理机,不处理虚拟机,容器等)
		buy_info = getPeriod.periodDate(dmi["sn"])
		if buy_info:
			# print "bbbbb",buy_info
			putdata = {
				"name": "%s"%number(),
				"management_ip": get_host_ip(),
				"sn":"%s"%dmi["sn"],
				"model":dmi["model"],
				"manufacturer":dmi["manufacturer"],
				"buy_time": buy_info["buy_info"]["start_time"],
				"expire_date":buy_info["buy_info"]["expires_date"],
				"status":3,
				"assets_type": "server"
			}
			logger.info("dell服务器资产信息提交")
			return putdata
		else:
			putdata = {
				"name": "%s" % number(),
				"management_ip": get_host_ip(),
				"sn": "%s" % dmi["sn"],
				"model": dmi["model"],
				"manufacturer": dmi["manufacturer"],
				"buy_time":"",
				"expire_date":"",
				"status": 3,
				"assets_type": "server"
			}
			logger.info("非dell服务器资产信息提交")
			return putdata


if __name__ == "__main__":
	AssetsMain()