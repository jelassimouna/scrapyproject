# -*- coding: utf-8 -*-
import scrapy


class PcSpider(scrapy.Spider):
    name = 'pc'
    allowed_domains = ['mytek.tn/10-ordinateurs-portables']
    start_urls = ['http://mytek.tn/10-ordinateurs-portables/']

    def parse(self, response):
        products = response.xpath('//*[@class="product-container"]')   
        if products:

            for product in products:
                title = product.xpath('.//*[@itemprop="name"]/a/@title').extract_first()   
                description = product.xpath('.//*[@class="product-desc"]/text()').extract_first()
                price = product.xpath('.//*[@class="price product-price"]/text()').extract_first()
                availability = product.xpath('.//*[@class="custAvailableClass"]/text()').extract_first()
                url = product.xpath('.//*[@itemprop="name"]/a/@href').extract_first()   


                yield {'title':title,'description': description,'price': price, 'availability' : availability, 'url':url}

            #next page exp: /page2
            next_page_url = response.xpath('//*[@id="pagination_next_bottom"]/a/@href').extract_first()
            #absolute next page exp: myteck.com/page2
            absolute_next_page_url = response.urljoin(next_page_url)
            if next_page_url is not None :
                yield scrapy.Request(absolute_next_page_url,dont_filter=True)
        else: 
            return
            #if absolute_next_page_url is not None:
            #    yield response.follow(absolute_next_page_url, self.parse, dont_filter=True)



