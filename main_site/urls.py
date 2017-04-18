from main_site import views
from django.conf.urls import url
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^search', views.SearchView.as_view(), name='search'),
    url(r'^journal/(?P<issn>\d{4}-\d{3}[\dxX])/$', views.ResultView.as_view(), name='result'),
    url(r'^bar', views.TemplateView.as_view(template_name='main_site/bar.html')),
    url(r'^scatter', views.TemplateView.as_view(template_name='main_site/scatter.html')),
]
