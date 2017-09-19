# -*- coding: utf-8 -*-
import scrapy

from scrapy_project.items import Item
from scrapy.spiders.crawl import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import Selector


class CarrypandaSpider(CrawlSpider):
    name = "carrypanda"
    start_urls = []
    allowed_domains = []
    def __init__(self, *args, **kwargs):
        super(CarrypandaSpider, self).__init__(*args, **kwargs)
        self.file_obj = open('url.txt', 'rb')
        self.url = self.file_obj.read()
        self.file_obj.close()
        self.start_urls = [self.url] # ["http://carrypanda.com/"]
        # kwargs.pop('url_list', [])
        # self.start_urls = url_list
        self.allowed_domains = [self.url.split("/")[2]]

    rules = (Rule(LxmlLinkExtractor(
        allow=()), callback='parse_obj', follow=True),)

    def parse_obj(self, response):
        itemQ = Item()
        itemQ["page_url"] = response.url
        itemQ["link"] = []
        itemQ["link_type"] = []
        href_links = response.xpath('//@href').extract()
        src_links = response.xpath('//@src').extract()
        all_link = href_links + src_links
        for href_item in all_link:
            link_arr = href_item.split('/')
            itemQ["link"].append(href_item)
            if link_arr[0] == 'http:' or link_arr[0] == 'https:':
                try:
                    if link_arr[2] == self.allowed_domains:
                        itemQ["link_type"].append("Absolute")
                    else:
                        itemQ["link_type"].append("External")
                except:
                        itemQ["link_type"].append("Incorrect")
            else:
                itemQ["link_type"].append("Relative")
        LxmlLinkExtractor(allow=()).extract_links(response)
        return itemQ
