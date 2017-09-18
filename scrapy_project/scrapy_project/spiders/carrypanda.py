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
        # itemQ["title"] = response.xpath('//title/text()').extract_first()
        itemQ["identifier"] = response.url.split("/")[3]
        itemQ["page_url"] = response.url

        itemQ["url_text"] = []
        itemQ["url_link"] = []
        for href_item in response.xpath('//*[@href]').extract():
            css_link = Selector(text=href_item).xpath(
                '//link/@href').extract_first()
            a_link = Selector(text=href_item).xpath(
                '//a/@href').extract_first()
            if css_link:
                itemQ["url_text"].append("CSS/Link")
                itemQ['url_link'].append(css_link)
            if a_link:
                itemQ["url_text"].append("Anchor Link")
                itemQ['url_link'].append(a_link)
            css_link = ''
            a_link = ''
        for src_item in response.xpath('//*[@src]').extract():
            script = Selector(text=src_item).xpath(
                '//script/@src').extract_first()
            image = Selector(text=src_item).xpath(
                '//img/@src').extract_first()
            if script:
                itemQ["url_text"].append("Script")
                itemQ['url_link'].append(script)
            if image:
                itemQ["url_text"].append("Image")
                itemQ['url_link'].append(image)
        LxmlLinkExtractor(allow=()).extract_links(response)
        return itemQ
