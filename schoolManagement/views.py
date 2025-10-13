from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import Management, Courses, SchoolDepartment, Student, Announcement, ExamManagement
from django.contrib import messages
from django.contrib.auth import get_user_model
User = get_user_model()
from datetime import datetime


# Create your views here.
def teacherProfile(request):
    user_instance = User.objects.get(email=request.user.email)  # now using custom user
    teacher_instance = Management.objects.get(user=user_instance)
    current_month = datetime.now().month
    current_year = datetime.now().year

    if 1 <= current_month <= 4:
        current_semester = 'first'
    elif 5 <= current_month <= 8:
        current_semester = 'second'
    else:
        current_semester = 'third'

    data = {
        "teacher_instance": teacher_instance,
        "current_semester": current_semester,
        "current_year":current_year
    }

    return render(request, 'teacher/profile.html', context=data)

def teacherCourse(request):
     department_id = request.GET.get('department')
     courses = Courses.objects.filter(teacher = request.user)
     teacher_instance = Management.objects.get(user=User.objects.get(email=request.user.email))
     current_month = datetime.now().month
     current_year = datetime.now().year

     if 1 <= current_month <= 4:
        current_semester = 'first'
     elif 5 <= current_month <= 8:
        current_semester = 'second'
     else:
        current_semester = 'third'
     if department_id:
         courses = courses.filter(department_id=department_id)

     departments = SchoolDepartment.objects.all()

     return render(request, 'teacher/courses.html', {
         "courses": courses,
         "departments": departments,
         "selectedDepartment": department_id,
         "teacher_instance": teacher_instance,
         "current_semester":current_semester,
         "current_year":current_year
         })

def adminCourse(request):
    courses = Courses.objects.all()
    admin_instance = Management.objects.get(user=User.objects.get(email=request.user.email))
    current_month = datetime.now().month
    current_year = datetime.now().year

    if 1 <= current_month <= 4:
        current_semester = 'first'
    elif 5 <= current_month <= 8:
        current_semester = 'second'
    else:
        current_semester = 'third'
    return render(request, 'schAdmin/courses.html', {
        "courses": courses,
        "admin_instance": admin_instance,
        "current_semester":current_semester,
        "current_year":current_year
    })

def adminDepartments(request):
    departments = SchoolDepartment.objects.all()
    admin_instance = Management.objects.get(user=User.objects.get(email=request.user.email))
    current_month = datetime.now().month
    current_year = datetime.now().year

    if 1 <= current_month <= 4:
        current_semester = 'first'
    elif 5 <= current_month <= 8:
        current_semester = 'second'
    else:
        current_semester = 'third'
    return render(request, 'schAdmin/departments.html', {
        "departments": departments,
        "admin_instance": admin_instance,
        "current_semester":current_semester,
        "current_year":current_year
    })

def teacherAttendance(request):
    return render(request, 'teacher/attendance.html')

def teacherAnnouncement(request):
    user_instance = User.objects.get(email=request.user.email)
    teacher_instance = Management.objects.get(user=user_instance)
    if request.method == "POST":
        title = request.POST.get("title")
        text = request.POST.get("announcement")
        if title and text:
            Announcement.objects.create(user=teacher_instance, title=title, announcement=text)
            messages.success(request, "Announcement created successfully!")
        else:
            messages.error(request, "Both title and announcement cannot be empty.")
        return redirect('/teacher-announcement')

    announcements = Announcement.objects.filter(user=teacher_instance, status=True).order_by('-created_at')
    current_month = datetime.now().month
    current_year = datetime.now().year

    if 1 <= current_month <= 4:
        current_semester = 'first'
    elif 5 <= current_month <= 8:
        current_semester = 'second'
    else:
        current_semester = 'third'
    data = {
        "teacher_instance": teacher_instance,
        "announcements": announcements,
        "current_semester":current_semester,
        "current_year":current_year
    }
    return render(request, "teacher/announcement.html", context=data)

def teacherAnnouncementDetail(request, ann_id):
    user_instance = User.objects.get(email=request.user.email)
    teacher_instance = Management.objects.get(user=user_instance)
    announcement = get_object_or_404(Announcement, id=ann_id,user=teacher_instance, status=True)
    current_month = datetime.now().month
    current_year = datetime.now().year

    if 1 <= current_month <= 4:
        current_semester = 'first'
    elif 5 <= current_month <= 8:
        current_semester = 'second'
    else:
        current_semester = 'third'
    data={
        "teacher_instance": teacher_instance,
        "announcement": announcement,
        "current_semester":current_semester,
        "current_year":current_year
    }
    return render(request, "teacher/announcementBody.html", context=data)
