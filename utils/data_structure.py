#!/usr/bin/env python
#coding:utf-8
#author: moorewqk@163.com
#date:


import os, sys, time, datetime, commands

from flask_restful import fields,reqparse


apiregister_fields = {
	"name": fields.String,
	"des": fields.String,
	"state": fields.String,
	"apiurl":fields.String,
	"ctime":fields.String
}

mailmsg_fields = {
	"appname": fields.String,
	"subject": fields.String,
	"recipients": fields.String,
	"text_body": fields.String,
	"html_body": fields.String,
	"sender": fields.String,
	"is_send":fields.Integer(default=0)
}
