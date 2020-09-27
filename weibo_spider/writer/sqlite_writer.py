import copy
import logging
import sys

from .writer import Writer

logger = logging.getLogger('spider.sqlite_writer')


class SqliteWriter(Writer):
    def __init__(self, sqlite_config):
        self.sqlite_config = sqlite_config

    def _sqlite_create(self, connection, sql):
        """创建sqlite数据库或表"""
        try:
            cursor = connection.cursor()
            cursor.execute(sql)
        finally:
            connection.close()

    def _sqlite_create_table(self, sql):
        """创建sqlite表"""
        import sqlite3
        connection = sqlite3.connect(self.sqlite_config)
        self._sqlite_create(connection, sql)

    def _sqlite_insert(self, table, data_list):
        """向sqlite表插入或更新数据"""
        import sqlite3
        if len(data_list) > 0:
            # We use this to filter out unset values.
            data_list = [{k: v
                          for k, v in data.items() if v is not None}
                         for data in data_list]

            keys = ', '.join(data_list[0].keys())
            values = ', '.join(['?'] * len(data_list[0]))
            connection = sqlite3.connect(self.sqlite_config)
            cursor = connection.cursor()
            sql = """INSERT OR REPLACE INTO {table}({keys}) VALUES ({values})""".format(
                table=table, keys=keys, values=values)
            try:
                cursor.executemany(
                    sql, [tuple(data.values()) for data in data_list])
                connection.commit()
            except Exception as e:
                connection.rollback()
                logger.exception(e)
            finally:
                connection.close()

    def write_weibo(self, weibos):
        """将爬取的微博信息写入sqlite数据库"""
        # 创建'weibo'表
        create_table = """
                CREATE TABLE IF NOT EXISTS weibo (
                id varchar(10) NOT NULL,
                user_id varchar(12),
                content varchar(2000),
                article_url varchar(200),
                original_pictures varchar(3000),
                retweet_pictures varchar(3000),
                original BOOLEAN NOT NULL DEFAULT 1,
                video_url varchar(300),
                publish_place varchar(100),
                publish_time DATETIME NOT NULL,
                publish_tool varchar(30),
                up_num INT NOT NULL,
                retweet_num INT NOT NULL,
                comment_num INT NOT NULL,
                PRIMARY KEY (id)
                )"""
        self._sqlite_create_table(create_table)
        # 在'weibo'表中插入或更新微博数据
        weibo_list = []
        info_list = copy.deepcopy(weibos)
        for weibo in info_list:
            weibo.user_id = self.user.id
            weibo_list.append(weibo.__dict__)
        self._sqlite_insert('weibo', weibo_list)
        logger.info(u'%d条微博写入sqlite数据库完毕', len(weibos))

    def write_user(self, user):
        """将爬取的用户信息写入sqlite数据库"""
        self.user = user

        # 创建'user'表
        create_table = """
                CREATE TABLE IF NOT EXISTS user (
                id varchar(20) NOT NULL,
                nickname varchar(30),
                gender varchar(10),
                location varchar(200),
                birthday varchar(40),
                description varchar(400),
                verified_reason varchar(140),
                talent varchar(200),
                education varchar(200),
                work varchar(200),
                weibo_num INT,
                following INT,
                followers INT,
                PRIMARY KEY (id)
                )"""
        self._sqlite_create_table(create_table)
        self._sqlite_insert('user', [user.__dict__])
        logger.info(u'%s信息写入sqlite数据库完毕', user.nickname)
