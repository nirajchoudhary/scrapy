from django.conf.urls import url
from questions.views import ScrapyForm, ScrapyViews
# from django.contrib import admin


urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^$', ScrapyForm.as_view()),
    url(r'^(?i)ScrapyView/$', ScrapyViews.as_view()),
]
