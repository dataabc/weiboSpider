import csv
import os
import sys
import traceback


def get_filepath(type, nickname):
    """获取结果文件路径"""
    file_dir = os.path.split(
        os.path.realpath(__file__))[0] + os.sep + 'weibo' + os.sep + nickname
    if type == 'img' or type == 'video':
        file_dir = file_dir + os.sep + type
    if not os.path.isdir(file_dir):
        os.makedirs(file_dir)
    if type == 'img' or type == 'video':
        return file_dir
    file_path = file_dir + os.sep + nickname + '.' + type
    return file_path


class Writer:
    def __init__(self, config):
        write_mode = config['write_mode']
        if write_mode == 'txt':
            self.writer = TxtWriter(config)
        elif write_mode == 'csv':
            self.writer = CsvWriter(config)
        elif write_mode == 'mysql':
            self.writer = MysqlWriter(config)
        elif write_mode == 'mongo':
            self.writer = MongoWriter(config)

    def write_user(self, user):
        self.writer.write_user(user)

    def write_weibo(self, weibo):
        self.writer.write_weibo(weibo)


class TxtWriter:
    def __init__(self, config):
        self.config = config

    def write_user(self, user):
        self.user = user
        if self.config['filter']:
            result_header = u'\n\n原创微博内容: \n'
        else:
            result_header = u'\n\n微博内容: \n'
        result_header = (u'用户信息\n用户昵称：' + user['nickname'] + u'\n用户id: ' +
                         str(user['user_id']) + u'\n微博数: ' +
                         str(user['weibo_num']) + u'\n关注数: ' +
                         str(user['following']) + u'\n粉丝数: ' +
                         str(user['followers']) + result_header)

        with open(get_filepath('txt', user['nickname']), 'ab') as f:
            f.write(result_header.encode(sys.stdout.encoding))

    def write_weibo(self, weibo):
        """将爬取的信息写入txt文件"""

        temp_result = []
        for w in weibo:
            temp_result.append(w['content'] + '\n' + u'微博位置: ' +
                               w['publish_place'] + '\n' + u'发布时间: ' +
                               w['publish_time'] + '\n' + u'点赞数: ' +
                               str(w['up_num']) + u'   转发数: ' +
                               str(w['retweet_num']) + u'   评论数: ' +
                               str(w['comment_num']) + '\n' + u'发布工具: ' +
                               w['publish_tool'] + '\n\n')
        result = ''.join(temp_result)
        with open(get_filepath('txt', self.user['nickname']), 'ab') as f:
            f.write(result.encode(sys.stdout.encoding))
        print(u'%d条微博写入txt文件完毕,保存路径:' % len(weibo))
        print(get_filepath('txt', self.user['nickname']))


class CsvWriter:
    def __init__(self, config):
        self.config = config

    def write_user(self, user):
        self.user = user
        result_headers = [
            '微博id',
            '微博正文',
            '原始图片url',
            '微博视频url',
            '发布位置',
            '发布时间',
            '发布工具',
            '点赞数',
            '转发数',
            '评论数',
        ]
        if not self.config['filter']:
            result_headers.insert(3, '被转发微博原始图片url')
            result_headers.insert(4, '是否为原创微博')
        with open(get_filepath('csv', self.user['nickname']),
                  'a',
                  encoding='utf-8-sig',
                  newline='') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerows([result_headers])

    def write_weibo(self, weibo):
        """将爬取的信息写入csv文件"""
        result_data = [w.values() for w in weibo]
        with open(get_filepath('csv', self.user['nickname']),
                  'a',
                  encoding='utf-8-sig',
                  newline='') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerows(result_data)

        print(u'%d条微博写入csv文件完毕,保存路径:' % len(weibo))
        print(get_filepath('csv', self.user['nickname']))


