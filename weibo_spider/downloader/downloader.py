# -*- coding: UTF-8 -*-
import logging
import os
import sys
from abc import ABC, abstractmethod

import requests
from requests.adapters import HTTPAdapter
from tqdm import tqdm

logger = logging.getLogger('spider.downloader')


class Downloader(ABC):
    def __init__(self, file_dir):
        self.file_dir = file_dir
        self.describe = u''
        self.key = ''

    @abstractmethod
    def handle_download(self, urls, w):
        """下载 urls 里所指向的图片或视频文件，使用 w 里的信息来生成文件名"""
        pass

    def download_one_file(self, url, file_path, weibo_id):
        """下载单个文件(图片/视频)"""
        try:
            if not os.path.isfile(file_path):
                s = requests.Session()
                s.mount(url, HTTPAdapter(max_retries=5))
                downloaded = s.get(url, timeout=(5, 10))
                with open(file_path, 'wb') as f:
                    f.write(downloaded.content)
        except Exception as e:
            error_file = self.file_dir + os.sep + 'not_downloaded.txt'
            with open(error_file, 'ab') as f:
                url = weibo_id + ':' + file_path + ':' + url + '\n'
                f.write(url.encode(sys.stdout.encoding))
            logger.exception(e)

    def download_files(self, weibos):
        """下载文件(图片/视频)"""
        try:
            logger.info(u'即将进行%s下载', self.describe)
            for w in tqdm(weibos, desc='Download progress'):
                if getattr(w, self.key) != u'无':
                    self.handle_download(getattr(w, self.key), w)
            logger.info(u'%s下载完毕,保存路径:', self.describe)
            logger.info(self.file_dir)
        except Exception as e:
            logger.exception(e)
