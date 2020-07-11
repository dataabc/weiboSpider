import logging
import sys

from .writer import Writer

logger = logging.getLogger('spider.txt_writer')


class TxtWriter(Writer):
    def __init__(self, file_path, filter):
        self.file_path = file_path

        self.user_header = u'用户信息'
        self.user_desc = [('nickname', '用户昵称'), ('id', '用户id'),
                          ('weibo_num', '微博数'), ('following', '关注数'),
                          ('followers', '粉丝数')]

        if filter:
            self.weibo_header = u'原创微博内容'
        else:
            self.weibo_header = u'微博内容'
        self.weibo_desc = [('publish_place', '微博位置'), ('publish_time', '发布时间'),
                           ('up_num', '点赞数'), ('retweet_num', '转发数'),
                           ('comment_num', '评论数'), ('publish_tool', '发布工具')]

    def write_user(self, user):
        self.user = user
        user_info = '\n'.join(
            [v + '：' + str(self.user.__dict__[k]) for k, v in self.user_desc])

        with open(self.file_path, 'ab') as f:
            f.write((self.user_header + '：\n' + user_info + '\n\n').encode(
                sys.stdout.encoding))
        logger.info(u'%s信息写入txt文件完毕，保存路径：%s', self.user.nickname,
                    self.file_path)

    def write_weibo(self, weibo):
        """将爬取的信息写入txt文件"""

        weibo_header = ''
        if self.weibo_header:
            weibo_header = self.weibo_header + '：\n'
            self.weibo_header = ''

        try:
            temp_result = []
            for w in weibo:
                temp_result.append(w.__dict__['content'] + '\n' + '\n'.join(
                    [v + '：' + str(w.__dict__[k])
                     for k, v in self.weibo_desc]))
            result = '\n\n'.join(temp_result) + '\n\n'

            with open(self.file_path, 'ab') as f:
                f.write((weibo_header + result).encode(sys.stdout.encoding))
            logger.info(u'%d条微博写入txt文件完毕，保存路径：%s', len(weibo), self.file_path)
        except Exception as e:
            logger.exception(e)
