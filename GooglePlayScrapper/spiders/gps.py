# -*- coding: utf-8 -*-
import scrapy
from GooglePlayScrapper.items import gpsItem

class gpsSpider(scrapy.Spider):
    name = "gps"
    allowed_domains = ["play.google.com"]
    start_urls = []
    prefix = "https://play.google.com/store/apps/details?id="
    file = open("apps_id.txt", "r")
    ids = file.readlines()
    file.close()

    for id in ids:
        url = prefix + id.strip()
        start_urls.append(url)

    def parse(self, response):
        self.log("Starting scan of " + response.url)
        item = gpsItem()
        infos = response.xpath('//*[@class="htlgb"]/text()')
        item["app_id"] = response.url.split("?id=")[-1]
        item["app_name"] = response.xpath('//*[@itemprop="name"]/span/text()')[0].extract()
        item["author"] = infos[-1].extract()
        item["genre"] = response.xpath('//*[@itemprop="genre"]/text()')[0].extract()
        item["description"] = response.xpath('//*[@jsname="sngebd"]//text()').extract()
        item["downloads"] = infos[2].extract()
        item["reviews"] = response.xpath('//*[@class="AYi5wd TBRnV"]/span/text()')[0].extract()
        item["rating"] = response.xpath('//div[@class="BHMmbe"]/text()').extract_first()
        if len(infos) > 6:
            item["price"] = infos[6].extract()
        else:
            item["price"] = '0.0'
        item["app_version"] = infos[3].extract()
        item["compability"] = infos[4].extract()
        item["filesize"] = infos[1].extract()
        item["updated"] = infos[0].extract()
        self.log("Finishing scan of " + response.url)
        
        return item




