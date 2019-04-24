# -*- coding: utf-8 -*-
import scrapy
from wallhaven.items import WallhavenItem

class ThumbSpider(scrapy.Spider):
    name = 'thumb'
    allowed_domains = ['alpha.wallhaven.cc']
    start_urls = ['https://alpha.wallhaven.cc/search']

    def parse(self, response):
        text = response.xpath('string(//*[@id="thumbs"]/section/header/h2)')[0].extract().strip()
        arr = text.split('/')
        max_page = int(arr[-1].strip())
        for page in range(1, 2):
            url = response.url + '?page=' + str(page)
            yield scrapy.Request(url, callback=self.parse_urls, dont_filter=True)

    def parse_urls(self, response):
        links = response.xpath('//*[@id="thumbs"]/section[1]/ul/li/figure/a/@href')
        for link in links:
            link = link.extract().strip()
            yield scrapy.Request(link, callback=self.parse_imgs, dont_filter=True)

    def parse_imgs(self, response):
        image_url = response.xpath('//*[@id="wallpaper"]/@src')[0].extract().strip()
        item = WallhavenItem()
        item['image_urls'] = 'https:' + image_url
        yield item


