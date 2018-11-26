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

    # start_urls = [
    #     # 'https://play.google.com/store/apps/details?id=info.intrasoft.habitgoaltracker',
    #     # 'https://play.google.com/store/apps/details?id=org.isoron.uhabits',
    #     # 'https://play.google.com/store/apps/details?id=com.SoftGamesInc.DaysSurvivalForest',
    #     # 'https://play.google.com/store/apps/details?id=com.oristats.habitbull'
    #     'https://play.google.com/store/apps/details?id=air.com.essig.spielplatz2lite'
    # ]

    for id in ids:
        url = prefix + id.strip()
        start_urls.append(url)

    def parse(self, response):
        self.log("Starting scan of " + response.url)
        item = gpsItem()
        atributes = response.xpath('//*[@class="BgcNfc"]/text()').extract()
        values = response.xpath('//*[@class="htlgb"]/text()').extract()
        translate = {"Offered By":"author",
                     "Installs":"downloads",
                     "In-app Products":"app_products",
                     "Updated":"updated",
                     "Current Version":"app_version",
                     "Requires Android":"compability",
                     "Size":"filesize"}
        ignore = {"Permissions", "Report", "Developer", "Content Rating"}
        item["app_id"] = response.url.split("?id=")[-1]
        item["app_name"] = response.xpath('//*[@itemprop="name"]/span/text()')[0].extract()
        item["genre"] = response.xpath('//*[@itemprop="genre"]/text()')[0].extract()
        item["description"] = response.xpath('//*[@jsname="sngebd"]//text()').extract()
        item["reviews"] = response.xpath('//*[@class="AYi5wd TBRnV"]/span/text()')[0].extract()
        item["rating"] = response.xpath('//div[@class="BHMmbe"]/text()').extract_first()
        item["app_products"] = "none"
        aux = response.xpath('//span[@class="oocvOe"]/button[@aria-label]/text()')[0].extract()
        if (aux == "Install"):
            item["price"] = "0.0"
        else:
            item["price"] = aux




        i = 0
        for atribute in atributes:
            if translate.has_key(atribute):
                item[translate[atribute]] = values[i]
            if not ignore.__contains__(atribute):
                i = i+1

        self.log("Finishing scan of " + response.url)
        return item




