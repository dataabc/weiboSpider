import copy
import logging
import sys

from .writer import Writer

logger = logging.getLogger('spider.mysql_writer')


class MySqlWriter(Writer):
    def __init__(self, mysql_config):
        self.mysql_config = mysql_config

        # 创建'weibo'数据库
        create_database = """CREATE DATABASE IF NOT EXISTS weibo DEFAULT
                            CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"""
        self._mysql_create_database(create_database)
        self.mysql_config['db'] = 'weibo'

    def _mysql_create(self, connection, sql):
        """创建MySQL数据库或表"""
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql)
        finally:
            connection.close()

    def _mysql_create_database(self, sql):
        """创建MySQL数据库"""
        try:
            import pymysql
        except ImportError:
            logger.warning(
                u'系统中可能没有安装pymysql库，请先运行 pip install pymysql ，再运行程序')
            sys.exit()
        try:
            connection = pymysql.connect(**self.mysql_config)
            self._mysql_create(connection, sql)
        except pymysql.OperationalError:
            logger.warning(u'系统中可能没有安装或正确配置MySQL数据库，请先根据系统环境安装或配置MySQL，再运行程序')
            sys.exit()

    def _mysql_create_table(self, sql):
        """创建MySQL表"""
        import pymysql
        connection = pymysql.connect(**self.mysql_config)
        self._mysql_create(connection, sql)

    def _mysql_insert(self, table, data_list):
        """向MySQL表插入或更新数据"""
        import pymysql
        if len(data_list) > 0:
            # We use this to filter out unset values.
            data_list = [{k: v
                          for k, v in data.items() if v is not None}
                         for data in data_list]

            keys = ', '.join(data_list[0].keys())
            values = ', '.join(['%s'] * len(data_list[0]))
            connection = pymysql.connect(**self.mysql_config)
            cursor = connection.cursor()
            sql = """INSERT INTO {table}({keys}) VALUES ({values}) ON
                        DUPLICATE KEY UPDATE""".format(table=table,
                                                       keys=keys,
                                                       values=values)
            update = ','.join([
                ' {key} = values({key})'.format(key=key)
                for key in data_list[0]
            ])
            sql += update
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
        """将爬取的微博信息写入MySQL数据库"""
        # 创建'weibo'表
        create_table = """
                CREATE TABLE IF NOT EXISTS weibo (
                id varchar(10) NOT NULL,
                user_id varchar(12),
                content varchar(5000),
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
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"""
        self._mysql_create_table(create_table)
        # 在'weibo'表中插入或更新微博数据
        weibo_list = []
        info_list = copy.deepcopy(weibos)
        for weibo in info_list:
            weibo.user_id = self.user.id
            weibo_list.append(weibo.__dict__)
        self._mysql_insert('weibo', weibo_list)
        logger.info(u'%d条微博写入MySQL数据库完毕', len(weibos))

    def write_user(self, user):
        """将爬取的用户信息写入MySQL数据库"""
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
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"""
        self._mysql_create_table(create_table)
        self._mysql_insert('user', [user.__dict__])
        logger.info(u'%s信息写入MySQL数据库完毕', user.nickname)
