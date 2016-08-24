from api import views
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'journals', views.JournalViewSet, 'journal')
router.register(r'prices', views.PriceViewSet, 'price')
router.register(r'influence', views.InfluenceViewSet, 'influence')
# router.register(r'docs', views.SchemaView, 'docs') Docs Broken Temporarily

urlpatterns = router.urls
