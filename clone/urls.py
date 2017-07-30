from django.conf.urls import url
from django.contrib import admin
from views import singnup_view

urlpatterns = [
    url(r'^', singnup_view)
]