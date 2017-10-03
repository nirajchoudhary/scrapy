# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy_app.models import Start_Url_List, Page_Url_List, Url_List
from django.db import transaction
from datetime import datetime, timedelta


class ScrapyProjectPipeline(object):
    def process_item(self, item, spider):
        with transaction.atomic():
            current_time = datetime.now() + timedelta(hours=5, minutes=30)
            try:
                start_url_List = Start_Url_List.objects.get(
                    start_url=item["start_url"], depth=item["depth"])
                start_url_List.page_count += 1
                start_url_List.save()
            except:
                start_url_List = Start_Url_List()
                start_url_List.start_url = item["start_url"]
                start_url_List.depth = item["depth"]
                start_url_List.page_count = 1
                start_url_List.executed_on = current_time
                start_url_List.save()
            link_count = len(item["link"])
            page_url_List = Page_Url_List()
            page_url_List.fk_start_url = start_url_List
            page_url_List.page_url = item["page_url"]
            page_url_List.link_count = link_count
            page_url_List.save()
            objList = []
            for i in range(link_count):
                url_List = Url_List()
                url_List.fk_page_url = page_url_List
                url_List.link = item["link"][i]
                url_List.link_type = item["link_type"][i]
                url_List.url_category = item["url_category"][i]
                objList.append(url_List)
            Url_List.objects.bulk_create(objList)
        return item
