#!/usr/bin/env python
#coding:utf-8
#author: moorewqk@163.com
#date:


import os, sys, time, datetime, commands
from flask_restful import Resource
from flask import jsonify
from api import all_list
from config.ApiConfig import loadApiConfig,config,appconfig
from utils.get_ipaddr import get_local_ip


onfuct_list = [ i["func"].split('.')[0] for i in loadApiConfig()]


class INFO(Resource):

    def get(self):
        infodata = []
        # print all_list
        for fc in all_list:
            for ak in loadApiConfig():
                apidict = {}

                if fc in onfuct_list:
                    apidict["apiName"] = ak["func"]
                    apidict["apiUrl"] = "http://{ip}:{port}/api/{url}".format(url=ak["url"],ip=get_local_ip(),port=config[appconfig].PORT)
                    apidict["apiStatus"] = "on"
                    if apidict not in infodata:
                        infodata.append(apidict)
                else:
                    apidict["apiName"] = fc
                    apidict["apiStatus"] = "off"
                    if apidict not in infodata:
                        infodata.append(apidict)

        return jsonify(sorted(infodata,key=len,reverse = True))



