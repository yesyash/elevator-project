from multiprocessing.spawn import import_main_path
from django import views
from django.contrib import admin
from django.urls import path, url, include
from django.views.static import serve
from django.conf import settings
from rest_framework import routers
from api.views import destination, doors, elevators, elevator_system, requests

router = routers.DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path("admin/", admin.site.urls),
    path("init", elevator_system),
    path("destination/", destination),
    path("current-status", elevators),
    path("requests/", requests),
    path("door", doors),
    url(r'^media/(?P<path>.*)$', serve,
        {'document_root':       settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,
        {'document_root': settings.STATIC_ROOT}),
]
