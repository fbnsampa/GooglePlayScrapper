# -*- coding: utf-8 -*-
import scrapy
from GooglePlayScrapper.items import GooglePlayScrapperItem
#from scrapy.loader import ItemLoader
#from scrapy.loader.processors import TakeFirst
#import psycopg2

class GplaySpider(scrapy.Spider):
    name = 'gplay'
    allowed_domains = ['play.google.com']
    start_urls = [
            'https://play.google.com/store/apps/details?id=info.intrasoft.habitgoaltracker',
            'https://play.google.com/store/apps/details?id=org.isoron.uhabits',
            'https://play.google.com/store/apps/details?id=com.oristats.habitbull'
            ]

    def parse(self, response):
        items = []
        item = GooglePlayScrapperItem()
        aux = response.xpath('//*[@class="htlgb"]/text()')
        item["app_id"] = response.url.split("?id=")[-1]
        item["app_name"] = response.xpath('//*[@itemprop="name"]/span/text()')[0].extract() 
        item["author"] = aux[-1].extract() 
        item["genre"] = response.xpath('//*[@itemprop="genre"]/text()')[0].extract()
        item["description"] = response.xpath('//*[@jsname="sngebd"]//text()').extract()
        item["downloads"] = aux[2].extract()
        item["reviews"] = response.xpath('//*[@class="AYi5wd TBRnV"]/span/text()')[0].extract()
        item["rating"] = response.xpath('//div[@class="pf5lIe"]/div/@aria-label').extract_first()
        if len(aux) > 6:
            item["price"] = aux[6].extract()
        else:
            item["price"] = '0.0'
        item["app_version"] = aux[3].extract()
        item["compability"] = aux[4].extract()
        item["filesize"] = aux[1].extract()
        item["updated"] = aux[0].extract()
        items.append(item)
        # self.log((("************************* APP %s SCRAPPED SUCCESSFULLY! *************************"), (item["app_name"])))
        
        return items
        
#        page = response.url.split("=")[-1]
#        filename = '%s.html' % page
#        
#        with open(filename, 'wb') as f:
#            f.write(response.body)
#            f.close()
        
#        item = ItemLoader(item=GooglePlayScrapperItem(), response=response)
#        item.add_xpath('genre', '//*[@itemprop="genre"]/text()')
#        item.add_xpath('all', '//*[@class="htlgb"]/text()'[1]) #TESTAR
#        return item.load_item()
#        item.add_xpath('updated', '//*[@class="htlgb"]/text()', TakeFirst(),re='(.*)')
        
        
