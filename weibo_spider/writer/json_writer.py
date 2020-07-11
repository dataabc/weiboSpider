import codecs
import json
import logging
import os

from .writer import Writer

logger = logging.getLogger('spider.json_writer')


class JsonWriter(Writer):
    def __init__(self, file_path):
        self.file_path = file_path

    def write_user(self, user):
        self.user = user

    def _update_json_data(self, data, weibo_info):
        """更新要写入json结果文件中的数据，已经存在于json中的信息更新为最新值，不存在的信息添加到data中"""
        data['user'] = self.user.__dict__
        if data.get('weibo'):
            is_new = 1  # 待写入微博是否全部为新微博，即待写入微博与json中的数据不重复
            for old in data['weibo']:
                if weibo_info[-1]['id'] == old['id']:
                    is_new = 0
                    break
            if is_new == 0:
                for new in weibo_info:
                    flag = 1
                    for i, old in enumerate(data['weibo']):
                        if new['id'] == old['id']:
                            data['weibo'][i] = new
                            flag = 0
                            break
                    if flag:
                        data['weibo'].append(new)
            else:
                data['weibo'] += weibo_info
        else:
            data['weibo'] = weibo_info
        return data

    def write_weibo(self, weibos):
        """将爬到的信息写入json文件"""
        data = {}
        if os.path.isfile(self.file_path):
            with codecs.open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        data = self._update_json_data(data, [w.__dict__ for w in weibos])
        with codecs.open(self.file_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(data, indent=4, ensure_ascii=False))
        logger.info(u'%d条微博写入json文件完毕，保存路径：%s', len(weibos), self.file_path)
