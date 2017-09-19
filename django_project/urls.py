from django.conf.urls import url
from scrapy_app.views import ScrapyForm, ScrapyViews, FilterViews
# from django.contrib import admin


urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^$', ScrapyForm.as_view()),
    url(r'^(?i)ScrapyView/$', ScrapyViews.as_view()),
    url(r'^(?i)urlFilter/$', FilterViews.as_view()),
]
