from .parser import Parser
from .util import handle_html


class PhotoParser(Parser):
    def __init__(self, cookie, user_id):
        self.cookie = cookie
        self.url = "https://weibo.cn/" + str(user_id) + "/photo?tf=6_008"
        self.selector = handle_html(self.cookie, self.url)
        self.user_id = user_id

    def extract_avatar_album_url(self):
        # Finds the href attribute of the table td div element with text 头像相册, e.g.
        # <a href="/album/166564740000001980768563?rl=1"><img width="80" height="80" src="https://tvax1.sinaimg.cn/crop.0.0.1080.1080.180/76102133ly8ga961tpte6j20u00u0q65.jpg?KID=imgbed,tva&amp;Expires=1629227741&amp;ssig=TEUDkMXcS1" alt="头像相册"></a>
        result = self.selector.xpath('//img[@alt="头像相册"]/../@href')
        if len(result) > 0:
            return "https://weibo.cn" + result[0]
        else:
            return "https://weibo.cn/" + str(self.user_id) + "/avatar?rl=0"
