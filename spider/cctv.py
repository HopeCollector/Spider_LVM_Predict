import os.path
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import json
import re

mainAddress = 'http://jingji.cctv.com/'
js = '''
window.scrollTo(0, document.getElementById("open_box").offsetTop - 100)
'''

def getHtml(url):
    browser = webdriver.Chrome()
    browser.get(url)
    browser.implicitly_wait(20)
    button = browser.find_element_by_xpath('//div[@id="open_box"]')
    text = button.text
    while button.text == text:
        browser.execute_script(js)
        button.click()
        button = browser.find_element_by_xpath('//div[@id="open_box"]')
    html = browser.page_source
    browser.close()
    return BeautifulSoup(html, 'lxml')

def getUrls(url):
    soup = getHtml(url)
    a_s = soup.select('.ecoA9805_con02')
    urls = []
    for a in a_s:
        urls.append(a.a['href'])
    return urls

def getArticle(url):
    r = requests.get(url)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'lxml')
    article = {}
    
    try:
        article['title'] = soup.select('.cnt_bd h1')[0].text.replace('/', '\\')
        text = []
        for p in soup.select('.cnt_bd p'):
            text.append(p.text)
        article['text'] = '\n'.join(text)
    except:
        return article

    # with open(os.path.abspath('./spider/historyPrice.json'), 'r') as f:
    #     history = json.load(f)
    time = re.search(r'[\s.]*?(\d{4}).(\d{2}).(\d{2}).*',soup.select('.cnt_bd .function .info')[-1].text)
    try:
        time = time[1] + '.' + str(int(time[2])) + '.' + str(int(time[3]))
    except:
        print(url)
        print('找不到时间信息')
    # if time in history:
    #     article['tag'] = history[time]
    #     article['time'] = time

    return article

def cctv_spider(path):
    newsAddresses = getUrls(mainAddress)
    for newsAddress in newsAddresses:
        article = getArticle(newsAddress)
        print(article['title'])
        # if 'tag' not in article:
        #     continue
        with open(path + article['title'], 'w', encoding='utf-8') as f:
            json.dump(article, f)

if __name__ == '__main__':
    cctv_spider(os.path.abspath('./') + '/news/')