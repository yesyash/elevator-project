from django import views
from django.contrib import admin
from django.urls import path, include
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
]
