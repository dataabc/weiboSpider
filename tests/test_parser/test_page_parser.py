from unittest.mock import patch

from weibo_spider.parser.page_parser import PageParser

from .util import mock_request_get_content


@patch('requests.get', mock_request_get_content)
def test_page_parser():
    user_config = {
        'user_uri': '1669879400',
        'since_date': '2020-06-01',
        'end_date': 'now'
    }
    page_parser = PageParser(cookie="",
                             user_config=user_config,
                             page=2,
                             filter=True)
    weibos, weibo_id_list, to_continue = page_parser.get_one_page([])
    assert (weibo_id_list == ['J4PGk4yMw', 'J4EUStJKu'])
    assert (len(weibos) == 2)
    assert (str(weibos[0]) == """生日动态 \xa0\n"""
            """微博发布位置：无\n"""
            """发布时间：2020-06-03 00:00\n"""
            """发布工具：生日动态\n"""
            """点赞数：1499675\n"""
            """转发数：1000000\n"""
            """评论数：1000000\n"""
            """url：https://weibo.cn/comment/J4PGk4yMw\n""")
    assert (str(weibos[1]) ==
            """#微博剧场# #周放设计淡黄的长裙# 这是一幅有声音的手稿#幸福触手可及# 绿洲 \xa0原图\xa0\n"""
            """微博发布位置：无\n"""
            """发布时间：2020-06-01 20:35\n"""
            """发布工具：绿洲APP\n"""
            """点赞数：419181\n"""
            """转发数：1000000\n"""
            """评论数：1000000\n"""
            """url：https://weibo.cn/comment/J4EUStJKu\n""")
