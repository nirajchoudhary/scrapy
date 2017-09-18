# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from questions.models import Url_List
from django.db import transaction

class ScrapyProjectPipeline(object):
    def process_item(self, item, spider):
        # try:
        #     question = Questions.objects.get(identifier=item["identifier"][0])
        #     print "Question already exist"
        #     return item
        # except Questions.DoesNotExist:
        #     pass
        with transaction.atomic():
            objList = []
            relative_link_count = len(item["relative_link"])
            absolute_link_count = len(item["absolute_link"])
            external_link_count = len(item["external_link"])
            max_count = max(relative_link_count, absolute_link_count,
                external_link_count)
            for i in range(max_count):
                url_List = Url_List()
                url_List.page_url = item["page_url"]
                try:
                    url_List.relative_link = item["relative_link"][i]
                except:
                    url_List.relative_link = ""
                try:
                    url_List.absolute_link = item["absolute_link"][i]
                except:
                    url_List.absolute_link = ""
                try:
                    url_List.external_link = item["external_link"][i]
                except:
                    url_List.external_link = ""
                objList.append(url_List)
            Url_List.objects.bulk_create(objList)
        return item
