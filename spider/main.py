from .souhu import souhu_spider
from .zhongguojingjiwang import china_spider
from .cctv import cctv_spider
from .priceHistory import price_spider
import os
from shutil import rmtree

def collectNews(path):
    if 'news' not in os.listdir(os.path.abspath('./spider')):
        os.mkdir(os.path.abspath('./spider') + '/news')
    # price_spider()
    souhu_spider(path)
    china_spider(path)
    cctv_spider(path)