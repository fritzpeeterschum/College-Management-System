from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import Student, Courses, SchoolDepartment
from django.contrib import messages
from django.contrib.auth import get_user_model
from schoolManagement.models import Announcement, ExamManagement
from student.models import Student
User = get_user_model()


# Create your views here.
def studentProfile(request):
    student_instance = Student.objects.get(user=User.objects.get(email=request.user.email))
    data = {
        "student_instance": student_instance
    }
    return render(request, 'student/profile.html', context=data) 

def studentCourse(request):
    student = Student.objects.filter(user=request.user).first()
    student_instance = Student.objects.get(user=User.objects.get(email=request.user.email))
    
    if not student:
        return render(request, 'student/courses.html', {
            "error": "No student record found"
        })

    
    courses = Courses.objects.filter(department=student.department)

    return render(request, 'student/courses.html', {
        "student": student,
        "courses": courses,
        "student_instance": student_instance
    })

def studentAttendance(request):
    return render(request, 'student/attendance.html')

def studentAnnouncement(request):
    user_instance = User.objects.get(email=request.user.email)
    student_instance = Student.objects.get(user=user_instance)
    announcements = Announcement.objects.filter(status=True).order_by('-created_at')
    data={
        "student_instance": student_instance,
        "announcements": announcements}
    return render(request, 'student/announcement.html', context=data)

def studentAnnouncementDetail(request, ann_id):
    user_instance = User.objects.get(email=request.user.email)
    student_instance = Student.objects.get(user=user_instance)
    announcement = get_object_or_404(Announcement, id=ann_id, status=True)
    data={
        "student_instance": student_instance,
        "announcement": announcement
    }
    return render(request, "student/announcementBody.html", context=data)


def studentFeeManagement(request):
    return render(request, 'student/feesManagement.html')

def finalResults(request):
    return render(request, 'student/finalResult.html')

def editProfile(request, student_id):
    user_instance = User.objects.get(email = request.user.email)
    student_instance = Student.objects.get(user = user_instance)
    data = {
        "student_instance": student_instance,
        "student_id": student_id
    }
    return render(request, 'student/editProfile.html', context=data)

def updateProfile(request, student_id):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        address = request.POST['address']
        student_number = request.POST['student_number']
        DOB = request.POST['DOB']
        user_instance = User.objects.get(email = request.user.email)
        user_instance.first_name = first_name
        user_instance.last_name = last_name
        user_instance.email = email
        user_instance.save()


        student_instance = Student.objects.get(user = user_instance)
        student_instance.address = address 
        student_instance.student_number = student_number
        student_instance.DOB = DOB
        student_instance.save()
        messages.success(request, "Student profile updated successfully")
        return redirect(f'/edit-student-profile/{student_id}') 

    else:
        messages.success(request, "Failed to update student profile")
        return redirect(f'/edit-student-profile/{student_id}')