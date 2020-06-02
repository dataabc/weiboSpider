import sys
import traceback

from .writer import Writer


class TxtWriter(Writer):
    def __init__(self, filter, file_path):
        self.filter = filter
        self.file_path = file_path

    def write_user(self, user):
        self.user = user
        if self.filter:
            result_header = u"\n\n原创微博内容: \n"
        else:
            result_header = u"\n\n微博内容: \n"
        result_header = (
            u"用户信息\n用户昵称："
            + self.user["nickname"]
            + u"\n用户id: "
            + str(self.user["id"])
            + u"\n微博数: "
            + str(self.user["weibo_num"])
            + u"\n关注数: "
            + str(self.user["following"])
            + u"\n粉丝数: "
            + str(self.user["followers"])
            + result_header
        )

        with open(self.file_path, "ab") as f:
            f.write(result_header.encode(sys.stdout.encoding))

    def write_weibo(self, weibo):
        """将爬取的信息写入txt文件"""
        try:
            temp_result = []
            for i, w in enumerate(weibo):
                temp_result.append(
                    w["content"]
                    + "\n"
                    + u"微博位置: "
                    + w["publish_place"]
                    + "\n"
                    + u"发布时间: "
                    + w["publish_time"]
                    + "\n"
                    + u"点赞数: "
                    + str(w["up_num"])
                    + u"   转发数: "
                    + str(w["retweet_num"])
                    + u"   评论数: "
                    + str(w["comment_num"])
                    + "\n"
                    + u"发布工具: "
                    + w["publish_tool"]
                    + "\n\n"
                )
            result = "".join(temp_result)
            with open(self.file_path, "ab") as f:
                f.write(result.encode(sys.stdout.encoding))
            print(u"%d条微博写入txt文件完毕,保存路径:" % len(weibo))
            print(self.file_path)
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()
