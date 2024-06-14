from django.http import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import *
from slideshow.models import *
from courses.models import courses
from reviews.models import *
from studymaterial.models import *
from allstaffdatabase.models import *
from allstudentdata.models import *
from allmessages.models import *
from allannouncements.models import *
from reviews.models import *
from staffusers.models import *
from adminusers.models import *
from marksheetdata.models import marksheetdata as marksheet1
from django.urls import reverse
from django.core.mail import send_mail
from CollegeManagement import settings
from django.core.exceptions import ObjectDoesNotExist
import os




#User Section
def home(request):
    imagesobj = slideshow.objects.all()
    coursesobj = courses.objects.all()
    reviewsobj = reviews.objects.all().order_by('-id')[:3]
    announcements_obj=allannouncements.objects.all().order_by('category')


    images = [image.file.url for image in imagesobj]  # Ensure the image URLs are correct
    course = []
    for c in coursesobj:
        course.append((c.icon.url, c.detail))  # Append as tuples

    review = []
    for r in reviewsobj:
        review.append((r.photo.url, r.name, r.review, r.rating))
    data = {'images': images, "courses": course, "reviews": review,'title':'HomePage','announcements':announcements_obj}
    return render(request, "index.html", data)


def download_marksheet(request):
    show = False
    data = {'show': show,'title':'Download Marksheet'}

    if request.method == "POST":
        year = request.POST.get('year')
        enrollment = request.POST.get('enrollment')
        try:
            marksheet = get_object_or_404(marksheet1, year=year, enrollment=enrollment)
            if marksheet.total_marks > 0:
                marksheet.percentage = (marksheet.total_marks_obtained / marksheet.total_marks) * 100
            else:
                marksheet.percentage = 0
            show = True
            data = {'result': marksheet, 'show': show,'title':'Download Marksheet'}
        except Http404:
            data = {'show': show, 'error_message': 'Marksheet not found','title':'Download Marksheet'}

    return render(request, "downloadmarksheet.html", data)


def study_material(request):
    study_materials = studymaterial.objects.all().order_by('department');
    ai=[]
    ce=[]
    me=[]
    cv=[]
    ee=[]
    it=[]
    for sm in study_materials:
        
        
        dept=sm.department
        if dept=='Artificial Intelligence Department':
            ai.append(sm)
        elif dept=='Information Technology Department':
            it.append(sm)
        elif dept=='Computer Engineering Department':
            ce.append(sm)
        elif dept=='Mechanical Engineering Department':
            me.append(sm)
        elif dept=='Civil Engineering Department':
            cv.append(sm)
        elif dept=='Electrical Engineering Department':
            ee.append(sm)
    
    data={'ai':ai,'it':it,'ce':ce,'me':me,'ee':ee,'cv':cv,'title':'Study Material'}
    
    return render(request,"studymaterial.html/",data)

def all_staff(request):
    staff_obj = allstaffdatabase.objects.all().order_by('department');
    top=[]
    top2=[]
    staff=[]

    for i in staff_obj:
        if "Principal" in i.designation:
            top.append(i)
        elif "HOD" in i.designation:
            top2.append(i)
        elif "Head Of Department" in i.designation:
            top2.append(i)
        else:
            staff.append(i)
    data={'top':top,'top2':top2,'staff':staff,'title':'All Staff'}
    return render(request,"staff.html/",data)

def about_us(request):
    return render(request,"aboutus.html/",{'title':'About Us'})

def contact_us(request):
    if request.method == 'POST':
            name=request.POST.get('name')
            email=request.POST.get('email')
            message=request.POST.get('message')
            message_obj=allmessages(name=name,email=email,message=message,read=False)
            message_obj.save()
            
    return render(request,"contactus.html/",{'title':'Contact Us'})

def addreview(request):
    if request.method == "POST":
        photo = request.FILES.get('photo') 
        name = request.POST.get('name')
        stars = request.POST.get('stars')
        review = request.POST.get('review')
        rev=reviews(photo=photo,name=name,rating=stars,review=review)
        rev.save()
        request.POST=[]
    reviews_obj=reviews.objects.all().order_by('-rating')[:16]
    data={'reviews':reviews_obj,'title':'Add Review '}
    return render(request,'add-review.html',data)


#Admin Section

