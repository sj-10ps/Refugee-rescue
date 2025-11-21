from django.forms import ModelForm
from .models import *

class person_detailsform(ModelForm):
    class Meta:
        model=Person_detail
        fields=['first_name','last_name','age','gender','image','district','sub_district','post','postal_code','landmark']