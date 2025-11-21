from django.shortcuts import render,redirect
from .models import *
from .forms import *
from user.views import user_home
from organisation.views import org_home
from authority.views import admin_home
from django.contrib.auth.decorators import login_required

from .forms import loginform, organisationform
from .models import Login, Organisation

# Create your views here.

def home(request):

    return render(request,'public_home.html')

def user_page(request):
    
    return(request,'user_page.html')
 

def login(request):
    frm=loginform()
    if request.method == "POST":
       uname=request.POST['username']
       pword=request.POST['password']
     
       a=Login.objects.filter(username=uname,password=pword)
       if a:
           temp=a[0].usertype
           approval=a[0].approval
           request.session['log_id']=a[0].pk
           if temp=='user':
               return redirect(user_home)
           
           elif temp=='organisation' and approval=='approved':
               return redirect(org_home)
           
           elif temp=='admin' and approval=='approved':
               return redirect(admin_home)
           else:
               return redirect(home)
        


    return render(request,'login.html',{'frm':frm})

def user_register(request):
    frm1=userform()
    frm2=loginform()
    if request.method == "POST":
        login_form=loginform(request.POST)
        user_form=userform(request.POST)
       

        if login_form.is_valid() and user_form.is_valid():
            print(login_form.cleaned_data.get('username'))
            login_instance=login_form.save(commit=False)
            login_instance.usertype='user'
            login_instance.approval='approved'
            login_instance.save()
            user_instance=user_form.save(commit=False)
            user_instance.login=login_instance
            
            user_instance.save()
           
            return redirect(login)

            
         

    return render(request,'user_reg.html',{'frm1':frm1,'frm2':frm2})



def org_register(request):
    # Initialize the forms
    frm1 = loginform()
    frm2 = organisationform()

    if request.POST:
        login_form = loginform(request.POST)
        org_form = organisationform(request.POST,request.FILES)

        # Ensure both forms are valid
        if login_form.is_valid() and org_form.is_valid():
            # Save login form (without committing to database yet)
            login_instance = login_form.save(commit=False)
            login_instance.usertype = 'organisation'
            login_instance.approval= 'pending'
            login_instance.save()

            # Save organisation form (without committing to database yet)
            org_instance = org_form.save(commit=False)
            org_instance.login = login_instance
            org_instance.status='pending'

            # Get latitude and longitude from POST data (ensure they are passed from the frontend)
            latitude = request.POST['latitude']
            longitude = request.POST['longitude']
            

            # Save latitude and longitude if available
            if latitude and longitude:
                org_instance.latitude = float(latitude)
                org_instance.longitude = float(longitude)
                

            # Save the organisation instance
            org_instance.save()

            # Redirect to the login page or any other page after successful registration
            return redirect(login)  # Assuming you want to redirect to the login page after successful registration

 
       

    # If the request is not POST, return the empty forms
    return render(request, 'org_register.html', {'frm1': frm1, 'frm2': frm2})

def logout(request):

    return redirect(home)
