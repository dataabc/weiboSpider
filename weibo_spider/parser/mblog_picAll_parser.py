from .parser import Parser
from .util import handle_html


class MblogPicAllParser(Parser):
    def __init__(self, cookie, weibo_id):
        self.cookie = cookie
        self.url = 'https://weibo.cn/mblog/picAll/' + weibo_id + '?rl=1'
        self.selector = handle_html(self.cookie, self.url)

    def extract_preview_picture_list(self):
        return self.selector.xpath('//img/@src')
