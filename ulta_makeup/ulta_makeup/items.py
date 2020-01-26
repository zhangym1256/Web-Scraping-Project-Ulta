# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UltaMakeupItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Top_category = scrapy.Field()
    Product_category = scrapy.Field()
    Product_brand = scrapy.Field()
    Product_name = scrapy.Field()
    Product_price = scrapy.Field()
    Product_size = scrapy.Field()
    Product_rating = scrapy.Field()
    Tot_reviews = scrapy.Field()
    Product_details = scrapy.Field()
