"""CollegeManagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from CollegeManagement import views
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home,name="homepage"),
    path('download-marksheet/', views.download_marksheet,name="downloadmarksheet"),
    path('study-material/', views.study_material,name="studymaterial"),
    path('all-staff/', views.all_staff,name="allstaff"),
    path('about-us', views.about_us,name="aboutus"),
    path('contact-us', views.contact_us,name="contactus"),
    path('add-review', views.addreview,name="addreview"),


      
    path('adminpanel/admin-home/', views.adminhome,name="adminhomepage"),
    path('adminpanel/', views.adminhome,name="adminhomepage"),
    path('adminpanel/all-reviews', views.allreviews,name="allreviews"),
    path('adminpanel/student/', views.student,name="student"),
    path('adminpanel/staff/', views.staff,name="staff"),
    path('adminpanel/profile/', views.profile,name="profile"),
    path('adminpanel/change-password/', views.changepassword,name="changepassword"),
    path('adminpanel/announcements/', views.announcements,name="announcements"),
    path('adminpanel/messages/', views.messages,name="messages"),
    path('adminpanel/add-staff/', views.addstaff,name="addstaff"),
    path('adminpanel/add-student/', views.addstudent,name="addstudent"),
    path('login-form/', views.loginform,name="loginform"),
    path('adminpanel/marksheet-data/', views.marksheetdata,name="marksheetdata"),
    path('adminpanel/marksheet-profile/', views.marksheetprofile,name="marksheetprofile"),
    path('adminpanel/add-marksheet/', views.addmarksheet,name="addmarksheet"),
    path('adminpanel/reply-message/<int:id>/', views.replymessage,name="replymessage"),
    path('adminpanel/staff-profile/', views.staffprofile,name="staffprofile"),
    path('delete-staff/<int:id>/', views.delete_staff, name='delete_staff'),
    path('adminpanel/student-profile/', views.studentprofile,name="studentprofile"),
    path('delete-student/<int:id>/', views.delete_student, name='delete_student'),
    path('adminpanel/students-data/', views.studentsdata,name="studentsdata"),
    path('adminpanel/study-materials/', views.studymaterials,name="studymaterials"),
    path('adminpanel/upload-document/', views.uploaddocument,name="uploaddocument"),


    path('staff/account-profile/', views.staffaccountprofile,name="staffaccountprofile"),
    path('staff/announcements/', views.staffannouncements,name="staffannouncements"),
    path('staff/add-student/', views.staffaddstudent,name="staffaddstudent"),
    path('staff/change-password/', views.staffchangepassword,name="staffchangepassword"),
    path('staff/', views.staffhome,name="staffhomepage"),
    path('staff/marksheet-data/', views.staffmarksheetdata,name="staffmarksheetdata"),
    path('staff/marksheet-profile/', views.staffmarksheetprofile,name="staffmarksheetprofile"),
    path('staff/add-marksheet/', views.staffaddmarksheet,name="staffaddmarksheet"),
    path('staff/messages/', views.staffmessages,name="staffmessages"),
    path('staff/reply-message/', views.staffreplymessage,name="staffreplymessage"),
    path('staff/student-profile/', views.staffstudentprofile,name="staffstudentprofile"),
    path('staff/student/', views.staffstudent,name="staffstudent"),
    path('staffdelete-student/<int:id>/', views.staffdelete_student, name='staffdelete_student'),
    path('staff/students-data/', views.staffstudentsdata,name="staffstudentsdata"),
    path('staff/study-materials-data/', views.staffstudymaterialsdata,name="staffstudymaterialsdata"),
    path('staff/upload-document/', views.staffuploaddocument,name="staffuploaddocument"),
    path('staff/reply-message/<int:id>/', views.staffreplymessage,name="staffreplymessage"),

    path('logout-admin/', views.logoutadmin,name="logout-admin"),
    path('logout-staff/', views.logoutstaff,name="logout-staff"),

    path('adminpanel/create-credentials/', views.createcredentials,name="createcredentials"),
    path('adminpanel/all-credentials/', views.allcredentials,name="allcredentials"),




    

]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
