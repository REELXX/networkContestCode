from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^rada', views.rada),
    url(r'^trend',views.trendmap),
    url(r'^monitor',views.monitor),
    url(r'^other', views.other),

    url(r'^detail1',views.monitorDetail),
    url(r'^detail2', views.otherDetail),

    url(r'^satisfaction',views.satisfaction),
    url(r'^manyidu',views.manyidu),

    url(r'^heart_map',views.heart_map),
    url(r'^userheart_map',views.heart_map2)


]