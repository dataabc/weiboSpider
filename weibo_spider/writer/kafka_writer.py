import json
import logging
import sys

from .writer import Writer

logger = logging.getLogger('spider.kafka_writer')


class KafkaWriter(Writer):
    def __init__(self, kafka_config):
        try:
            from kafka import KafkaProducer
        except ImportError:
            logger.warning(
                u'系统中可能没有安装kafka库，请先运行 pip install kafka-python ，再运行程序')
            sys.exit()

        self.kafka_config = kafka_config
        self.producer = KafkaProducer(
            bootstrap_servers=str(kafka_config['bootstrap-server']).split(','),
            value_serializer=lambda m: json.dumps(m, ensure_ascii=False
                                                  ).encode('UTF-8'))
        self.weibo_topics = list(kafka_config['weibo_topics'])
        self.user_topics = list(kafka_config['user_topics'])
        logger.info('{}', kafka_config)

    def write_weibo(self, weibo):
        for w in weibo:
            for topic in self.weibo_topics:
                self.producer.send(topic, value=w.__dict__)

    def write_user(self, user):
        for topic in self.user_topics:
            self.producer.send(topic, value=user.__dict__)

    def __del__(self):
        self.producer.close()
