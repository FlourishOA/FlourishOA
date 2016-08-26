from api import views
from rest_framework import routers
from django.conf.urls import url, include


router = routers.DefaultRouter()
router.register(r'journals', views.JournalViewSet, 'journal')
router.register(r'prices', views.PriceViewSet, 'price')
router.register(r'influence', views.InfluenceViewSet, 'influence')


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^docs', views.SchemaView.as_view()),
]
