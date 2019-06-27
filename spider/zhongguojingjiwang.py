import os.path
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import json
import re

mainAddress = 'http://finance.ce.cn/futures/'

def getHtml(url):
    r = requests.get(url)
    r.encoding = 'GB2312'
    return BeautifulSoup(r.text, 'lxml')

def getUrls(url):
    soup = getHtml(url)
    urls = []
    a_s = soup.select('li > a')
    for a in a_s:
        url = a['href']
        if url[0] != '.':
            continue
        else:
            if url[:2] == '..':
                urls.append('http://finance.ce.cn/' + url[3:])
            else:
                urls.append('http://finance.ce.cn/futures/' + url[2:])
    return urls

def getArticle(url):
    soup = getHtml(url)
    article = {}
    try:
        article['title'] = re.search(soup.select(r'(\s*)(.*)(\s*)' ,'#articleTitle')[0].text).group(2).replace('/', '\\')
        print(article['title'])
        article['text'] = soup.select('#articleText')[0].text
    except:
        return article
    
    with open(os.path.abspath('./spider/historyPrice.json'), 'r') as f:
        history = json.load(f)
    time = re.search(r'\s*(\d{4}).(\d{2}).(\d{2})[\s.]*',soup.select('#articleTime')[0].text)
    try:
        time = time[1] + '.' + str(int(time[2])) + '.' + str(int(time[3]))
    except:
        return article
    if time in history:
        article['tag'] = history[time]
        article['time'] = time
    return article

def china_spider(path):
    newsAddresses = getUrls(mainAddress)
    for newsAddress in newsAddresses:
        article = getArticle(newsAddress)
        if 'tag' not in article:
            continue
        with open(path + article['title'], 'w', encoding='utf-8') as f:
            json.dump(article, f)

if __name__ == '__main__':
    china_spider(os.path.abspath('./') + '/news/')