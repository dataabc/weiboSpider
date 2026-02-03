# coding=utf-8
import smtplib
import time
# 需要 MIMEMultipart 类
from email.mime.multipart import MIMEMultipart
# 发送字符串的邮件
from email.mime.text import MIMEText

import update


def send(code, dest):
    # 设置服务器所需信息
    fromEmailAddr = '865011721@qq.com'  # 邮件发送方邮箱地址
    password = 'wnumbsdltnkebehf'  # 密码(部分邮箱为授权码)
    # toEmailAddrs = ['steve.mei@jfz.com']  # 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
    toEmailAddrs = ['865011721@qq.com']  # 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发

    msg = update.grid_notice(code, dest)
    if '1' == msg:
        return

    # 设置email信息
    # ---------------------------发送带附件邮件-----------------------------
    # 邮件内容设置
    message = MIMEMultipart()
    # 邮件主题
    message['Subject'] = '网格提醒-' + code
    # 发送方信息
    message['From'] = fromEmailAddr
    # 接受方信息
    message['To'] = toEmailAddrs[0]

    # 邮件正文内容
    message.attach(MIMEText(msg, 'plain', 'utf-8'))
    # ---------------------------------------------------------------------

    # 登录并发送邮件
    try:
        server = smtplib.SMTP('smtp.qq.com')  # 邮箱服务器地址，端口默认为25
        server.login(fromEmailAddr, password)
        server.sendmail(fromEmailAddr, toEmailAddrs, message.as_string())
        print('success')
        server.quit()
    except smtplib.SMTPException as e:
        print("error:", e)


if __name__ == '__main__':
    send('588000', 1.23)
