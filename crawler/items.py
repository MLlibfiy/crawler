# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Comment(scrapy.Item):
    id = scrapy.Field()
    score = scrapy.Field()
    nickname = scrapy.Field()
    productColor = scrapy.Field()
    productSize = scrapy.Field()
    userClientShow = scrapy.Field()
    userLevelName = scrapy.Field()
    content = scrapy.Field()
    referenceName = scrapy.Field()
