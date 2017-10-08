from scrapy import Request
from scrapy.spiders import Spider
from doubancrawler.items import DoubanBookItem

"""

示例为抓取豆瓣标签为“C”的图书

"""

class DoubanBook(Spider):
    name = 'douban_book'
    allowed_domains = ['book.douban.com']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    }

    def start_requests(self):
        url = 'https://book.douban.com/tag/C'
        yield Request(url, headers=self.headers)


    def parse(self, response):

        books = response.xpath('//ul[@class="subject-list"]/li')

        for book in books:
            item = DoubanBookItem()
            try:
                item['book_name'] = book.xpath('div[@class="info"]/h2/a/text()').extract()[0].strip()
                item['public_info'] = book.xpath('div[@class="info"]/div[@class="pub"]/text()').extract()[0].strip()
                item['rating_num'] = \
                book.xpath('div[@class="info"]/div[2]/span[@class="rating_nums"]/text()').extract()[0].strip()
                item['comment_num'] = book.xpath('div[@class="info"]/div[2]/span[@class="pl"]/text()').extract()[
                    0].strip()

                print(item['book_name'])
                yield item

            except:
                pass

        next_url = response.xpath('//div[@class="paginator"]/span[@class="next"]/a/@href').extract()
        if next_url:
            next_url = 'https://book.douban.com' + next_url[0]
            yield Request(next_url, headers=self.headers)