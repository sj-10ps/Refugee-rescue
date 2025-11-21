from django.forms import ModelForm
from .models import *

class raise_fund_form(ModelForm):
    class Meta:
        model=org_fund
        fields=['proof','prescription','amount','fund_description']

class person_list_form(ModelForm):
    class Meta:
        model=person_list
        fields= ['first_name','last_name','age','gender','image']

class InfrastructureImageForm(ModelForm):
    class Meta:
        model = infrastructure_images
        fields = ['images', 'type']
