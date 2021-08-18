from unittest.mock import patch

from weibo_spider.parser.photo_parser import PhotoParser

from .util import mock_request_get_content


@patch('requests.get', mock_request_get_content)
def test_photo_parser():
    photo_parser = PhotoParser(cookie="", user_id=1980768563)

    avatar_album_url = photo_parser.extract_avatar_album_url()
    assert (avatar_album_url ==
            "https://weibo.cn/album/166564740000001980768563?rl=1")
