from django.shortcuts import render,redirect
from .models import Organisation,User,Person_detail
from .forms import *
from home.models import User,Organisation
from django.http import JsonResponse,HttpResponse
from organisation.models import infrastructure_images,person_list,org_fund
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.

def user_home(request):
    a=User.objects.get(login=request.session.get('log_id'))
    request.session['user_id']=a.id

    return render(request,'user_home.html')


def adoption_home(request):
    return render(request,'adoptionhome.html')


def charity_home(request):
    return render(request,'charity_home.html')


def upload_person(request):
    frm = person_detailsform()  # Initialize the form instance
    
    if request.POST and request.FILES:
        person_form = person_detailsform(request.POST, request.FILES)
        
        if person_form.is_valid():  # Fixed the is_valid() method call
            # Get the current user from the session
            user_instance = User.objects.get(id=request.session.get('user_id'))
            
            if user_instance:
                person_instance = person_form.save(commit=False)
                person_instance.uploaded = user_instance  # Set the user who uploaded
                person_instance.status = 'pending'  # Set the status to 'pending'
                
                person_instance.save()  # Save the instance
                
                return redirect(adoption_home)  # Redirect after saving
                
            else:
                print("User not found")
        else:
            # Print the form errors if the form is not valid
            print(person_form.errors)
            # Optionally, you can return the errors to the template
            return render(request, 'upload_person.html', {'frm': frm, 'form_errors': person_form.errors})

    return render(request, 'upload_person.html', {'frm': frm})


def view_person(request):
    data=Person_detail.objects.filter(uploaded=request.session.get('user_id'))
    fields=['first_name','last_name','age','gender','image','adoption status']
   
    return render(request,'view_person.html',{'data':data,'fields':fields})





def organisation_list(request):
    organisations = Organisation.objects.filter(status='approved')
    return render(request, 'organisation_list.html', {'organisations': organisations})


def organisation_data(request):
    # Get all organisations with latitude and longitude
    organisations = Organisation.objects.filter(status='approved').values('id','name', 'district', 'sub_district', 'post', 'postal_code','landmark', 'latitude', 'longitude')
    return JsonResponse(list(organisations), safe=False)


def selected_organisation_data(request,id):
    data=Organisation.objects.get(id=id)
    print(id)
    images=infrastructure_images.objects.filter(uploaded_by=id)
    print(images)
   
    
    # Fetch the organization using the orgId
    
    # Render a template with the organization details
    return render(request, 'selected_organisation.html',{'data':data,'images':images})

def all_organisations(request):
    
    data=Organisation.objects.filter(status='approved')

    district=Organisation.objects.filter(status='approved').distinct('district').order_by('district')
    sub_district=Organisation.objects.filter(status='approved').distinct('sub_district').order_by('sub_district')
    if request.POST:
        dis=request.POST['district']
        sub_dis=request.POST['sub_district']
        data=Organisation.objects.filter(status='approved',district=dis,sub_district=sub_dis)
    return render(request,'all_org.html',{'org':data,'district':district,'sub_district':sub_district})

def all_members(request,id):
    data=person_list.objects.filter(adopted_by=Organisation.objects.get(id=id))
    return render(request,'all_members.html',{'data':data})


def all_fund_requests(request):
    user_instance=User.objects.get(id=request.session.get('user_id'))
    existing_carts_ids=Charity_cart.objects.filter(user=user_instance).values_list('charity_id',flat=True)
    data=org_fund.objects.filter(status='pending').exclude(id__in=existing_carts_ids).select_related('raised_by').select_related('person')
    cart_data=Charity_cart.objects.filter(user=user_instance,charity__status='pending').select_related('charity')
    closed=Charity_cart.objects.filter(user=user_instance,charity__status='closed').select_related('charity')
    complaints=fund_complaints.objects.filter(complainted_by=user_instance)
    


    return render(request,'all_fund_requests.html',{'data':data,'cart_data':cart_data,'closed':closed,'complaints':complaints})

