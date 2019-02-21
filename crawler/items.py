# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Comment(scrapy.Item):
    flag = scrapy.Field()
    id = scrapy.Field()
    productId = scrapy.Field()
    score = scrapy.Field()
    nickname = scrapy.Field()
    productColor = scrapy.Field()
    productSize = scrapy.Field()
    userClientShow = scrapy.Field()
    userLevelName = scrapy.Field()
    content = scrapy.Field()
    referenceName = scrapy.Field()
    referenceTime = scrapy.Field()


class JingDongItemInfo(scrapy.Item):
    flag = scrapy.Field()
    price = scrapy.Field()
    id = scrapy.Field()
    StockStateName = scrapy.Field()
    vender = scrapy.Field()
    website = scrapy.Field()
    url = scrapy.Field()


class GuoMeiItemInfo(scrapy.Item):
    flag = scrapy.Field()
    price = scrapy.Field()
    id = scrapy.Field()
    StockStateName = scrapy.Field()
    vender = scrapy.Field()
    website = scrapy.Field()
    url = scrapy.Field()
