from main_site import views
from django.conf.urls import url

urlpatterns =[
    url(r'^viz', views.VisualizationView.as_view(), name='viz'),
    url(r'^priceAI/', views.PriceAIView.as_view(), name='priceAI'),
    url(r'', views.IndexView.as_view(), name='index'),
]