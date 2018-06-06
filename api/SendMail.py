#!/usr/bin/env python
# coding:utf-8
# author: moorewqk@163.com
# date:


import os, sys, time, datetime, commands, json
from flask_mail import Message, charset,Mail
charset.add_charset('utf-8', charset.SHORTEST, charset.BASE64, 'utf-8')
reload(sys)
sys.setdefaultencoding('utf-8')
from flask import current_app,abort
from flask_restful import Resource, marshal_with, reqparse, marshal
from utils.decorators import async_task
from config import app
from config import SendMail_config
from utils import data_structure
from flask import jsonify

mail = Mail()



def config_control():
    #配置发邮件服务器

    mailserver_config = SendMail_config.MAIL_SETTINGS
    app.config["MAIL_SERVER"] = mailserver_config["MAIL_SERVER"]
    app.config["MAIL_PORT"] = mailserver_config["MAIL_PORT"]
    app.config["MAIL_USE_SSL"] = mailserver_config["MAIL_USE_SSL"]
    app.config["MAIL_DEFAULT_SENDER"] = mailserver_config["MAIL_DEFAULT_SENDER"]
    app.config["MAIL_MAX_EMAILS"] = mailserver_config["MAIL_MAX_EMAILS"]
    app.config["MAIL_USERNAME"] = mailserver_config["MAIL_USERNAME"]
    app.config["MAIL_PASSWORD"] = mailserver_config["MAIL_PASSWORD"]
    mail.init_app(app)

#邮件数据结构化
post_parser = reqparse.RequestParser()
post_parser.add_argument("appname", location=['json', 'args'])
post_parser.add_argument("subject",location=['json', 'args'])
post_parser.add_argument("recipients",location=['json', 'args'])
post_parser.add_argument("text_body",location=['json', 'args'])
post_parser.add_argument("html_body",location=['json', 'args'])
post_parser.add_argument("sender", location=['json', 'args'])

# mailmsg_fields = {
# 	"appname": fields.String,
# 	"subject": fields.String,
# 	"recipients": fields.String,
# 	"text_body": fields.String,
# 	"html_body": fields.String,
# 	"sender": fields.String,
# 	"is_send":fields.Integer(default=0)
# }



@async_task
def _send_async_email(flask_app, msg):
    """ Sends an send_email asynchronously
    Args:
        flask_app (flask.Flask): Current flask instance
        msg (Message): Message to send
    Returns:
        None
    """
    with flask_app.app_context():
        mail.send(msg)


def send_email(subject=None, sender=None, recipients=None, text_body=None, html_body=None, **kwargs):
    app.logger.info("send_email(subject='{subject}', recipients=['{recp}'], text_body='{txt}')".format(sender=sender,
                                                                                                       subject=subject,
                                                                                                       recp=recipients,
                                                                                                       txt=text_body))
    msg = Message(subject, sender=sender, recipients=recipients, charset='utf-8', **kwargs)
    msg.body = text_body
    msg.html = html_body

    app.logger.info("Message(to=[{m.recipients}], from='{m.sender}')".format(m=msg))
    try:
        _send_async_email(app, msg)
        return True
    except Exception,e:
        return False


class SendMail(Resource):
    """
    发送邮件主程序,
    """
    # @marshal_with(data_structure.mailmsg_fields)
    def post(self):
        config_control()
        current_app.logger.info('{cls}.GET called'.format(cls=self.__class__.__name__))
        # print data_structure.mailmsg_fields
        args = post_parser.parse_args()
        # print "111111",args
        # 收件人邮箱列表化
        # list_recipients = args["recipients"].split(',')
        # print args["recipients"],type(args["recipients"].split(',')),args["recipients"].encode().split(',')
        if args["recipients"].split(','):
            list_recipients = args["recipients"].encode().split(',')
        else:
            list_recipients = args["recipients"].encode()

        print list_recipients,type(list_recipients)
        message = dict(subject="%s:[%s]" % (args["appname"], args["subject"]),
                       recipients=list_recipients,
                       text_body=args["text_body"],
                       html_body=args["html_body"],
                       sender=args["sender"])

        try:
            # Avoiding a circular import - there must be a better way...
            send_email(**message)
            return jsonify({"status":"success"})
        except Exception as err:
            current_app.logger.error("Failed to send email: {error}".format(error=err))
            return jsonify({"status":"failed"})


