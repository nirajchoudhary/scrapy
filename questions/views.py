from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
import json
from scrapyd_api import ScrapydAPI
from questions.models import Url_List
import time
# from scrapy.crawler import CrawlerRunner
# from scrapy.utils.project import get_project_settings

class ScrapyForm(View):
    '''
        Class based view for loading scrapy page.
    '''

    def get(self, request):
        return render(request, 'scrapy.html')


class ScrapyViews(View):
    '''
        Class based view to call scrapy api
        (url -> /ScrapyView/)
    '''

    def post(self, request):
        try:
            start_url = request.POST.get('start_url')
            file_obj = open('scrapy_project/url.txt', 'w')
            file_obj.write(start_url)
            file_obj.close()
            try:
                last_record = Url_List.objects.all().last()
                last_pk_id = last_record.pk_id
            except:
                last_pk_id = 0
            scrapyd = ScrapydAPI('http://localhost:6800')
            job_id = scrapyd.schedule('default', 'carrypanda')
            # url_list=[start_url])
            is_finished = False
            while 1:
                spider_status = scrapyd.job_status('default', job_id)
                if spider_status == '':
                    scrapyJson = json.dumps({"msg": "Issue in Crawling."})
                    statusCode = 500
                    break
                if spider_status == 'running':
                    print "Still Running"
                if spider_status == 'pending':
                    print "In Panding"
                if spider_status == 'finished':
                    print "Finished"
                    is_finished = True
                    break
                time.sleep(2)
            if is_finished:
                url_List = Url_List.objects.filter(pk_id__gt=last_pk_id)
                item_list = []
                for url in url_List:
                    item = {}
                    item["page_url"] = url.page_url
                    item["relative_link"] = url.relative_link
                    item["absolute_link"] = url.absolute_link
                    item["external_link"] = url.external_link
                    item_list.append(item)
                scrapyJson = json.dumps({"msg": "Successfull",
                                         "res_data": item_list})
                statusCode = 200
        except Exception as e:
            scrapyJson = json.dumps({"msg": str(e)})
            statusCode = 500
        return HttpResponse(scrapyJson, 'application/json', status=statusCode)
