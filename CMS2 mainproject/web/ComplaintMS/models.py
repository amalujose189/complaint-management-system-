from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import RegexValidator
from datetime import datetime


class Meta:

    app_label = 'ComplaintMS'
class Profile(models.Model):
    typeofuser =(('student','student'),('staff', 'staff'))
    dep=(('maths','maths'),('BCA','BCA'),('BCOM','BCOM'),('physcics','physics'),('English','English'),('FoodScience','FoodScience')) #change college names
    user =models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    department_name=models.CharField(max_length=50,default='maths',choices=dep,blank=False)
    type_of_user=models.CharField(max_length=50,default='student',choices=typeofuser)
    phone_regex =RegexValidator(regex=r'^\d{10,10}$', message="Phone number must be entered in the format:Up to 10 digits allowed.")
    contactnumber = models.CharField(validators=[phone_regex], max_length=10, blank=True) 
    def __str__(self):
        return self.dep_name
    def __str__(self):
        return self.user.username
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Complaint(models.Model):
    STATUS =((1,'Solved'),(2, 'InProgress'),(3,'Pending'))
    #TYPE=(('ClassRoom',"ClassRoom"),('Teacher',"Teacher"),('Management',"Management"),('College',"College"),('system',"system"),('college bus',"college bus"),('wiring',"wiring"),('water',"water"),('student',"student"),('parking',"parking"),('Other',"Other"))
    TYPE=(('Technical',"Technical"),('management',"management"),('infrastructure',"infrastructure"),('Department',"Department"))
    #staff=(('anu',"anu"),('suhail',"suhail"),('sandya',"sandya"))
    #assignto=models.CharField(max_length=200)
    assignto = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_complaints', null=True, blank=True)
    Subject=models.CharField(max_length=200,blank=False,null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="user")
    
    Type_of_complaint=models.CharField(choices=TYPE,max_length=200)
    Description=models.TextField(max_length=4000,blank=False,null=True)
    Time = models.DateField(auto_now=True)
    status=models.IntegerField(choices=STATUS,default=3)
    Reply=models.TextField(max_length=1000,null=True,blank=True)
    staff_reply=models.TextField(max_length=1000,null=True)
   
    def __init__(self, *args, **kwargs):
        super(Complaint, self).__init__(*args, **kwargs)
        self.__status = self.status

    def save(self, *args, **kwargs):
        if self.status and not self.__status:
            self.active_from = datetime.now()
        super(Complaint, self).save(*args, **kwargs)
    
    def __str__(self):
     	return self.get_Type_of_complaint_display()
     

   

                                                                                                                                                                                        