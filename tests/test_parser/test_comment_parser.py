from unittest.mock import patch

from .util import mock_request_get_content
from weibo_spider.parser.comment_parser import CommentParser


@patch('requests.get', mock_request_get_content)
def test_comment_parser():
    comment_parser = CommentParser(cookie="", weibo_id="J5cVGuUNq")
    long_weibo = comment_parser.get_long_weibo()
    long_retweet = comment_parser.get_long_retweet()
    assert (
        long_retweet == """去年和亲善大使热巴@Dear-迪丽热巴 的特别回忆。"""
        """我们在藏北羌塘一起爬山，探访藏羚羊、雪豹、黑颈鹤的栖息地，感受野生动物保护工作的点滴。"""
        """此时此刻，我们比以往更加重视与自然相处的方式，我们也从未如此迫切需要将想法付诸行动。"""
        """热巴已经和我们@北京绿色阳光 站在一起，希望看完视频的你们，也能获得同样感受与动力。"""
        """We Stand for Wildlife.  明日朝阳68309的优酷视频                    \xa0""")
    assert (
        long_weibo == """去年和亲善大使热巴@Dear-迪丽热巴 的特别回忆。"""
        """我们在藏北羌塘一起爬山，探访藏羚羊、雪豹、黑颈鹤的栖息地，感受野生动物保护工作的点滴。"""
        """此时此刻，我们比以往更加重视与自然相处的方式，我们也从未如此迫切需要将想法付诸行动。"""
        """热巴已经和我们@北京绿色阳光 站在一起，希望看完视频的你们，也能获得同样感受与动力。"""
        """We Stand for Wildlife.  明日朝阳68309的优酷视频                    \xa0"""
        """原文转发[1000000]    \xa0原文评论[38688]        转发理由:    在羌塘的美好回忆～"""
        """第一次来到这片独特的荒野，看到野生动物自由生活，还有一群快乐可爱的人在守护着它们。"""
        """把这些美好留存下来，关注野生动物保护，积极行动，我们每个人都能贡献力量。                \xa0    """)
