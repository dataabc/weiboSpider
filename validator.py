from datetime import datetime
import sys

class Validator:
    def __init__(self, config):
        """
        self.user_id = ''  # 用户id,如昵称为"Dear-迪丽热巴"的id为'1669879400'
        self.filter = filter  # 取值范围为0、1,程序默认值为0,代表要爬取用户的全部微博,1代表只爬取用户的原创微博
        self.since_date = since_date  # 起始时间，即爬取发布日期从该值到现在的微博，形式为yyyy-mm-dd
        self.mongodb_write = mongodb_write  # 值为0代表不将结果写入MongoDB数据库,1代表写入
        self.mysql_write = mysql_write  # 值为0代表不将结果写入MySQL数据库,1代表写入
        self.pic_download = pic_download  # 取值范围为0、1,程序默认值为0,代表不下载微博原始图片,1代表下载
        self.video_download = video_download  # 取值范围为0、1,程序默认为0,代表不下载微博视频,1代表下载
        self.mysql_config = {
        }  # MySQL数据库连接配置，可以不填，当使用者的mysql用户名、密码等与本程序默认值不同时，需要通过mysql_config来自定义
        """
        self.config = config

    def validate(self):
        bool_config = ["filter", "pic_download", "video_download"]
        date_config = ["since_date"]

        for key in bool_config:
            if self.config[key] not in [0, 1]:
                sys.exit(f"{key}值应为0或1,请重新输入")
        for key in date_config:
            if not self.is_date(self.config[key]):
                sys.exit(f"{key}值应为yyyy-mm-dd形式,请重新输入")
        for mode in self.config['write_mode']:
            if mode not in ['txt', 'csv', 'mysql', 'mongo']:
                sys.exit("write_mode值应为txt,csv,mysql,mongo,请重新输入")

    def is_date(self, since_date):
        """判断日期格式是否正确"""
        try:
            datetime.strptime(since_date, "%Y-%m-%d")
            return True
        except ValueError:
            return False
