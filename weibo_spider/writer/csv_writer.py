import csv
import logging

from .writer import Writer

logger = logging.getLogger('spider.csv_writer')


class CsvWriter(Writer):
    def __init__(self, file_path, filter):
        self.file_path = file_path

        self.result_headers = [('微博id', 'id'), ('微博正文', 'content'),
                               ('头条文章url', 'article_url'),
                               ('原始图片url', 'original_pictures'),
                               ('微博视频url', 'video_url'),
                               ('发布位置', 'publish_place'),
                               ('发布时间', 'publish_time'),
                               ('发布工具', 'publish_tool'), ('点赞数', 'up_num'),
                               ('转发数', 'retweet_num'), ('评论数', 'comment_num')]
        if not filter:
            self.result_headers.insert(4, ('被转发微博原始图片url', 'retweet_pictures'))
            self.result_headers.insert(5, ('是否为原创微博', 'original'))
        try:
            with open(self.file_path, 'a', encoding='utf-8-sig',
                      newline='') as f:
                writer = csv.writer(f)
                writer.writerows([[kv[0] for kv in self.result_headers]])
        except Exception as e:
            logger.exception(e)

    def write_user(self, user):
        self.user = user

    def write_weibo(self, weibos):
        """将爬取的信息写入csv文件"""
        try:
            result_data = [[w.__dict__[kv[1]] for kv in self.result_headers]
                           for w in weibos]
            with open(self.file_path, 'a', encoding='utf-8-sig',
                      newline='') as f:
                writer = csv.writer(f)
                writer.writerows(result_data)
            logger.info(u'%d条微博写入csv文件完毕，保存路径：%s', len(weibos), self.file_path)
        except Exception as e:
            logger.exception(e)
