#!C:\Users\Administrator\AppData\Local\Programs\Python\Python36\python.exe
# -*- coding: utf-8 -*-
"""
Created on 15:20:00 2018-01-11

@author: kplam
"""

import smtplib
import email.mime.multipart
import email.mime.text

def sendmail(subject,content):


    msg = email.mime.multipart.MIMEMultipart()
    msg['from'] = 'kplam@qq.com'
    msg['to'] = 'admin@kplam.com'
    msg['subject'] = subject
    txt = email.mime.text.MIMEText(content)
    msg.attach(txt)

    smtp = smtplib.SMTP_SSL()
    smtp.connect('smtp.qq.com', '465')
    smtp.login('359765646', 'kplam2014')
    smtp.sendmail('kplam@qq.com', 'admin@kplam.com', str(msg))
    smtp.quit()


if __name__ == '__main__':
    sendmail("test","test")
