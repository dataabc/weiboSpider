#!/usr/bin/env python
#! python3
# -*- coding: UTF-8 -*-

import os
import re
import requests
import sys
import traceback
from datetime import datetime
from datetime import timedelta
from lxml import etree
import time
import codecs
import pandas as pd
from bs4 import BeautifulSoup


class Weibo():

    # Weibo类初始化
    def __init__(self, user_id, ck, filter=0):
        self.user_id = user_id  # 用户id，即需要我们输入的数字，如昵称为“Dear-迪丽热巴”的id为1669879400
        self.filter = filter  # 取值范围为0、1，程序默认值为0，代表要爬取用户的全部微博，1代表只爬取用户的原创微博
        self.username = ''  # 用户名，如“Dear-迪丽热巴”
        self.origin = []  # 微博来源，如'原创'
        self.weibo_num = 0  # 用户全部微博数
        self.weibo_num2 = 0  # 爬取到的微博数
        self.following = 0  # 用户关注数
        self.followers = 0  # 用户粉丝数
        self.weibo_content = []  # 微博内容
        self.weibo_content3 = []  # 微博所转发的原文
        self.publish_time = []  # 微博发布时间
        self.publish_device = []  # 微博发布设备
        self.up_num = []  # 微博对应的点赞数
        self.retweet_num = []  # 微博对应的转发数
        self.comment_num = []  # 微博对应的评论数

    # 获取用户昵称
    def get_username(self):
        try:
            url = "https://weibo.cn/%d/info" % (self.user_id)
            html = requests.get(url, cookies=self.cookie).content
            selector = etree.HTML(html)
            username = selector.xpath("//title/text()")[0]
            self.username = username[:-3]
            print(u"用户名: " + self.username)
        except Exception as e:
            print("[ Error ]  ", e)
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
            print(u"[ Info ] 微博数: " + str(self.weibo_num))

            # 关注数
            str_gz = selector.xpath("//div[@class='tip2']/a/text()")[0]
            guid = re.findall(pattern, str_gz, re.M)
            self.following = int(guid[0])
            print(u"[ Info ] 关注数: " + str(self.following))

            # 粉丝数
            str_fs = selector.xpath("//div[@class='tip2']/a/text()")[1]
            guid = re.findall(pattern, str_fs, re.M)
            self.followers = int(guid[0])
            print(u"[ Info ] 粉丝数: " + str(self.followers))

        except Exception as e:
            print("[ Error ]  ", e)
            traceback.print_exc()
            self.fail_list.append(self.user_id)

    # 获取用户微博内容及对应的发布时间、点赞数、转发数、评论数
    def get_weibo_info(self):

        # 获取微博消息全文
        # 该函数负责接受列表i，微博信息对象，然后返回全文对象
        # 对没有全文链接的微博，直接返回正则替换过的该文本
        def get_full_text(info, i, weibo_content, idname):
            if re.findall(r"\$\$全文\$\$", weibo_content):
                # 判断是否存在未读取的全文

                # 利用id属性获得全文链接 例如"/comment/FoeC00oeA"
                full_url = '/comment/' + idname.split('_')[-1]
                url3 = "https://weibo.cn%s" % full_url
                # 获取全文url

                print(u"[ Info ] 获取全文中......")
                time.sleep(3)
                html3 = requests.get(url3, cookies=self.cookie).content
                soup1 = BeautifulSoup(html3, 'lxml')
                content = str(soup1.select('.ctt')[0])
                content = content[18:-7]  # 去除span
                content = re.sub(r"</a>", '$$', content)  # 先将替换</a>为$$
                content = re.sub(r"<a href=\"(.+?)\">", '$$',
                                 content)  # 再将前面的<a href>替换为$$
                if content[:1] == ":":
                    content = weibo_content[1:]
                # 全文跳转后句首会出现':'  因此切片
                # 全文中包含换行符但打印为5到6个半角空格或3个全角空格，因此正则替换
                # csv不允许出现, 因此替换为"," 采取转义\'（后两项对于非全文的也一样适用）
                weibo_content = content
            weibo_content = re.sub(r"\u200B+|\u202F+", "", weibo_content)
            weibo_content = re.sub(r"\s{2,}|\u3000{2,}", "<br>", weibo_content)
            weibo_content = weibo_content.replace(',', '\',\'')
            return weibo_content

        # 获取微博文本的6个指标
        # 发布时间,发布设备,点赞,转发,评论,message_id
        def get_message_attr(self, info, i):
            # 微博发布时间与设备
            str_time = info[i].xpath("div/span[@class='ct']")
            str_time = str_time[0].xpath("string(.)").encode(
                sys.stdout.encoding, "ignore").decode(
                sys.stdout.encoding)
            publish_time = str_time.split(u'来自')[0]
            publish_device = str_time.split(u'来自')[-1]
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
                publish_time = publish_time[:19]
            self.publish_time.append(publish_time)
            self.publish_device.append(publish_device)
            print(u"[ Info ] 微博发布时间：" + publish_time)
            # print(u"[ Info ] 微博发布设备：" + publish_device)

            # 点赞数
            str_zan = info[i].xpath("div/a/text()")[-4]
            guid = re.findall(pattern, str_zan, re.M)
            up_num = int(guid[0])
            self.up_num.append(up_num)
            # print(u"[ Info ] 点赞数: " + str(up_num))

            # 转发数
            retweet = info[i].xpath("div/a/text()")[-3]
            guid = re.findall(pattern, retweet, re.M)
            retweet_num = int(guid[0])
            self.retweet_num.append(retweet_num)
            # print(u"[ Info ] 转发数: " + str(retweet_num))

            # 评论数
            comment = info[i].xpath("div/a/text()")[-2]
            guid = re.findall(pattern, comment, re.M)
            comment_num = int(guid[0])
            self.comment_num.append(comment_num)
            # print(u"[ Info ] 评论数: " + str(comment_num))

            # 创建微博内容的message_id 格式为id_weibo_num2
            seq1 = [str(self.user_id), str(self.weibo_num2 + 1)]
            message_id = '_'.join(seq1)
            self.message_id.append(message_id)
            print(u"[ Info ] message_id：" + message_id)

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
                print("~" * 5)
                print("[ Waiting ] 4.5s ..........")
                time.sleep(4.5)
                if page % 30 == 0:
                    print(
                        "[ Waiting ] 30 pages or more has passed, waiting "
                        "150s ..........")
                    time.sleep(150)
                url2 = "https://weibo.cn/u/%d?filter=%d&page=%d" % (
                    self.user_id, self.filter, page)
                html2 = requests.get(url2, cookies=self.cookie).content
                soup = BeautifulSoup(html2, "lxml")
                selector2 = etree.HTML(html2)
                info = selector2.xpath("//div[@class='c']")
                if len(info) > 2:
                    for i in range(0, len(info) - 2):
                        # 对每条微博进行爬取
                        # len=3 转发 原创在div[3]
                        # len=2 转发 原创在div[2] 也有可能是原创+图片 原创在div[1]
                        # len=1 原创
                        # len=0 无微博

                        # 如果是转发，利用列表切片获得用户昵称
                        # 如果是原创，则利用except进行手动赋值'原创'

                        # 获取转发时的该微博的评论
                        # 三个问题：1 一般不会超过140个字，所以不进行全文的爬取，也忽略原图甚至其他链接
                        # 2 有时会出现三个转发；3 有时只有两个div 转发微博和转发理由
                        # 即A: 转发微博评论//@B: 转发微博评论//@C: 微博评论
                        # 这种情况下认为c是被转发，而A和B的评论均认为是A的评论
                        # 用bs4直接获取最后一个div的html文本

                        # 不读取 置顶微博
                        if page == 1:
                            if i == 0:
                                if (len(info[i].xpath(
                                        "div/span[@class='kt']/text()")) != 0):
                                    print(u"[ Waiting ] 跳过置顶微博")
                                    continue

                        # 增加对于0条微博的支持
                        if not self.weibo_num:
                            # 为0条微博的博主赋空值
                            self.weibo_content.append('')
                            self.weibo_content3.append('')
                            self.publish_time.append('')
                            self.publish_device.append('')
                            self.up_num.append('0')
                            self.retweet_num.append('0')
                            self.comment_num.append('0')
                            self.origin.append('')
                            self.message_id.append('')
                            continue

                        info_num = len(info[i])
                        idname = info[i].xpath("@id")[0]

                        if info_num == 3:

                            # 微博来源与进度
                            str_source = info[i].xpath(
                                "div/span[@class='cmt']")
                            origin = str_source[0].xpath("string(.)").encode(
                                sys.stdout.encoding, "ignore").decode(
                                sys.stdout.encoding)
                            origin = origin[4:-4]
                            self.origin.append(origin)
                            print("~" * 5)
                            print(u"[ Info ] 进度 %.2f%%" % ((
                                self.weibo_num2 + 1) / self.weibo_num * 100))
                            print(u"[ Info ] 微博来源：" + origin)

                            # 微博内容（转发理由）
                            a = str(soup.select(
                                '#' + idname + ' div:nth-of-type(3)')[0])
                            a = a[35:-6]  # 去除div
                            a = re.sub(r"</span>", '', a)  # 去除</span>
                            a = re.sub(
                                r"<span class=\"cmt\>", '', a)  # 去除<span class='cmt>
                            a = a[:a.find('<!--')]  # 去除后面的span
                            a = re.sub(r"</a>", '$$', a)  # 先将替换</a>为$$
                            a = re.sub(r"<a href=\"(.+?)\">", '$$',
                                       a)  # 再将前面的<a href>替换为$$
                            a = a[:a.find('$$赞')]
                            a = a.replace('\u202F', '')  # 去除&nbsp;
                            a = a.replace('\u200b', '')  # 去除&#8203;
                            weibo_content = a
                            self.weibo_content.append(weibo_content)
                            print(u"[ Info ] 微博内容：" + weibo_content)

                            # 被转发的正文
                            ctt = str(soup.select('#' + idname + ' .ctt')[0])
                            ctt = ctt[18:-7]
                            ctt = re.sub(r"</a>", '$$', ctt)  # 先将替换</a>为$$
                            ctt = re.sub(
                                r"<a href=\"(.+?)\">", '$$', ctt)  # 再将前面的<a href>替换为$$
                            weibo_content3 = get_full_text(
                                info, i, ctt, idname)
                            self.weibo_content3.append(weibo_content3)
                            print(u"[ Info ] 转发原文：" + weibo_content3)

                            # 获取微博指标
                            get_message_attr(self, info=info, i=i)

                            # 计数增加
                            self.weibo_num2 += 1

                        elif info_num == 2:

                            # 判断是 转发+理由 还是 原创+图片
                            if len(
                                soup.select(
                                    '#' +
                                    idname +
                                    ' > div:nth-of-type(2) > .cmt')) == 0:

                                # 判断是原创，因为不包含span[class='cmt']

                                # 微博来源和进度
                                origin = u'原创'
                                self.origin.append(origin)
                                print("~" * 5)
                                print(
                                    u"[ Info ] 进度 %.2f%%" %
                                    ((self.weibo_num2 + 1) / self.weibo_num * 100))
                                print(u"[ Info ] 微博来源：" + origin)

                                # 微博内容
                                ctt = str(
                                    soup.select('#' + idname + ' .ctt')[0])
                                ctt = ctt[18:-7]
                                ctt = re.sub(r"</a>", '$$', ctt)  # 先将替换</a>为$$
                                ctt = re.sub(r"<a href=\"(.+?)\">", '$$',
                                             ctt)  # 再将前面的<a href>替换为$$
                                weibo_content = get_full_text(info, i, ctt,
                                                              idname)
                                self.weibo_content.append(weibo_content)
                                print(u"[ Info ] 微博内容：" + weibo_content)

                                # (转发内容)保持对齐 手动赋值"Original Weibo"
                                weibo_content3 = u"Original Weibo"
                                self.weibo_content3.append(weibo_content3)

                                # 获取微博指标
                                get_message_attr(self=self, info=info, i=i)

                                # 计数增加
                                self.weibo_num2 += 1

                            else:
                                # 判断是转发

                                # 微博来源与进度
                                str_source = info[i].xpath(
                                    "div/span[@class='cmt']")
                                origin = str_source[0].xpath("string(.)").encode(
                                    sys.stdout.encoding, "ignore").decode(
                                    sys.stdout.encoding)
                                origin = origin[4:-4]
                                self.origin.append(origin)
                                print("~" * 5)
                                print(
                                    u"[ Info ] 进度 %.2f%%" %
                                    ((self.weibo_num2 + 1) / self.weibo_num * 100))
                                print(u"[ Info ] 微博来源：" + origin)

                                # 微博内容（转发理由）
                                a = str(
                                    soup.select(
                                        '#' +
                                        idname +
                                        ' > div:nth-of-type(2)')[0])
                                a = a[35:-6]  # 去除div
                                a = re.sub(r"</span>", '', a)  # 去除</span>
                                a = re.sub(
                                    r"<span class=\"cmt\>", '', a)  # 去除<span class='cmt>
                                a = a[:a.find('<!--')]  # 去除后面的span
                                a = re.sub(r"</a>", '$$', a)  # 先将替换</a>为$$
                                a = re.sub(r"<a href=\"(.+?)\">", '$$',
                                           a)  # 再将前面的<a href>替换为$$
                                a = a[:a.find('$$赞')]
                                a = a.replace('\u202F', '')  # 去除&nbsp;
                                a = a.replace('\u200b', '')  # 去除&#8203;

                                weibo_content = a
                                self.weibo_content.append(weibo_content)
                                print(u"[ Info ] 微博内容：" + weibo_content)

                                # 被转发的正文
                                ctt = str(
                                    soup.select(
                                        '#' + idname + ' .ctt')[0])
                                ctt = ctt[18:-7]
                                ctt = re.sub(r"</a>", '$$', ctt)  # 先将替换</a>为$$
                                ctt = re.sub(r"<a href=\"(.+?)\">", '$$',
                                             ctt)  # 再将前面的<a href>替换为$$
                                weibo_content3 = get_full_text(
                                    info, i, ctt, idname)
                                self.weibo_content3.append(weibo_content3)
                                print(u"[ Info ] 转发原文：" + weibo_content3)

                                # 获取微博指标
                                get_message_attr(self=self, info=info, i=i)

                                # 计数增加
                                self.weibo_num2 += 1

                        # 接下来时原创微博的爬取
                        elif info_num == 1:

                            # 微博来源和进度
                            origin = u'原创'
                            self.origin.append(origin)
                            print("~" * 5)
                            print(u"[ Info ] 进度 %.2f%%" % ((
                                self.weibo_num2 + 1) / self.weibo_num * 100))
                            print(u"[ Info ] 微博来源：" + origin)

                            # 微博内容
                            ctt = str(soup.select('#' + idname + ' .ctt')[0])
                            ctt = ctt[18:-7]
                            ctt = re.sub(r"</a>", '$$', ctt)  # 先将替换</a>为$$
                            ctt = re.sub(r"<a href=\"(.+?)\">", '$$',
                                         ctt)  # 再将前面的<a href>替换为$$
                            weibo_content = get_full_text(info, i, ctt, idname)
                            self.weibo_content.append(weibo_content)
                            print(u"[ Info ] 微博内容：" + weibo_content)

                            # (转发内容)保持对齐 手动赋值"Original Weibo"
                            weibo_content3 = u"Original Weibo"
                            self.weibo_content3.append(weibo_content3)

                            # 获取微博指标
                            get_message_attr(self=self, info=info, i=i)

                            # 计数增加
                            self.weibo_num2 += 1

                        # 为0条微博的博主赋空值
                        else:
                            self.weibo_content.append('')
                            self.weibo_content3.append('')
                            self.publish_time.append('')
                            self.publish_device.append('')
                            self.up_num.append('0')
                            self.retweet_num.append('0')
                            self.comment_num.append('0')
                            self.origin.append('')
                            self.message_id.append('')

            '''
            if not self.filter:
                print(u"共" + str(self.weibo_num2) + u"条微博")
            else:
                print(u"共" + str(self.weibo_num) + u"条微博，其中" +
                       str(self.weibo_num2) + u"条为原创微博")
            '''

        except Exception as e:
            print("[ Error ]  ", e)
            traceback.print_exc()
            self.fail_list.append(self.user_id)

    # 将爬取的信息写入文件
    def write_csv(self):
        try:

            df = pd.DataFrame({
                u"用户id": self.user_id,
                u"用户昵称": self.username,
                u"微博来源": self.origin,
                u"微博数": self.weibo_num,
                u"爬取微博数": self.weibo_num2,
                u"关注数": self.following,
                u"粉丝数": self.followers,
                u"微博内容": self.weibo_content,
                u"转发内容": self.weibo_content3,
                u"发布时间": self.publish_time,
                u"发布设备": self.publish_device,
                u"点赞数": self.up_num,
                u"转发数": self.retweet_num,
                u"评论数": self.comment_num,
            })
            li = [
                u'用户昵称',
                u'用户id',
                u'微博数',
                u'关注数',
                u'粉丝数',
                u'爬取微博数',
                u'微博来源',
                u'微博内容',
                u'转发内容',
                u'发布时间',
                u'发布设备',
                u'点赞数',
                u'转发数',
                u'评论数'
            ]

            file_dir = os.path.split(os.path.realpath(__file__))[
                0] + os.sep + "weibo_files"
            if not os.path.isdir(file_dir):
                os.mkdir(file_dir)
            file_path = file_dir + os.sep + "%d_%d" % (
                self.user_id, self.filter) + ".csv"

            df = df.reindex(columns=li)

            df.to_csv(file_path, sep=',', header=True,
                      index=False, encoding='utf-8', mode='w')

            print(u"[ Success ] 文件已写入：%d_%d.csv" % (self.user_id, self.filter))
            '''
            这是txt文件内容
            result = (u"用户昵称：" + self.username +
                      u"\n用户id：" + str(self.user_id) +
                      u"\n微博数：" + str(self.weibo_num) +
                      u"\n关注数：" + str(self.following) +
                      u"\n粉丝数：" + str(self.followers) +
                      u"\n爬取微博数：" + str(self.weibo_num2) + "\n\n")
            for i in range(1, self.weibo_num2 + 1):
                text = (u"信息id：" + self.message_id[i - 1] + "\n" +
                        u"微博来源：" + self.origin[i - 1] + "\n" +
                        u"微博内容：" + self.weibo_content[i - 1] + "\n" +
                        u"转发内容：" + self.weibo_content3[i - 1] + "\n" +
                        u"发布时间：" + self.publish_time[i - 1] + "\n" +
                        u"发布设备：" + self.publish_device[i - 1] + "\n" +
                        u"点赞数：" + str(self.up_num[i - 1]) + "\n" +
                        u"转发数：" + str(self.retweet_num[i - 1]) + "\n" +
                        u"评论数：" + str(self.comment_num[i - 1]) + "\n\n"
                        )
                result = result + text

            下面为txt写入方法
            文件采取utf-8编码
            f =codecs.open(file_path,"wb","utf-8")
            f.write(result)
            f.close()
            print 'type(result)=%r'%type(result)
            print 'len(result)=%d'%len(result)
            '''

        except Exception as e:
            print("[ Error ]  ", e)
            traceback.print_exc()
            self.fail_list.append(self.user_id)

    # 运行爬虫
    def start(self):
        try:
            self.get_username()
            self.get_user_info()
            self.get_weibo_info()
            self.write_csv()
            print(u"[ Success ] 信息抓取完毕")
            print("=" * 20 + '\n')
        except Exception as e:
            print("[ Error ]  ", e)
            self.fail_list.append(self.user_id)


