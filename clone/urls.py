from django.conf.urls import url
from django.contrib import admin
from views import singnup_view,login_user,post_view,feed_view,like_view,comment_view,logout_view

urlpatterns = [
    url(r'^$', singnup_view),
    url(r'^login/',login_user),
    url(r'^post/', post_view),
    url(r'^feed/', feed_view),
    url(r'^like/', like_view),
    url(r'^comment/', comment_view),
    url(r'^upload/',post_view),
    url(r'^logout',logout_view)
]