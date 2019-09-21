
# -*- coding: utf-8 -*-
# from scrapy.spiders import CrawlSpider, Rule

# import new Scrapy parts of library

from scrapy import Spider
from scrapy.http import Request


class BooksSpider(Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com']

    def parse(self, response):
        books = response.xpath('//h3/a/@href').extract()
        for book in books:
            absolute_url = response.urljoin(book)
            yield Request(absolute_url, callback=self.parse_book)

    def parse_book(self, response):
        pass


# From first example to show scraping multiple pages

# from scrapy.linkextractors import LinkExtractor


# class BooksSpider(CrawlSpider):
#     name = "books"
#     allowed_domains = ["books.toscrape.com"]
#     # always remove www part
#     start_urls = (
#         'http://books.toscrape.com',
#     )
#     # follow is a boolean meaning that Scrapy will or won't keep following URLS/hpyerlinks
#     rules = (Rule(LinkExtractor(),
#                   callback='parse_page', follow=False),)

#     def parse_page(self, response):
#         yield {'URL': response.url}
