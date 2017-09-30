#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from urllib.request import urlopen, Request
import requests
from bs4 import BeautifulSoup


home_url = 'http://www.mmjpg.com'

class Foto():
    def __init__(self):
        self.headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/60.0.3112.113 Safari/537.36',
            'Referer': "http://www.mmjpg.com"
        }

    def album_info(self, album_url):
        req = requests.get(album_url, headers=self.headers)
        html = req.text
        soup = BeautifulSoup(html, 'lxml')
        title = soup.find('h2').get_text().encode('ISO-8859-1').decode('utf-8')
        self.title = title.replace('?', ' ')
        self.max_num = soup.find('div', class_='page').find_all('a')[-2].get_text()

    def make_dir(self):
        path = os.path.join(r'D:/mm', self.title)
        if not os.path.exists(path):
            os.makedirs(path)

    def all_urls(self):
        pic_urls = []
        for count in range(1, (int(self.max_num)+1)):
            url = album_url + "/" + str(count)
            each_html = requests.get(url, headers=self.headers).text
            if count < int(self.max_num):
                each_soup = BeautifulSoup(each_html, 'lxml')
                pic_url = each_soup.find("div", class_='content').find('a').img['src']
                pic_urls.append(pic_url)
            else:
                each_soup = BeautifulSoup(each_html, 'lxml')
                pic_url = each_soup.find('div', class_='content').find('img')['src']
                pic_urls.append(pic_url)
        return pic_urls

    def save_album(self, pic_urls):
        cnt = 1
        print('正在下载： %s，共 %s 张小黄图' % (self.title, self.max_num))
        for url in pic_urls:
            req = Request(url=url, headers=self.headers)
            img = urlopen(req).read()
            with open(r'D:/mm/%s/%s.jpg' % (self.title, str(cnt)), 'wb') as f:
                f.write(img)
            cnt = cnt + 1

    def download(self):
        self.album_info(album_url)
        self.make_dir()
        www = self.all_urls()
        self.save_album(www)

if __name__ == '__main__':
    f = Foto()
    for x in range(1, 10):
        album_url = home_url + '/mm/' + str(x)
        f.download()