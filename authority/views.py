from django.shortcuts import render,redirect
from home.models import Organisation,Login
from user.models import fund_complaints
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.utils import timezone
# Create your views here.

def admin_home(request):
    return render(request,'admin_home.html')


def approve_org(request):
    organisations = Organisation.objects.filter(status='pending')
    approved=Organisation.objects.filter(status='approved').order_by('approved_date')
    rejected=Organisation.objects.filter(status='rejected').order_by('approved_date')
    return render(request,'approve_org.html',{'org':organisations,'approved':approved,'rejected':rejected})


def approve_organisation(request,id,login):
    organisation_instance=Organisation.objects.get(id=id)
    organisation_instance.status='approved'
    organisation_instance.approved_date=timezone.now()
    organisation_instance.save()
    
    login_instance=Login.objects.get(id=login)
    login_instance.approval='approved'
    login_instance.save()
    return redirect(approve_org)


def reject_organisation(request,id,login):
    organisation_instance=Organisation.objects.get(id=id)
    organisation_instance.status='rejected'
    organisation_instance.approved_date=timezone.now()
    a=organisation_instance.save()
    
    login_instance=Login.objects.get(id=login)
    login_instance.approval='rejected'
    login_instance.save()

    return redirect(approve_org)


def delete_organisation(request,id,login):
    organisation_instance=Organisation.objects.filter(id=id)
    organisation_instance.delete()
    login_instance=Login.objects.get(id=login)
    login_instance.delete()
    return redirect(approve_org)

def viewallcomplaints(request):
    data=fund_complaints.objects.all().select_related('complaint_against').select_related('complainted_by').select_related('complaint_raised')
    if request.POST:
        reply=request.POST['reply']
        id=request.POST['id']
        complaint_instance=fund_complaints.objects.get(id=id)
        complaint_instance.reply=reply
        complaint_instance.replied_date=timezone.now()
        complaint_instance.save()
    return render(request,"viewcomplaints.html",{"data":data})

def fund_raised_company(request,id):
    org=Organisation.objects.get(id=id)
    
    return render(request,"fund_raised_company.html",{"organisation":org})