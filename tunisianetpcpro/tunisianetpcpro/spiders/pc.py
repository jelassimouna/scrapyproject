# -*- coding: utf-8 -*-
import os
import csv
import glob
import mysql.connector
import scrapy
from scrapy import signals



class PcSpider(scrapy.Spider):
    name = 'pc'
    allowed_domains = ['tunisianet.com.tn/703-pc-portable-pro']
    start_urls = ['http://tunisianet.com.tn/703-pc-portable-pro/']

    def parse(self, response):
        products =  response.xpath('//*[@class="product-miniature js-product-miniature"]')
        for product in products :
            title = product.xpath('.//*[@class="product-description"]/h2/a/text()').extract_first()
            #  category = 1
            #Company = "tunisianet"
            availability = product.xpath('.//*[@id="stock_availability"]/span/text()').extract_first( )
            price = product.xpath('.//*[@itemprop="price"]/text()').extract_first()
            reference = product.xpath('.//*[@class="product-reference"]/text()').extract_first()
            mark = product.xpath('.//*[@class="img img-thumbnail manufacturer-logo"]/@alt').extract_first()
            image = product.xpath('.//*[@class="thumbnail-container"]/a/img/@src').extract_first()
            url=product.xpath('.//*[@class="product-short-description"]/a/@href').extract_first()


            yield { 'title':  title ,
                    'reference': reference,
                    'availability' : availability,
                    'price': price,
                    'mark': mark,
                    'image': image,
                    'url':url
                     }
        
        
    def spider_closed (self,spider):
        csv_file = max(glob.iglob('*.csv'),key=os.path.getctime )
        #print (csv_file)
        cnx = mysql.connector.connect(user='lina', password='lina@je22', host='127.0.0.1', database='testpfa')
        test=open(csv_file)
        csv_data = csv.reader(test,delimiter = ',')

        row_count = 0
        cursor = cnx.cursor()
        for row in csv_data:
            if row_count != 0:
                cursor.execute('INSERT INTO product (title, reference, availability,price,mark,image,url) VALUES (%s,%s,%s,%s,%s,%s,%s)',row)
            row_count += 1
        cnx.commit()
        cursor.close()
        cnx.close()