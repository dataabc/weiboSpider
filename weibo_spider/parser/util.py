import hashlib
import logging
import sys

import requests
from lxml import etree

# Set GENERATE_TEST_DATA to True when generating test data.
GENERATE_TEST_DATA = False
TEST_DATA_DIR = 'tests/testdata'
URL_MAP_FILE = 'url_map.json'
logger = logging.getLogger('spider.util')


def hash_url(url):
    return hashlib.sha224(url.encode('utf8')).hexdigest()


def handle_html(cookie, url):
    """处理html"""
    try:
        resp = requests.get(url, cookies=cookie)

        if GENERATE_TEST_DATA:
            import io
            import json
            import os

            resp_file = os.path.join(TEST_DATA_DIR, '%s.html' % hash_url(url))
            with io.open(resp_file, 'w') as f:
                f.write(resp.text)

            with io.open(os.path.join(TEST_DATA_DIR, URL_MAP_FILE), 'r+') as f:
                url_map = json.loads(f.read())
                url_map[url] = resp_file
                f.seek(0)
                f.write(json.dumps(url_map, indent=4, ensure_ascii=False))
                f.truncate()

        selector = etree.HTML(resp.content)
        return selector
    except Exception as e:
        logger.exception(e)


def handle_garbled(info):
    """处理乱码"""
    try:
        info = (info.xpath('string(.)').replace(u'\u200b', '').encode(
            sys.stdout.encoding, 'ignore').decode(sys.stdout.encoding))
        return info
    except Exception as e:
        logger.exception(e)


def bid2mid(bid):
    """convert string bid to string mid"""
    alphabet = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    base = len(alphabet)
    bidlen = len(bid)
    head = bidlen % 4
    digit = int((bidlen-head)/4)
    dlist = [bid[0:head]]
    for d in range(1,digit+1):
        dlist.append(bid[head:head+d*4])
        head += 4
    mid = ''
    for d in dlist:
        num = 0
        idx = 0
        strlen = len(d)
        for char in d:
            power = (strlen - (idx + 1))
            num += alphabet.index(char) * (base ** power)
            idx += 1
            strnum = str(num)
            while (len(d) == 4 and len(strnum) < 7):
                strnum = '0' + strnum
        mid += strnum
    return mid
