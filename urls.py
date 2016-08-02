from main_site import views
from django.conf.urls import url

urlpatterns =[
    url(r'^', views.IndexView.as_view(), name='index'),
    url(r'^priceAI/', views.PriceAIView.as_view(), name='priceAI')
]