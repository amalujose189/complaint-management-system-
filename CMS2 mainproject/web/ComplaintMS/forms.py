from django import forms
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import DateInput
from django.shortcuts import render, redirect
from .models import Profile, Complaint
from django.db.models import CharField, Value
from django.db.models.functions import Concat, Replace, Upper

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
import requests


class UserProfileform(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('department_name', 'contactnumber', 'type_of_user')


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2', )

    def clean_email(self):
        # Get the email
        email = self.cleaned_data.get('email')

        # Check to see if any users already exist with this email as a username.
        try:
            match = User.objects.get(email=email)
        except User.DoesNotExist:
            # Unable to find a user, this is fine
            return email

        # A user was found with this as a username, raise an error.
        raise forms.ValidationError('This email address is already in use.')


'''class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'location',)'''


class ProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'readonly': 'readonly'}))
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        labels = {'username': "username", 'email': "email",
                  'first_name': "first_name", 'last_name': "last_name"}

    def clean_email(self):
        # Get the email
        username = self.cleaned_data.get('email')

        # Check to see if any users already exist with this email as a username.
        try:
            match = User.objects.exclude(
                pk=self.instance.pk).get(username=username)

        except User.DoesNotExist:
            # Unable to find a user, this is fine
            return username

        # A user was found with this as a username, raise an error.
        raise forms.ValidationError('This email address is already in use.')


class UserProfileUpdateform(forms.ModelForm):

    department_name = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    type_of_user = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
   

    class Meta:
        model = Profile
        fields = ('department_name','contactnumber', 'type_of_user')
        labels = {'first_name': 'First Name', 'last_name': 'Last Name','contactnumber':'contact number'}
'''class UserProfileUpdateform(forms.ModelForm):

    department_name = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    type_of_user = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
   

    class Meta:
        model = Profile
        fields = ('department_name', 'contactnumber', 'type_of_user')
        labels = {'first_name': 'First Name', 'last_name': 'Last Name', 'contactnumber': 'Contact Number'}
class UserProfileUpdateform(forms.ModelForm):
    department_name = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    type_of_user = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    email = forms.EmailField(label='Email')

    class Meta:
        model = Profile
        fields = ('department_name', 'contactnumber', 'type_of_user', 'user__first_name', 'user__last_name', 'user__email')
        labels = {
            'user__first_name': 'First Name', 
            'user__last_name': 'Last Name', 
            'contactnumber': 'Contact Number',
            'user__email': 'Email'
        }'''
class ComplaintChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.first_name

class ComplaintForm(forms.ModelForm):
    
    assignto = ComplaintChoiceField(
           queryset=User.objects.filter(profile__type_of_user='staff').order_by('first_name'),
           to_field_name='first_name',
           label='Assign To',
           widget=forms.Select(attrs={'class':'form-control'})
    )
    class Meta:
        model = Complaint
        fields = ["Subject", "Type_of_complaint", "Description","assignto"]
    '''def _init_(self, *args, **kwargs):
        super(ComplaintForm, self)._init_(*args, **kwargs)
        # Set custom label for bus_operator field
        self.fields['assignto'].label_from_instance = lambda obj: obj.first_name
        self.fields['assignto'].label = 'assignto'  '''  
'''class ComplaintForm(forms.ModelForm):        
    class Meta:
        model = Complaint

        fields = ["Subject", "Type_of_complaint", "Description","assignto"]
        labels = {'subject': "subject",'Type_of_complaint':"Type_of_complaint",'Description':"Description",'assignto':"Assign to"}
        
    
    assignto = forms.ModelChoiceField(
           queryset=User.objects.filter(profile__type_of_user='staff').order_by('first_name'),
           to_field_name='first_name',
           label='Assign To',
           widget=forms.Select(attrs={'class':'form-control'})
    )'''
    
    
    
    
    
'''
        # If the user is an admin, include the assignto field and override the queryset
            if user.is_superuser:
                self.fields['assignto']  = forms.ModelChoiceField(
                    queryset=User.objects.filter(profile__type_of_user='staff').order_by('first_name'),
                    to_field_name='username',
                    label='Assign To',
                    widget=forms.Select(attrs={'class':'form-control'})
                )
                self.fields['assignto'] = forms.ModelChoiceField(
                queryset=User.objects.filter(profile__type_of_user='staff').order_by('first_name'),
                label='Assign To',
                widget=forms.Select(attrs={'class':'form-control'})
               
            )
            self.fields['assignto'].to_field_name = 'username'
            self.fields['assignto'].queryset = User.objects.filter(profile__type_of_user='staff').order_by('first_name')

    
    assignto = forms.ModelChoiceField(
           queryset=User.objects.filter(profile__type_of_user='staff').order_by('first_name'),
           to_field_name='username',
           label='Assign To',
           widget=forms.Select(attrs={'class':'form-control'})
    )
    assignto = forms.ModelChoiceField(
         queryset=User.objects.filter(profile__type_of_user='staff')
        .annotate(full_name=Concat(Upper('first_name'), Value(' '), Upper('last_name')))
        .annotate(name_without_spaces=Replace('full_name', Value(' '), Value('')))
        .values_list('id', 'name_without_spaces'),
        widget=forms.Select(attrs={'class':'form-control'})
    ) 
      
    assignto = forms.ModelChoiceField(
    queryset=User.objects.filter(profile__type_of_user='staff'),
    widget=forms.Select(attrs={'class':'form-control'})
    )

                


class Assignto(forms.Form):
    assignto= forms.ModelChoiceField(queryset=User.objects.filter(groups__name='Staff'))


class Assignto(forms.ModelForm):
    assignto = forms.ModelChoiceField(queryset=Profile.objects.filter(type_of_user='staff'),label = 'assign complaint')

    class Meta:
        model = Complaint
        fields = ['assignto']


class ComplaintCreateView(CreateView):
    class Meta:
         model = Complaint
         form_class = Assignto
         #template_name = 'ComplaintMS/addComplaintMS.html'
         fields=('assignto',)
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form) 
 '''


class statusupdate(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ('status',)
        help_texts = {
            'status': None,

        }