def adminhome(request):
    if 'admin_user' not in request.session:
        return redirect('loginform')
    studentsno=allstudentdata.objects.count()
    announcementsno=allannouncements.objects.count()
    messagesno=allmessages.objects.count()
    reviewsno=reviews.objects.count()
    data={'students':studentsno,'announcements':announcementsno,'messages':messagesno,'reviews':reviewsno,'title':'Admin Homepage'}
    return render(request,"admin2/index.html",data)

def student(request):
    if 'admin_user' not in request.session:
        return redirect('loginform')
    #no implementation needed
    return render(request,"admin2/student.html",{'title':'Student'})

def staff(request):
    if 'admin_user' not in request.session:
        return redirect('loginform')
    staff_list = allstaffdatabase.objects.all().order_by('department')
    paginator = Paginator(staff_list, 10)  # Show 10 students per page.
    page_number = request.GET.get('page')
    staff_obj = paginator.get_page(page_number)
    context = {"staff": staff_obj,'title':'Staff'}
    return render(request,"admin2/staff-data.html",context)

def profile(request):
    #for future
    if 'admin_user' not in request.session:
        return redirect('loginform')
    return render(request,"admin2/account-profile.html",{'title':'Profile'})

def changepassword(request):
    #for future
    if 'admin_user' not in request.session:
        return redirect('loginform')
    return render(request,"admin2/change-password.html",{'title':'Change Password'})

def allreviews(request):
    if 'admin_user' not in request.session:
        return redirect('loginform')
    if request.method == "POST":
        id = request.POST.get('id')
        try:
            obj = reviews.objects.get(id=id)
            
            # Delete the associated photo file from the server directory
            if obj.photo:
                photo_path = obj.photo.path
                if os.path.exists(photo_path):
                    os.remove(photo_path)
            
            obj.delete()
            return redirect('allreviews')
        except reviews.DoesNotExist:
            pass  # Object with the given ID does not exist, do nothing
    
    reviews_data = reviews.objects.all().order_by('-rating')
    paginator = Paginator(reviews_data, 5)  # Show 5 reviews per page

    page = request.GET.get('page')
    try:
        reviews_data = paginator.page(page)
    except PageNotAnInteger:
        reviews_data = paginator.page(1)
    except EmptyPage:
        reviews_data = paginator.page(paginator.num_pages)
    
    data = {'reviews': reviews_data, 'title': 'All Reviews'}
    return render(request, 'admin2/all-reviews.html', data)

def announcements(request):
    if 'admin_user' not in request.session:
        return redirect('loginform')
    if request.method == "POST":
        if 'announcement' in request.POST:
            category = request.POST.get('category')
            announcement = request.POST.get('announcement')
            date = request.POST.get('date', timezone.now().date())
            new_announcement = allannouncements(category=category, announcement=announcement, date=date)
            new_announcement.save()
        elif 'id' in request.POST:
            announcement_id = request.POST.get('id')
            obj = get_object_or_404(allannouncements, id=announcement_id)
            obj.delete()
    announcements_list = allannouncements.objects.all().order_by("id")
    paginator = Paginator(announcements_list, 5)
    page = request.GET.get('page')
    try:
        announcements_list = paginator.page(page)
    except PageNotAnInteger:
        announcements_list = paginator.page(1)
    except EmptyPage:
        announcements_list = paginator.page(paginator.num_pages)
    data = {'announcements': announcements_list,'title':'All Announcements'}
    return render(request,"admin2/announcements.html",data)


def messages(request):
    if 'admin_user' not in request.session:
        return redirect('loginform')
    if request.method == "GET" and 'id' in request.GET:
        msg_id = request.GET.get('id')
        msg = get_object_or_404(allmessages, id=msg_id)
        msg.read = True
        msg.save()
    if request.method == "POST" and 'id' in request.POST:
        msg_id = request.POST.get('id')
        msg = get_object_or_404(allmessages, id=msg_id)
        msg.delete()
    messages=allmessages.objects.all().order_by("read")
    paginator = Paginator(messages, 5)  # Show 5 messages per page

    page = request.GET.get('page')
    try:
        messages = paginator.page(page)
    except PageNotAnInteger:
        messages = paginator.page(1)
    except EmptyPage:
        messages = paginator.page(paginator.num_pages)
    data={'messages':messages,'title':'All Messages'}
    return render(request,"admin2/messages.html",data)