class MongoWriter:
    def __init__(self, config):
        self.config = config

    def write_user(self, user):
        """将爬取的用户信息写入MongoDB数据库"""
        self.user = user

        user_list = [user]
        self.info_to_mongodb('user', user_list)
        print(u'%s信息写入MongoDB数据库完毕' % user['nickname'])

    def info_to_mongodb(self, collection, info_list):
        """将爬取的信息写入MongoDB数据库"""
        from pymongo import MongoClient

        client = MongoClient()
        db = client['weibo']
        collection = db[collection]
        for info in info_list:
            if not collection.find_one({'id': info['id']}):
                collection.insert_one(info)
            else:
                collection.update_one({'id': info['id']}, {'$set': info})

    def weibo_to_mongodb(self, weibo):
        """将爬取的微博信息写入MongoDB数据库"""
        weibo_list = []
        for w in weibo:
            w['user_id'] = self.user['user_id']
            weibo_list.append(w)
        self.info_to_mongodb('weibo', weibo_list)
        print(u'%d条微博写入MongoDB数据库完毕' % len(weibo))


class MysqlWriter:
    def __init__(self, config):
        self.config = config

    def write_user(self, user):
        """将爬取的用户信息写入MySQL数据库"""
        self.user = user
        # 创建'weibo'数据库
        create_database = """CREATE DATABASE IF NOT EXISTS weibo DEFAULT
                         CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"""
        self.mysql_create_database(create_database)
        # 创建'user'表
        create_table = """
                CREATE TABLE IF NOT EXISTS user (
                id varchar(12) NOT NULL,
                nickname varchar(30),
                weibo_num INT,
                following INT,
                followers INT,
                PRIMARY KEY (id)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"""
        self.mysql_create_table(create_table)
        self.mysql_insert('user', [user])
        print(u'%s信息写入MySQL数据库完毕' % user['nickname'])

    def write_weibo(self, weibo):
        """将爬取的微博信息写入MySQL数据库"""
        # 创建'weibo'表
        create_table = """
                CREATE TABLE IF NOT EXISTS weibo (
                id varchar(10) NOT NULL,
                user_id varchar(12),
                content varchar(2000),
                original_pictures varchar(1000),
                retweet_pictures varchar(1000),
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
        self.mysql_create_table(create_table)
        # 在'weibo'表中插入或更新微博数据
        weibo_list = []
        for w in weibo:
            w['user_id'] = self.user['user_id']
            weibo_list.append(w)
        self.mysql_insert('weibo', weibo_list)
        print(u'%d条微博写入MySQL数据库完毕' % len(weibo))

    def mysql_create(self, connection, sql):
        """创建MySQL数据库或表"""
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql)
        finally:
            connection.close()

    def mysql_create_database(self, sql):
        """创建MySQL数据库"""
        import pymysql
        mysql_config = self.config['mysql_config']
        connection = pymysql.connect(**mysql_config)
        self.mysql_create(connection, sql)

    def mysql_create_table(self, sql):
        """创建MySQL表"""
        import pymysql
        mysql_config = self.config['mysql_config']
        mysql_config['db'] = 'weibo'
        connection = pymysql.connect(**mysql_config)
        self.mysql_create(connection, sql)

    def mysql_insert(self, table, data_list):
        """向MySQL表插入或更新数据"""
        import pymysql
        mysql_config = self.config['mysql_config']

        if len(data_list) > 0:
            keys = ', '.join(data_list[0].keys())
            values = ', '.join(['%s'] * len(data_list[0]))
            mysql_config['db'] = 'weibo'
            connection = pymysql.connect(**mysql_config)
            cursor = connection.cursor()
            sql = """INSERT INTO {table}({keys}) VALUES ({values}) ON
                     DUPLICATE KEY UPDATE""".format(table=table,
                                                    keys=keys,
                                                    values=values)
            update = ','.join([
                " {key} = values({key})".format(key=key)
                for key in data_list[0]
            ])
            sql += update
            try:
                cursor.executemany(
                    sql, [tuple(data.values()) for data in data_list])
                connection.commit()
            except Exception as e:
                connection.rollback()
                print('Error: ', e)
                traceback.print_exc()
            finally:
                connection.close()