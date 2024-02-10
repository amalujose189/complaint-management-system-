from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import reportlab
from datetime import datetime

from django.db.models import Count, Q
from .models import Profile,Complaint

from django.shortcuts import get_object_or_404,render, redirect
from django.http import HttpResponse
from .forms import UserRegisterForm,UserProfileform,ProfileUpdateForm,UserProfileUpdateform,statusupdate,ComplaintForm
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render
from django.views.generic import ListView


#page loading.
def index(request):
    return render(request,"ComplaintMS/home.html")

def aboutus(request):
    return render(request,"ComplaintMS/aboutus.html")

def login(request):
    return render(request,"ComplaintMS/login.html")

def login_redirect(request):
    if request.user.profile.type_of_user=='student':
        return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/counter/')


def signin(request):
    return render(request,"ComplaintMS/signin.html")




#registration page.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        profile_form=UserProfileform(request.POST)
        if form.is_valid() and profile_form.is_valid() :
            
            new_user=form.save()
            profile=profile_form.save(commit=False)
            if profile.user_id is None:
                profile.user_id=new_user.id
            profile.save()
            messages.add_message(request,messages.SUCCESS, f' Registered Successfully ')
            return redirect('/login/')
    else:
        form = UserRegisterForm()
        profile_form=UserProfileform()

    context={'form': form,'profile_form':profile_form }
    return render(request, 'ComplaintMS/register.html',context )

def login_redirect(request):
    if request.user.profile.type_of_user=='student':
       return HttpResponseRedirect('/dashboard/')
    else:
       return HttpResponseRedirect('/counter/')
  

@login_required
def dashboard(request):
        
    if request.method == 'POST':
        p_form=ProfileUpdateForm(request.POST,instance=request.user)
        profile_update_form=UserProfileUpdateform(request.POST,instance=request.user.profile)
        if p_form.is_valid() and profile_update_form.is_valid():
                user=p_form.save()
                profile=profile_update_form.save(commit=False)
                profile.user=user
                profile.save()
                messages.add_message(request,messages.SUCCESS, f'Updated Successfully')
            
                if request.user.profile.type_of_user=='student':
                    return HttpResponseRedirect('/dashboard/')
                else:
                    return HttpResponseRedirect('/profile/')  
    else:
        p_form=ProfileUpdateForm(instance=request.user)
        profile_update_form=UserProfileUpdateform(instance=request.user.profile)
    context={
        'p_form':p_form,
        'profile_update_form':profile_update_form
        }
    return render(request, 'ComplaintMS/dashboard.html',context)


'''
@login_required
def complaints(request):
  
    if request.method == 'POST':
           
        
        complaint_form=ComplaintForm(request.POST)
        if complaint_form.is_valid():
            
          
               instance=complaint_form.save(commit=False)
               instance.user=request.user
        #        mail=request.user.email
        #        print(mail)
        #        send_mail('Hi Complaint has been Received', 'Thank you for letting us know of your concern, Have a Cookie while we explore into this matter.  Dont Reply to this mail', 'testerpython13@gmail.com', [mail],fail_silently=False)
               instance.save()
               
               messages.add_message(request,messages.SUCCESS, f'Your complaint has been registered!')
               return render(request,'ComplaintMS/addComplaintMS.html',)
    else:
        
        complaint_form=ComplaintForm(request.POST)
    context={'complaint_form':complaint_form,}
    return render(request,'ComplaintMS/addComplaintMS.html',context)
'''


@login_required  
def complaints(request):   
         
        if request.method == "POST":
            saverecords=Complaint()
            
            ###
            id = request.user.id
            #assignto=request.user.get_username()
            Subject = request.POST.get('subject')
            Type_of_complaint = request.POST.get('Type_of_complaint')
            Description = request.POST.get('Description')
            saverecords.user_id=id
            #saverecords.assignto_id=assignto
            saverecords.Subject=Subject
            saverecords.Type_of_complaint=Type_of_complaint
            saverecords.Description=Description
          
            saverecords.save()
            messages.success(request, 'User complaint added Successfully')
        
        return render(request,"ComplaintMS/addComplaintMS.html")
