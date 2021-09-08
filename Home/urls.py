from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.admin),
    url(r'^overview1', views.overview1),
    url(r'^voice_detect', views.voice_detect),
    url(r'^Sign_IN&UP', views.Sign),
    url(r'^register', views.register),
    url(r'^getUserInfo', views.getUserInfo),
    url(r'^infoChange', views.infoChange),

]
