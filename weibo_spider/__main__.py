import os
import sys

from absl import app
sys.path.append(os.path.abspath(os.path.dirname(os.getcwd())))
from weibo_spider.spider import main

app.run(main)
