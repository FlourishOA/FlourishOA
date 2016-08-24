from api import views
from rest_framework import routers
from django.conf.urls import url

urlpatterns = [
    url('^docs', views.SchemaView.as_view()),
]
router = routers.SimpleRouter()
router.register(r'journals', views.JournalViewSet, 'journal')
router.register(r'prices', views.PriceViewSet, 'price')
router.register(r'influence', views.InfluenceViewSet, 'influence')


urlpatterns += router.urls
