# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GooglePlayScrapperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    app_id = scrapy.Field()
    app_name = scrapy.Field()
    author = scrapy.Field()
    genre = scrapy.Field()
    description = scrapy.Field()
    downloads = scrapy.Field()
    reviews = scrapy.Field()
    rating = scrapy.Field()
    price = scrapy.Field()
    app_version = scrapy.Field()
    compability = scrapy.Field()
    filesize = scrapy.Field()
    updated = scrapy.Field()
    
    pass
