#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import random
import sys
from datetime import date, datetime, timedelta
from time import sleep

from tqdm import tqdm

from downloader import Downloader
from html_parser import Parser
from printer import Printer
from validator import Validator
from writer import Writer, get_filepath, write_log


class Spider(object):
    def __init__(self, config):
        """Weibo类初始化"""
        self.config = config
        # change cookie from string to dict
        if type(self.config['cookie']) == type(u''):
            self.config['cookie'] = {
                t.strip().split("=")[0]: t.strip().split("=")[1]
                for t in self.config['cookie'].split(";")
            }
        if type(self.config['user_id_list']) == type(u""):
            user_id_list = self.config['user_id_list']
            if not os.path.isabs(user_id_list):
                user_id_list = os.path.split(
                    os.path.realpath(__file__))[0] + os.sep + user_id_list
            self.config['user_id_list'] = user_id_list
            with open(self.config['user_id_list'], 'rb') as f:
                lines = f.read().splitlines()
                lines = [line.decode('utf-8') for line in lines]
                self.config['user_id_list'] = [
                    line.split(' ')[0] for line in lines if
                    len(line.split(' ')) > 0 and line.split(' ')[0].isdigit()
                ]
        if type(self.config['since_date']) == type(0):
            self.config['since_date'] = str(
                date.today() - timedelta(self.config['since_date']))

        self.validator = Validator(self.config)
        self.validator.validate()
        self.printer = Printer()
        self.writer = Writer(self.config)
        self.downloader = Downloader(self.config)
        self.parser = Parser(self.config)

    def get_nickname(self):
        """获取用户昵称"""
        url = 'https://weibo.cn/%s/info' % (self.user['id'])
        selector = self.parser.deal_html(url, self.config['cookie'])
        nickname = selector.xpath('//title/text()')[0]
        nickname = nickname[:-3]
        if nickname == u'登录 - 新' or nickname == u'新浪':
            write_log(self.config['since_date'])
            sys.exit(u'cookie错误或已过期,请按照README中方法重新获取')
        self.user['nickname'] = nickname

    def get_user_info(self, selector):
        """获取用户昵称、微博数、关注数、粉丝数"""
        self.get_nickname()  # 获取用户昵称
        user_info = selector.xpath("//div[@class='tip2']/*/text()")

        self.user['weibo_num'] = int(user_info[0][3:-1])
        self.user['following'] = int(user_info[1][3:-1])
        self.user['followers'] = int(user_info[2][3:-1])
        self.printer.print_user_info(self.user)
        self.writer.write_user(self.user)
        print('*' * 100)

    def get_one_page(self, page):
        """获取第page页的全部微博"""
        url = 'https://weibo.cn/u/%s?page=%d' % (self.user['id'], page)
        selector = self.parser.deal_html(url, self.config['cookie'])
        info = selector.xpath("//div[@class='c']")
        is_exist = info[0].xpath("div/span[@class='ctt']")
        if is_exist:
            for i in range(0, len(info) - 2):
                weibo = self.parser.get_one_weibo(info[i])
                if weibo:
                    if weibo['id'] in self.weibo_id_list:
                        continue
                    publish_time = datetime.strptime(
                        weibo['publish_time'][:10], "%Y-%m-%d")
                    since_date = datetime.strptime(self.config['since_date'],
                                                   "%Y-%m-%d")
                    if publish_time < since_date:
                        if self.parser.is_pinned_weibo(info[i]):
                            continue
                        else:
                            return True
                    self.printer.print_one_weibo(weibo)

                    self.weibo.append(weibo)
                    self.weibo_id_list.append(weibo['id'])
                    self.got_num += 1
                    print('-' * 100)

                    self.writer.write_weibo([weibo])

    def get_weibo_info(self):
        """获取微博信息"""
        url = 'https://weibo.cn/u/%s' % (self.user['id'])
        selector = self.parser.deal_html(url, self.config['cookie'])
        self.get_user_info(selector)  # 获取用户昵称、微博数、关注数、粉丝数

        page_num = self.parser.get_page_num(selector)  # 获取微博总页数
        page1 = 0
        random_pages = random.randint(1, 5)
        for page in tqdm(range(1, page_num + 1), desc='Progress'):
            is_end = self.get_one_page(page)  # 获取第page页的全部微博
            if is_end:
                break

            # 通过加入随机等待避免被限制。爬虫速度过快容易被系统限制(一段时间后限
            # 制会自动解除)，加入随机等待模拟人的操作，可降低被系统限制的风险。默
            # 认是每爬取1到5页随机等待6到10秒，如果仍然被限，可适当增加sleep时间
            if page - page1 == random_pages and page < page_num:
                sleep(random.randint(6, 10))
                page1 = page
                random_pages = random.randint(1, 5)

        if not self.config['filter']:
            print(u'共爬取' + str(self.got_num) + u'条微博')
        else:
            print(u'共爬取' + str(self.got_num) + u'条原创微博')

    def initialize_info(self, user_id):
        """初始化爬虫信息"""
        self.got_num = 0  # 爬取到的微博数
        self.weibo = []  # 存储爬取到的所有微博信息
        self.user = {'id': user_id}  # 存储爬取到的用户信息
        self.weibo_id_list = []  # 存储爬取到的所有微博id

    def start(self):
        """运行爬虫"""
        for user_id in self.config['user_id_list']:
            self.initialize_info(user_id)
            print('*' * 100)
            self.get_weibo_info()
            print(u'信息抓取完毕')
            print('*' * 100)
            if self.config['pic_download'] == 1:
                file_path = get_filepath('img', self.user['nickname'])
                self.downloader.download_files(file_path, 'img', self.weibo)
            if self.config['video_download'] == 1:
                file_path = get_filepath('video', self.user['nickname'])
                self.downloader.download_files(file_path, 'video', self.weibo)


if __name__ == '__main__':
    import json
    config_path = os.path.split(
        os.path.realpath(__file__))[0] + os.sep + 'config.json'
    if not os.path.isfile(config_path):
        sys.exit(u'当前路径：%s 不存在配置文件config.json' %
                 (os.path.split(os.path.realpath(__file__))[0] + os.sep))
    with open(config_path) as f:
        config = json.loads(f.read())
    spider = Spider(config)
    spider.start()  # 爬取微博信息
