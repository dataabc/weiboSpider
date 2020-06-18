from unittest.mock import patch, Mock
import json
import os

from weibo_spider.parser.page_parser import PageParser
from weibo_spider.parser.util import TEST_DATA_DIR, URL_MAP_FILE


def mock_request_get_content(url, cookies):
    with open(os.path.join(TEST_DATA_DIR, URL_MAP_FILE)) as f:
        url_map = json.loads(f.read())
    resp_file = url_map[url]
    mock = Mock()
    with open(resp_file, "rb") as f:
        mock.content = f.read()
    return mock


@patch('requests.get', mock_request_get_content)
def test_page_parser():
    page_parser = PageParser(cookie="",
                             user_uri="1669879400",
                             page=2,
                             filter=True)
    weibos, weibo_id_list = page_parser.get_one_page("2020-06-01", [])
    assert (weibo_id_list == ['J4PGk4yMw', 'J4EUStJKu'])
    assert (len(weibos) == 2)
    assert (str(weibos[0]) == """生日动态 \xa0\n"""
            """微博发布位置：无\n"""
            """发布时间：2020-06-03 00:00\n"""
            """发布工具：生日动态\n"""
            """点赞数：1499637\n"""
            """转发数：1000000\n"""
            """评论数：1000000\n"""
            """url：https://weibo.cn/comment/J4PGk4yMw\n""")
    assert (str(weibos[1]) ==
            """#微博剧场# #周放设计淡黄的长裙# 这是一幅有声音的手稿#幸福触手可及# 绿洲 \xa0原图\xa0\n"""
            """微博发布位置：无\n"""
            """发布时间：2020-06-01 20:35\n"""
            """发布工具：绿洲APP\n"""
            """点赞数：419172\n"""
            """转发数：1000000\n"""
            """评论数：1000000\n"""
            """url：https://weibo.cn/comment/J4EUStJKu\n""")
