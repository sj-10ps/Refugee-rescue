from django.db import models
from cloudinary.models import CloudinaryField
# Create your models here.

class Login(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    usertype=models.CharField(max_length=50)
    approval=models.CharField(max_length=20)

    def __str__(self):
        return self.username
    
class User(models.Model):
    gender_choices=[
                    ('male','Male'),
                    ('female','Female'),
                    ('others','Others')
                    ]


    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    age=models.IntegerField()
    gender=models.CharField(max_length=20,choices=gender_choices,default='male')
    phone=models.BigIntegerField()
    email=models.CharField(max_length=100)
    district=models.CharField(max_length=100)
    sub_district=models.CharField(max_length=100)
    post=models.CharField(max_length=100)
    postal_code=models.IntegerField()
    login=models.OneToOneField(Login,on_delete=models.CASCADE,related_name='user_details')
    
    def __str__(self):
        return self.first_name

class Organisation(models.Model):
    name=models.CharField(max_length=100)
    district=models.CharField(max_length=100)
    sub_district=models.CharField(max_length=100)
    post=models.CharField(max_length=50)
    postal_code=models.IntegerField(null=True)
    licence=models.CharField(max_length=100)
    licence_image=CloudinaryField('licence')
    email=models.CharField(max_length=100)
    phone=models.BigIntegerField()
    landmark=models.TextField()
    login=models.OneToOneField(Login,on_delete=models.CASCADE,related_name='organisation_details')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    status=models.CharField(max_length=100)
    approved_date=models.DateTimeField(null=True,blank=True)
    def __str__(self):
        return self.name
    





    


