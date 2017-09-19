from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
import json
from scrapyd_api import ScrapydAPI
from scrapy_app.models import Url_List
from scrapy_app.forms import URLFilterForm
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
            try:
                is_crawled = Url_List.objects.filter(
                    start_url=start_url).count()
            except:
                is_crawled = 0
            if is_crawled:
                scrapyJson = json.dumps({"msg": "Successfull"})
                statusCode = 200
                return HttpResponse(scrapyJson, 'application/json',
                    status=statusCode)
            file_obj = open('scrapy_project/url.txt', 'w')
            file_obj.write(start_url)
            file_obj.close()
            scrapyd = ScrapydAPI('http://localhost:6800')
            job_id = scrapyd.schedule('default', 'carrypanda')
            # url_list=[start_url])
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
                    scrapyJson = json.dumps({"msg": "Successfull"})
                    statusCode = 200
                    break
                time.sleep(1)
        except Exception as e:
            scrapyJson = json.dumps({"msg": str(e)})
            statusCode = 500
        return HttpResponse(scrapyJson, 'application/json', status=statusCode)


class FilterViews(View):
    '''
        Class based view to filter data
        (url -> /urlFilter/)
    '''

    def get(self, request):
        try:
            form = URLFilterForm(request.GET)
            if form.is_valid():
                start_url = request.GET.get('start_url')
                link_type = request.GET.get('link_type')
                if link_type and link_type != '-1':
                    url_List = Url_List.objects.filter(start_url=start_url,
                        link_type=link_type)
                else:
                    url_List = Url_List.objects.filter(start_url=start_url)
                item_list = []
                for url in url_List:
                    item = {}
                    item["page_url"] = url.page_url
                    item["link"] = url.link
                    item["link_type"] = url.link_type
                    item_list.append(item)
                scrapyJson = json.dumps({"msg": "Successfull",
                                         "res_data": item_list})
                statusCode = 200
            else:
                scrapyJson = json.dumps({"msg": str(form.errors)})
                statusCode = 400
        except Exception as e:
            scrapyJson = json.dumps({"msg": str(e)})
            statusCode = 500
        return HttpResponse(scrapyJson, 'application/json', status=statusCode)
