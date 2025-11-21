from django.shortcuts import render,redirect
from django.http import HttpResponse
from user.models import Person_detail,Charity_cart,adoption_request
from django.contrib import messages
from .models import *
from .forms import *
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils import timezone



# Create your views here.
def organisation_home(request):
    return render(request,"org_home.html")

def org_home(request):
    org_instance=Organisation.objects.get(login=request.session.get('log_id'))
    request.session['org_id']=org_instance.id
    request.session['district']=org_instance.district
    return render(request,'org_home.html')


def adopt_people(request):
    data=Person_detail.objects.filter(status='pending')
    fields=['first_name','last_name','age','gender','image','district','sub_district','post','postal code','landmark','Adopt']
    adopted=person_list.objects.filter(adopted_by=request.session.get('org_id'))
    if request.POST:
        sub_district=request.POST['search']
        if sub_district:
           data=Person_detail.objects.filter(status='pending').filter(sub_district=sub_district).filter(district=request.session.get('district'))
        else:
            data=Person_detail.objects.filter(status='pending').filter(district=request.session.get('district'))


        
    return render(request,'adopt_people.html',{'data':data,'fields':fields,'adopted':adopted})



def adoption(request,id):
    instance=Person_detail.objects.get(pk=id)
    instance.status='adopted'
    org_instance=Organisation.objects.get(id=request.session.get('org_id')) 
    instance.adopted_by=org_instance
    instance.save()
  
    fname=instance.first_name
    lname=instance.last_name
    age=instance.age
    gender=instance.gender
    image=instance.image
    adopted_by=Organisation.objects.get(id=request.session.get('org_id'))



    person_list.objects.create(first_name=fname,last_name=lname,age=age,gender=gender,image=image,adopted_by=adopted_by)
    
    

    messages.success(request,f"{instance.first_name} Adopted succesfully")
    return redirect(adopt_people)


def edit_home(request):
    instance=Organisation.objects.get(id=request.session.get('org_id'))
    data=infrastructure_images.objects.filter(uploaded_by=instance)

    return render(request,'edit_home.html',{'data':data})


from .forms import InfrastructureImageForm
from .models import infrastructure_images
def upload_infrastructure_image(request):
    if request.method == 'POST':
        form = InfrastructureImageForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            # Assign the logged-in organisation (assuming you have request.user linked)
            instance.uploaded_by = request.user.organisation
            instance.save()
            return redirect('infrastructure_gallery')  # redirect to gallery view
    else:
        form = InfrastructureImageForm()
    
    images = infrastructure_images.objects.all()
    return render(request, 'infrastructure_upload.html', {'form': form, 'images': images})

def edit_carousal(request):
    instance=Organisation.objects.get(id=request.session.get('org_id'))
    data=infrastructure_images.objects.filter(uploaded_by=instance)

    if request.FILES and request.POST:
        image=request.FILES['image']
        print(image)
        org_instance=Organisation.objects.get(id=request.session.get('org_id'))
        infrastructure_images.objects.create(images=image,uploaded_by=org_instance)
        return redirect(edit_carousal)

  

    return render(request,'edit_carousal.html',{'data':data})


def delete_carousal(request,id):
    instance=infrastructure_images.objects.get(id=id)
    instance.delete()
    return redirect(edit_carousal)


def org_raise_funds(request):
    frm=raise_fund_form()
    select_data=person_list.objects.filter(adopted_by=Organisation.objects.get(id=request.session.get('org_id')))
    if request.POST and request.FILES:
        person_id=request.POST['person']
        fund_form=raise_fund_form(request.POST,request.FILES)
        instance=fund_form.save(commit=False)
        instance.person=person_list.objects.get(id=person_id)
        instance.raised_by=Organisation.objects.get(id=request.session.get('org_id'))
        fund_form.save()
        return redirect(org_raise_funds)
    
    uploaded=org_fund.objects.filter(raised_by=Organisation.objects.get(id=request.session.get('org_id')),status='pending')
    closed=org_fund.objects.filter(raised_by=Organisation.objects.get(id=request.session.get('org_id')),status='closed')
    
    return render(request,'raise_funds.html',{'frm':frm,'select_data':select_data,'uploaded':uploaded,'closed':closed})


def fund_person(request,id):
    
    fund_data=person_list.objects.filter(id=id)
    
    return render(request,'raise_funds.html',{'fund_data':fund_data})

# def update_fund_status(request,id):
#     instance=org_fund.objects.get(id=id)
#     collected=instance.amount_got
#     total=instance.amount
#     if request.POST:
#         status=request.POST['status']
#         amount=request.POST['amount']
#         instance.status=status
#         instance.amount_got=amount
#         instance.save()
       

#     return render(request,'update_fund_status.html',{'collected':collected,'total':total})


def recieved_funds(request):
    
    charity_instance=Charity_cart.objects.filter(charity__raised_by__id=request.session.get('org_id'),charity__status='pending').select_related('charity').select_related('user')
    if request.POST:
        num=request.POST['num']
        cart_id=request.POST['cart_id']
        fund_id=request.POST['fund_id']
        if num:
           
            prev=Charity_cart.objects.filter(id=cart_id)
            if prev:
                prev_amount=int(prev[0].amount_given)
                now_amount=int(num)
                sum1=prev_amount+now_amount
                prev.update(amount_given=sum1)
                

                a=org_fund.objects.filter(id=fund_id)
                num1=int(a[0].amount_got)

            
                num2=int(num)
                sum=num1+num2
                a.update(amount_got=sum)
                if int(sum)>=a[0].amount:
                    a.update(status='closed')
                    return redirect(recieved_funds)

    closed=org_fund.objects.filter(status='closed',raised_by__id=request.session.get('org_id'))

 
    return render(request,'recieved_funds.html',{'charity_instance':charity_instance,'closed':closed}) 


   
def add_members(request):
    frm=person_list_form()
    if request.POST and request.FILES:
        frm=person_list_form(request.POST,request.FILES)
        save_instance=frm.save(commit=False)
        save_instance.adopted_by=Organisation.objects.get(id=request.session.get('org_id'))
        save_instance.save()
        return redirect(add_members)

    return render(request,'add_members.html',{'frm':frm})

   
def adoption_requests_home(request):
    
    return render(request,'adoption_requests_home.html')


   
def kid_requests(request):
    data=adoption_request.objects.filter(person__adopted_by__id=request.session.get('org_id')).filter(status='pending').filter(type='kid')
    approved=adoption_request.objects.filter(person__adopted_by__id=request.session.get('org_id')).filter(status='approved').filter(type='kid')

     
    return render(request,'kid_requests.html',{'data':data,'approved':approved})

   
def kid_requests_approve(request,id,per_id):
    instance=adoption_request.objects.get(id=id)
    instance.status='approved'
    instance.adopted_date=timezone.now()
    instance.save()
    person_instance=person_list.objects.get(id=per_id)
    person_instance.status='adopted'
    person_instance.save()


    return render(request,'kid_requests.html')


   
def kid_requests_reject(request,id):
    instance=adoption_request.objects.filter(id=id)
    instance.status='rejected'
    instance.update()
   
    return render(request,'kid_requests.html')



    

    

    
    



    
    


    

