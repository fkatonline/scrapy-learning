# -*- coding: utf-8 -*-
import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['toscrape.com']
    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        for quote in response.css('div.quote'):
            item = {
                'author': response.css('small.author::text').extract_first(),
                'text': response.css('span.text::text').extract_first(),
                'tags': response.css('a.tag::text').extract(),
            }
            yield item
        # follow the next page
        next_page_url = response.css('li.next a::attr(href)').get()
        if next_page_url is not None:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(next_page_url, callback=self.parse)
