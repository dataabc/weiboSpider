import logging
import random
import requests
import re
from time import sleep
from lxml.html import tostring
from lxml.html import fromstring
from lxml import etree
from .parser import Parser
from .util import handle_garbled, handle_html

logger = logging.getLogger('spider.comment_parser')


class CommentParser(Parser):
    def __init__(self, cookie, weibo_id):
        self.cookie = cookie
        self.url = 'https://weibo.cn/comment/' + weibo_id
        self.selector = handle_html(self.cookie, self.url)

    def get_long_weibo(self):
        """获取长原创微博"""
        try:
            for i in range(5):
                self.selector = handle_html(self.cookie, self.url)
                if self.selector is not None:
                    info_div = self.selector.xpath("//div[@class='c' and @id='M_']")[0]
                    info_span = info_div.xpath("//span[@class='ctt']")[0]
                    # 1. 获取 info_span 中的所有 HTML 代码作为字符串
                    html_string = etree.tostring(info_span, encoding='unicode', method='html')
                    # 2. 将 <br> 替换为 \n
                    html_string = html_string.replace('<br>', '\n')
                    # 3. 去掉所有 HTML 标签，但保留标签内的有效文本
                    new_content = fromstring(html_string).text_content()
                    # 4. 替换多个连续的 \n 为一个 \n
                    new_content = re.sub(r'\n+\s*', '\n', new_content)
                    weibo_content = handle_garbled(new_content)
                    if weibo_content is not None:
                        return weibo_content
                sleep(random.randint(6, 10))
        except Exception:
            logger.exception(u'网络出错')

    def get_long_retweet(self):
        """获取长转发微博"""
        try:
            wb_content = self.get_long_weibo()
            weibo_content = wb_content[:wb_content.rfind(u'原文转发')]
            return weibo_content
        except Exception as e:
            logger.exception(e)

    def get_video_page_url(self):
        """获取微博视频页面的链接"""
        video_url = ''
        try:
            self.selector = handle_html(self.cookie, self.url)
            if self.selector is not None:
                # 来自微博视频号的格式与普通格式不一致，不加 span 层级
                links = self.selector.xpath("body/div[@class='c' and @id][1]/div//a")
                for a in links:
                    if 'm.weibo.cn/s/video/show?object_id=' in a.xpath(
                            '@href')[0]:
                        video_url = a.xpath('@href')[0]
                        break
        except Exception:
            logger.exception(u'网络出错')

        return video_url
