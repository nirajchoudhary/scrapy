from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View, RedirectView
import json
from scrapyd_api import ScrapydAPI
from scrapy_app.models import Url_List, Start_Url_List, Page_Url_List
from scrapy_app.forms import URLFilterForm
import time
from django.db import connection
import urllib2
import math
from collections import deque


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
                    is_crawled = Start_Url_List.objects.get(start_url=start_url,
                                                            depth=depth)
                except:
                    is_crawled = 0
                if is_crawled:
                    scrapyJson = json.dumps({"msg": "Fetch Successful.",
                                             "job_id": ""})
                    statusCode = 200
                    return HttpResponse(scrapyJson, 'application/json',
                        status=statusCode)
                file_obj = open('scrapy_project/url.txt', 'w')
                file_obj.write(start_url)
                file_obj.close()
                depth_obj = open('scrapy_project/depth.txt', 'w')
                depth_obj.write(depth)
                depth_obj.close()
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
                        scrapyJson = json.dumps({"msg": "Issue in Crawling.",
                                                 "job_id": ""})
                        statusCode = 500
                        break
                    if spider_status == 'running':
                        scrapyJson = json.dumps({"msg": "Still Running...",
                                                 "job_id": job_id})
                        statusCode = 200
                        break
                    if spider_status == 'pending':
                        print "In Panding"
                    if spider_status == 'finished':
                        print "Finished"
                        scrapyJson = json.dumps({"msg": "Fetch Successful.",
                                                 "job_id": ""})
                        statusCode = 200
                        break
                    time.sleep(2)
            else:
                scrapyJson = json.dumps({"msg": "You must have logged in."})
                statusCode = 401
        except Exception as e:
            scrapyJson = json.dumps({"msg": str(e), "job_id": ""})
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
                        start_url=start_url, depth=depth).delete()
                except:
                    is_crawled = 0
                file_obj = open('scrapy_project/url.txt', 'w')
                file_obj.write(start_url)
                file_obj.close()
                depth_obj = open('scrapy_project/depth.txt', 'w')
                depth_obj.write(depth)
                depth_obj.close()
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
                        scrapyJson = json.dumps({"msg": "Issue in Crawling.",
                                                 "job_id": ""})
                        statusCode = 500
                        break
                    if spider_status == 'running':
                        scrapyJson = json.dumps({"msg": "Still Running...",
                                                 "job_id": job_id})
                        statusCode = 200
                        break
                    if spider_status == 'pending':
                        print "In Panding"
                    if spider_status == 'finished':
                        print "Finished"
                        scrapyJson = json.dumps(
                            {"msg": "Crawl and Fetch Successful.",
                             "job_id": ""})
                        statusCode = 200
                        break
                    time.sleep(2)
            else:
                scrapyJson = json.dumps({"msg": "You must have logged in."})
                statusCode = 401
        except Exception as e:
            scrapyJson = json.dumps({"msg": str(e), "job_id": ""})
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
                    job_id = request.GET.get('job_id')
                    is_finished = True
                    msg = "Fetch Successful."
                    if job_id:
                        scrapyd = ScrapydAPI('http://localhost:6800')
                        spider_status = scrapyd.job_status('default', job_id)
                        if spider_status == '':
                            msg = "Issue in Crawling."
                            job_id = ""
                            is_finished = True
                        if spider_status == 'running':
                            msg = "Still Running..."
                            job_id = job_id
                            is_finished = False
                        if spider_status == 'pending':
                            msg = "In Panding..."
                            job_id = job_id
                            is_finished = False
                        if spider_status == 'finished':
                            msg = "Crawl and Fetch Successful."
                            job_id = ""
                            is_finished = True
                    start_url = request.GET.get('start_url')
                    depth = request.GET.get('depth', '0')
                    link_type = request.GET.get('link_type')
                    page_URL = request.GET.get('page_URL')
                    category = request.GET.get('category')
                    link_input = request.GET.get('link_input')
                    page_no = int(request.GET.get('page_no'))
                    query = 'select pul.page_url, ul.link, ul.link_type, \
                        ul.url_category, sul.page_count, \
                        pul.link_count from url_list as ul \
                        right outer join page_url_list as pul \
                        on pul.pk_id = ul.fk_page_url \
                        join start_url_list as sul \
                        on sul.pk_id = pul.fk_start_url \
                        where sul.start_url="{0}" and sul.depth={1}'\
                        .format(start_url, depth)
                    if link_type and link_type != '-1':
                        query += ' and ul.link_type="{0}"'.format(link_type)
                    if category and category != '-1':
                        query += ' and ul.url_category="{0}"'.format(category)
                    if page_URL:
                        query += ' and pul.page_url like "%%{0}%%"'.format(page_URL)
                    if link_input:
                        query += ' and ul.link like "%%{0}%%"'.format(link_input)
                    query += ';'
                    cursor = connection.cursor()
                    cursor.execute(query)
                    url_List = cursor.fetchall()
                    records_per_page = 500
                    row_count = len(list(url_List))
                    url_page = pagination(row_count, page_no, records_per_page)
                    start_row = (page_no - 1) * records_per_page
                    end_row = page_no * records_per_page
                    item_list = []
                    page_url_data = ""
                    page_count = 0
                    for url in url_List:
                        if page_url_data != url[0]:
                            page_count += 1
                            page_url_data = url[0]
                    for url in url_List[start_row: end_row]:
                        item = {}
                        item["page_url"] = url[0]
                        item["link"] = url[1]
                        item["link_type"] = url[2]
                        item["url_category"] = url[3]
                        item["link_count"] = url[5]
                        item_list.append(item)
                    scrapyJson = json.dumps({"msg": msg,
                                             "res_data": item_list,
                                             "row_count": row_count,
                                             "url_page": url_page,
                                             "page_count": page_count,
                                             "is_finished": is_finished})
                    statusCode = 200
                else:
                    scrapyJson = json.dumps({"msg": str(form.errors)})
                    statusCode = 400
            else:
                scrapyJson = json.dumps({"msg": "You must have logged in."})
                statusCode = 401
        except Exception as e:
            scrapyJson = json.dumps({"msg": str(e), "job_id": ""})
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
            depth = request.GET.get('depth', '0')
            start_url_obj = Start_Url_List.objects.get(start_url=start_url,
                                                        depth=depth)
            page_URL_list = Page_Url_List.objects.values_list(
                'page_url', flat=True).filter(
                fk_start_url=start_url_obj, page_url__icontains=page_URL)
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
            depth = request.GET.get('depth', '0')
            query = 'select distinct ul.link from url_list as ul \
                    join page_url_list as pul \
                    on pul.pk_id = ul.fk_page_url \
                    join start_url_list as sul \
                    on sul.pk_id = pul.fk_start_url \
                    where sul.start_url="{0}" and sul.depth={1} and \
                    ul.link like "%%{2}%%"'.format(start_url, depth, link)
            query += ';'
            cursor = connection.cursor()
            cursor.execute(query)
            link_list = cursor.fetchall()
            link_results = []
            for link_item in link_list:
                link_dict = {}
                link_dict['label'] = link_item[0]
                link_dict['value'] = link_item[0]
                link_results.append(link_dict)
            link_JSON = json.dumps(link_results)
            statusCode = 200
        except Exception as e:
            link_JSON = json.dumps({"msg": str(e)})
            statusCode = 500
        return HttpResponse(link_JSON, 'application/json', status=statusCode)


