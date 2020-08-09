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

class BeautyLinks():
    def __init__(self, title_rule, n_articles, upvote_threshold):
        self.urls = list()
        self.title_rule, self.n_articles = title_rule, n_articles
        self.upvote_threshold = upvote_threshold

    def random_get(self):
        while True:
            try:
                return np.random.choice(self.urls)
            except: time.sleep(5)

    def update(self):
        new_articles = get_recent_articles(self.title_rule, self.n_articles)
        self.urls = filter_by_upvotes(new_articles, self.upvote_threshold)

boobs_links = BeautyLinks(r'.*[兇|凶|胸|奶|\b脾氣\b].*', 10, 10)
beauty_links = BeautyLinks('.*', 50, 10)

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
                    pass
    return images

def get_beauty():
    return '隨機表特：{}'.format(beauty_links.random_get())

def get_boobs():
    return '隨機奶特：{}'.format(boobs_links.random_get())

def timer_parser():
    threading.Thread(target=beauty_links.update).start()
    threading.Thread(target=boobs_links.update).start()
    threading.Timer(60*30, timer_parser).start()
timer_parser()