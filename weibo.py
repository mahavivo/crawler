#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''

user_id 处填入要爬取的账号ID
cookie处用自己的有效cookie替代

'''

import os
import re
import requests
from bs4 import BeautifulSoup

user_id = ''
cookie = {
    'Cookie': ''
}

url = 'https://weibo.cn/u/%s?filter=1&page=1' % user_id

html = requests.get(url, cookies=cookie).content
soup = BeautifulSoup(html, 'lxml')
max_no = int(soup.find('input', attrs={'name': 'mp'})['value'])

print(u'爬虫正在准备......')

result = ''
text_count = 1
img_url_set = set()

for page in range(1, max_no + 1):
    url = 'http://weibo.cn/u/%s?filter=1&page=%d' % (user_id, page)
    req = requests.get(url, cookies=cookie).content
    soup_req = BeautifulSoup(req, 'lxml')

    # 提取文字
    wb_text = soup_req.find_all('span', attrs={'class': 'ctt'})
    for each in wb_text:
        text = each.get_text()
        if text_count >= 4:
            text = '%d：' % (text_count - 3) + text + '\n\n'
        else:
            text = text + '\n\n'
        result = result + text
        text_count += 1

    # 提取图片
    pic_url_list = soup_req.find_all('a', href=re.compile(r'^https://weibo.cn/mblog/oripic'))
    for imgurl in pic_url_list:
        img_url_set.add(requests.get(imgurl['href'], cookies=cookie).url)

    # 处理微博中存在组图的情况
    url_pic_all = soup_req.find_all('a', href=re.compile(r'^https://weibo.cn/mblog/picAll'))
    for img_all in url_pic_all:
        temp_html = requests.get(img_all['href'], cookies=cookie).content
        temp_soup = BeautifulSoup(temp_html, 'lxml')
        all_list = temp_soup.find_all('img', src=re.compile(r'http'))
        for each_url in all_list:
            img_src = each_url['src'].replace('thumb180', 'large')
            img_url_set.add(img_src)

path = os.getcwd() + '/微博爬虫'
if not os.path.exists(path):
    os.mkdir(path)

with open(u'%s/%s.txt' % (path, user_id), 'w', encoding='utf-8', errors='ignore') as fp:
    fp.write(result)
    txt_path = path + '/%s' % user_id
print(u'微博文字爬取完毕')

link = ''
with open('%s/%s_imageurls' % (path, user_id), 'w') as fp:
    for eachlink in img_url_set:
        link = link + eachlink + '\n'
    fp.write(link)
print(u'图片链接爬取完毕')

image_count = len(img_url_set)
if not img_url_set:
    print(u'图片不存在')
else:
    img_path = path + '/weibopic'
    if not os.path.exists(img_path):
        os.mkdir(img_path)

    x = 1
    for imgurl in img_url_set:
        temp = img_path + '/%s.jpg' % x
        print(u'正在下载第 %s 张图片' % x)
        try:
            img = requests.get(imgurl).content
            with open(temp, 'ab') as f:
                f.write(img)
        except:
            print(u'图片下载失败：%s' % imgurl)
        x += 1

print(u'文字爬取完毕，共 %d 条，保存路径 %s' % (text_count - 4, txt_path))
print(u'图片爬取完毕，共 %d 张，保存路径 %s' % (image_count, img_path))