''' 
@login_required  
def complaints(request):   
         
        if request.method == "POST":
            saverecords=Complaint()
            assigncomplaint=Assignto(instance=request.user.profile)
            ###
            id = request.user.id
            assigncom=[]
            assigncom=request.user.get_username()
            #staff=request.user.staff
            Subject = request.POST.get('subject')
            Type_of_complaint = request.POST.get('Type_of_complaint')
            Description = request.POST.get('Description')
            saverecords.user_id=id
            assigncomplaint.assignto=assigncom
            saverecords.Subject=Subject
            saverecords.Type_of_complaint=Type_of_complaint
            saverecords.Description=Description
            assigncomplaint.save()
            saverecords.save()
            messages.success(request, 'User complaint added Successfully')
        
        return render(request,"ComplaintMS/addComplaintMS.html") '''
       
'''def assign_complaint(request, id):
    complaint = Complaint.objects.get(id=id)
    staff = Staff.objects.filter(area_of_expertise=complaint.area_of_expertise).first()
    if staff:
        complaint.assigned_to = staff
        complaint.save()
        return redirect('complaint_list')
    else:
        return render(request, 'error.html', {'message': 'No staff available for this area of expertise'}) '''                   
                      
       
#@login_required

'''def complaintsstaff(request):
  
    if request.method == 'POST':
           
        
        complaint_formstaff=ComplaintFormstaff(request.POST)
        if complaint_formstaff.is_valid():
            
          
               instance=complaint_formstaff.save(commit=False)
               instance.user=request.user
        #        mail=request.user.email
        #        print(mail)
        #        send_mail('Hi Complaint has been Received', 'Thank you for letting us know of your concern, Have a Cookie while we explore into this matter.  Dont Reply to this mail', 'testerpython13@gmail.com', [mail],fail_silently=False)
               instance.save()
               
               messages.add_message(request,messages.SUCCESS, f'Your complaint has been registered!')
                if request.user.profile.type_of_user=='student':
                    #return render(request,'ComplaintMS/addcomplaint.html',)
                return render(request,'ComplaintMS/addcomplaint_staff.html',)
               #else:
              # return render(request,'ComplaintMS/addcomplaint.html',)
               #return render(request,'ComplaintMS/addcomplaint.html',)
    else:
        
        complaint_formstaff=ComplaintFormstaff(request.POST)
    context={'complaint_form':complaint_formstaff,}
    #return render(request,'ComplaintMS/addcomplaint.html',context)
    if request.user.profile.type_of_user=='staff':
    return render(request,'ComplaintMS/addcomplaint_staff.html',)

   # return render(request,'ComplaintMS/addcomplaint.html',)'''
    
@login_required
def solved(request):
        
        cid=request.POST.get('cid2')
        c=Complaint.objects.all().exclude(Q(status='3') | Q(status='2'))
        comp=request.GET.get("search")
        drop=request.GET.get("drop")

        if drop:
                c=c.filter(Q(Type_of_complaint__icontains=drop))
        if comp:
               
                c=c.filter(Q(Type_of_complaint__icontains=comp)|Q(Description__icontains=comp)|Q(Subject__icontains=comp))
        if request.method=='POST':
                cid=request.POST.get('cid2')
                print(cid)
                project = Complaint.objects.get(id=cid)
                forms=statusupdate(request.POST,instance=project)
                if forms.is_valid():
                        
                        obj=forms.save(commit=False)
                        obj.save()
                        messages.add_message(request,messages.SUCCESS, f'The complaint has been updated!')
                        return HttpResponseRedirect(reverse('solved'))
                else:
                        return render(request,'ComplaintMS/solved.html')
                 #testing

        else:
                forms=statusupdate()
        #c=Complaint.objects.all().exclude(Q(status='3') | Q(status='2'))
        
        args={'c':c,'forms':forms,'comp':comp}
        return render(request,'ComplaintMS/solved.html',args)
@login_required
def slist(request):
    result=Complaint.objects.filter(user=request.user).exclude(Q(status='3') | Q(status='2'))
    #c=Complaint.objects.all()
    args={'result':result}
    return render(request,'ComplaintMS/solvedcomplaint.html',args)

@login_required
def list(request):
    c=Complaint.objects.filter(user=request.user).exclude(status='1')
    result=Complaint.objects.filter(user=request.user).exclude(Q(status='3') | Q(status='2'))
    #c=Complaint.objects.all()
    args={'c':c,'result':result}
    return render(request,'ComplaintMS/unsolvedcomplaint.html',args)

