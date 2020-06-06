import sys
import traceback

from lxml import etree
import requests


def handle_html(cookie, url):
    """处理html"""
    try:
        html = requests.get(url, cookies=cookie).content
        selector = etree.HTML(html)
        return selector
    except Exception as e:
        print("Error: ", e)
        traceback.print_exc()


def handle_garbled(info):
    """处理乱码"""
    try:
        info = (
            info.xpath("string(.)")
            .replace(u"\u200b", "")
            .encode(sys.stdout.encoding, "ignore")
            .decode(sys.stdout.encoding)
        )
        return info
    except Exception as e:
        print("Error: ", e)
        traceback.print_exc()
