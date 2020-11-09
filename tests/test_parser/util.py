import json
import os
from unittest.mock import Mock

from weibo_spider.parser.util import TEST_DATA_DIR, URL_MAP_FILE


def mock_request_get_content(url, headers):
    with open(os.path.join(TEST_DATA_DIR, URL_MAP_FILE)) as f:
        url_map = json.loads(f.read())
    resp_file = url_map[url]
    mock = Mock()
    with open(resp_file, "rb") as f:
        mock.content = f.read()
    return mock
