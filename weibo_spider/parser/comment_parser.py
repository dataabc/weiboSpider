import random
import traceback
from time import sleep

from weibo_spider.parser.parser import Parser
from weibo_spider.parser.util import handle_html, handle_garbled


class CommentParser(Parser):
    def __init__(self, cookie, weibo_id):
        self.cookie = cookie
        self.url = "https://weibo.cn/comment/" + weibo_id
        self.selector = handle_html(self.cookie, self.url)

    def get_long_weibo(self):
        """获取长原创微博"""
        try:
            for i in range(5):
                self.selector = handle_html(self.cookie, self.url)
                if self.selector is not None:
                    info = self.selector.xpath("//div[@class='c']")[1]
                    wb_content = handle_garbled(info)
                    wb_time = info.xpath("//span[@class='ct']/text()")[0]
                    weibo_content = wb_content[wb_content.find(":") +
                                               1:wb_content.rfind(wb_time)]
                    if weibo_content is not None:
                        return weibo_content
                sleep(random.randint(6, 10))
        except Exception as e:
            return u"网络出错"
            print("Error: ", e)
            traceback.print_exc()

    def get_long_retweet(self):
        """获取长转发微博"""
        try:
            wb_content = self.get_long_weibo()
            weibo_content = wb_content[:wb_content.rfind(u"原文转发")]
            return weibo_content
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()