def delete(request, id):
    a = Complaint.objects.get(id=id)
    a.delete()
    return redirect('list')

'''def delete(request, id):
    a = Complaint.objects.get(id=id)
    if a in request.user.profile.solved_complaints.all():
        request.user.profile.solved_complaints.remove(a)
    else:
        a.delete()
    return redirect('slist')'''

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.add_message(request,messages.SUCCESS, f'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.add_message(request,messages.WARNING, f'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'ComplaintMS/change_password.html', {
        'form': form
    })




@login_required   
def counter(request):
    if request.method == 'POST':
        p_form=ProfileUpdateForm(request.POST,instance=request.user)
        profile_update_form=UserProfileUpdateform(request.POST,instance=request.user.profile)
        if p_form.is_valid() and profile_update_form.is_valid():
                user=p_form.save()
                profile=profile_update_form.save(commit=False)
                profile.user=user
                profile.save()
                messages.add_message(request,messages.SUCCESS, f'Updated Successfully')
            
                if request.user.profile.type_of_user=='student':
                    return HttpResponseRedirect('/counter/')
                else:
                    return HttpResponseRedirect('/profile/')  
    else:
        p_form=ProfileUpdateForm(instance=request.user)
        profile_update_form=UserProfileUpdateform(instance=request.user.profile)
    context={
        'p_form':p_form,
        'profile_update_form':profile_update_form
        }
    return render(request, 'ComplaintMS/counter.html',context)
def statistics(request):
    total=Complaint.objects.all().count()
    unsolved=Complaint.objects.all().exclude(status='1').count()
    solved=Complaint.objects.all().exclude(Q(status='3') | Q(status='2')).count()
    dataset=Complaint.objects.values('Type_of_complaint').annotate(total=Count('status'),solved=Count('status', filter=Q(status='1')),
    notsolved=Count('status', filter=Q(status='3')),inprogress=Count('status',filter=Q(status='2'))).order_by('Type_of_complaint')
    args={'total':total,'unsolved':unsolved,'solved':solved,'dataset':dataset,}
    return render(request,"ComplaintMS/statistics.html",args)

def change_password_staff(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.add_message(request,messages.SUCCESS, f'Your password was successfully updated!')
            return redirect('change_password_staff')
        else:
            messages.add_message(request,messages.WARNING, f'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'ComplaintMS/change_password_staff.html', {
        'form': form
    })
@login_required
def allcomplaints(request):
      
        
        c=Complaint.objects.all().exclude(status='1')
        comp=request.GET.get("search")
        drop=request.GET.get("drop")

        if drop:
                c=c.filter(Q(Type_of_complaint__icontains=drop))
        if comp:
                c=c.filter(Q(Type_of_complaint__icontains=comp)|Q(Description__icontains=comp)|Q(Subject__icontains=comp))
        if request.method=='POST':
                cid=request.POST.get('cid2')
                uid=request.POST.get('uid')
                print(uid)
                project = Complaint.objects.get(id=cid)
                
                forms=statusupdate(request.POST,instance=project)
                if forms.is_valid():
                        
                        obj=forms.save(commit=False)
                        mail = User.objects.filter(id=uid)
                        for i in mail:
                                m=i.email
                       
                      
                        print(m)
                        # send_mail('Hi, Complaint has been Resolved ', 'Thanks for letting us know of your concern, Hope we have solved your issue. Dont Reply to this mail', 'testerpython13@gmail.com', [m],fail_silently=False)
                        obj.save()
                        messages.add_message(request,messages.SUCCESS, f'The complaint has been updated!')
                        return HttpResponseRedirect(reverse('allcomplaints'))
                else:
                        return render(request,'ComplaintMS/allComplaints.html')
                 #testing

        else:
                forms=statusupdate()
        #c=Complaint.objects.all().exclude(status='1')
           
        args={'c':c,'forms':forms,'comp':comp}
        return render(request,'ComplaintMS/allcomplaints.html',args)
