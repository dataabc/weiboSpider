from .util import handle_html
from .parser import Parser


class AlbumParser(Parser):
    def __init__(self, cookie, album_url):
        self.cookie = cookie
        self.url = album_url
        self.selector = handle_html(self.cookie, self.url)

    def extract_pic_urls(self):
        # <img src="http://wx2.sinaimg.cn/wap180/76102133ly8fwr33wpn8fj20v90v9tbw.jpg" alt="" class="c">
        return self.selector.xpath('//img[@class="c"]/@src')