# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TwitterprojectItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    author = scrapy.Field()
    username = scrapy.Field()
    tweet = scrapy.Field()