def editTeacherAnnouncement(request, ann_id):
    user_instance = User.objects.get(email=request.user.email)
    teacher_instance = Management.objects.get(user=user_instance)
    announcement = get_object_or_404(Announcement, id=ann_id, user=teacher_instance, status=True)

    if request.method == "POST":
        title = request.POST.get("title")
        text = request.POST.get("announcement")
        if title and text:
            announcement.title = title
            announcement.announcement = text
            announcement.save()
            messages.success(request, "Announcement updated successfully!")
            return redirect(f'/teacher-announcement/{ann_id}/')
        else:
            messages.error(request, "Both title and announcement cannot be empty.")
            return redirect(f'/teacher-announcement/edit/{ann_id}/')

    data = {
        "teacher_instance": teacher_instance,
        "announcement": announcement
    }
    return render(request, "teacher/editAnnouncement.html", context=data)

def deleteTeacherAnnouncement(request, ann_id):
    user_instance = User.objects.get(email=request.user.email)
    teacher_instance = Management.objects.get(user=user_instance)
    announcement = get_object_or_404(Announcement, id=ann_id, user=teacher_instance)
    if request.method == "POST":
        announcement.status = False
        announcement.save()
        messages.success(request, "Announcement deleted successfully!")
        return redirect('/teacher-announcement')
    
    current_month = datetime.now().month
    current_year = datetime.now().year

    if 1 <= current_month <= 4:
        current_semester = 'first'
    elif 5 <= current_month <= 8:
        current_semester = 'second'
    else:
        current_semester = 'third'

    data = {
        "teacher_instance": teacher_instance,
        "announcement": announcement,
        "current_semester":current_semester,
        "current_year":current_year
    }
    return render(request, 'teacher/deleteAnnouncement.html', context=data)

    
def teacherEditProfile(request,teacher_id):
    user_instance = User.objects.get(email=request.user.email)  
    teacher_instance = Management.objects.get(user=user_instance)
    current_month = datetime.now().month
    current_year = datetime.now().year

    if 1 <= current_month <= 4:
        current_semester = 'first'
    elif 5 <= current_month <= 8:
        current_semester = 'second'
    else:
        current_semester = 'third'

    data = {
        "teacher_instance": teacher_instance,
        "teacher_id" : teacher_id,
        "current_semester":current_semester,
        "current_year":current_year
    }
    return render(request, 'teacher/editProfile.html',context=data)

def teacherUpdateProfile(request,teacher_id):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        address = request.POST['address']
        marital_status = request.POST['marital_status']
        DOB = request.POST['DOB']
        user_instance = User.objects.get(email=request.user.email)
        user_instance.first_name = first_name
        user_instance.last_name = last_name
        user_instance.email = email
        user_instance.username = username
        user_instance.save()
        teacher_instance = Management.objects.get(user=user_instance)
        teacher_instance.address = address
        teacher_instance.marital_status = marital_status
        teacher_instance.DOB = DOB
        teacher_instance.save()
        messages.success(request, "profile updated successfully")
        return redirect(f'/edit-teacher-profile/{teacher_id}')  
    else:
        messages.success(request, "Fail to Update")
        return redirect(f'/edit-teacher-profile/{teacher_id}')  
    
def adminAddCourse(request):
    if request.method == "POST":
        name = request.POST['name']
        course_code = request.POST['course_code']
        course_value = request.POST['course_value']
        semester = request.POST['semester']
        year = request.POST['year']
        departmentId = request.POST.get('department')
        userId = request.POST.get('teacher')
        if not departmentId:
            messages.error(request, "Please Select A Department")
            return redirect('/admin-add-course')

        department = SchoolDepartment.objects.get(id = departmentId)
        teacher = User.objects.get(id = userId)

        Courses.objects.create(
            teacher = teacher,
            department = department,
            name = name,
            course_code = course_code,
            course_value = course_value,
            semester = semester,
            year = year,
        )
        messages.success(request, "Course created successfully!")
        return redirect('/admin-courses')
    else:
        departments = SchoolDepartment.objects.all()
        teachers = User.objects.filter(is_teacher = True)
        current_month = datetime.now().month
        current_year = datetime.now().year

        if 1 <= current_month <= 4:
            current_semester = 'first'
        elif 5 <= current_month <= 8:
            current_semester = 'second'
        else:
            current_semester = 'third'
        return render(request, "schAdmin/addCourse.html", {"departments": departments, "teachers": teachers,  "current_semester":current_semester,
        "current_year":current_year})    
    
def adminEditCourse(request, courseId):
        admin_instance = Management.objects.get(user=request.user)
        course = Courses.objects.get(id=courseId)
        departments = SchoolDepartment.objects.all()
        current_month = datetime.now().month
        current_year = datetime.now().year

        if 1 <= current_month <= 4:
            current_semester = 'first'
        elif 5 <= current_month <= 8:
            current_semester = 'second'
        else:
            current_semester = 'third'
        
        data = {
            "admin_instance": admin_instance,
            "teacher_id": admin_instance.id,
            "courseId": courseId,
            "course": course,
            'departments': departments,
            "current_semester":current_semester,
            "current_year":current_year
        }
        return render(request, "schAdmin/editCourse.html", context=data)    

