# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import psycopg2
import re

class gpsPipeline(object):
    monthNumber = {"January": "01", "February": "02", "March": "03", "April": "04",
                   "May": "05", "June": "06", "July": "07", "August": "08",
                   "September": "09", "October": "10", "November": "11", "December": "12", }

    def __init__(self):
        self.conn = psycopg2.connect("dbname='gps' user='postgres' host='localhost' password='root'")

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        app_id = item["app_id"]
        app_name = item["app_name"]
        author = item["author"]
        genre = item["genre"]
        downloads = re.sub('[,+ ]', '', item["downloads"])
        reviews = re.sub('[, ]', '', item["reviews"])
        rating = item["rating"]
        price = re.sub('[R$ Buy]', '', item["price"])
        app_version = item["app_version"]
        app_products = item["app_products"]
        description = item["description"]
        updated = re.sub('[,]', '', item["updated"].strip())
        updated = updated.split(" ")
        updated = updated[1] + "-" + self.monthNumber[updated[0]] + "-" + updated[2]
        compability = item["compability"]

        if not compability.startswith("Varies"):
            compability = re.sub('[and up]', '', compability)

        filesize = item["filesize"]
        if filesize.startswith("Varies"):
            filesize = -1
        else:
            filesize = re.sub('[Mk ]', '', item["filesize"])
            if item["filesize"].endswith('M'):
                filesize = str(int(filesize)*1000)
        try:
            cur = self.conn.cursor()
            cur.execute("insert into public.apps(app_id, app_name, author, genre, description, downloads, reviews, rating, price, updated, app_version, compability, filesize, app_products) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, to_date(%s,'DD-MM-YYYY'), %s, %s, %s, %s)",(app_id, app_name, author, genre, description, downloads, reviews, rating, price, updated, app_version, compability, filesize, app_products))
            self.conn.commit()
        except:
            self.conn.rollback()


        return item
