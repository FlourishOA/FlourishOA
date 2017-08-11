from main_site import views
from django.conf.urls import url
from django.views.generic import TemplateView
"""
url(r'^submitjournal', views.TemplateView.as_view(
    template_name='main_site/journalinfo.html')),
url(r'^submitprice', views.TemplateView.as_view(
    template_name='main_site/priceinfo.html')),
    """

urlpatterns = [
    url(r'^search', views.SearchView.as_view(), name='search'),
    url(r'^journal/(?P<issn>\d{4}-\d{3}[\dxX])/$', views.ResultView.as_view(), 
        name='result'),
    url(r'^bar', views.TemplateView.as_view(template_name='main_site/bar.html')),
    url(r'^scatter', views.TemplateView.as_view(
        template_name='main_site/scatter.html')),
    url(r'^submitjournal/?', views.JournalInfoFormView.as_view(), name='submitj'),
    url(r'^submitprice/?', views.PriceInfoFormView.as_view(), name='submitj'),
    url(r'^submit/?', views.SubmitInfoFormView.as_view(), name='submitj'),
    url(r'^success', views.TemplateView.as_view(
        template_name='main_site/success.html')),
    url(r'^jname-autocomplete/', views.JournalNameAutocomplete.as_view(create_field='name'),
        name='jname-autocomplete')
]