def addstaff(request):
    if 'admin_user' not in request.session:
        return redirect('loginform')
    if request.method == "POST":
        photo = request.FILES.get('photo')  # Use request.FILES for file uploads
        name = request.POST.get('name')
        department = request.POST.get('dept')
        designation = request.POST.get('designation')
        contact = request.POST.get('contact')
        aadhar = request.POST.get('aadharno')
        address = request.POST.get('address')
        
        try:
            staff = allstaffdatabase(
                photo=photo,
                name=name,
                department=department,
                designation=designation,
                contact=contact,
                aadhar_no=aadhar,
                addressline=address
            )
            staff.save()
            # Handle file saving if needed
            # For example: student.photo.save(photo.name, photo)
        except Exception as e:
            # Handle exception appropriately
            print(e)
    return render(request,"admin2/add-staff.html",{'title':'Add Staff'})


def addstudent(request):
    if 'admin_user' not in request.session:
        return redirect('loginform')
    if request.method == "POST":
        photo = request.FILES.get('photo')  # Use request.FILES for file uploads
        name = request.POST.get('name')
        enrollment = request.POST.get('enrollment')
        department = request.POST.get('dept')
        dob = request.POST.get('dob')
        cast = request.POST.get('cast')
        selfcontact = request.POST.get('contact1')
        parentcontact = request.POST.get('contact2') 
        aadhar = request.POST.get('aadharno')
        address = request.POST.get('address')
        
        try:
            student = allstudentdata(
                photo=photo,
                name=name,
                enrollment=enrollment,
                department=department,
                dob=dob,
                cast=cast,
                selfcontact=selfcontact,
                parentcontact=parentcontact,
                aadhar=aadhar,
                address=address
            )
            student.save()
            # Handle file saving if needed
            # For example: student.photo.save(photo.name, photo)
        except Exception as e:
            # Handle exception appropriately
            print(e)
    return render(request, "admin2/add-student.html",{'title':'Add Student'})

def loginform(request):
    
    data={'title':'Login','error':False}
    if 'staff_submit' in request.POST:
        username=request.POST.get('staffusername')
        password=request.POST.get('staffpassword')
        try:
            obj=staffusers.objects.get(username=username,password=password)
            if obj:
                request.session['staff_user']=username
                return staffhome(request)
            else:
                data={'title':'Login','error':True}
        except:
            data={'title':'Login','error':True}

    elif 'admin_submit' in request.POST:
        username=request.POST.get('adminusername')
        password=request.POST.get('adminpassword')
        try:
            obj=adminusers.objects.get(username=username,password=password)
            if obj:
                request.session['admin_user']=username
                return adminhome(request)
            else:
                data={'title':'Login','error':True}
        except:
                data={'title':'Login','error':True}
    return render(request,"login-form.html",data)

def marksheetdata(request):
    if 'admin_user' not in request.session:
        return redirect('loginform')
    if request.method == "POST":
        id = request.POST.get('id')
        marksheet = get_object_or_404(marksheet1, id=id)
        marksheet.delete()

    marksheetdatas = marksheet1.objects.all().order_by('year', 'enrollment')
    
    for marksheet in marksheetdatas:
        if marksheet.total_marks > 0:
            marksheet.percentage = (marksheet.total_marks_obtained / marksheet.total_marks) * 100
        else:
            marksheet.percentage = 0

    paginator = Paginator(marksheetdatas, 10)
    page = request.GET.get('page')
    try:
        marksheetdatas = paginator.page(page)
    except PageNotAnInteger:
        marksheetdatas = paginator.page(1)
    except EmptyPage:
        marksheetdatas = paginator.page(paginator.num_pages)
    
    data = {"marksheets": marksheetdatas,'title':'Marksheet Data'}
    return render(request, "admin2/marksheet-data.html", data)

def marksheetprofile(request):
    if 'admin_user' not in request.session:
        return redirect('loginform')
    id = request.GET.get('id')
    marksheet = get_object_or_404(marksheet1, id=id)
    data={"marksheet":marksheet,'title':'Marksheet Profile'}
    return render(request,"admin2/marksheet-profile.html",data)


