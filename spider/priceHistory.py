import os.path
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import json
import re

mainAddress = 'https://cn.investing.com/indices/csi-300-futures-historical-data'
pattern = r'^(\d{4}).(\d{1,2}).(\d{1,2}).$'

def getHtml(url):
    r = requests.get(url)
    while r.status_code != 200:
        print('Connection problem, reconntect')
        r = requests.get(url)
    r.encoding = 'utf-8'
    return BeautifulSoup(r.text, 'lxml')

def getDateAndTag(url):
    history = {}
    tr_s = getHtml(url).select('#curr_table tbody tr')
    for tr in tr_s:
        tag = 1
        td_s = tr.select('td')
        if float(td_s[-1].text[:-1]) < 0:
            tag = -1
        history['.'.join(re.search(pattern, td_s[0].text).groups([1,2,3]))] = tag
    return history

def price_spider():
    with open(os.path.abspath('./spider') + '/historyPrice.json', 'w') as f:
        json.dump(getDateAndTag(mainAddress), f)

if __name__ == '__main__':
    spider()