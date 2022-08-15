import logging
import smtplib
import sys
import time
# 需要 MIMEMultipart 类
from email.mime.multipart import MIMEMultipart
# 发送字符串的邮件
from email.mime.text import MIMEText

from .writer import Writer

logger = logging.getLogger('spider.txt_writer')


class TxtWriter(Writer):
    def __init__(self, file_path, filter):
        self.file_path = file_path

        self.user_header = u'用户信息'
        self.user_desc = [('nickname', '用户昵称'), ('id', '用户id'),
                          ('weibo_num', '微博数'), ('following', '关注数'),
                          ('followers', '粉丝数')]

        if filter:
            self.weibo_header = u'原创微博内容'
        else:
            self.weibo_header = u'微博内容'
        # self.weibo_desc = [('publish_place', '微博位置'), ('publish_time', '发布时间'),
        #                    ('up_num', '点赞数'), ('retweet_num', '转发数'),
        #                    ('comment_num', '评论数'), ('publish_tool', '发布工具')]
        self.weibo_desc = [('publish_time', '发布时间')]

    def write_user(self, user):
        self.user = user
        user_info = '\n'.join(
            [v + '：' + str(self.user.__dict__[k]) for k, v in self.user_desc])

        with open(self.file_path, 'ab') as f:
            f.write((self.user_header + '：\n' + user_info + '\n\n').encode(
                sys.stdout.encoding))
        logger.info(u'%s信息写入txt文件完毕，保存路径：%s', self.user.nickname,
                    self.file_path)

    def write_weibo(self, weibo):
        """将爬取的信息写入txt文件"""

        # weibo_header = ''
        # if self.weibo_header:
        #     weibo_header = self.weibo_header + '：\n'
        #     self.weibo_header = ''

        try:
            temp_result = []
            for w in weibo:
                temp_result.append(w.__dict__['content'] + '\n' + '\n'.join(
                    [v + '：' + str(w.__dict__[k])
                     for k, v in self.weibo_desc]))
            result = '\n\n'.join(temp_result) + '\n\n'
            # 同步到印象笔记
            self.sendEmail(str(result))

            # with open(self.file_path, 'ab') as f:
            #     f.write((weibo_header + result).encode(sys.stdout.encoding))
            # logger.info(u'%d条微博写入txt文件完毕，保存路径：%s', len(weibo), self.file_path)
        except Exception as e:
            logger.exception(e)

    def sendEmail(self, result):
        # 设置服务器所需信息
        fromEmailAddr = '865011721@qq.com'  # 邮件发送方邮箱地址
        password = 'wnumbsdltnkebehf'  # 密码(部分邮箱为授权码)
        toEmailAddrs = ['865011721.42f1aa8@m.yinxiang.com']  # 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发

        currentDate = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        # 设置email信息
        # ---------------------------发送带附件邮件-----------------------------
        # 邮件内容设置
        message = MIMEMultipart()
        # 邮件主题
        message['Subject'] = currentDate
        # 发送方信息
        message['From'] = fromEmailAddr
        # 接受方信息
        message['To'] = toEmailAddrs[0]

        # 邮件正文内容
        message.attach(MIMEText(result, 'plain', 'utf-8'))
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
