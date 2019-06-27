import os.path
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import json
import re

mainAddress = 'http://www.sohu.com/tag/66048'
js = 'window.scroll(0, document.body.scrollHeight)'

# js会改变网页的DOM模型，模拟滚动可以最大限度地获取新闻
def useBrowser(url): 
    browser = webdriver.Chrome()
    browser.get(url)
    browser.implicitly_wait(20)
    browser.execute_script(js)
    # 这句话用来确定页面位置
    position = int(browser.find_elements_by_xpath('''//div[@class="news-wrapper"]/div[@data-position]''')[-1].get_attribute('data-position'))
    while position < 50: # 50 是硬编码，从网页源代码能查到
        position = int(browser.find_elements_by_xpath('''//div[@class="news-wrapper"]/div[@data-position]''')[-1].get_attribute('data-position'))
        browser.execute_script(js)
        browser.implicitly_wait(20)
    html = browser.page_source
    browser.close()
    return BeautifulSoup(html, 'lxml')

def getHtml(url):
    r = requests.get(url)
    r.encoding = 'utf-8'
    return BeautifulSoup(r.text, 'lxml')

def getUrls(url):
    soup = useBrowser(url)
    new_blocks = soup('div', attrs = {'data-role': 'news-item'})
    news = []
    for new_block in new_blocks:
        news.append('http:' + new_block.select('h4 > a')[0]['href'])
    return news

def getArticle(url):
    soup = getHtml(url)
    article = {}

    try:
        title = soup.select('.text-title')[0].h1.text
    except:
        return article
    title = re.search(r'(.{1,})(\s*)$' ,title).group(1)
    article['title'] = title.replace('/', '\\')
    article['text'] = soup.article.text
    # 确定文章发表时间并结合当日沪深指数打上标签
    with open(os.path.abspath('./spider/historyPrice.json'), 'r') as f: # 加载历史沪深指数
        history = json.load(f)
    time = re.search(r'[\s.]*?(\d{4}).(\d{2}).(\d{2}).*',soup.select('.time')[-1].text)
    try:
        time = time[1] + '.' + str(int(time[2])) + '.' + str(int(time[3]))
    except TypeError:
        print(url)
        print('找不到时间信息')
    if time in history:
        article['tag'] = history[time]
        article['time'] = time

    return article

def souhu_spider(path):
    newsAddresses = getUrls(mainAddress)
    for newsAddress in newsAddresses:
        article = getArticle(newsAddress)
        if 'tag' not in article:
            continue
        with open(path + article['title'], 'w', encoding='utf-8') as f:
            json.dump(article, f)

if __name__ == '__main__':
    souhu_spider(os.path.abspath('./') + '/news/')