# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Item(scrapy.Item):
    # define the fields for item here like:
    # name = scrapy.Field()
    identifier = scrapy.Field()
    page_url = scrapy.Field()
    url_text = scrapy.Field()
    url_link = scrapy.Field()
