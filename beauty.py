import requests
import datetime
import json
import time
import re
import os
import numpy as np
import urllib.request
from bs4 import BeautifulSoup
import threading

PTT_url = "https://www.ptt.cc"

update_time = None
image_urls = list()

boobs_update_time = None
boobs_urls = list()

def get_webPage(url):
    res = requests.get(url,cookies = {'over18': '1'})
    if res.status_code !=200:
        print("Invalid URL",res.url)
        return None
    else:
        return res.text

def get_articles(page,date):
    soup = BeautifulSoup(page,'lxml')
    
    #上一頁連結位置
    prevURL = soup.select('.btn-group-paging a')[1]['href']
    
    #取得文章清單
    articles = []
    divs = soup.select('.r-ent')
    for article in divs:
        if article.find('div','date').text.strip() == date:
            #取得推文數
            pushCount = 0
            pushString = article.find('div','nrec').text
            if pushString:
                try:
                    pushCount = int(pushString) #將字串轉換成數字
                except ValueError:
                    if pushString == "爆":
                        pushCount = 99
                    elif pushString.startswith('X'):
                        pushCount = -10
            if article.find('a'):
                title = article.find('a').text #取得文章標頭
                href = article.find('a')['href'] #取得文章連結
                author = article.find('div','author').text #取得作者名
                articles.append({
                    'title':title,
                    'href':href,
                    'pushCount':pushCount,
                    'author':author
                })
    return articles, prevURL

def get_recent_articles(title_rule='.*', n_articles=10):
    allArticles = list()

    # 取得表特版頁面
    currentPage = get_webPage(PTT_url+'/bbs/Beauty/index.html')
    # 取得電腦端時間資料
    todayRoot = datetime.date.today()
    # 更新為 PTT 時間格式，並去掉開頭的'0' 
    today = todayRoot.strftime("%m/%d").lstrip('0')
    
    articles, prevURL = get_articles(currentPage,today)
    #當有符合日期的文章回傳時，搜尋上一頁是否有文章
    while len(allArticles) < n_articles:
        while articles:
            allArticles += [article for article in articles if re.match(title_rule, article['title'])]
            currentPage = get_webPage(PTT_url+prevURL)
            articles, prevURL = get_articles(currentPage,today)

        todayRoot = todayRoot - datetime.timedelta(days=1)
        # 更新為 PTT 時間格式，並去掉開頭的'0' 
        today = todayRoot.strftime("%m/%d").lstrip('0')
        articles, prevURL = get_articles(currentPage,today)

    return allArticles

def filter_by_upvotes(allArticles, threshold=10):
    images = list()

    for article in allArticles:
        if int(article['pushCount']) > threshold:
            url = PTT_url+article['href']
            newRequest = get_webPage(url)
            soup = BeautifulSoup(newRequest,'lxml')

            # 找尋符合的 img 圖片網址
            imgLinks = soup.findAll('a',{'href':re.compile('https:\/\/(imgur|i\.imgur)\.com\/.*.jpg$')})
            
            if len(imgLinks)>0:
                try:
                    for imgLink in imgLinks:
                        images.append(imgLink['href'])
                except Exception as e:
                    print(e)
                    pass
    return images

def get_random_image_url(boobs_only=False):
    global update_time
    global image_urls
    global boobs_update_time
    global boobs_urls

    now = time.time()

    if boobs_only:
        if boobs_update_time is not None and now - boobs_update_time < 60*60:
            return '隨機奶特：{}'.format(np.random.choice(boobs_urls))
        boobs_urls = list()

        boobs_urls = filter_by_upvotes(get_recent_articles(r'.*[兇|凶|胸|奶|\b脾氣\b].*', 10), 10)
        boobs_update_time = time.time()
        print('boobs updated!')
        return '隨機奶特：{}'.format(np.random.choice(boobs_urls))
    else:
        if update_time is not None and now - update_time < 60*30:
            return '隨機表特：{}'.format(np.random.choice(image_urls))

        image_urls = list()

        image_urls = filter_by_upvotes(get_recent_articles(n_articles=50), 10)
        update_time = time.time()
        print('beauty updated!')
        return '隨機表特：{}'.format(np.random.choice(image_urls))

def get_random_boobs():
    return get_random_image_url(True)

def initial_parser():
    get_random_boobs()
    get_random_image_url()

def timer_parser():
    threading.Thread(target=initial_parser).start()
    threading.Timer(60*30, timer_parser).start()
timer_parser()

if __name__ == '__main__':
    print(get_random_image_url(True))
    print(get_random_image_url(True))