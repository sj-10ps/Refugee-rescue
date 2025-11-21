from django.db import models
from home.models import Organisation
from cloudinary.models import CloudinaryField

# Create your models here.
class infrastructure_images(models.Model):
    uploaded_by=models.ForeignKey(Organisation,on_delete=models.CASCADE,related_name='organisation')
    images=CloudinaryField('infra')
    type=models.CharField(max_length=50)

    def __str__(self):
        return self.type

class person_list(models.Model):
       
        gender_choices=[
                    ('male','Male'),
                    ('female','Female'),
                    ('others','Others')
                    ]
    
  

        first_name=models.CharField(max_length=100)
        last_name=models.CharField(max_length=100)
        age=models.IntegerField(null=True)
        gender=models.CharField(max_length=100,choices=gender_choices,default='male')
        image=CloudinaryField('Person')
        adopted_date=models.DateTimeField(auto_now_add=True)
        adopted_by=models.ForeignKey(Organisation,on_delete=models.CASCADE,related_name='organisation_details')
        status=models.CharField(max_length=20,default='pending')
        
        def __str__(self):
             return self.first_name
    
class org_fund(models.Model): 
     
     person=models.ForeignKey(person_list,on_delete=models.SET_NULL,null=True,related_name='person_details')
     raised_by=models.ForeignKey(Organisation,on_delete=models.SET_NULL,null=True,related_name='org_details')
     fund_description=models.TextField()
     proof=CloudinaryField('videos')
     prescription=CloudinaryField('prescription')
     amount=models.IntegerField()
     amount_got=models.IntegerField(default=0)
     status=models.CharField(max_length=30,default='pending')
  

   
          