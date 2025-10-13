from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
User = get_user_model()
from parent.models import *
from student.models import *
from schoolManagement.models import *
from django.contrib import messages
from datetime import datetime

# Create your views here.
def parentProfile(request):
    user_instance = User.objects.get(email = request.user.email)
    parent_instance = Parent.objects.get(user = user_instance)
    all_registrations = Parent.objects.all()
    current_month = datetime.now().month
    current_year = datetime.now().year

    if 1 <= current_month <= 4:
        current_semester = 'first'
    elif 5 <= current_month <= 8:
        current_semester = 'second'
    else:
        current_semester = 'third'
    data = {
        "all_registrations": all_registrations,
        "parent_instance": parent_instance,
        "current_semester": current_semester,
        "current_year":current_year
    }
    return render(request, 'parent/profile.html', context = data)

def parentAttendance(request):
    parent_instance = Parent.objects.get(user=User.objects.get(email=request.user.email))
    current_month = datetime.now().month
    current_year = datetime.now().year

    if 1 <= current_month <= 4:
        current_semester = 'first'
    elif 5 <= current_month <= 8:
        current_semester = 'second'
    else:
        current_semester = 'third'

    courses = Courses.objects.filter(department=parent_instance.parent_of.department)
    selected_course_id = request.GET.get("course_id")
    attendance_instance = Attendance.objects.filter(student = parent_instance.parent_of)
    attendance_qs = Attendance.objects.filter(student__user=request.user).select_related('course__teacher')
    if selected_course_id:
        attendance_qs = attendance_qs.filter(course_id=selected_course_id)


    context = {
        "attendance_instance":attendance_instance,
        "current_semester":current_semester,
        "current_year":current_year,
        "parent_instance":parent_instance,
        "selected_course_id":int(selected_course_id) if selected_course_id else None,
        "courses":courses
    }
    return render(request, 'parent/attendance.html', context)

def parentResults(request):
    return render(request, 'parent/results.html')

def editParentProfile(request, parent_id):
    user_instance = User.objects.get(email = request.user.email)
    parent_instance = Parent.objects.get(user = user_instance)
    current_month = datetime.now().month
    current_year = datetime.now().year

    if 1 <= current_month <= 4:
        current_semester = 'first'
    elif 5 <= current_month <= 8:
        current_semester = 'second'
    else:
        current_semester = 'third'
    data = {
        "parent_instance": parent_instance,
        "parent_id": parent_id,
        "current_semester": current_semester,
        "current_year":current_year
    }
    return render(request, 'parent/editProfile.html', context=data)

def updateParentProfile(request, parent_id):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        address = request.POST['address']
        user_instance = User.objects.get(email=request.user.email)
        user_instance.first_name = first_name
        user_instance.last_name = last_name
        user_instance.email = email
        user_instance.username = username
        user_instance.save()
        admin_instance = Parent.objects.get(user=user_instance)
        admin_instance.address = address
        admin_instance.save()
        messages.success(request, "profile updated successfully")
        return redirect(f'/edit-parent-profile/{parent_id}')  
    else:
        messages.success(request, "Fail to Update")
        return redirect(f'/edit-parent-profile/{parent_id}')  