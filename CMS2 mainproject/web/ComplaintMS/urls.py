
from django.conf.urls import url
from . import views
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns=[
    url(r'^$',views.index,name='index'),
    url(r'^aboutus/$',views.aboutus,name='aboutus'),
    url(r'^register/$', views.register, name='register'),
    url(r'^signin/$',auth_views.LoginView.as_view(template_name='ComplaintMS/signin.html'), name='signin'),
    url('logout/', auth_views.LogoutView.as_view(template_name='ComplaintMS/logout.html'), name='logout'),
    url(r'^addComplaintMS/$', views.complaints, name='complaints'),
    #url('addComplaintstaff/$', views.complaint1, name='complaint1'),
    url(r'^login/$',views.login,name='login'),
    url(r'^login_redirect/$',views.login_redirect,name='login_redirect'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^slist/$',views.slist,),
    url(r'^counter/$', views.counter, name='counter'),
    url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'^change_password_staff/$', views.change_password_staff, name='change_password_staff'),
    url(r'^list/$', views.list, name='list'),
    url(r'^delete/(?P<id>\d+)/$', views.delete, name='delete'),
    
    url(r'^solved/$', views.solved, name='solved'),
    url(r'^allcomplaints/$', views.allcomplaints, name='allcomplaints'),
    url(r'^profile/$', views.dashboard, name='profile'),
    url(r'^statistics/$', views.statistics, name='statistics'),
   # url(r'^complaintsstaff/$',views.complaintsstaff,name="complaints_staff"),
    url(r'^pdf/$',views.pdf_view,name='view'),
    url(r'^pdf_g/$',views.pdf_viewer,name='view'),
    url('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='ComplaintMS/password_reset.html'
         ),
         name='password_reset'),
    url(r'^password-reset-done/$',
         auth_views.PasswordResetDoneView.as_view(
             template_name='ComplaintMS/password_reset_done.html'
         ),
         name='password_reset_done'),
    url(r'^password-reset-confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='ComplaintMS/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    url(r'^password-reset-complete/$',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='ComplaintMS/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    
   ]