def adminUpdateCourse(request, courseId):
    if request.method == "POST":
        name = request.POST['name']
        course_code = request.POST['course_code']
        course_value = request.POST['course_value']
        semester = request.POST['semester']
        year = request.POST['year']
        user_instance = User.objects.get(email = request.user.email)

        course = Courses.objects.get(id = courseId)
        course.name = name
        course.course_code = course_code
        course.course_value = course_value
        course.semester = semester
        course.year = year
        course.save()
        messages.success(request, "Course Updated Successfully!")
        return redirect('/admin-courses')
    else:
        messages.error(request, "Failed To Update Course")
        return redirect(f'/edit-admin-course/{courseId}')
    
def adminDeleteCourse(request, courseId):
    Courses.objects.filter(id=courseId).delete()
    return redirect('/admin-courses')        

def adminAddDepartments(request):
    admin_instance = Management.objects.get(user=User.objects.get(email=request.user.email))
    current_month = datetime.now().month
    current_year = datetime.now().year

    if 1 <= current_month <= 4:
            current_semester = 'first'
    elif 5 <= current_month <= 8:
            current_semester = 'second'
    else:
            current_semester = 'third'
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            SchoolDepartment.objects.create(name=name)
            return redirect('/admin-departments')
    return render(request, 'schAdmin/addDepartment.html', {
        "admin_instance": admin_instance,
        "current_semester":current_semester,
        "current_year":current_year
    })

def adminEditDepartments(request, id):
    admin_instance = Management.objects.get(user=User.objects.get(email=request.user.email))
    department = SchoolDepartment.objects.get(id=id)
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            department.name = name
            department.save()
            return redirect('/admin-departments')
    return render(request, 'schAdmin/editDepartment.html', {
        "admin_instance": admin_instance,
        "department": department
    })    
        
def adminDeleteDepartments(request, id):
    department = SchoolDepartment.objects.get(id=id)
    department.delete()
    return redirect('/admin-departments')

def updateAttendanceRecord(request):
    pass

def adminProfile(request):
    user_instance = User.objects.get(email=request.user.email)  # now using custom user
    admin_instance = Management.objects.get(user=user_instance)
    current_month = datetime.now().month
    current_year = datetime.now().year

    if 1 <= current_month <= 4:
        current_semester = 'first'
    elif 5 <= current_month <= 8:
        current_semester = 'second'
    else:
        current_semester = 'third'

    data = {
        "admin_instance": admin_instance,
        "current_semester":current_semester,
        "current_year":current_year
    }
    return render(request, 'schAdmin/profile.html', context=data)

def adminUserManagement(request):
    if request.user.is_authenticated:
        user_instance = User.objects.get(email=request.user.email)  # now using custom user
        admin_instance = Management.objects.get(user=user_instance)
        current_user = request.user
        all_users = User.objects.filter(status = True).exclude(pk = current_user.pk)
        active_users = True

        current_month = datetime.now().month
        current_year = datetime.now().year

        if 1 <= current_month <= 4:
            current_semester = 'first'
        elif 5 <= current_month <= 8:
            current_semester = 'second'
        else:
            current_semester = 'third'

        data = {
            "all_users": all_users,
            "active_users": active_users,
            "admin_instance": admin_instance,
            "current_semester":current_semester,
            "current_year":current_year
        }
        return render(request, 'schAdmin/userManagement.html', context=data)
    
def adminDeleteConfirmationPage(request, delete_id):
    fetchedUser = User.objects.get(id = delete_id)
    current_month = datetime.now().month
    current_year = datetime.now().year

    if 1 <= current_month <= 4:
        current_semester = 'first'
    elif 5 <= current_month <= 8:
        current_semester = 'second'
    else:
        current_semester = 'third'

    if fetchedUser:
        data = {
            "fetchedUser": fetchedUser,
            "current_semester":current_semester,
            "current_year":current_year
        }
        return render(request, 'schAdmin/deleteConfirmationPage.html', context=data)
    else:
        messages.success(request, "No user Found")
        return redirect('/admin-user-management')

def adminSuspendConfirmationPage(request, suspend_id):
    fetchedUser = User.objects.get(id = suspend_id)
    current_month = datetime.now().month
    current_year = datetime.now().year

    if 1 <= current_month <= 4:
        current_semester = 'first'
    elif 5 <= current_month <= 8:
        current_semester = 'second'
    else:
        current_semester = 'third'

    if fetchedUser:
        data = {
            "fetchedUser": fetchedUser,
            "current_semester":current_semester,
            "current_year":current_year
        }
        return render(request, 'schAdmin/suspendConfirmationPage.html', context=data)
    else:
        messages.success(request, "No user Found")
        return redirect('/admin-user-management')
    