def pagination(totalRows, currentPage, rowsInPage):
    '''
    General method for pagination. It accepts total number of rows,
    current page number and total number of rows in one page and
    return paginated data.
    '''
    totalPage = int(math.ceil(totalRows / float(rowsInPage)))
    if 0 < currentPage < totalPage + 1:
        if totalPage > 1:
            hasOtherPages = True
            if 1 < currentPage < totalPage:
                hasNextPage = True
                hasPreviousPage = True
            elif currentPage == 1:
                hasNextPage = True
                hasPreviousPage = False
            elif currentPage == totalPage and currentPage > 1:
                hasNextPage = False
                hasPreviousPage = True
            paginationLen = 5
            pageRange = deque()
            if totalPage <= paginationLen:
                pageRange = range(1, totalPage + 1)
            else:
                for page in range(currentPage - 2, currentPage + 3):
                    if 0 < page < totalPage + 1:
                        pageRange.append(page)
                n = len(pageRange)
                if n < paginationLen:
                    if pageRange[n - 1] == totalPage:
                        for page in range(pageRange[0] - 1, 0, -1):
                            n += 1
                            if n > paginationLen:
                                break
                            pageRange.appendleft(page)
                    else:
                        for page in range(pageRange[n - 1] + 1, totalPage + 1):
                            n += 1
                            if n > paginationLen:
                                break
                            pageRange.append(page)
            previousPageNo = currentPage - 1
            nextPageNo = currentPage + 1
            return {"hasOtherPages": hasOtherPages,
                    "currentPage": currentPage,
                    "hasNextPage": hasNextPage,
                    "hasPreviousPage": hasPreviousPage,
                    "pageRange": list(pageRange),
                    "previousPageNo": previousPageNo,
                    "nextPageNo": nextPageNo,
                    "totalPage": totalPage
                    }
        else:
            hasOtherPages = False
    else:
        hasOtherPages = False
    return {"hasOtherPages": hasOtherPages}