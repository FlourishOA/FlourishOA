"""pricesleuth_rest URL Configuration
"""
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin

# to avoid confusion with actual views file
from rest_framework.authtoken import views as auth_views

urlpatterns = [
    url(r'^api/', include('api.urls')),
    url(r'^api-token-auth/', auth_views.ObtainAuthToken.as_view()),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^', include('main_site.urls')),
]
