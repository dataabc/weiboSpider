# -*- coding: UTF-8 -*-
import os
import sys
import traceback

from abc import ABC, abstractmethod
import requests
from requests.adapters import HTTPAdapter
from tqdm import tqdm


class Downloader(ABC):
    def __init__(self, file_dir):
        self.file_dir = file_dir

        self.file_type = ""
        self.describe = u""
        self.key = ""

    @abstractmethod
    def handle_download(self, urls, w):
        """下载 urls 里所指向的图片或视频文件，使用 w 里的信息来生成文件名"""
        pass

    def get_filepath(self):
        """获取结果文件路径"""
        try:
            file_dir = self.file_dir + os.sep + self.file_type
            if not os.path.isdir(file_dir):
                os.makedirs(file_dir)
            return file_dir
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

    def download_one_file(self, url, file_path, weibo_id):
        """下载单个文件(图片/视频)"""
        try:
            if not os.path.isfile(file_path):
                s = requests.Session()
                s.mount(url, HTTPAdapter(max_retries=5))
                downloaded = s.get(url, timeout=(5, 10))
                with open(file_path, "wb") as f:
                    f.write(downloaded.content)
        except Exception as e:
            error_file = self.get_filepath() + os.sep + "not_downloaded.txt"
            with open(error_file, "ab") as f:
                url = weibo_id + ":" + url + "\n"
                f.write(url.encode(sys.stdout.encoding))
            print("Error: ", e)
            traceback.print_exc()

    def download_files(self, weibos):
        """下载文件(图片/视频)"""
        try:
            print(u"即将进行%s下载" % self.describe)
            for w in tqdm(weibos, desc="Download progress"):
                if getattr(w, self.key) != u"无":
                    self.handle_download(getattr(w, self.key), w)
            print(u"%s下载完毕,保存路径:" % self.describe)
            print(self.file_dir)
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()
