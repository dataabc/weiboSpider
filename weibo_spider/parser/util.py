import sys
import traceback
import hashlib

import requests
from lxml import etree

# Set GENERATE_TEST_DATA to True when generating test data.
GENERATE_TEST_DATA = False
TEST_DATA_DIR = 'tests/testdata'
URL_MAP_FILE = "url_map.json"


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

            resp_file = os.path.join(TEST_DATA_DIR, "%s.html" % hash_url(url))
            with io.open(resp_file, "w") as f:
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
        print("Error: ", e)
        traceback.print_exc()


def handle_garbled(info):
    """处理乱码"""
    try:
        info = (info.xpath("string(.)").replace(u"\u200b", "").encode(
            sys.stdout.encoding, "ignore").decode(sys.stdout.encoding))
        return info
    except Exception as e:
        print("Error: ", e)
        traceback.print_exc()
