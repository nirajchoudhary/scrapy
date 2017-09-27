from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View, RedirectView
import json
from scrapyd_api import ScrapydAPI
from scrapy_app.models import Url_List, Start_Url_List
from scrapy_app.forms import URLFilterForm
import time
from django.db import connection
import urllib2


class LoginForm(View):
    '''
        Class based view for loading login page.
    '''

    def get(self, request):
        '''
            if userId exist, redirect to Scrapy page
            else render login page (url -> /Login/)
        '''
        try:
            if 'userId' in request.session:
                return HttpResponseRedirect('/Scrapy/')
            else:
                return render(request, 'login.html')
        except Exception as e:
            statusCode = 500
            return HttpResponse(str(e), status=statusCode)


class LoginView(View):
    '''
        Class based view for login authentication
        (url -> /loginView/)
    '''

    def post(self, request):
        userName = request.POST.get('userName')
        password = request.POST.get('password')
        try:
            if userName == "admin" and password == "mindfire1#":
                # password is verified for the user
                request.session['userId'] = userName
                redirectTo = '/Scrapy/'
                loginJson = json.dumps({"redirectTo": redirectTo})
                statusCode = 200
            else:
                loginJson = json.dumps({"userName": userName,
                                        "msg": "Invalid password"})
                statusCode = 400
        except:
            loginJson = json.dumps({"msg": "Invalid user name"})
            statusCode = 400
        return HttpResponse(loginJson, 'application/json', status=statusCode)


class LogoutUser(RedirectView):
    '''
    Class based view for logout of user
    (url -> /logout/)
    '''
    url = '/Login/'

    def get(self, request, *args, **kwargs):
        if 'userId' in request.session:
            del request.session['userId']
        return super(LogoutUser, self).get(request, *args, **kwargs)


class ScrapyForm(View):
    '''
        Class based view for loading scrapy page.
    '''

    def get(self, request):
        try:
            if 'userId' in request.session:
                return render(request, 'scrapy.html')
            else:
                return HttpResponseRedirect('/')
        except:
            msg = "There is an error in your request."
            statusCode = 500
            return HttpResponse(msg, status=statusCode)


class ScrapyViews(View):
    '''
        Class based view to call scrapy api
        (url -> /ScrapyView/)
    '''

    def post(self, request):
        try:
            if 'userId' in request.session:
                start_url = request.POST.get('start_url')
                depth = request.POST.get('depth', '0')
                # try:
                #     f = urllib2.urlopen(start_url)
                # except Exception as e:
                #     scrapyJson = json.dumps({"msg": str(e)})
                #     statusCode = 200
                #     return HttpResponse(scrapyJson, 'application/json',
                #         status=statusCode)
                try:
                    is_crawled = Start_Url_List.objects.get(start_url=start_url)
                except:
                    is_crawled = 0
                if is_crawled:
                    scrapyJson = json.dumps({"msg": "Fetch Successful."})
                    statusCode = 200
                    return HttpResponse(scrapyJson, 'application/json',
                        status=statusCode)
                file_obj = open('scrapy_project/url.txt', 'w')
                file_obj.write(start_url)
                file_obj.close()
                scrapyd = ScrapydAPI('http://localhost:6800')
                if depth == '1':
                    job_id = scrapyd.schedule('default', 'default_spider')
                else:
                    if depth == '0':
                        settings = {"DEPTH_LIMIT": depth}
                    else:
                        settings = {"DEPTH_LIMIT": int(depth)-1}
                    job_id = scrapyd.schedule('default', 'carrypanda',
                        settings=settings)
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
                        scrapyJson = json.dumps({"msg": "Fetch Successful."})
                        statusCode = 200
                        break
                    time.sleep(1)
            else:
                scrapyJson = json.dumps({"msg": "You must have logged in."})
                statusCode = 403
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
            if 'userId' in request.session:
                start_url = request.GET.get('start_url')
                depth = request.GET.get('depth', '0')
                # try:
                #     f = urllib2.urlopen(start_url)
                # except Exception as e:
                #     scrapyJson = json.dumps({"msg": str(e)})
                #     statusCode = 200
                #     return HttpResponse(scrapyJson, 'application/json',
                #         status=statusCode)
                try:
                    is_crawled = Start_Url_List.objects.filter(
                        start_url=start_url).delete()
                except:
                    is_crawled = 0
                file_obj = open('scrapy_project/url.txt', 'w')
                file_obj.write(start_url)
                file_obj.close()
                # settings = {'JOBDIR': 'job_dir/'}
                scrapyd = ScrapydAPI('http://localhost:6800')
                if depth == '1':
                    job_id = scrapyd.schedule('default', 'default_spider')
                else:
                    if depth == '0':
                        settings = {"DEPTH_LIMIT": depth}
                    else:
                        settings = {"DEPTH_LIMIT": int(depth)-1}
                    job_id = scrapyd.schedule('default', 'carrypanda',
                        settings=settings)
                # , settings=settings)
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
                        scrapyJson = json.dumps(
                            {"msg": "Crawl and Fetch Successful"})
                        statusCode = 200
                        break
                    time.sleep(1)
            else:
                scrapyJson = json.dumps({"msg": "You must have logged in."})
                statusCode = 403
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
            if 'userId' in request.session:
                form = URLFilterForm(request.GET)
                if form.is_valid():
                    start_url = request.GET.get('start_url')
                    link_type = request.GET.get('link_type')
                    page_URL = request.GET.get('page_URL')
                    category = request.GET.get('category')
                    link_input = request.GET.get('link_input')
                    query = 'select ul.page_url, ul.link, ul.link_type, \
                        ul.url_category from url_list as ul \
                        join start_url_list as sul  \
                        on sul.pk_id = ul.fk_start_url \
                        where sul.start_url="{0}"'.format(start_url)
                    if link_type and link_type != '-1':
                        query += ' and ul.link_type="{0}"'.format(link_type)
                    if category and category != '-1':
                        query += ' and ul.url_category="{0}"'.format(category)
                    if page_URL:
                        query += ' and ul.page_url like "%%{0}%%"'.format(page_URL)
                    if link_input:
                        query += ' and ul.link like "%%{0}%%"'.format(link_input)
                    query += ';'
                    cursor = connection.cursor()
                    cursor.execute(query)
                    url_List = cursor.fetchall()
                    row_count = len(url_List)
                    item_list = []
                    for url in url_List:
                        item = {}
                        item["page_url"] = url[0]
                        item["link"] = url[1]
                        item["link_type"] = url[2]
                        item["url_category"] = url[3]
                        item_list.append(item)
                    scrapyJson = json.dumps({"msg": "Successful",
                                             "res_data": item_list,
                                             "row_count": row_count})
                    statusCode = 200
                else:
                    scrapyJson = json.dumps({"msg": str(form.errors)})
                    statusCode = 400
            else:
                scrapyJson = json.dumps({"msg": "You must have logged in."})
                statusCode = 403
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
            start_url_obj = Start_Url_List.objects.get(start_url=start_url)
            page_URL_list = Url_List.objects.values_list(
                'page_url', flat=True).filter(
                fk_start_url=start_url_obj, page_url__icontains=page_URL).distinct()
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
            start_url_obj = Start_Url_List.objects.get(start_url=start_url)
            link_list = Url_List.objects.values_list('link', flat=True).filter(
                fk_start_url=start_url_obj, link__icontains=link).distinct()
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
