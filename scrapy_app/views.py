from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
import json
from scrapyd_api import ScrapydAPI
from scrapy_app.models import Url_List
from scrapy_app.forms import URLFilterForm
import time
from django.db import connection
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


class FreshCrawlViews(View):
    '''
        Class based view to call scrapy api
        (url -> /freshCrawl/)
    '''

    def get(self, request):
        try:
            start_url = request.GET.get('start_url')
            try:
                is_crawled = Url_List.objects.filter(
                    start_url=start_url).delete()
            except:
                is_crawled = 0
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
                page_URL = request.GET.get('page_URL')
                link_input = request.GET.get('link_input')
                filterQuery = 'select page_url, link, link_type \
                    from url_list where start_url="{0}"'\
                        .format(start_url)
                if link_type and link_type != '-1':
                    filterQuery += ' and link_type="{0}"'.format(link_type)
                if page_URL:
                    filterQuery += ' and page_url like "%%{0}%%"'.format(page_URL)
                if link_input:
                    filterQuery += ' and link like "%%{0}%%"'.format(link_input)
                filterQuery += ' ;'
                print filterQuery
                cursor = connection.cursor()
                cursor.execute(filterQuery)
                url_List = cursor.fetchall()
                item_list = []
                for url in url_List:
                    item = {}
                    item["page_url"] = url[0]
                    item["link"] = url[1]
                    item["link_type"] = url[2]
                    item_list.append(item)
                scrapyJson = json.dumps({"msg": "Successfull",
                                         "res_data": item_list})
                statusCode = 200
            else:
                scrapyJson = json.dumps({"msg": str(form.errors)})
                statusCode = 400
        except Exception as e:
            print e
            scrapyJson = json.dumps({"msg": str(e)})
            statusCode = 500
        return HttpResponse(scrapyJson, 'application/json', status=statusCode)


class GetPageURLViews(View):
    '''
    Class based view for auto suggestion of page url
    '''

    def get(self, request):
        '''
            Autocomplete view for page url
            (url -> /getPageURL/)
        '''
        try:
            page_URL = request.GET.get('term', '')
            start_url = request.GET.get('start_url', '')
            page_URL_list = Url_List.objects.values_list(
                'page_url', flat=True).filter(
                start_url=start_url, page_url__icontains=page_URL).distinct()
            page_url_results = []
            for page_url in page_URL_list:
                page_url_dict = {}
                page_url_dict['label'] = page_url
                page_url_dict['value'] = page_url
                page_url_results.append(page_url_dict)
            page_url_JSON = json.dumps(page_url_results)
            statusCode = 200
        except Exception as e:
            page_url_JSON = json.dumps({"msg": str(e)})
            statusCode = 500
        return HttpResponse(page_url_JSON, 'application/json', status=statusCode)


class GetLinkViews(View):
    '''
    Class based view for auto suggestion of link
    '''

    def get(self, request):
        '''
            Autocomplete view for link
            (url -> /getLink/)
        '''
        try:
            link = request.GET.get('term', '')
            start_url = request.GET.get('start_url', '')
            link_list = Url_List.objects.values_list(
                'link', flat=True).filter(
                start_url=start_url, link__icontains=link).distinct()
            link_results = []
            for link_item in link_list:
                link_dict = {}
                link_dict['label'] = link_item
                link_dict['value'] = link_item
                link_results.append(link_dict)
            link_JSON = json.dumps(link_results)
            statusCode = 200
        except Exception as e:
            link_JSON = json.dumps({"msg": str(e)})
            statusCode = 500
        return HttpResponse(link_JSON, 'application/json', status=statusCode)