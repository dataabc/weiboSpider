#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import re
import requests
import sys
import traceback
import csv
import time
from datetime import datetime
from datetime import timedelta
from lxml import etree
from googletrans import Translator

emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)


class Weibo:
    cookie = {"Cookie": "_T_WM=3ee66893b0c9bfd883628d437ccdb644; SCF=Aqt1CGgzsIJiOEI_UrIiVE4sjjLz6YI7JXnoy65qoX5SBDW29c-SHrlkJaigKdSjXpq_F86MXllb7P0_oP55KtM.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWvW0Jk66DBo_dquLugAH8g5JpX5K-hUgL.Fo-4S0epSK5cShM2dJLoIEvJi--fiK.7iKn0i--NiKnpi-8Fi--4iK.XiKnfi--NiKLWiKnXi--NiKyhi-8FP7tt; M_WEIBOCN_PARAMS=uicode%3D20000174%26featurecode%3D20000320%26fid%3Dhotword; SUB=_2A253SuJZDeRhGeNH7FEQ9S7KzzuIHXVUtI4RrDV6PUJbkdBeLWf9kW1NSpoOV0ki5QMBX32mUOLHh_eGthS4LWw8; SUHB=010G4fK5jataN9; SSOLoginState=1515098633"}  # 将your cookie替换成自己的cookie


    # Weibo类初始化
    def __init__(self, user_id, filter=0):
        self.user_id = user_id  # 用户id，即需要我们输入的数字，如昵称为“Dear-迪丽热巴”的id为1669879400
        self.filter = filter  # 取值范围为0、1，程序默认值为0，代表要爬取用户的全部微博，1代表只爬取用户的原创微博
        self.username = ''  # 用户名，如“Dear-迪丽热巴”
        self.weibo_num = 0  # 用户全部微博数
        self.weibo_num2 = 0  # 爬取到的微博数
        self.following = 0  # 用户关注数
        self.followers = 0  # 用户粉丝数
        self.weibo_content = []  # 微博内容
        self.publish_time = []  # 微博发布时间
        self.up_num = []  # 微博对应的点赞数
        self.retweet_num = []  # 微博对应的转发数
        self.comment_num = []  # 微博对应的评论数

    def read_from_file(self,filepath):
        try:
            f = open(filepath, "r")
        except Exception, e:
            print "Error: ", e
            traceback.print_exc()

        last_line = ""

        # 读取微博信息
        try:
            f.next()
            self.username = f.next()[15:]
            self.user_id = int(f.next()[11:])
            self.weibo_num = int(f.next()[12:])
            self.weibo_num2 = self.weibo_num
            self.following = int(f.next()[12:])
            self.followers = int(f.next()[12:])
            f.next()
            f.next()
        except Exception, e:
            print "Error: ", e
            traceback.print_exc()

        # 读取每条微博
        weibo_num = 0
        weibo_content = ""
        for line in f:
            if line != '\n':
                if u"发布时间" == line.decode(sys.stdout.encoding)[:4]:
                    self.publish_time.append(line[15:])
                elif u"点赞数" == line.decode(sys.stdout.encoding)[:3]:
                    pattern = r"\d+\.?\d*"
                    guid = re.findall(pattern, line, re.S | re.M)
                    self.up_num.append(int(guid[0])) # 微博对应的点赞数
                    self.retweet_num.append(int(guid[1])) # 微博对应的转发数
                    self.comment_num.append(int(guid[2]))  # 微博对应的评论数
                else:
                    weibo_content = weibo_content + line.decode(sys.stdout.encoding).encode(sys.stdout.encoding)
            else:
                self.weibo_content.append(weibo_content)
                weibo_content = ""
                weibo_num = weibo_num + 1

                # 检查信息空集
                if len(self.up_num) < weibo_num:
                    self.up_num.append(0)
                if len(self.retweet_num) < weibo_num:
                    self.retweet_num.append(0)
                if len(self.comment_num) < weibo_num:
                    self.comment_num.append(0)
                if len(self.weibo_content) < weibo_num:
                    self.weibo_content.append("")

            last_line = line

        # 不完整结尾信息
        if last_line != "\n":
            weibo_num = weibo_num + 1
            if len(self.up_num) < weibo_num:
                self.up_num.append(0)
            if len(self.retweet_num) < weibo_num:
                self.retweet_num.append(0)
            if len(self.comment_num) < weibo_num:
                self.comment_num.append(0)
            if len(self.weibo_content) < weibo_num:
                self.weibo_content.append("")

        self.weibo_num2 = weibo_num

    # 获取用户昵称
    def get_username(self):
        try:
            url = "https://weibo.cn/%d/info" % (self.user_id)
            html = requests.get(url, cookies=self.cookie).content
            selector = etree.HTML(html)
            username = selector.xpath("//title/text()")[0]
            self.username = username[:-3]
            print u"用户名: " + self.username
        except Exception, e:
            print "Error: ", e
            traceback.print_exc()

    # 获取用户微博数、关注数、粉丝数
    def get_user_info(self):
        try:
            url = "https://weibo.cn/u/%d?filter=%d&page=1" % (
                self.user_id, self.filter)
            html = requests.get(url, cookies=self.cookie).content
            selector = etree.HTML(html)
            pattern = r"\d+\.?\d*"

            # 微博数
            str_wb = selector.xpath(
                "//div[@class='tip2']/span[@class='tc']/text()")[0]
            guid = re.findall(pattern, str_wb, re.S | re.M)
            for value in guid:
                num_wb = int(value)
                break
            self.weibo_num = num_wb
            print u"微博数: " + str(self.weibo_num)

            # 关注数
            str_gz = selector.xpath("//div[@class='tip2']/a/text()")[0]
            guid = re.findall(pattern, str_gz, re.M)
            self.following = int(guid[0])
            print u"关注数: " + str(self.following)

            # 粉丝数
            str_fs = selector.xpath("//div[@class='tip2']/a/text()")[1]
            guid = re.findall(pattern, str_fs, re.M)
            self.followers = int(guid[0])
            print u"粉丝数: " + str(self.followers)

        except Exception, e:
            print "Error: ", e
            traceback.print_exc()

    # 获取用户微博内容及对应的发布时间、点赞数、转发数、评论数
    def get_weibo_info(self):
        try:
            url = "https://weibo.cn/u/%d?filter=%d&page=1" % (
                self.user_id, self.filter)
            html = requests.get(url, cookies=self.cookie).content
            selector = etree.HTML(html)
            if selector.xpath("//input[@name='mp']") == []:
                page_num = 1
            else:
                page_num = (int)(selector.xpath(
                    "//input[@name='mp']")[0].attrib["value"])
            pattern = r"\d+\.?\d*"
            for page in range(1, page_num + 1):
                url2 = "https://weibo.cn/u/%d?filter=%d&page=%d" % (
                    self.user_id, self.filter, page)
                html2 = requests.get(url2, cookies=self.cookie).content
                selector2 = etree.HTML(html2)
                info = selector2.xpath("//div[@class='c']")
                if len(info) > 3:
                    for i in range(0, len(info) - 2):
                        # 微博内容
                        # 修改: 因为转发和原创所用class不同,所以取消[@class]直接查询

                        str_class = info[i].xpath("div/span/@class")[0]
                        if str_class == "cmt":
                            # 原信息 + 转发理由
                            weibo_content = \
                                    info[i].xpath("div/span")[0].xpath("string(.)").encode(sys.stdout.\
                                    encoding,"ignore").decode(sys.stdout.encoding) + '\n' + \
                                    info[i].xpath("div/span")[1].xpath("string(.)").encode(sys.stdout.encoding,\
                                    "ignore").decode(sys.stdout.encoding) + '\n' + \
                                    re.search(r'(.*?)\xa0', info[i].xpath("div")[-1].xpath("string(.)").\
                                    encode(sys.stdout.encoding,"ignore").decode(sys.stdout.encoding)).group(1)
                        else: #  str_class == "ctt" 默认原创
                            str_t = info[i].xpath("div/span[@class='ctt']")
                            weibo_content = str_t[0].xpath("string(.)").encode(
                                sys.stdout.encoding, "ignore").decode(
                                sys.stdout.encoding)

                        self.weibo_content.append(weibo_content)
                        print u"微博内容：" + weibo_content

                        # 微博发布时间
                        if str_class == "cmt":
                            str_time = info[i].xpath("div")[-1].xpath("span[@class='ct']")
                        else:
                            str_time = info[i].xpath("div/span[@class='ct']")
                        str_time = str_time[0].xpath("string(.)").encode(
                            sys.stdout.encoding, "ignore").decode(
                            sys.stdout.encoding)
                        publish_time = str_time.split(u'来自')[0]
                        if u"刚刚" in publish_time:
                            publish_time = datetime.now().strftime(
                                '%Y-%m-%d %H:%M')
                        elif u"分钟" in publish_time:
                            minute = publish_time[:publish_time.find(u"分钟")]
                            minute = timedelta(minutes=int(minute))
                            publish_time = (
                                datetime.now() - minute).strftime(
                                "%Y-%m-%d %H:%M")
                        elif u"今天" in publish_time:
                            today = datetime.now().strftime("%Y-%m-%d")
                            time = publish_time[3:]
                            publish_time = today + " " + time
                        elif u"月" in publish_time:
                            year = datetime.now().strftime("%Y")
                            month = publish_time[0:2]
                            day = publish_time[3:5]
                            time = publish_time[7:12]
                            publish_time = (
                                year + "-" + month + "-" + day + " " + time)
                        else:
                            publish_time = publish_time[:16]
                        self.publish_time.append(publish_time)
                        print u"微博发布时间：" + publish_time

                        # 修改2: 直接读取整条信息,避免"已赞"格式无法分析 -> empty zan list
                        #        分别在不同区块读取原创和转发信息

                        # guid: 赞、转发、评论
                        if str_class == "cmt":
                            str_meta = info[i].xpath("div")[-1]
                        else: # str_class == "ctt"
                            if len(info[i].xpath("div")) > 1:
                                str_meta = info[i].xpath("div")[1] # 带图
                            else:
                                str_meta = info[i].xpath("div")[0] # 文字博

                        str_meta = str_meta.xpath("string(.)").encode(sys.stdout.encoding, "ignore").decode(
                            sys.stdout.encoding)
                        str_meta = str_meta[str_meta.find(u'赞'):]
                        guid = re.findall(pattern, str_meta, re.M)

                        # 点赞数
                        up_num = int(guid[0])
                        self.up_num.append(up_num)
                        print u"点赞数: " + str(up_num)

                        # 转发数
                        retweet_num = int(guid[1])
                        self.retweet_num.append(retweet_num)
                        print u"转发数: " + str(retweet_num)

                        # 评论数
                        comment_num = int(guid[2])
                        self.comment_num.append(comment_num)
                        print u"评论数: " + str(comment_num)

                        self.weibo_num2 += 1

            if not self.filter:
                print u"共" + str(self.weibo_num2) + u"条微博"
            else:
                print (u"共" + str(self.weibo_num) + u"条微博，其中" +
                       str(self.weibo_num2) + u"条为原创微博"
                       )
        except Exception, e:
            print "Error: ", e
            traceback.print_exc()

    # 将爬取的信息写入文件
    def write_txt(self):
        try:
            if self.filter:
                result_header = u"\n\n原创微博内容：\n"
            else:
                result_header = u"\n\n微博内容：\n"
            result = (u"用户信息\n用户昵称：" + self.username +
                      u"\n用户id：" + str(self.user_id) +
                      u"\n微博数：" + str(self.weibo_num) +
                      u"\n关注数：" + str(self.following) +
                      u"\n粉丝数：" + str(self.followers) +
                      result_header
                      )
            for i in range(1, self.weibo_num2 + 1):
                text = (str(i) + ":" + self.weibo_content[i - 1] + "\n" +
                        u"发布时间：" + self.publish_time[i - 1] + "\n" +
                        u"点赞数：" + str(self.up_num[i - 1]) +
                        u"	 转发数：" + str(self.retweet_num[i - 1]) +
                        u"	 评论数：" + str(self.comment_num[i - 1]) + "\n\n"
                        )
                result = result + text
            file_dir = os.path.split(os.path.realpath(__file__))[
                0] + os.sep + "weibo"
            if not os.path.isdir(file_dir):
                os.mkdir(file_dir)
            file_path = file_dir + os.sep + "%d" % self.user_id + ".txt"
            f = open(file_path, "wb")
            f.write(result.encode(sys.stdout.encoding))
            f.close()
            print u"微博写入文件完毕，保存路径:" + file_path
        except Exception, e:
            print "Error: ", e
            traceback.print_exc()

    def write_pure(self):
        try:
            result = ""
            for i in range(1, self.weibo_num2 + 1):
                result = result + self.weibo_content[i-1] + '\n\n'
            file_dir = os.path.split(os.path.realpath(__file__))[
                0] + os.sep + "weibo"
            if not os.path.isdir(file_dir):
                os.mkdir(file_dir)
            file_path = file_dir + os.sep + "%d" % self.user_id + "_pure.txt"
            f = open(file_path, "wb")
            f.write(result.encode(sys.stdout.encoding))
            f.close()
            print u"微博写入文件完毕，保存路径:" + file_path
        except Exception, e:
            print "Error: ", e
            traceback.print_exc()

    def write_csv(self,file_path, translation=0):
        try:
            f = open(file_path, "wb")
            port_csv = csv.writer(f)
            port_csv.writerow(["微博","翻译","点赞数","转发数","评论数","发布时间"])

            translator = Translator()
            for i in range(0,len(self.weibo_content)):
                if translation == 0:
                    translated = ""
                else:
                    translated = translator.translate(emoji_pattern.sub(r'', self.weibo_content[i])).text.encode(sys.stdout.encoding)
                    time.sleep(1.5)
                    print(translated)

                newrow = [self.weibo_content[i],translated,self.up_num[i],self.retweet_num[i],self.comment_num[i],self.publish_time[i]]
                port_csv.writerow(newrow)
            f.close()
            print u"csv写入文件完毕，保存路径:" + file_path
        except Exception,e:
            print "Error: ", e
            traceback.print_exc()

    # 运行爬虫
    def start(self):
        try:
            self.get_username()
            self.get_user_info()
            self.get_weibo_info()
            print("done with info")
            self.write_txt()
            print u"信息抓取完毕"
            print "==========================================================================="
        except Exception, e:
            print "Error: ", e

