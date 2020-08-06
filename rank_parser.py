import re
import requests
from bs4 import BeautifulSoup
from flask import request

def get_level_and_name(soup):
    level_and_name = soup.select('#personalfile_refresh > div > h1:nth-child(2) > div')[0].text.strip()

    level = level_and_name.split(' ')[0]
    name = level_and_name.split(' ')[1]
    return level, name

def get_rank(soup):
    rank, section, number, score = [s.text for s in soup.select('dd')[:4]]
    return rank, section, number, score

def get_last_update(soup):
    return soup.select('#tabs-personalfile > div.label.label-info.pull-left.personalfile-last-update')[0].text

def parser():
    try:
        summoner_name = request.args.get('id')

        form ={
            'summonerName': summoner_name,
        }
        headers = {'User-Agent': 'Mozilla/5.0'}
        session = requests.Session()

        r = session.post('https://lol.moa.tw/tft/search', headers=headers, data=form)
        soup = BeautifulSoup(r.text, 'html.parser')
        level, name = get_level_and_name(soup)
        rank, section, number, score = get_rank(soup)
        last_update = get_last_update(soup)

        if rank != 'TIER_UNboard':
            return '{} - {} 在聯盟戰棋已經爬到了 {}{} 排名{} 分數: {}, {}'.format(
                level, name,
                rank, section if section!='NA' else '', number, score,
                last_update
            )
        else: # no data can be found
            return '{} - {} 沒有戰棋資料'.format(
                level, name
            )
    except:
        return '是不是打錯名字了呢 >< 指令用法：!rank [召喚者名稱]'
