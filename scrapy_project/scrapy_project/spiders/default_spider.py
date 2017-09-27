# -*- coding: utf-8 -*-
import scrapy

from scrapy_project.items import Item
from scrapy.spiders.crawl import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import Selector


class CarrypandaSpider(CrawlSpider):
    name = "default_spider"
    start_urls = []
    allowed_domains = []
    def __init__(self, *args, **kwargs):
        super(CarrypandaSpider, self).__init__(*args, **kwargs)
        self.file_obj = open('url.txt', 'r')
        self.url = self.file_obj.read()
        self.file_obj.close()
        self.depth_obj = open('depth.txt', 'r')
        self.depth = self.depth_obj.read()
        self.depth_obj.close()
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


    def parse(self, response):
        itemQ = Item()
        itemQ["start_url"] = self.url
        itemQ["depth"] = self.depth
        itemQ["page_url"] = response.url
        itemQ["link"] = []
        itemQ["link_type"] = []
        itemQ["url_category"] = []
        href_links = response.xpath('//*[@href]').extract()
        src_links = response.xpath('//*[@src]').extract()
        all_link = href_links + src_links
        for link_item in all_link:
            css_link = Selector(text=link_item).xpath(
                '//link/@href').extract_first()
            a_link = Selector(text=link_item).xpath(
                '//a/@href').extract_first()
            script = Selector(text=link_item).xpath(
                '//script/@src').extract_first()
            image = Selector(text=link_item).xpath(
                '//img/@src').extract_first()
            iframe = Selector(text=link_item).xpath(
                '//iframe/@src').extract_first()
            if css_link:
                itemQ["url_category"].append("link href")
                itemQ["link"].append(css_link)
                link_arr = css_link.split('/')
            elif a_link:
                itemQ["url_category"].append("anchor href")
                itemQ["link"].append(a_link)
                link_arr = a_link.split('/')
            elif script:
                itemQ["url_category"].append("script src")
                itemQ["link"].append(script)
                link_arr = script.split('/')
            elif image:
                itemQ["url_category"].append("image src")
                itemQ["link"].append(image)
                link_arr = image.split('/')
            elif iframe:
                itemQ["url_category"].append("iframe src")
                itemQ["link"].append(iframe)
                link_arr = iframe.split('/')
            else:
                itemQ["url_category"].append("unknown")
                itemQ["link"].append(link_item)
                link_arr = ['unknown']
            try:
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
            except:
                itemQ["link_type"].append("Unknown")
        # LxmlLinkExtractor(allow=()).extract_links(response)
        return itemQ
