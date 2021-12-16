from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from .api import api

urlpatterns = [
    path("", api.urls), 
] + staticfiles_urlpatterns()
