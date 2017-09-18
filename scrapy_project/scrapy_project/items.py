# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Item(scrapy.Item):
    page_url = scrapy.Field()
    relative_link = scrapy.Field()
    absolute_link = scrapy.Field()
    external_link = scrapy.Field()
