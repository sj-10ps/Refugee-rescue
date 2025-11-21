from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.login,name='login'),
    path('user_page/',views.user_page,name='user_page'),
    path('user_register/',views.user_register,name='user_register'),
    path('org_register/',views.org_register,name='org_register'),
    path('logout/',views.logout,name='logout'),
 

    
  

]
