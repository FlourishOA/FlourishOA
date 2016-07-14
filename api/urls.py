from django.conf.urls import url, include
from api import views
from rest_framework import routers
import rest_framework.authtoken

router = routers.SimpleRouter()
router.register(r'journals', views.JournalViewSet, 'Journals')
#router.register(r'prices', views.PriceViewSet)
#router.register(r'publishers', views.PublisherViewSet)

urlpatterns = [

]

urlpatterns += router.urls

