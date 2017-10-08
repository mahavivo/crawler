# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanMovieItem(scrapy.Item):

    # 排名
    ranking = scrapy.Field()
    # 电影名称
    movie_name = scrapy.Field()
    # 评分
    score = scrapy.Field()
    # 评论人数
    score_num = scrapy.Field()

class DoubanBookItem(scrapy.Item):

    # 书名
    book_name = scrapy.Field()
    # 出版信息
    public_info = scrapy.Field()
    # 评分
    rating_num = scrapy.Field()
    # 评价人数
    comment_num = scrapy.Field()

    # # 封面图片
    # cover = scrapy.Field()

