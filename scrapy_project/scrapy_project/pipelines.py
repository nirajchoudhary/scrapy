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
            url_link_count = len(item["url_link"])
            for i in range(url_link_count):
                url_List = Url_List()
                url_List.identifier = item["identifier"]
                url_List.page_url = item["page_url"]
                url_List.url_link = item["url_link"][i]
                url_List.url_text = item["url_text"][i]
                objList.append(url_List)
            Url_List.objects.bulk_create(objList)
        return item
