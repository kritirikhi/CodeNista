from django.urls import path,include 
from django.contrib import admin
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path('resetdone/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.resetdone, name='resetdone'),
    path('contact/',views.contact,name='contact'),
    path('about/',views.about,name='about'),
    path('search/',views.search,name='search'),
    path('signupuser/',views.signupuser,name='signupuser'),
    path('loginuser/',views.loginuser,name='loginuser'),
    path('logoutuser/',views.logoutuser,name='logoutuser'),
    path('resetpassword/',views.resetpassword,name='resetpassword'),
    path('resetpwdaction/',views.resetpwdaction,name='resetpwdaction'),
    # path('resetpassworddone/',views.resetpassworddone,name='resetpassworddone'),
    path('resetpwddoneaction/',views.resetpwddoneaction,name='resetpwddoneaction'),
    path('profilepage/',views.profilepage,name='profilepage'),
]
