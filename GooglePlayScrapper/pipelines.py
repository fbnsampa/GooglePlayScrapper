# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import psycopg2

class gpsPipeline(object):
    filename = 'db-query-error.txt'
    logfile = open(filename, 'wb')

    def __init__(self):
        self.conn = psycopg2.connect("dbname='gps' user='postgres' host='localhost' password='root'")

    def close_spider(self, spider):
        self.conn.close()
        self.logfile.close()

    def process_item(self, item, spider):
        try:
            cur = self.conn.cursor()
            cur.execute("insert into public.apps(app_id, app_name, author, genre, description, downloads, reviews, rating, price, updated, app_version, compability, filesize, app_products) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, to_date(%s,'DD-MM-YYYY'), %s, %s, %s, %s)",(item["app_id"], item["app_name"], item["author"], item["genre"], item["description"], item["downloads"], item["reviews"], item["rating"], item["price"], item["updated"], item["app_version"], item["compability"], item["filesize"], item["app_products"]))
            self.conn.commit()
        except:
            self.conn.rollback()
            self.logfile.write(item["app_id"] + "\n")

        return item
