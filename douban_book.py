#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

爬取豆瓣某一标签的图书，示例为“python”。

"""

import requests
from bs4 import BeautifulSoup


tag = 'python'
home_url = 'https://book.douban.com/tag/' + tag


def html_downloader(url):
    res = requests.get(url).text
    return res

def html_parser(html):
    books = []
    soup = BeautifulSoup(html, 'lxml')
    book_list = soup.find_all('li', 'subject-item')
    for book in book_list:
        book_name = book.find('div', 'info').find('a')['title']
        books.append(book_name)

    next_page = soup.find('span', attrs={'class':'next'}).find('a')
    if next_page:
        next_page = 'https://book.douban.com' + next_page['href']
        return books, next_page
    else:
        return books, None

def main():
    url = home_url
    with open('豆瓣 %s 标签图书列表.txt' % tag, 'w') as f:
        while url:
            html = html_downloader(url)
            books, url = html_parser(html)
            for book in books:
                f.write(book+'\n')


if __name__ == '__main__':
    main()