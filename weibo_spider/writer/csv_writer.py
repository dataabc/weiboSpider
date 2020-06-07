import csv
import traceback

from .writer import Writer


class CsvWriter(Writer):
    def __init__(self, filter, file_path):
        self.file_path = file_path
        self.filter = filter

    def write_user(self, user):
        self.user = user

        result_headers = [
            "微博id",
            "微博正文",
            "头条文章url",
            "原始图片url",
            "微博视频url",
            "发布位置",
            "发布时间",
            "发布工具",
            "点赞数",
            "转发数",
            "评论数",
        ]
        if not self.filter:
            result_headers.insert(4, "被转发微博原始图片url")
            result_headers.insert(5, "是否为原创微博")
        try:
            with open(self.file_path, "a", encoding="utf-8-sig",
                      newline="") as f:
                writer = csv.writer(f)
                writer.writerows([result_headers])
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

    def write_weibo(self, weibos):
        """将爬取的信息写入csv文件"""
        try:
            result_data = [w.values() for w in weibos]
            with open(self.file_path, "a", encoding="utf-8-sig",
                      newline="") as f:
                writer = csv.writer(f)
                writer.writerows(result_data)
            print(u"%d条微博写入csv文件完毕,保存路径:" % len(weibos))
            print(self.file_path)
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()
