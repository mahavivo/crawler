#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from urllib.request import urlopen, Request
import requests
from bs4 import BeautifulSoup

headers = {
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/60.0.3112.113 Safari/537.36',
    'Referer': "http://www.mmjpg.com"
}

home_url = 'http://www.mmjpg.com'

for x in range(1,10):
    album_url = home_url + '/mm/' + str(x)
    req = requests.get(album_url, headers=headers)
    html = req.text
    soup = BeautifulSoup(html, 'lxml')
    title = soup.find('h2').get_text().encode('ISO-8859-1').decode('utf-8')
    title = title.replace('?', ' ')
    max_num = soup.find('div', class_='page').find_all('a')[-2].get_text()

    path = os.path.join(r'D:/mm', title)
    if not os.path.exists(path):
        os.makedirs(path)

    pic_urls = []
    for count in range(1, (int(max_num)+1)):
        url = album_url + "/" + str(count)
        each_html = requests.get(url, headers=headers).text
        if count < int(max_num):
            each_soup = BeautifulSoup(each_html, 'lxml')
            pic_url = each_soup.find("div", class_='content').find('a').img['src']
            pic_urls.append(pic_url)
        else:
            each_soup = BeautifulSoup(each_html, 'lxml')
            pic_url = each_soup.find('div', class_='content').find('img')['src']
            pic_urls.append(pic_url)

    cnt = 1
    print('正在下载： %s，共 %s 张照片' % (title, max_num))
    for url in pic_urls:
        req = Request(url=url, headers=headers)
        img = urlopen(req).read()
        with open(r'D:/mm/%s/%s.jpg' % (title, str(cnt)), 'wb') as f:
            f.write(img)
        cnt = cnt + 1