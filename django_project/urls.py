from django.conf.urls import url
from scrapy_app.views import ScrapyForm, ScrapyViews, FilterViews, \
    FreshCrawlViews, GetPageURLViews, GetLinkViews, LoginForm, LoginView, \
    LogoutUser
# from django.contrib import admin


urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^$', LoginForm.as_view()),
    url(r'^(?i)loginView/$', LoginView.as_view()),
    url(r'^(?i)logout/$', LogoutUser.as_view()),
    url(r'^(?i)Login/$',  LoginForm.as_view()),
    url(r'^(?i)Scrapy/$', ScrapyForm.as_view()),
    url(r'^(?i)ScrapyView/$', ScrapyViews.as_view()),
    url(r'^(?i)urlFilter/$', FilterViews.as_view()),
    url(r'^(?i)freshCrawl/$', FreshCrawlViews.as_view()),
    url(r'^(?i)getPageURL/$', GetPageURLViews.as_view()),
    url(r'^(?i)getLink/$', GetLinkViews.as_view()),
]
