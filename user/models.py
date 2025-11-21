from django.db import models
from home.models import User,Organisation
from organisation.models import org_fund,person_list
from cloudinary.models import CloudinaryField
# Create your models here.

    

class Person_detail(models.Model):
    gender_choices=[
                    ('male','Male'),
                    ('female','Female'),
                    ('others','Others')
                    ]
    
  

    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    age=models.IntegerField(null=True)
    gender=models.CharField(max_length=100,choices=gender_choices,default='male')
    image=CloudinaryField('uploads')
    uploaded_at=models.DateTimeField(auto_now_add=True)
    district=models.CharField(max_length=100)
    sub_district=models.CharField(max_length=100)
    post=models.CharField(max_length=100)
    postal_code=models.IntegerField()
    landmark=models.TextField()
    uploaded=models.ForeignKey(User,on_delete=models.SET_NULL,related_name='uploaded_person',null=True)
    status=models.CharField(max_length=100,default='pending')
    adopted_by=models.ForeignKey(Organisation,on_delete=models.CASCADE,null=True)

    
   
    

    def __str__(self):
        return self.first_name
    
class Charity_cart(models.Model):
    charity=models.ForeignKey(org_fund,on_delete=models.CASCADE,related_name='fund_details')
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='fund_provider_details')
    amount_given=models.IntegerField(default=0)
    

class adoption_request(models.Model):
    person=models.ForeignKey(person_list,on_delete=models.SET_NULL,null=True,related_name='adopted_person_details')
    request_from=models.ForeignKey(User,on_delete=models.CASCADE,related_name='requested_person')
    date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=30)
    adopted_date=models.DateTimeField(null=True)
    type=models.CharField(max_length=30)

class fund_complaints(models.Model):
    complaint_against=models.ForeignKey(Organisation,on_delete=models.SET_NULL,related_name='fund_complaint_org',null=True)
    complaint_raised=models.ForeignKey(org_fund,on_delete=models.SET_NULL,related_name='fund_complaint_user',null=True)
    complainted_by=models.ForeignKey(User,on_delete=models.CASCADE,related_name='complainted_person')
    complaint=models.CharField(max_length=100)
    proof=CloudinaryField('billbroof')
    date=models.DateTimeField(auto_now_add=True)
    reply=models.CharField(max_length=100,null=True)
    replied_date=models.DateTimeField(null=True)
    status=models.CharField(max_length=100)
