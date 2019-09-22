
# -*- coding: utf-8 -*-
# from scrapy.spiders import CrawlSpider, Rule

# import new Scrapy parts of library

from scrapy import Spider
from scrapy.http import Request

def product_info(response, value):
    return response.xpath('//th[text()="' + value + '"]/following-sibling::td/text()').extract_first()

class BooksSpider(Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com']

    def parse(self, response):
        books = response.xpath('//h3/a/@href').extract()
        for book in books:
            # must make absolute url since different server
            absolute_url = response.urljoin(book)
            yield Request(absolute_url, callback=self.parse_book)

        # process next page
        next_page_url = response.xpath(
            '//a[text()="next"]/@href').extract_first()

        absolute_next_page_url = response.urljoin(next_page_url)
        yield Request(absolute_next_page_url)

    def parse_book(self, response):
        title = response.css('h1::text').extract_first()
        price = response.xpath(
            '//*[@class="price_color"]/text()').extract_first()

        image_url = response.xpath('//img/@src').extract_first()
        image_url = image_url.replace('../..', 'http://books.toscrape.com')
        rating = response.xpath(
            '//*[contains(@class, "star-rating")]/@class').extract_first()
        rating = rating.replace('star-rating ', '')
        description = response.xpath('//*[@id="product_info"]/following-sibling::p/text()').extract_first()
        
        #product information data points
        upc = product_info(response, 'UPC')
        product_type = product_info(response, 'Product Type')
        price_without_tax = product_info(response, 'Price (excl.tax)')
        price_with_tax = product_info(response, 'Price (incl. tax)')
        tax = product_info(response, 'Tax')
        availability = product_info(response, 'Availability')
        number_of_reviews = product_info(response, 'Number of Reviews')

        
        yield {
            'title': title,
            'price': price,
            'image_url': image_url,
            'rating': rating,
            'description': description,
            'upc': upc,
            'product_type': product_type,
            'price_without_tax': price_without_tax,
            'price_with_tax': price_with_tax,
            'tax': tax,
            'availability': availability,
            'number_of_reviews': number_of_reviews,

        }

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
