from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from api import views


urlpatterns = [
    url(r'^journals/$', views.JournalList.as_view()),
    url(r'^journals/(?P<issn_number>\d{4}\-\d{3}(\d|x|X))', views.JournalDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