def main():

    cktxt = ''  # cookie输入

    try:
        # 使用实例,输入一组用户id，所有信息都会存储在wb实例中
        # 可以改成任意合法的用户id（爬虫的微博id除外）
        idlist = [
            1289712177,
            3536870004,
            3901874281,
            3153215033,
            5035462987,
            3910388233,
            3599267313,
            3942833739,
        ]
        for uid in idlist:

            user_id = uid  # 进行循环赋值
            filter = 0  # 值为0表示爬取全部微博（原创微博+转发微博），值为1表示只爬取原创微博
            wb = Weibo(user_id, cktxt, filter)  # 调用Weibo类，创建微博实例wb
            wb.start()  # 爬取微博信息
            print(u"用户名：" + wb.username)
            print(u"全部微博数：" + str(wb.weibo_num))
            print(u"关注数：" + str(wb.following))
            print(u"粉丝数：" + str(wb.followers))
            print("[ Waiting ] change to next id. Waiting 150s ..........")
            time.sleep(150)
            if (idlist.index(uid) > 2) and (idlist.index(uid) % 3 == 0):
                print("[ Waiting ] Occasionally waiting 100s .........")
                time.sleep(100)

            if idlist.index(uid) % 2 == 0:
                os.system("cls")  # Windows下清屏
                # os.system("clear")  # Linux下清屏
        print(u"[ Success ] 请更换cookie或list !!!")

    except Exception as e:
        print("[ Error ]  ", e)
        traceback.print_exc()


if __name__ == "__main__":
    main()