def addmarksheet(request):
    if 'admin_user' not in request.session:
        return redirect('loginform')
    if request.method == "POST":
        name = request.POST.get('name')
        enrollment = request.POST.get('enrollment')
        department = request.POST.get('department')
        year = request.POST.get('year')
        result = request.POST.get('result')
        total_marks = request.POST.get('total_marks')
        total_marks_obtained = request.POST.get('total_marks_obtained')
        data=marksheet1(name=name,enrollment=enrollment,department=department,year=year,result=result,total_marks=total_marks,total_marks_obtained=total_marks_obtained)
        data.save()
        

    return render(request,'admin2/add-marksheet.html',{'title':'Add Marksheet'})


def replymessage(request,id):
    if 'admin_user' not in request.session:
        return redirect('loginform')
    if request.method == "POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        message=request.POST.get('message')
        subject = f'Reply to: {email}'
        messagebody = request.POST.get('replymessage')
        
        try:
            send_mail(subject, messagebody, settings.EMAIL_HOST_USER, [email])
            print('message sent')
        except Exception as e:
            return HttpResponseServerError(f"An error occurred: {e}")
    msg_obj=allmessages.objects.get(id=id)
    data={'message':msg_obj,'title':'Reply Message'}
    return render(request,"admin2/reply-message.html",data)
    
def staffprofile(request):
    if 'admin_user' not in request.session:
        return redirect('loginform')
    
    staff_obj = get_object_or_404(allstaffdatabase, id=request.GET.get('id'))
    
    if request.method == 'POST':
        staff_obj.name = request.POST.get('name')
        staff_obj.designation = request.POST.get('designation')
        staff_obj.department = request.POST.get('department')
        staff_obj.aadhar_no = request.POST.get('aadhar_no')
        staff_obj.contact = request.POST.get('contact')
        staff_obj.addressline = request.POST.get('addressline')
        
        staff_obj.save()
        # Adjust according to your URL naming
    
    data = {"staff": staff_obj, 'title': 'Staff Profile'}
    return render(request, "admin2/staff-profile.html", data)

def studentprofile(request):
    update=False
    if 'admin_user' not in request.session:
        return redirect('loginform')
    data={}
    if request.method == "POST":
        student = get_object_or_404(allstudentdata, id=request.POST.get('id'))
        student.name = request.POST.get('name')
        student.enrollment = request.POST.get('enrollment')
        student.department = request.POST.get('department') 
        student.cast = request.POST.get('cast')
        student.selfcontact = request.POST.get('selfcontact')
        student.parentcontact = request.POST.get('parentcontact')
        student.aadhar = request.POST.get('aadhar')
        student.address = request.POST.get('address')
        student.save()
        update=True
        

    student_obj=allstudentdata.objects.get(id=request.GET.get('id'))
    data={"student":student_obj,'title':'Student Profile'}
    if update:
        data['message']="Data Updated"
    return render(request,"admin2/student-profile.html",data)

def delete_student(request, id):
    student = get_object_or_404(allstudentdata, id=id)
    
    # Delete the photo from the server directory
    if student.photo:
        photo_path = student.photo.path
        if os.path.exists(photo_path):
            os.remove(photo_path)
    
    # Delete the student instance
    student.delete() 
    
    return studentsdata(request)

def delete_staff(request, id):
    staff1 = get_object_or_404(allstaffdatabase, id=id)
    
    # Delete the photo from the server directory
    if staff1.photo:
        photo_path = staff1.photo.path
        if os.path.exists(photo_path):
            os.remove(photo_path)
    
    # Delete the staff instance
    staff1.delete() 
    
    return staff(request)

def studentsdata(request):
    if 'admin_user' not in request.session:
        return redirect('loginform')
    students_list = allstudentdata.objects.all().order_by('enrollment')
    paginator = Paginator(students_list, 10)  # Show 10 students per page.

    page_number = request.GET.get('page')
    students_obj = paginator.get_page(page_number)

    context = {"students": students_obj,'title':'Students'}
    return render(request, "admin2/students-data.html", context)


def studymaterials(request):
    if 'admin_user' not in request.session:
        return redirect('loginform')
    if request.method == "POST":
        id = request.POST.get('id')
        try:
            obj = studymaterial.objects.get(id=id)
            # Delete the file from the server directory
            if obj.file:
                file_path = obj.file.path
                if os.path.exists(file_path):
                    os.remove(file_path)
            obj.delete()
        except ObjectDoesNotExist:
            pass  # Object with the given ID does not exist, do nothing
    
    material_obj = studymaterial.objects.all().order_by('department')
    paginator = Paginator(material_obj, 5)
    page = request.GET.get('page')
    try:
        material_obj = paginator.page(page)
    except PageNotAnInteger:
        material_obj = paginator.page(1)
    except EmptyPage:
        material_obj = paginator.page(paginator.num_pages)
    data = {'materials': material_obj,'title':'Study Materials'}
    return render(request, "admin2/study-materials-data.html", data)