def adminActivateConfirmationPage(request, activate_id):
    fetchedUser = User.objects.get(id = activate_id)
    current_month = datetime.now().month
    current_year = datetime.now().year

    if 1 <= current_month <= 4:
        current_semester = 'first'
    elif 5 <= current_month <= 8:
        current_semester = 'second'
    else:
        current_semester = 'third'

    if fetchedUser:
        data = {
            "fetchedUser": fetchedUser,
            "current_semester":current_semester,
            "current_year":current_year
        }
        return render(request, 'schAdmin/activateConfirmationPage.html', context=data)
    else:
        messages.success(request, "No user Found")
        return redirect('/admin-user-management')
    
def adminDeleteUser(request, delete_id):
    if request.method == "GET":
        deleteUser = User.objects.filter(id = delete_id).update(status = False)
        if deleteUser:
            messages.success(request, "User deleted successfully.")
            return redirect('/admin-user-management')
        else:
            messages.success(request, "Unable to delete user.")
            return redirect('/admin-user-management')
    
def adminDeletedUsers(request):
    if request.user.is_authenticated:
        current_user = request.user
        all_users = User.objects.filter(status = False).exclude(pk = current_user.pk)
        all_deleted_users = True
        current_month = datetime.now().month
        current_year = datetime.now().year

        if 1 <= current_month <= 4:
            current_semester = 'first'
        elif 5 <= current_month <= 8:
            current_semester = 'second'
        else:
            current_semester = 'third'

        data = {
            "all_users": all_users,
            "all_deleted_users": all_deleted_users,
            "current_semester":current_semester,
            "current_year":current_year 
        }
        return render(request, 'schAdmin/userManagement.html', context=data)
    
def adminActivateUsers(request, activate_id):
      if request.method == "GET":
        deleteUser = User.objects.filter(id = activate_id).update(status = True)
        if deleteUser:
                messages.success(request, "User Activated successfully.")
                return redirect('/admin-user-management')
        else:
            messages.success(request, "Unable to activate user.")
            return redirect('/admin-user-management')
        
def adminSuspendUsers(request, suspend_id):
    if request.method == "GET":
        deleteUser = User.objects.filter(id = suspend_id).update(status = "suspend")
        if deleteUser:
            messages.success(request, "User suspended successfully.")
            return redirect('/admin-user-management')
        else:
            messages.success(request, "Unable to delete user.")
            return redirect('/admin-user-management')
        
def adminSuspendedUsers(request):
    if request.user.is_authenticated:
        current_user = request.user
        all_users = User.objects.filter(status = "suspend").exclude(pk = current_user.pk)
        all_suspended_users = True
        current_month = datetime.now().month
        current_year = datetime.now().year

        if 1 <= current_month <= 4:
            current_semester = 'first'
        elif 5 <= current_month <= 8:
            current_semester = 'second'
        else:
            current_semester = 'third'

        data = {
            "all_users": all_users,
            "all_suspended_users": all_suspended_users,
            "current_semester":current_semester,
            "current_year":current_year 
        }
        return render(request, 'schAdmin/userManagement.html', context=data)

def adminEditProfile(request,admin_id):
    user_instance = User.objects.get(email=request.user.email)  # now using custom user
    admin_instance = Management.objects.get(user=user_instance)
    current_month = datetime.now().month
    current_year = datetime.now().year

    if 1 <= current_month <= 4:
        current_semester = 'first'
    elif 5 <= current_month <= 8:
        current_semester = 'second'
    else:
        current_semester = 'third'

    data = {
        "admin_instance": admin_instance,
        "admin_id" : admin_id,
        "current_semester":current_semester,
        "current_year":current_year
    }
    return render(request, 'schAdmin/editProfile.html',context=data)

def adminUpdateProfile(request,admin_id):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        address = request.POST['address']
        marital_status = request.POST['marital_status']
        DOB = request.POST['DOB']
        user_instance = User.objects.get(email=request.user.email)
        user_instance.first_name = first_name
        user_instance.last_name = last_name
        user_instance.email = email
        user_instance.username = username
        user_instance.save()
        admin_instance = Management.objects.get(user=user_instance)
        admin_instance.address = address
        admin_instance.marital_status = marital_status
        admin_instance.DOB = DOB
        admin_instance.save()
        messages.success(request, "profile updated successfully")
        return redirect(f'/edit-admin-profile/{admin_id}')  
    else:
        messages.success(request, "Fail to Update")
        return redirect(f'/edit-admin-profile/{admin_id}')  