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
        self.file_obj = open('url.txt', 'r')
        self.url = self.file_obj.read()
        self.file_obj.close()
        self.start_urls = [self.url] # ["http://carrypanda.com/"]
        # kwargs.pop('url_list', [])
        # self.start_urls = url_list
        self.domain_url = self.url.split("/")[2]
        if self.domain_url.split(".")[0] == "www":
            self.without_www_domain = self.domain_url.replace('www.', '')
            self.allowed_domains = [self.domain_url, self.without_www_domain]
        else:
            self.www_prepend_domain = "www." + self.domain_url
            self.allowed_domains = [self.domain_url, self.www_prepend_domain]


    rules = (Rule(LxmlLinkExtractor(
        allow=()), callback='parse_obj', follow=True),)

    def parse_obj(self, response):
        itemQ = Item()
        itemQ["start_url"] = self.url
        itemQ["page_url"] = response.url
        itemQ["link"] = []
        itemQ["link_type"] = []
        href_links = response.xpath('//@href').extract()
        src_links = response.xpath('//@src').extract()
        all_link = href_links + src_links
        for href_item in all_link:
            link_arr = href_item.split('/')
            itemQ["link"].append(href_item)
            if link_arr[0] == 'http:':
                try:
                    if link_arr[2] in self.allowed_domains:
                        itemQ["link_type"].append("Internal - Absolute - HTTP")
                    else:
                        itemQ["link_type"].append("External - Absolute - HTTP")
                except:
                        itemQ["link_type"].append("Incorrect")
            elif link_arr[0] == 'https:':
                try:
                    if link_arr[2] in self.allowed_domains:
                        itemQ["link_type"].append("Internal - Absolute - HTTPS")
                    else:
                        itemQ["link_type"].append("External - Absolute - HTTPS")
                except:
                        itemQ["link_type"].append("Incorrect")
            else:
                itemQ["link_type"].append("Internal - Relative")
        LxmlLinkExtractor(allow=()).extract_links(response)
        return itemQ
