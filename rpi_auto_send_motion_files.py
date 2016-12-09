#!/bin/evn python
# -*- encoding: utf-8 -*-

import os
import time
import random
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
# 15秒(time_check)检测一次，检测最近3分钟(timve_interval)内有多少张图片，
#   (从上次发送的照片下一张算起)超过30张(send_watermark)时就平均发送10张(send_count)。发送之后保存最后一张照片名称。
#   发送完之后休息15分钟(time_sleep_after_sent)。

time_check = 15
timve_interval = 180
send_watermark = 10
send_count = 5
time_sleep_after_sent = 180
path = '/home/pi/pi/motion_pics/'
mail_host = "smtp.exmail.qq.com"  # 设置服务器
mail_user = "zhongjie.li@viziner.cn"  # 用户名
mail_pass = "1111"  # 口令
sender = 'zhongjie.li@viziner.cn'
receivers = ['lzj3278@126.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

last_sent_file_create_time = 0


def sendpic(sendlist):
    message = MIMEMultipart()
    message['From'] = Header("李忠杰", 'utf-8')
    message['To'] = Header("报警图片", 'utf-8')
    subject = '报警监控'
    message['Subject'] = Header(subject, 'utf-8')
    message.attach(MIMEText('最近时间段有频繁活跃，请查看', 'plain', 'utf-8'))

    for item in sendlist:
        att1 = MIMEText(open(item, 'rb').read(), 'base64', 'utf-8')
        filenm = 'pic' + str(random.randint(1000, 9999)) + '.jpg'
        att1["Content-Type"] = 'application/octet-stream'
        att1["Content-Disposition"] = 'attachment; filename=%s' % (filenm)
        message.attach(att1)
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
        # smtpObj.starttls()
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print "邮件发送成功"
    except smtplib.SMTPException, e:
        print e
        print "Error: 无法发送邮件"


def TrySend(files):
    global last_sent_file_create_time
    for x in files:
        created_time = os.path.getctime(x)
        if created_time > last_sent_file_create_time:
            last_sent_file_create_time = created_time
    print 'last_sent_file_create_time=', last_sent_file_create_time
    sendpic(files)

    time.sleep(time_sleep_after_sent)
    pass


def Run():
    global last_sent_file_create_time
    while True:
        time.sleep(time_check)

        fl = os.listdir(path)

        time_now = time.time()
        sendlst = []
        for x in fl:
            if os.path.splitext(x)[1] != ".jpg":
                continue
            filename = path + x
            created_time = os.path.getctime(filename)
            # print 'filename=',filename
            # print 'created_time=',created_time
            if time_now - created_time < timve_interval:
                sendlst.append(filename)

        print 'sendlst=', sendlst
        if len(sendlst) < send_watermark:
            continue

        reslst = []
        for x in sendlst:
            created_time = os.path.getctime(x)
            if created_time > last_sent_file_create_time:
                reslst.append(x)
        print 'reslst=', reslst
        if len(reslst) < send_watermark:
            continue

        rt = random.sample(reslst, send_count)  # 从list中随机获取n个元素，作为一个片断返回
        print '#### rt=', rt
        TrySend(rt)


if __name__ == '__main__':
    while True:
        try:
            Run()
        except Exception, e:
            print e
            continue
