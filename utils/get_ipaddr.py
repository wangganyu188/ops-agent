#!/usr/bin/env python
#coding:utf-8
#author: moorewqk@163.com
#date:


import os, sys, time, datetime, commands
import socket


def get_local_ip():
    try:
        s = socket.socket (socket.AF_INET, socket.SOCK_DGRAM)
        s.connect (('8.8.8.8', 80))
        ip = s.getsockname ()[0]
    finally:
        s.close ()
    return ip


if __name__ == "__main__":
    print get_host_ip()