#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import json
import logging
import logging.config
import os
import random
import shutil
import sys
from datetime import date, datetime, timedelta
from time import sleep

from absl import app, flags
from tqdm import tqdm

from . import config_util, datetime_util
from .parser import IndexParser, PageParser
from .user import User

FLAGS = flags.FLAGS

flags.DEFINE_string('config_path', None, 'The path to config.json.')
flags.DEFINE_string('u', None, 'The user_id we want to input.')
flags.DEFINE_string('user_id_list', None, 'The path to user_id_list.txt.')
flags.DEFINE_string('output_dir', None, 'The dir path to store results.')

logging_path = os.path.split(
    os.path.realpath(__file__))[0] + os.sep + 'logging.conf'
logging.config.fileConfig(logging_path)
logger = logging.getLogger('spider')


class Spider:
    def __init__(self, config):
        """Weibo类初始化"""
        self.filter = config[
            'filter']  # 取值范围为0、1,程序默认值为0,代表要爬取用户的全部微博,1代表只爬取用户的原创微博
        since_date = config['since_date']
        if isinstance(since_date, int):
            since_date = date.today() - timedelta(since_date)
        self.since_date = str(
            since_date)  # 起始时间，即爬取发布日期从该值到结束时间的微博，形式为yyyy-mm-dd
        self.end_date = config[
            'end_date']  # 结束时间，即爬取发布日期从起始时间到该值的微博，形式为yyyy-mm-dd，特殊值"now"代表现在
        random_wait_pages = config['random_wait_pages']
        self.random_wait_pages = [
            min(random_wait_pages),
            max(random_wait_pages)
        ]  # 随机等待频率，即每爬多少页暂停一次
        random_wait_seconds = config['random_wait_seconds']
        self.random_wait_seconds = [
            min(random_wait_seconds),
            max(random_wait_seconds)
        ]  # 随机等待时间，即每次暂停要sleep多少秒
        self.global_wait = config['global_wait']  # 配置全局等待时间，如每爬1000页等待3600秒等
        self.page_count = 0  # 统计每次全局等待后，爬取了多少页，若页数满足全局等待要求就进入下一次全局等待
        self.write_mode = config[
            'write_mode']  # 结果信息保存类型，为list形式，可包含txt、csv、json、mongo和mysql五种类型
        self.pic_download = config[
            'pic_download']  # 取值范围为0、1,程序默认值为0,代表不下载微博原始图片,1代表下载
        self.video_download = config[
            'video_download']  # 取值范围为0、1,程序默认为0,代表不下载微博视频,1代表下载
        self.cookie = {'Cookie': config['cookie']}
        self.mysql_config = config.get('mysql_config')  # MySQL数据库连接配置，可以不填

        self.sqlite_config = config.get('sqlite_config')

        self.user_config_file_path = ''
        user_id_list = config['user_id_list']
        if FLAGS.user_id_list:
            user_id_list = FLAGS.user_id_list
        if not isinstance(user_id_list, list):
            if not os.path.isabs(user_id_list):
                user_id_list = os.getcwd() + os.sep + user_id_list
            if not os.path.isfile(user_id_list):
                logger.warning('不存在%s文件', user_id_list)
                sys.exit()
            self.user_config_file_path = user_id_list
        if FLAGS.u:
            user_id_list = FLAGS.u.split(',')
        if isinstance(user_id_list, list):
            user_id_list = list(set(user_id_list))
            user_config_list = [{
                'user_uri': user_id,
                'since_date': self.since_date,
                'end_date': self.end_date
            } for user_id in user_id_list]
            if FLAGS.u:
                config_util.add_user_uri_list(self.user_config_file_path,
                                              user_id_list)
        else:
            user_config_list = config_util.get_user_config_list(
                user_id_list, self.since_date)
            for user_config in user_config_list:
                user_config['end_date'] = self.end_date
        self.user_config_list = user_config_list  # 要爬取的微博用户的user_config列表
        self.user_config = {}  # 用户配置,包含用户id和since_date
        self.new_since_date = ''  # 完成某用户爬取后，自动生成对应用户新的since_date
        self.user = User()  # 存储爬取到的用户信息
        self.got_num = 0  # 存储爬取到的微博数
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
        """获取用户信息"""
        self.user = IndexParser(self.cookie, user_uri).get_user()
        self.page_count += 1

    def get_weibo_info(self):
        """获取微博信息"""
        try:
            since_date = datetime_util.str_to_time(
                self.user_config['since_date'])
            now = datetime.now()
            if since_date <= now:
                page_num = IndexParser(
                    self.cookie,
                    self.user_config['user_uri']).get_page_num()  # 获取微博总页数
                self.page_count += 1
                if self.page_count > 2 and (self.page_count +
                                            page_num) > self.global_wait[0][0]:
                    wait_seconds = int(
                        self.global_wait[0][1] *
                        min(1, self.page_count / self.global_wait[0][0]))
                    logger.info(u'即将进入全局等待时间，%d秒后程序继续执行' % wait_seconds)
                    for i in tqdm(range(wait_seconds)):
                        sleep(1)
                    self.page_count = 0
                    self.global_wait.append(self.global_wait.pop(0))
                page1 = 0
                random_pages = random.randint(*self.random_wait_pages)
                for page in tqdm(range(1, page_num + 1), desc='Progress'):
                    weibos, self.weibo_id_list, to_continue = PageParser(
                        self.cookie,
                        self.user_config, page, self.filter).get_one_page(
                            self.weibo_id_list)  # 获取第page页的全部微博
                    logger.info(
                        u'%s已获取%s(%s)的第%d页微博%s',
                        '-' * 30,
                        self.user.nickname,
                        self.user.id,
                        page,
                        '-' * 30,
                    )
                    self.page_count += 1
                    if weibos:
                        yield weibos
                    if not to_continue:
                        break

                    # 通过加入随机等待避免被限制。爬虫速度过快容易被系统限制(一段时间后限
                    # 制会自动解除)，加入随机等待模拟人的操作，可降低被系统限制的风险。默
                    # 认是每爬取1到5页随机等待6到10秒，如果仍然被限，可适当增加sleep时间
                    if (page - page1) % random_pages == 0 and page < page_num:
                        sleep(random.randint(*self.random_wait_seconds))
                        page1 = page
                        random_pages = random.randint(*self.random_wait_pages)

                    if self.page_count >= self.global_wait[0][0]:
                        logger.info(u'即将进入全局等待时间，%d秒后程序继续执行' %
                                    self.global_wait[0][1])
                        for i in tqdm(range(self.global_wait[0][1])):
                            sleep(1)
                        self.page_count = 0
                        self.global_wait.append(self.global_wait.pop(0))
        except Exception as e:
            logger.exception(e)

    def _get_filepath(self, type):
        """获取结果文件路径"""
        try:
            if FLAGS.output_dir is not None:
                file_dir = FLAGS.output_dir + os.sep + self.user.nickname
            else:
                file_dir = (os.getcwd() + os.sep + 'weibo' + os.sep +
                            self.user.nickname)
            if type == 'img' or type == 'video':
                file_dir = file_dir + os.sep + type
            if not os.path.isdir(file_dir):
                os.makedirs(file_dir)
            if type == 'img' or type == 'video':
                return file_dir
            file_path = file_dir + os.sep + self.user.id + '.' + type
            return file_path
        except Exception as e:
            logger.exception(e)

    def initialize_info(self, user_config):
        """初始化爬虫信息"""
        self.got_num = 0
        self.user_config = user_config
        self.weibo_id_list = []
        if self.end_date == 'now':
            self.new_since_date = datetime.now().strftime('%Y-%m-%d %H:%M')
        else:
            self.new_since_date = self.end_date
        self.writers = []
        if 'csv' in self.write_mode:
            from .writer import CsvWriter

            self.writers.append(
                CsvWriter(self._get_filepath('csv'), self.filter))
        if 'txt' in self.write_mode:
            from .writer import TxtWriter

            self.writers.append(
                TxtWriter(self._get_filepath('txt'), self.filter))
        if 'json' in self.write_mode:
            from .writer import JsonWriter

            self.writers.append(JsonWriter(self._get_filepath('json')))
        if 'mysql' in self.write_mode:
            from .writer import MySqlWriter

            self.writers.append(MySqlWriter(self.mysql_config))
        if 'mongo' in self.write_mode:
            from .writer import MongoWriter

            self.writers.append(MongoWriter())
        if 'sqlite' in self.write_mode:
            from .writer import SqliteWriter

            self.writers.append(SqliteWriter(self.sqlite_config))

        self.downloaders = []
        if self.pic_download == 1:
            from .downloader import ImgDownloader

            self.downloaders.append(ImgDownloader(self._get_filepath('img')))
        if self.video_download == 1:
            from .downloader import VideoDownloader

            self.downloaders.append(
                VideoDownloader(self._get_filepath('video')))

    def start(self):
        """运行爬虫"""
        try:
            if not self.user_config_list:
                logger.info(
                    u'没有配置有效的user_id，请通过config.json或user_id_list.txt配置user_id')
                return
            user_count = 0
            user_count1 = random.randint(*self.random_wait_pages)
            random_users = random.randint(*self.random_wait_pages)
            for user_config in self.user_config_list:
                if (user_count - user_count1) % random_users == 0:
                    sleep(random.randint(*self.random_wait_seconds))
                    user_count1 = user_count
                    random_users = random.randint(*self.random_wait_pages)
                user_count += 1
                self.get_user_info(user_config['user_uri'])
                logger.info(self.user)
                logger.info('*' * 100)

                self.initialize_info(user_config)
                self.write_user(self.user)
                logger.info('*' * 100)

                for weibos in self.get_weibo_info():
                    self.write_weibo(weibos)
                    self.got_num += len(weibos)
                if not self.filter:
                    logger.info(u'共爬取' + str(self.got_num) + u'条微博')
                else:
                    logger.info(u'共爬取' + str(self.got_num) + u'条原创微博')
                logger.info(u'信息抓取完毕')
                logger.info('*' * 100)

                if self.user_config_file_path or FLAGS.u:
                    config_util.update_user_config_file(
                        self.user_config_file_path,
                        self.user_config['user_uri'],
                        self.user.nickname,
                        self.new_since_date,
                    )
        except Exception as e:
            logger.exception(e)


def _get_config():
    """获取config.json数据"""
    src = os.path.split(
        os.path.realpath(__file__))[0] + os.sep + 'config_sample.json'
    config_path = os.getcwd() + os.sep + 'config.json'
    if FLAGS.config_path:
        config_path = FLAGS.config_path
    elif not os.path.isfile(config_path):
        shutil.copy(src, config_path)
        logger.info(u'请先配置当前目录(%s)下的config.json文件，'
                    u'如果想了解config.json参数的具体意义及配置方法，请访问\n'
                    u'https://github.com/dataabc/weiboSpider#2程序设置' %
                    os.getcwd())
        sys.exit()
    try:
        with open(config_path) as f:
            config = json.loads(f.read())
            return config
    except ValueError:
        logger.error(u'config.json 格式不正确，请访问 '
                     u'https://github.com/dataabc/weiboSpider#2程序设置')
        sys.exit()


def main(_):
    try:
        config = _get_config()
        config_util.validate_config(config)
        wb = Spider(config)
        wb.start()  # 爬取微博信息
    except Exception as e:
        logger.exception(e)


if __name__ == '__main__':
    app.run(main)