def uploaddocument(request):
    if 'admin_user' not in request.session:
        return redirect('loginform')
    if request.method == "POST":
        name = request.POST.get('name')
        dept = request.POST.get('dept')
        file = request.FILES['file']  # Use request.FILES to access uploaded files
        obj = studymaterial(filename=name, file=file, department=dept)
        obj.save()
    return render(request, "admin2/upload-document.html",{'title':'Upload Document'})


#Staff Section

def staffaccountprofile(request):
    if 'staff_user' not in request.session:
        return redirect('loginform')
    return render(request,'staff/account-profile.html',{'title':'Profile'})

def staffaddstudent(request):
    if 'staff_user' not in request.session:
        return redirect('loginform')
    if request.method == "POST":
        photo = request.FILES.get('photo')  # Use request.FILES for file uploads
        name = request.POST.get('name')
        enrollment = request.POST.get('enrollment')
        department  = request.POST.get('dept')
        dob = request.POST.get('dob')
        cast = request.POST.get('cast')
        selfcontact = request.POST.get('contact1')
        parentcontact = request.POST.get('contact2') 
        aadhar = request.POST.get('aadharno')
        address = request.POST.get('address')
        
        try:
            student = allstudentdata(
                photo=photo,
                name=name,
                enrollment=enrollment,
                department=department,
                dob=dob,
                cast=cast,
                selfcontact=selfcontact,
                parentcontact=parentcontact,
                aadhar=aadhar,
                address=address
            )
            student.save()
            # Handle file saving if needed
            # For example: student.photo.save(photo.name, photo)
        except Exception as e:
            # Handle exception appropriately
            print(e)
    return render(request,"staff/add-student.html",{'title':'Add Student'})

def staffchangepassword(request):
    if 'staff_user' not in request.session:
        return redirect('loginform')
    return render(request,'staff/change-password.html',{'title':'Change Password'})


def staffhome(request):
    if 'staff_user' not in request.session:
        return redirect('loginform')
    studentsno=allstudentdata.objects.count()
    announcementsno=allannouncements.objects.count()
    messagesno=allmessages.objects.count()
    data={'students':studentsno,'announcements':announcementsno,'messages':messagesno,'title':'Staff Homepage'}
    return render(request,'staff/index.html',data)

def staffmarksheetdata(request):
    if 'staff_user' not in request.session:
        return redirect('loginform')
    if request.method == "POST":
        id = request.POST.get('id')
        marksheet = get_object_or_404(marksheet1, id=id)
        marksheet.delete()

    marksheetdatas = marksheet1.objects.all().order_by('year', 'enrollment')
    
    for marksheet in marksheetdatas:
        if marksheet.total_marks > 0:
            marksheet.percentage = (marksheet.total_marks_obtained / marksheet.total_marks) * 100
        else:
            marksheet.percentage = 0

    paginator = Paginator(marksheetdatas, 10)
    page = request.GET.get('page')
    try:
        marksheetdatas = paginator.page(page)
    except PageNotAnInteger:
        marksheetdatas = paginator.page(1)
    except EmptyPage:
        marksheetdatas = paginator.page(paginator.num_pages)
    
    data = {"marksheets": marksheetdatas,'title':'Marksheets'}
    return render(request,'staff/marksheet-data.html',data)

def staffmarksheetprofile(request):
    if 'staff_user' not in request.session:
        return redirect('loginform')
    id = request.GET.get('id')
    marksheet = get_object_or_404(marksheet1, id=id)
    data={"marksheet":marksheet,'title':'Marksheet Profile'}
    return render(request,'staff/marksheet-profile.html',data)