def read_cookie(file_path):
    data = ""
    try:
        with open(file_path,'r') as f:
            data = f.read()
    except Exception, e:
        print "Error: ", e
        traceback.print_exc()

    return data


def main():

    print("选择任务：1.采集微博信息 2.转换txt到csv")
    choice = str(raw_input("您的选择: "))

    if choice == "1":
        try:
            # 使用实例,输入一个用户id，所有信息都会存储在wb实例中
            user_id = 5491331848 # 可以改成任意合法的用户id（爬虫的微博id除外）
            filter = 0  # 值为0表示爬取全部微博（原创微博+转发微博），值为1表示只爬取原创微博
            wb = Weibo(user_id, filter)  # 调用Weibo类，创建微博实例wb
            wb.start()  # 爬取微博信息
            print u"用户名：" + wb.username
            print u"全部微博数：" + str(wb.weibo_num)
            print u"关注数：" + str(wb.following)
            print u"粉丝数：" + str(wb.followers)
            print u"最新一条原创微博为：" + wb.weibo_content[0]
            print u"最新一条原创微博发布时间：" + wb.publish_time[0]
            print u"最新一条原创微博获得的点赞数：" + str(wb.up_num[0])
            print u"最新一条原创微博获得的转发数：" + str(wb.retweet_num[0])
            print u"最新一条原创微博获得的评论数：" + str(wb.comment_num[0])
        except Exception, e:
            print "Error: ", e
            traceback.print_exc()
    elif choice == "2":
        try:
            print("请输入文件名: weibo/filename")
            file_path = raw_input("您的输入： ")
            filter = 0
            wb = Weibo('0000',filter)
            file_path = os.getcwd() + os.path.sep + "weibo" + os.path.sep + file_path

            if os.path.exists(file_path):
                wb.read_from_file(file_path)
                print u"用户名：" + wb.username.decode(sys.stdout.encoding)
                print u"全部微博数：" + str(wb.weibo_num)
                print u"关注数：" + str(wb.following)
                print u"粉丝数：" + str(wb.followers)
                print u"最新一条原创微博为：" + wb.weibo_content[0].decode(sys.stdout.encoding)
                print u"最新一条原创微博发布时间：" + wb.publish_time[0].decode(sys.stdout.encoding)
                print u"最新一条原创微博获得的点赞数：" + str(wb.up_num[0])
                print u"最新一条原创微博获得的转发数：" + str(wb.retweet_num[0])
                print u"最新一条原创微博获得的评论数：" + str(wb.comment_num[0])
                wb.write_csv(file_path[:-4] + '.csv',1)
                print u"文件转化完毕: " + file_path
            else:
                raise Exception, u"文件不存在: " + file_path

        except Exception, e:
            print "Error: ", e
            traceback.print_exc()
    else:
        print("请输入合法选择：1.采集微博信息 2.转换txt到csv")
        print("退出")


if __name__ == "__main__":
    main()
