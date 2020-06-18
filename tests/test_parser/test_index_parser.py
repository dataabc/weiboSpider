from unittest.mock import patch

from .util import mock_request_get_content
from weibo_spider.parser.index_parser import IndexParser


@patch('requests.get', mock_request_get_content)
def test_index_parser():
    index_parser = IndexParser(cookie="", user_uri="1669879400")
    assert (index_parser.get_page_num() == 117)
    assert (str(index_parser.get_user()) == """用户昵称: Dear-迪丽热巴\n"""
            """用户id: 1669879400\n"""
            """微博数: 1159\n"""
            """关注数: 253\n"""
            """粉丝数: 70805574\n""")
