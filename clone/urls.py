from django.conf.urls import url
from django.contrib import admin
from views import singnup_view,login_user

urlpatterns = [
    url(r'^$', singnup_view),
    url(r'^login/',login_user)
]