def staffmessages(request):
    if 'staff_user' not in request.session:
        return redirect('loginform')
    if request.method == "GET" and 'id' in request.GET:
        msg_id = request.GET.get('id')
        msg = get_object_or_404(allmessages, id=msg_id)
        msg.read = True
        msg.save()
    if request.method == "POST" and 'id' in request.POST:
        msg_id = request.POST.get('id')
        msg = get_object_or_404(allmessages, id=msg_id)
        msg.delete()
    messages=allmessages.objects.all().order_by("read")
    paginator = Paginator(messages, 5)  # Show 5 messages per page

    page = request.GET.get('page')
    try:
        messages = paginator.page(page)
    except PageNotAnInteger:
        messages = paginator.page(1)
    except EmptyPage:
        messages = paginator.page(paginator.num_pages)
    data={'messages':messages,'title':'Messages'}
    return render(request,'staff/messages.html',data)

def staffreplymessage(request,id):
    if 'staff_user' not in request.session:
        return redirect('loginform')
    if request.method == "POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        message=request.POST.get('message')
        subject = f'Reply to: {email}'
        messagebody = request.POST.get('replymessage')
        
        try:
            send_mail(subject, messagebody, settings.EMAIL_HOST_USER, [email])
            print('message sent')
        except Exception as e:
            return HttpResponseServerError(f"An error occurred: {e}")
    msg_obj=allmessages.objects.get(id=id)
    data={'message':msg_obj,'title':'Reply Message'}
    return render(request,'staff/reply-message.html',data)
def staffstudentprofile(request):
    if 'staff_user' not in request.session:
        return redirect('loginform')

    student_id = request.GET.get('id')
    student_obj = get_object_or_404(allstudentdata, id=student_id)

    if request.method == 'POST':
        student_obj.name = request.POST.get('name')
        student_obj.enrollment = request.POST.get('enrollment')
        student_obj.department = request.POST.get('department')
        student_obj.cast = request.POST.get('cast')
        student_obj.selfcontact = request.POST.get('selfcontact')
        student_obj.parentcontact = request.POST.get('parentcontact')
        student_obj.aadhar = request.POST.get('aadhar')
        student_obj.address = request.POST.get('address')
        
        student_obj.save() 

    data = {"student": student_obj, 'title': 'Student Profile'}
    return render(request, 'staff/student-profile.html', data)

def staffdelete_student(request, id):
    if 'staff_user' not in request.session:
        return redirect('loginform')
    student = get_object_or_404(allstudentdata, id=id)
    
    # Delete the associated photo file from the server directory
    if student.photo:
        photo_path = student.photo.path
        if os.path.exists(photo_path):
            os.remove(photo_path)
    
    student.delete()
    
    # Redirect to the appropriate page
    return redirect('staffstudentsdata')

def staffstudent(request):
    if 'staff_user' not in request.session:
        return redirect('loginform')
    return render(request,'staff/student.html',{'title':'Student'})

def staffstudentsdata(request):
    if 'staff_user' not in request.session:
        return redirect('loginform')
    students_list = allstudentdata.objects.all().order_by('enrollment')
    paginator = Paginator(students_list, 10)  # Show 10 students per page.

    page_number = request.GET.get('page')
    students_obj = paginator.get_page(page_number)

    context = {"students": students_obj,'title':'Students'}
    return render(request,'staff/students-data.html',context)



def staffstudymaterialsdata(request):
    if 'staff_user' not in request.session:
        return redirect('loginform')
    if request.method == "GET":
        id = request.GET.get('id')
        try:
            obj = studymaterial.objects.get(id=id)
            # Delete the associated file from the server directory
            if obj.file:
                file_path = obj.file.path
                if os.path.exists(file_path):
                    os.remove(file_path)
            obj.delete()
        except studymaterial.DoesNotExist:
            pass  # Object with the given ID does not exist, do nothing
    
    material_obj = studymaterial.objects.all().order_by('department')
    paginator = Paginator(material_obj, 5)
    page = request.GET.get('page')
    try:
        material_obj = paginator.page(page)
    except PageNotAnInteger:
        material_obj = paginator.page(1)
    except EmptyPage:
        material_obj = paginator.page(paginator.num_pages)
    data = {'materials': material_obj, 'title': 'Study Materials'}
    return render(request, 'staff/study-materials-data.html', data)


def staffuploaddocument(request):
    if 'staff_user' not in request.session:
        return redirect('loginform')
    if request.method == "POST":
        name = request.POST.get('name')
        dept = request.POST.get('dept')
        file = request.FILES['file']  # Use request.FILES to access uploaded files
        obj = studymaterial(filename=name, file=file, department=dept)
        obj.save()
    return render(request,'staff/upload-document.html',{'title':'Upload Document'})

