# -*- coding: UTF-8 -*-
import os
import sys
import traceback

import requests
from requests.adapters import HTTPAdapter
from tqdm import tqdm


class Downloader:
    def __init__(self, config):
        self.config = config

    def download_files(self, file_path, type, weibo):
        """下载文件(图片/视频)"""
        try:
            if type == 'img':
                describe = u'图片'
                key = 'original_pictures'
            else:
                describe = u'视频'
                key = 'video_url'
            print(u'即将进行%s下载' % describe)
            for w in tqdm(weibo, desc='Download progress'):
                if w[key] != u'无':
                    file_prefix = w['publish_time'][:11].replace(
                        '-', '') + '_' + w['id']
                    if type == 'img' and ',' in w[key]:
                        w[key] = w[key].split(',')
                        for j, url in enumerate(w[key]):
                            file_suffix = url[url.rfind('.'):]
                            file_name = file_prefix + '_' + str(
                                j + 1) + file_suffix
                            self.download_one_file(
                                url, file_path + os.sep + file_name, type,
                                w['id'])
                    else:
                        if type == 'video':
                            file_suffix = '.mp4'
                        else:
                            file_suffix = w[key][w[key].rfind('.'):]
                        file_name = file_prefix + file_suffix
                        self.download_one_file(w[key],
                                               file_path + os.sep + file_name,
                                               type, w['id'])
            print(u'%s下载完毕,保存路径:' % describe)
            print(file_path)
        except Exception as e:
            print('Error: ', e)
            traceback.print_exc()

    def download_one_file(self, url, file_path, type, weibo_id):
        """下载单个文件(图片/视频)"""
        try:
            if not os.path.isfile(file_path):
                s = requests.Session()
                s.mount(url, HTTPAdapter(max_retries=5))
                downloaded = s.get(url, timeout=(5, 10))
                with open(file_path, 'wb') as f:
                    f.write(downloaded.content)
        except Exception as e:
            error_file = './not_downloaded.txt'
            with open(error_file, 'ab') as f:
                url = weibo_id + ':' + url + '\n'
                f.write(url.encode(sys.stdout.encoding))
            print('Error: ', e)
            traceback.print_exc()
