from unittest.mock import patch

from .util import mock_request_get_content
from weibo_spider.parser.album_parser import AlbumParser


@patch('requests.get', mock_request_get_content)
def test_album_parser():
    album_parser = AlbumParser(
        cookie="",
        album_url="https://weibo.cn/album/166564740000001980768563?rl=1")

    pic_urls = album_parser.extract_pic_urls()
    assert (len(pic_urls) == 4)
    assert (pic_urls == [
        'http://wx1.sinaimg.cn/wap180/76102133ly8ga961tpte6j20u00u0q65.jpg',
        'http://wx2.sinaimg.cn/wap180/76102133ly8fwr33wpn8fj20v90v9tbw.jpg',
        'http://wx4.sinaimg.cn/wap180/76102133ly8fvlyn5n52gj20v90v949a.jpg',
        'http://wx2.sinaimg.cn/wap180/76102133ly8fk0btnrn5zj20dp0e8q3t.jpg'
    ])
