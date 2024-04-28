import codecs
import json
import logging
import os
import requests

from .writer import Writer
from time import sleep
from requests.exceptions import RequestException

logger = logging.getLogger('spider.post_writer')

class PostWriter(Writer):
    def __init__(self, post_config):
        self.post_config = post_config
        self.api_url = post_config['api_url']
        self.api_token = post_config.get('api_token', None)
        self.dba_password = post_config.get('dba_password', None)

    def write_user(self, user):
        self.user = user

    def _update_json_data(self, data, weibo_info):
        """将获取到的微博数据转换为json输出模式一致"""
        data['user'] = self.user.__dict__
        if data.get('weibo'):
            data['weibo'] += weibo_info
        else:
            data['weibo'] = weibo_info
        return data

    def send_post_request_with_token(self, url, data, token, max_retries, backoff_factor):
        headers = {
            'Content-Type': 'application/json',
            'api-token': f'{token}',
        }
        for attempt in range(max_retries + 1):
            try:
                response = requests.post(url, json=data, headers=headers)
                if response.status_code == requests.codes.ok:
                    return response.json()
                else:
                    raise RequestException(f"Unexpected response status: {response.status_code}")
            except RequestException as e:
                if attempt < max_retries:
                    sleep(backoff_factor * (attempt + 1))  # 逐步增加等待时间，避免频繁重试
                    continue
                else:
                    logger.error(f"在尝试{max_retries}次发出POST连接后，请求失败：{e}")

    def write_weibo(self, weibos):
        """将爬到的信息POST到API"""
        data = {}
        data = self._update_json_data(data, [w.__dict__ for w in weibos])
        if data:
            self.send_post_request_with_token(self.api_url, data, self.api_token, 3, 2)
            logger.info(u'%d条微博通过POST发送到 %s', len(weibos), self.api_url)
        else:
            logger.info(u'没有获取到微博，略过API POST')