def charity_cart(request,id):
    
    
    user_instance=User.objects.get(id=request.session.get('user_id'))

    fund_instance=org_fund.objects.get(id=id)
  
       

    Charity_cart.objects.create(charity=fund_instance,user=user_instance)
    return redirect(all_fund_requests)


def community_home(request):
    return render(request,'community_home.html')


def video_feed(request):
    # Fetch all OrgFund objects where proof (video) exists and status is 'pending'
    org_funds = org_fund.objects.filter(proof__isnull=False, status='pending').order_by('?')

    # Paginate the results, 1 video per page
    paginator = Paginator(org_funds, 1)  # Show 1 item per page (you can adjust the number of videos per page)
    page_number = request.GET.get('page')  # Get the page number from the GET request
    page_obj = paginator.get_page(page_number)

    return render(request, 'video_feed.html', {'page_obj': page_obj})

def video_detail(request,id):
    data=org_fund.objects.get(id=id)
    my_cart=Charity_cart.objects.filter(user=User.objects.get(id=request.session.get('user_id')))

    return render(request,'video_detail.html',{'data':data,'my_cart':my_cart})


def charity_contact(request,id):
    contact=Organisation.objects.get(id=id)
    return render(request,'video_detail.html',{'contact':contact})


def charity_cart2(request,id):
    
    
    user_instance=User.objects.get(id=request.session.get('user_id'))
    existing_carts_ids=Charity_cart.objects.filter(user=user_instance).values_list('charity_id',flat=True)
    fund_instance=org_fund.objects.get(id=id)
    if fund_instance.id in existing_carts_ids:
       messages.warning(request,'Already exists in cart')
       return redirect(video_detail,id)
        
    else:
        Charity_cart.objects.create(charity=fund_instance,user=user_instance)
        return redirect(video_feed)
    

def kid_elders_adoption_home(request):
    return render(request,'kid_elders_adoption_home.html')
    

def kid_adoption(request):
    data=person_list.objects.filter(age__lte=17).filter(status='pending')
    requests=adoption_request.objects.filter(request_from=User.objects.get(id=request.session.get('user_id'))).filter(type='kid')

    return render(request,'kid_adoption.html',{'data':data,'requests':requests})



def key_adopt_confirm(request,id):
    person_instance=person_list.objects.get(id=id)
    user_instance=User.objects.get(id=request.session.get('user_id'))
    adoption_request.objects.create(person=person_instance,request_from=user_instance,status='pending',type='kid')
    return redirect(kid_adoption)
    

def adopt_org_details(request,org_id):
    adopt_data=Organisation.objects.get(id=org_id)
    return render(request,'kid_adoption.html',{'adopt_data':adopt_data})
        


def adult_adoption(request):
    data=person_list.objects.filter(age__gte=18).filter(status='pending')
    requests=adoption_request.objects.filter(request_from=User.objects.get(id=request.session.get('user_id'))).filter(type='adult')

    return render(request,'adult_adoption.html',{'data':data,'requests':requests})


def adult_adopt_confirm(request,id):
    person_instance=person_list.objects.get(id=id)
    user_instance=User.objects.get(id=request.session.get('user_id'))
    adoption_request.objects.create(person=person_instance,request_from=user_instance,status='pending',type='adult')
    return redirect(adult_adoption)




def raise_complaint(request,org_id,fund_id):
    user_instance=User.objects.get(id=request.session.get('user_id'))
    if request.POST and request.FILES:
        complaint=request.POST['complaint']
        proof=request.FILES['proof']
        
        complaint_against_instance=Organisation.objects.get(id=org_id)
        complaint_raised_instance=org_fund.objects.get(id=fund_id)

        fund_complaints.objects.create(complaint_against=complaint_against_instance,complaint_raised=complaint_raised_instance,complainted_by=user_instance,complaint=complaint,proof=proof,status='pending')
    
    return render(request,'raise_complaint.html')

