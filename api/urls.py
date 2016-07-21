from django.conf.urls import url, include
from api import views
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'journals', views.JournalViewSet, 'journal')
router.register(r'price', views.PriceViewSet, 'price')

urlpatterns = router.urls


