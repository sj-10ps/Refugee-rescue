from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('organisation_home/',organisation_home,name="organisation_home"),
    path('org_home/',org_home,name='org_home'),
    path('adopt_people/',adopt_people,name='adopt_people'),
    path('adoption/<int:id>',adoption,name='adoption'),
    path('edit_home/',edit_home,name='edit_home'),
    path('edit_carousal/',edit_carousal,name='edit_carousal'),
    path('delete_carousal/<int:id>',delete_carousal,name='delete_carousal'),
    path('org_raise_funds',org_raise_funds,name='org_raise_funds'),
    path('fund_person<int:id>',fund_person,name='fund_person'),
    path('recieved_funds/',recieved_funds,name='recieved_funds'),
    path('add_members/',add_members,name='add_members'),
    path('adoption_requests_home/',adoption_requests_home,name='adoption_requests_home'),
    path('kid_requests/',kid_requests,name='kid_requests'),
    path('kid_requests_approve/<int:id>/<int:per_id>',kid_requests_approve,name='kid_requests_approve'),
    path('kid_requests_reject/<int:id>',kid_requests_reject,name='kid_requests_reject'),





    # path('update_fund_status/<int:id>',update_fund_status,name='update_fund_status'),
]

