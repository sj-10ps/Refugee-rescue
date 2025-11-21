from django.forms import ModelForm
from .models import *

class loginform(ModelForm):
    class Meta:
        model=Login
        fields=['username','password']

class userform(ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','age','gender','phone','email','district',"sub_district","post",'postal_code']

class organisationform(ModelForm):
    class Meta:
        model=Organisation
        fields=['name','district','sub_district','post','postal_code','licence','licence_image','email','phone','landmark',]