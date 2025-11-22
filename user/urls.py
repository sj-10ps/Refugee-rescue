from django.contrib import admin
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('user_home/',user_home,name='user_home'),
    path('upload_person/',upload_person,name='upload_person'),
    path('adoption_home/',adoption_home,name='adoption_home'),
    path('view_person/',view_person,name='view_person'), 
    path('organisation-list/', organisation_list, name='organisation_list'),
    path('organisation-data/', organisation_data, name='organisation_data'),
    path('selected_organisation_data/<int:id>/', selected_organisation_data, name='selected_organisation_data'),
    path('charity_home/',charity_home,name='charity_home'),
    path('all_organisations/',all_organisations,name='all_organisations'),
    path('all_members/<int:id>',all_members,name='all_members'),
    path('all_fund_requests/',all_fund_requests,name='all_fund_requests'),
    path('community_home/',community_home,name='community_home'),
    path('video_feed/',video_feed,name='video_feed'),
    path('video_detail/<int:id>/', video_detail, name='video_detail'),
    path('charity_contact/<int:id>/', charity_contact, name='charity_contact'),
    path('charity_cart/<int:id>/', charity_cart, name='charity_cart'),
    path('charity_cart2/<int:id>/', charity_cart2, name='charity_cart2'),
    path('kid_elders_adoption_home/', kid_elders_adoption_home, name='kid_elders_adoption_home'),
    path('kid_adoption/', kid_adoption, name='kid_adoption'),
    path('key_adopt_confirm/<int:id>', key_adopt_confirm, name='key_adopt_confirm'),
    path('adopt_org_details/<int:org_id>', adopt_org_details, name='adopt_org_details'),
    path('adult_adoption/', adult_adoption, name='adult_adoption'),
    path('adult_adopt_confirm/<int:id>', adult_adopt_confirm, name='adult_adopt_confirm'),
    path('raise_complaint/<int:org_id>/<int:fund_id>', raise_complaint, name='raise_complaint'),

    


    

    

    

    

]