#allcomplaints pdf viewer.
def pdf_viewer(request):
    detail_string={}
    #detailname={}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Complaint_id.pdf'
    p = canvas.Canvas(response,pagesize=A4)
    
    cid=request.POST.get('cid')
    uid=request.POST.get('uid')
    #print(cid)
    
    details = Complaint.objects.filter(id=cid).values('Description')
    name = Complaint.objects.filter(id=cid).values('user_id')
    '''Branch = Complaint.objects.filter(id=cid).values('Branch')'''
    Subject = Complaint.objects.filter(id=cid).values('Subject')
    Type = Complaint.objects.filter(id=cid).values('Type_of_complaint')
    Issuedate = Complaint.objects.filter(id=cid).values('Time')
    #date_format1 = "%Y-%m-%d %H:%M:%S.%f%z"
   
    
    for val in details:
            detail_string=("{}".format(val['Description']))
    for val in name:
           detailname=("User: {}".format(val['user_id']))
    '''for val in Branch:
            detailbranch=("Branch: {}".format(val['Branch']))'''
    for val in Subject:
            detailsubject=("Subject: {}".format(val['Subject']))
    for val in Type:
            detailtype=("Type of complaint: {}".format(val['Type_of_complaint']))
            
    for val in Issuedate:
            ptime=("{}".format(val['Time']))
            detailtime=("Time of Issue/ Time of Solved: {}".format(val['Time']))
    #detail_string = u", ".join(("Desc={}".format(val['Description'])) for val in details) 
    date_format = "%Y-%m-%d"
    a = datetime.strptime(str(datetime.now().date()), date_format)
    b = datetime.strptime(str(ptime), date_format)
    delta = a - b
    print(b)
    print(a)
    print (delta.days )       
    if detailtype=='1':
            detailtype="Type of Complaint: Technical"
    if detailtype=='3':
            detailtype="Type of Complaint: management"
    if detailtype=='2':
            detailtype="Type of Complaint: infrastructure"
    if detailtype=='4':
            detailtype="Type of Complaint: Department"
    
 
    p.drawString(25, 770,"Report:")
    p.drawString(30, 750,detailname)
    ''' p.drawString(30, 730,detailbranch)'''
    p.drawString(30, 710,detailtype)
    p.drawString(30, 690,detailtime)
    p.drawString(30, 670,detailsubject)
    p.drawString(30, 650,"Description:")
    p.drawString(30, 630,detail_string)

    p.showPage()
    p.save()
    return response

#complaints pdf view.
@login_required
def pdf_view(request):
    detail_string={}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=complaint_id.pdf'
    
    p = canvas.Canvas(response,pagesize=A4)
    cid=request.POST.get('cid')
    #print(cid)
    details = Complaint.objects.filter(id=cid).values('Description')
    name = User.objects.filter(username=request.user.username).values('username')
    #Branch = Complaint.objects.filter(id=cid).values('Branch')
    Subject = Complaint.objects.filter(id=cid).values('Subject')
    Type = Complaint.objects.filter(id=cid).values('Type_of_complaint')
    Issuedate = Complaint.objects.filter(id=cid).values('Time')

    for val in details:
            detail_string=("{}".format(val['Description']))
    for val in name:
            detailname=("User: {}".format(val['username']))
    #for val in Branch:
            #detailbranch=("Branch: {}".format(val['Branch']))
    for val in Subject:
            detailsubject=("Subject: {}".format(val['Subject'])) 
    for val in Type:
            detailtype=("Type of complaint: {}".format(val['Type_of_complaint']))
            
    for val in Issuedate:
            detailtime=("Time of Issue: {}".format(val['Time']))
    #detail_string = u", ".join(("Desc={}".format(val['Description'])) for val in details) 

    if detailtype=='1':
            detailtype="Type of Complaint: Technical"
    if detailtype=='3':
            detailtype="Type of Complaint: management"
    if detailtype=='2':
            detailtype="Type of Complaint: infrastructure"
    if detailtype=='4':
            detailtype="Type of Complaint: Department"
   

    p.drawString(25, 770,"Report:")
    p.drawString(30, 750,detailname)
    #p.drawString(30, 730,detailbranch)
    p.drawString(30, 710,detailtype)
    p.drawString(30, 690,detailtime)
    p.drawString(30, 670,detailsubject)
    p.drawString(30, 650,"Description:")
    p.drawString(30, 630,detail_string)

    p.showPage()
    p.save()
    return response




             


    