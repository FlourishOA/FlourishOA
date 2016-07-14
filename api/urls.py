from django.conf.urls import url, include
from api import views
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'journals', views.JournalViewSet)
#router.register(r'prices', views.PriceViewSet)
#router.register(r'publishers', views.PublisherViewSet)

urlpatterns = [

]

urlpatterns += router.urls

