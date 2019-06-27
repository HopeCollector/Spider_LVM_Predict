import spider
import NLP
import os
import json

# with open(os.path.abspath('./module.ini'), 'r', encoding='utf-8') as f:
    # init_file = json.load(f)

spider.collectNews(os.path.abspath('./spider') + '/news/')
# NLP.createData()
# NLP.predict()