import logging
import random
from time import sleep

from .parser import Parser
from .util import handle_html, get_long_weibo_detail

logger = logging.getLogger('spider.comment_parser')


class CommentParser(Parser):
    def __init__(self, cookie, weibo_id):
        self.cookie = cookie
        self.weibo_id = weibo_id
        self.url = 'https://weibo.cn/comment/' + weibo_id

    def get_long_weibo(self):
        """获取长原创微博"""
        try:
            for i in range(5):
                weibo_content = get_long_weibo_detail(self.cookie, self.weibo_id)
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
