from unittest.mock import patch

from .util import mock_request_get_content
from weibo_spider.parser.info_parser import InfoParser


@patch('requests.get', mock_request_get_content)
def test_info_parser():
    info_parser = InfoParser(cookie="", user_id="1669879400")
    user = info_parser.extract_user_info()
    # With info_parser, we can only get the nickname.
    assert (user.nickname == "Dear-迪丽热巴")