def staffannouncements(request):
    if 'staff_user' not in request.session:
        return redirect('loginform')
    if request.method == "POST":
        if 'announcement' in request.POST:
            category = request.POST.get('category')
            announcement = request.POST.get('announcement')
            date = request.POST.get('date', timezone.now().date())
            new_announcement = allannouncements(category=category, announcement=announcement, date=date)
            new_announcement.save()
        elif 'id' in request.POST:
            announcement_id = request.POST.get('id')
            obj = get_object_or_404(allannouncements, id=announcement_id)
            obj.delete()
    announcements_list = allannouncements.objects.all().order_by("id")
    paginator = Paginator(announcements_list, 5)
    page = request.GET.get('page')
    try:
        announcements_list = paginator.page(page)
    except PageNotAnInteger:
        announcements_list = paginator.page(1)
    except EmptyPage:
        announcements_list = paginator.page(paginator.num_pages)
    data = {'announcements': announcements_list,'title':'Announcements'}
    return render(request,"staff/announcements.html",data)

def staffaddmarksheet(request):
    if 'staff_user' not in request.session:
        return redirect('loginform')
    if request.method == "POST":
        name = request.POST.get('name')
        enrollment = request.POST.get('enrollment')
        department = request.POST.get('department')
        year = request.POST.get('year')
        result = request.POST.get('result')
        total_marks = request.POST.get('total_marks')
        total_marks_obtained = request.POST.get('total_marks_obtained')
        data=marksheet1(name=name,enrollment=enrollment,department=department,year=year,result=result,total_marks=total_marks,total_marks_obtained=total_marks_obtained)
        data.save()
    return render(request,'staff/add-marksheet.html',{'title':'Add Marksheet'})

#logout code


def logoutadmin(request):
    if 'admin_user' in request.session:
        del request.session['admin_user']
    return redirect('homepage')

def logoutstaff(request):
    if 'staff_user' in request.session:
        del request.session['staff_user']
    return redirect('homepage')



#create credentials

def createcredentials(request):
    data = {}
    if 'admin_user' not in request.session:
        return redirect('loginform')  # Ensure you have a 'home' URL name configured
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')
        role = request.POST.get('role')

        if password != confirm_password:
            data = {'error': True, 'message': "Password and Confirm Password don't match"}
        else:
            if role == "admin":
                if adminusers.objects.filter(username=username).exists():
                    data = {'error': True, 'message': "Username already exists!"}
                else:
                    obj = adminusers(username=username, password=password)
                    obj.save()
                    data = {'success': True, 'message': "Admin user added!"}
            elif role == "staff":
                if staffusers.objects.filter(username=username).exists():
                    data = {'error': True, 'message': "Username already exists!"}
                else:
                    obj = staffusers(username=username, password=password)
                    obj.save()
                    data = {'success': True, 'message': "Staff user added!"}
    
    return render(request, 'admin2/create-credentials.html', data)


def allcredentials(request):
    if 'admin_user' not in request.session:
        return redirect('loginform')
    
    if request.method == "POST":
        id=request.POST.get('id')
        obj=adminusers.objects.get(id=id)
        obj.delete()
    elif request.method == "GET" and 'id' in request.GET:
        id=request.GET.get('id')
        obj=staffusers.objects.get(id=id)
        obj.delete()

    admin_obj=adminusers.objects.all().order_by('username')
    staff_obj=staffusers.objects.all().order_by('username')

    paginator = Paginator(admin_obj, 5)  # Show 5 messages per page

    page = request.GET.get('page')
    try:
        admin_obj = paginator.page(page)
    except PageNotAnInteger:
        admin_obj = paginator.page(1)
    except EmptyPage:
        admin_obj = paginator.page(paginator.num_pages)

    paginator2 = Paginator(staff_obj, 5)  # Show 5 messages per page

    page2 = request.GET.get('page2')
    try:
        staff_obj = paginator2.page(page2)
    except PageNotAnInteger:
        staff_obj = paginator2.page(1)
    except EmptyPage:
        staff_obj = paginator2.page(paginator2.num_pages)
    
    data={'admins':admin_obj,'staffs':staff_obj}
    return render(request,'admin2/all-credentials.html',data)