#!/usr/bin/env python
#coding:utf-8
#author: moorewqk@163.com
#date:
"""
保证/usr/local/python27/bin 目录下有pip,virtualenv,python
"""

import os, sys, time, datetime, commands
import platform,shutil
from checkTools import isCmdExits


checkConfig = {
    "srcDir":"/data/setup",
    "virtaulenv":{
        "pythonVerion":"2.7",
        "Centos6PythonPath":['/usr/local/python27/bin/python','/usr/local/python27/bin/pip'],
        "Centos7PythonPath":['/usr/bin/python','/usr/bin/pip']
    }
}

def checkSystemVer():
    """
    获取当前操作系统的大版本，centos6/centos7
    :return:
    """
    systemVerdict = {}
    osver = platform.dist()
    systemVerdict["system"] = osver[0]
    systemVerdict["version"] = int(osver[1].split('.')[0])

    return systemVerdict





def initVirtualenv():
    """
    检查项,并返回检查结果
    :param pro:
    :return:
    """
    pythonenv = checkConfig["virtaulenv"]
    checkres = {}
    sysV = checkSystemVer()
    if sysV["system"] == 'centos' and sysV["version"] == 6:
        for k,v in pythonenv.iteritems():
            if k == "Centos6PythonPath" and isinstance(v,list):
                if isCmdExits(shellpath=v[0]) and isCmdExits(shellpath=v[1]):
                    checkres["centos6VirtEnv"] = "ok"
                    print "安装Centos6PythonPath 环境"
                    vs,vv =commands.getstatusoutput("{pipbin} install virtualenv".format(pipbin=v[1]))
                    if vs == 0:
                        print "virtualenv 环境安装成功"
                    else:
                        print "virtualenv 环境安装失败"
                else:
                    if os.path.exists("{srcDir}/python27".format(srcDir=checkConfig["srcDir"])):
                        print "安装Centos6PythonPath 环境"
                        shutil.move(src="{srcDir}/python27".format(srcDir=checkConfig["srcDir"]),dst="/usr/local/")
                        vs, vv = commands.getstatusoutput("{pipbin} install virtualenv".format(pipbin=v[1]))
                        if vs == 0:
                            print "virtualenv 环境安装成功"
                        else:
                            print "virtualenv 环境安装失败"
    elif sysV["system"] == 'centos' and sysV["version"] == 7:

        for k,v in pythonenv.iteritems():
            if k == "Centos7PythonPath" and isinstance(v,list):
                if isCmdExits(shellpath=v[0]) and isCmdExits(shellpath=v[1]):
                    checkres["centos6VirtEnv"] = "ok"
                    print "安装Centos7PythonPath 环境"
                    vs,vv =commands.getstatusoutput("{pipbin} install virtualenv".format(pipbin=v[1]))
                    if vs == 0:
                        print "virtualenv 环境安装成功"
                    else:
                        print "virtualenv 环境安装失败"
                else:
                    if os.path.exists("{srcDir}/python27".format(srcDir=checkConfig["srcDir"])):
                        print "安装Centos7PythonPath 环境"
                        shutil.move(src="{srcDir}/python27".format(srcDir=checkConfig["srcDir"]),dst="/usr/local/")
                        vs, vv = commands.getstatusoutput("{pipbin} install virtualenv".format(pipbin=v[1]))
                        if vs == 0:
                            print "virtualenv 环境安装成功"
                        else:
                            print "virtualenv 环境安装失败"

    else:
        print "不支持当前版本"



if __name__ == '__main__':
    print initVirtualenv()