# -*- coding: utf-8 -*-
import scrapy
import re
from GooglePlayScrapper.items import gpsItem

class gpsSpider(scrapy.Spider):
    name = "gps"
    allowed_domains = ["play.google.com"]
    translate = {"Offered By": "author",
                 "Installs": "downloads",
                 "In-app Products": "app_products",
                 "Updated": "updated",
                 "Current Version": "app_version",
                 "Requires Android": "compability",
                 "Size": "filesize"}
    monthNumber = {"January": "01", "February": "02", "March": "03", "April": "04",
                   "May": "05", "June": "06", "July": "07", "August": "08",
                   "September": "09", "October": "10", "November": "11", "December": "12", }

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
        atributes = response.xpath('//*[@class="BgcNfc"]/text()').extract()
        values = response.xpath('//*[@class="htlgb"]/text()').extract()
        ignore = {"Permissions", "Report", "Developer", "Content Rating", "Eligible for Family Library"}

        item["app_products"] = "none"

        if (atributes[0].startswith('Eligible')):
            i = 1
        else:
            i = 0

        for atribute in atributes:
            if self.translate.has_key(atribute):
                item[self.translate[atribute]] = values[i]
            if not ignore.__contains__(atribute):
                i = i+1

        item["app_id"] = response.url.split("?id=")[-1]
        item["app_name"] = response.xpath('//*[@itemprop="name"]/span/text()').extract_first()
        item["genre"] = response.xpath('//*[@itemprop="genre"]/text()').extract_first()
        item["description"] = response.xpath('//*[@jsname="sngebd"]//text()').extract()
        item["downloads"] = re.sub('[,+ ]', '', item["downloads"])

        item["reviews"] = response.xpath('//*[@class="AYi5wd TBRnV"]/span/text()').extract_first()
        item["reviews"] = re.sub('[, ]', '', item["reviews"])

        item["rating"] = response.xpath('//div[@class="BHMmbe"]/text()').extract_first()

        item["price"] = response.xpath('//span[@class="oocvOe"]/button[@aria-label]/text()').extract_first()
        price = re.sub('[R$ Buy]', '', item["price"])
        if (price == "Install"):
            item["price"] = "0.0"
        else:
            item["price"] = price

        updated = re.sub('[,]', '', item["updated"].strip())
        updated = updated.split(" ")
        item["updated"] = updated[1] + "-" + self.monthNumber[updated[0]] + "-" + updated[2]

        if not item["compability"].startswith("Varies"):
            item["compability"] = re.sub('[and up]', '', item["compability"])

        filesize = item["filesize"]
        if filesize.startswith("Varies"):
            item["filesize"] = "-1"
        else:
            filesize = re.sub('[Mk ]', '', item["filesize"])
            if item["filesize"].endswith('M'):
                if '.' not in filesize:
                    item["filesize"] = str(int(filesize)*1000)
                else:
                    filesize = re.sub('[.]', '', filesize)
                    item["filesize"] = str(int(filesize) * 100)

        self.log("Finishing scan of " + response.url)

        return item