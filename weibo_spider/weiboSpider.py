#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import json
import os
import random
import shutil
import sys
import traceback
from datetime import date, datetime, timedelta
from time import sleep

from absl import app, flags
from tqdm import tqdm

from . import config_util, datetime_util, printer
from .parser import IndexParser, PageParser

FLAGS = flags.FLAGS

flags.DEFINE_string("config_path", None, "The path to config.json.")
flags.DEFINE_string("user_id_list", None, "The path to user_id_list.txt.")
flags.DEFINE_string("output_dir", None, "The dir path to store results.")


class Spider:
    def __init__(self, config):
        """Weibo类初始化"""
        self.filter = config[
            "filter"]  # 取值范围为0、1,程序默认值为0,代表要爬取用户的全部微博,1代表只爬取用户的原创微博
        since_date = str(config["since_date"])
        if since_date.isdigit():
            since_date = str(date.today() - timedelta(int(since_date)))
        self.since_date = since_date  # 起始时间，即爬取发布日期从该值到现在的微博，形式为yyyy-mm-dd
        self.write_mode = config[
            "write_mode"]  # 结果信息保存类型，为list形式，可包含txt、csv、json、mongo和mysql五种类型
        self.pic_download = config[
            "pic_download"]  # 取值范围为0、1,程序默认值为0,代表不下载微博原始图片,1代表下载
        self.video_download = config[
            "video_download"]  # 取值范围为0、1,程序默认为0,代表不下载微博视频,1代表下载
        self.cookie = {"Cookie": config["cookie"]}
        self.mysql_config = config.get("mysql_config")  # MySQL数据库连接配置，可以不填
        user_id_list = config["user_id_list"]
        if not isinstance(user_id_list, list):
            if FLAGS.user_id_list is not None:
                user_id_list = FLAGS.user_id_list
            else:
                user_id_list = os.getcwd() + os.sep + user_id_list
            if not os.path.isfile(user_id_list):
                sys.exit(u"当前路径：%s 不存在配置文件config.json" % user_id_list)
            self.user_config_file_path = user_id_list  # 用户配置文件路径
            user_config_list = config_util.get_user_config_list(
                user_id_list, self.since_date)
        else:
            self.user_config_file_path = ""
            user_config_list = [{
                "user_uri": user_id,
                "since_date": self.since_date
            } for user_id in user_id_list]
        self.user_config_list = user_config_list  # 要爬取的微博用户的user_config列表
        self.user_config = {}  # 用户配置,包含用户id和since_date
        self.start_time = ""  # 获取用户第一条微博时的时间
        self.user = {}  # 存储爬取到的用户信息
        self.got_num = 0  # 存储爬取到的微博数
        self.weibo = []  # 存储爬取到的所有微博信息
        self.weibo_id_list = []  # 存储爬取到的所有微博id

    def write_weibo(self, weibos):
        """将爬取到的信息写入文件或数据库"""
        for writer in self.writers:
            writer.write_weibo(weibos)
        for downloader in self.downloaders:
            downloader.download_files(weibos)

    def write_user(self, user):
        """将用户信息写入数据库"""
        for writer in self.writers:
            writer.write_user(user)

    def get_user_info(self, user_uri):
        # 获取用户信息、微博数、关注数、粉丝数
        self.user = {}
        user = IndexParser(self.cookie, user_uri).get_user()
        for k, v in user.items():
            self.user[k] = v

    def get_weibo_info(self):
        """获取微博信息"""
        try:
            since_date = datetime_util.str_to_time(
                self.user_config["since_date"])
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            now = datetime.strptime(now, "%Y-%m-%d %H:%M")
            if since_date <= now:
                page_num = IndexParser(
                    self.cookie,
                    self.user_config["user_uri"]).get_page_num()  # 获取微博总页数
                page1 = 0
                random_pages = random.randint(1, 5)
                self.start_time = datetime.now().strftime("%Y-%m-%d %H:%M")
                for page in tqdm(range(1, page_num + 1), desc="Progress"):
                    weibos, self.weibo_id_list = PageParser(
                        self.cookie, self.user_config["user_uri"],
                        page, self.filter).get_one_page(
                            self.since_date,
                            self.weibo_id_list)  # 获取第page页的全部微博
                    print(u"{}已获取{}({})的第{}页微博{}".format(
                        "-" * 30,
                        self.user["nickname"],
                        self.user["id"],
                        page,
                        "-" * 30,
                    ))
                    if weibos:
                        yield weibos
                    else:
                        return weibos

                    # 通过加入随机等待避免被限制。爬虫速度过快容易被系统限制(一段时间后限
                    # 制会自动解除)，加入随机等待模拟人的操作，可降低被系统限制的风险。默
                    # 认是每爬取1到5页随机等待6到10秒，如果仍然被限，可适当增加sleep时间
                    if (page - page1) % random_pages == 0 and page < page_num:
                        sleep(random.randint(6, 10))
                        page1 = page
                        random_pages = random.randint(1, 5)
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

    def _get_filepath(self, type):
        """获取结果文件路径"""
        try:
            if FLAGS.output_dir is not None:
                file_dir = FLAGS.output_dir
            else:
                file_dir = (os.getcwd() + os.sep + "weibo" + os.sep +
                            self.user["nickname"])
            if type == "img" or type == "video":
                file_dir = file_dir + os.sep + type
            if not os.path.isdir(file_dir):
                os.makedirs(file_dir)
            if type == "img" or type == "video":
                return file_dir
            file_path = file_dir + os.sep + self.user["id"] + "." + type
            return file_path
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

    def initialize_info(self, user_config):
        """初始化爬虫信息"""
        self.got_num = 0
        self.weibo = []
        self.user_config = user_config
        self.weibo_id_list = []

        self.writers = []
        if "csv" in self.write_mode:
            from .writer import CsvWriter

            self.writers.append(
                CsvWriter(self.filter, self._get_filepath("csv")))
        if "txt" in self.write_mode:
            from .writer import TxtWriter

            self.writers.append(
                TxtWriter(self.filter, self._get_filepath("txt")))
        if "json" in self.write_mode:
            from .writer import JsonWriter

            self.writers.append(JsonWriter(self._get_filepath("json")))
        if "mysql" in self.write_mode:
            from .writer import MySqlWriter

            self.writers.append(MySqlWriter(self.mysql_config))
        if "mongo" in self.write_mode:
            from .writer import MongoWriter

            self.writers.append(MongoWriter())

        self.downloaders = []
        if self.pic_download == 1:
            from .downloader import ImgDownloader

            self.downloaders.append(ImgDownloader(self._get_filepath("img")))
        if self.video_download == 1:
            from .downloader import VideoDownloader

            self.downloaders.append(
                VideoDownloader(self._get_filepath("video")))

    def start(self):
        """运行爬虫"""
        try:
            for user_config in self.user_config_list:
                self.get_user_info(user_config["user_uri"])
                printer.print_user_info(self.user)
                print("*" * 100)

                self.initialize_info(user_config)
                self.write_user(self.user)
                print("*" * 100)

                for weibos in self.get_weibo_info():
                    self.write_weibo(weibos)
                    self.got_num += len(weibos)
                if not self.filter:
                    print(u"共爬取" + str(self.got_num) + u"条微博")
                else:
                    print(u"共爬取" + str(self.got_num) + u"条原创微博")
                print(u"信息抓取完毕")
                print("*" * 100)

                if self.user_config_file_path:
                    config_util.update_user_config_file(
                        self.user_config_file_path,
                        self.user_config["user_uri"],
                        self.user["nickname"],
                        self.start_time,
                    )
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()


def _get_config():
    """获取config.json数据"""
    src = os.path.split(
        os.path.realpath(__file__))[0] + os.sep + 'config_sample.json'
    config_path = os.getcwd() + os.sep + 'config.json'
    if FLAGS.config_path:
        config_path = FLAGS.config_path
    elif not os.path.isfile(config_path):
        shutil.copy(src, config_path)
        sys.exit(u'请先配置当前目录(%s)下的config.json文件，'
                 u'如果想了解config.json参数的具体意义及配置方法，请访问\n'
                 u'https://github.com/dataabc/weiboSpider#2程序设置' % os.getcwd())
    try:
        with open(config_path) as f:
            config = json.loads(f.read())
            return config
    except ValueError:
        sys.exit(u'config.json 格式不正确，请访问 '
                 u'https://github.com/dataabc/weiboSpider#2程序设置')


def main(_):
    try:
        config = _get_config()
        wb = Spider(config)
        wb.start()  # 爬取微博信息
    except Exception as e:
        print("Error: ", e)
        traceback.print_exc()


if __name__ == "__main__":
    app.run(main)
