from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
   
    path('admin_home/',admin_home,name='admin_home'),
    path('approve_org/',approve_org,name='approve_org'),
    path('approve_organisation/<int:id>/<int:login>',approve_organisation,name='approve_organisation'),
    path('reject_organisation/<int:id>/<int:login>',reject_organisation,name='reject_organisation'),
    path('delete_organisation/<int:id>/<int:login>',delete_organisation,name='delete_organisation'),
    path('viewallcomplaints/',viewallcomplaints,name="viewallcomplaints"),
    path('fund_raised_company/<int:id>',fund_raised_company,name="fund_raised_company")
    

    


]
