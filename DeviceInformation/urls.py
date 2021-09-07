from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^APinformation', views.APinformation),
    url(r'^UserListServlet', views.UserListServlet),
    url(r'^errorDetect',views.errorDetect),
    url(r'userlist',views.userlist),
    url(r'userfeedback',views.userfeedback),
    url(r'userJourney',views.userJourney),
    url(r'getUserWay', views.getUserWay),


]
