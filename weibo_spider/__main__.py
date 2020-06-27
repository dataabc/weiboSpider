from absl import app

import sys,os
sys.path.append(os.path.abspath(os.path.dirname(os.getcwd())))

from weibo_spider.spider import main

app.run(main)
