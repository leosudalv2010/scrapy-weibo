# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from scrapy.loader.processors import MapCompose, Join
from w3lib.html import remove_tags
import datetime


class WeiboItem(Item):
    collection = 'weibonews-%s' % str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    user_name = Field(
        input_processor=MapCompose(str.strip),
    )
    time = Field()
    type = Field()
    text = Field(
        input_processor=MapCompose(str.strip, remove_tags),
    )
    comments = Field()
    likes = Field()
