# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.exceptions import DropItem


class UsernameFilterPipeline(object):
    def process_item(self, item, spider):
        if not item.get('user_name'):
            raise DropItem('No User_name Item Found')
        else:
            return item


class DuplicateFilterPipeline(object):
    def __init__(self):
        self.text_seen = set()

    def process_item(self, item, spider):
        if item.get('text') in self.text_seen:
            raise DropItem('Duplicate Item Found')
        else:
            self.text_seen.add(item.get('text'))
            return item


class MongoPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient('localhost', 27017)
        self.db = self.client['mydb']

    def spider_close(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[item.collection].insert_one(dict(item))
        return item

