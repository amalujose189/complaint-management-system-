

from django.contrib import admin
from .models import Profile,Complaint
from .forms import ComplaintForm
from .models import User
from django import forms


class ComplaintAdmin(admin.ModelAdmin):
    form = ComplaintForm
    

    list_display = ('user','id', 'Subject', 'Type_of_complaint', 'Description', 'Time', 'status','assignto','Reply')
    #fields=('user', 'Subject', 'Type_of_complaint', 'Description','assignto','Reply')
    fields=['user','Subject','Type_of_complaint','Description','status','assignto','Reply']
    list_filter = ('Type_of_complaint', 'status')
    #search_fields = ('Subject', 'Description', 'assignto__username', 'user__username')
    ordering = ('-id',)

    #actions = ['mark_as_solved', 'mark_as_in_progress', 'assign_to_staff']
    actions = ['mark_as_solved', 'mark_as_in_progress']

    def mark_as_solved(self, request, queryset):
        queryset.update(status=1)

    mark_as_solved.short_description = 'Mark selected complaints as solved'

    def mark_as_in_progress(self, request, queryset):
        queryset.update(status=2)

    mark_as_in_progress.short_description = 'Mark selected complaints as in progress'
    

    def assign_to_staff(self, request, queryset):
        selected_staff = request.POST.getlist('staff')
        if selected_staff:
            staff_usernames = [User.objects.get(id=id).username for id in selected_staff]
            queryset.update(assignto__username__in=staff_usernames)

    assign_to_staff.short_description = 'Assign selected complaints to staff'

    
admin.site.register(Profile)
admin.site.register(Complaint,ComplaintAdmin)
admin.site.site_title="Complaint management system"
admin.site.site_header="CMS Admin"
'''from django.contrib import admin
from .models import Profile,Complaint



# Register your models here.
class CAdmin(admin.ModelAdmin):
    list_display = ['user','Subject','Description','Time','status']

admin.site.register(Profile)
admin.site.register(Complaint,CAdmin)
(1)
class ComplaintAdmin(admin.ModelAdmin):
    form = ComplaintForm
    list_display = ('id', 'Subject', 'Type_of_complaint', 'assignto')
    list_filter = ('Type_of_complaint',)
    search_fields = ('Subject', 'Description', 'assignto__username')
    ordering = ('-id',)

# Register your models here.
class CAdmin(admin.ModelAdmin):
    model=Complaint
    #fields=['user','Subject','Type_of_complaint','Description','status','assignto','Reply']
    list_display = ['user','Subject','Description','Time','status']
   

admin.site.register(Profile)
admin.site.register(Complaint,ComplaintAdmin)
admin.site.site_title="Complaint management system"
admin.site.site_header="CMS Admin"

assignto = forms.ModelChoiceField(
        queryset=User.objects.filter(profile__type_of_user='staff').order_by('first_name'),
        to_field_name='first_name',
        label='Assign To',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    assignto = forms.ModelChoiceField(
         queryset=User.objects.filter(profile__type_of_user='staff')
        .annotate(full_name=Concat(Upper('first_name'), Value(' '), Upper('last_name')))
        .annotate(name_without_spaces=Replace('full_name', Value(' '), Value('')))
        .values_list('id', 'name_without_spaces'),
        widget=forms.Select(attrs={'class':'form-control'})
    )'''  