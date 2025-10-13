from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import Student, Courses, SchoolDepartment, User
from django.contrib import messages
from django.contrib.auth import get_user_model
from schoolManagement.models import Announcement, Attendance, Management, ExamManagement
from student.models import Student
User = get_user_model()
from datetime import datetime



# Create your views here.
def studentProfile(request):
    student_instance = Student.objects.get(user=User.objects.get(email=request.user.email))
    current_month = datetime.now().month
    current_year = datetime.now().year

    if 1 <= current_month <= 4:
        current_semester = 'first'
    elif 5 <= current_month <= 8:
        current_semester = 'second'
    else:
        current_semester = 'third'

    data = {
        "student_instance": student_instance,
        "current_semester":current_semester,
        "current_year":current_year
    }
    return render(request, 'student/profile.html', context=data) 

def studentCourse(request):
    student = Student.objects.filter(user=request.user).first()
    student_instance = Student.objects.get(user=User.objects.get(email=request.user.email))
    current_month = datetime.now().month
    current_year = datetime.now().year

    if 1 <= current_month <= 4:
        current_semester = 'first'
    elif 5 <= current_month <= 8:
        current_semester = 'second'
    else:
        current_semester = 'third'
    
    if not student:
        return render(request, 'student/courses.html', {
            "error": "No student record found"
        })

    
    courses = Courses.objects.filter(department=student.department)

    return render(request, 'student/courses.html', {
        "student": student,
        "courses": courses,
        "student_instance": student_instance,
        "current_semester":current_semester,
        "current_year":current_year
    })

def studentAttendance(request):
    # Get student instance
    student = Student.objects.filter(user=request.user).select_related('department').first()
    if not student:
        return render(request, 'student/courses.html', {"error": "No student record found"})
    # All courses in the student's department
    courses = Courses.objects.filter(department=student.department)
    # Get selected course from query string (?course_id=)
    selected_course_id = request.GET.get("course_id")
    # Base queryset for attendance

    attendance_qs = Attendance.objects.filter(student__user=request.user).select_related('course__teacher')

    # If a course filter is applied
    if selected_course_id:
        attendance_qs = attendance_qs.filter(course_id=selected_course_id)
    # Order records by most recent
    attendance_records = attendance_qs.order_by('-date')
    # Attendance history summary (recent distinct courses)
    history = (
        Attendance.objects
        .filter(student__user=request.user)
        .values(
            'course__name',
            'course__course_code',
            'course__teacher__first_name',
            'course__teacher__last_name'
        )
        .distinct()
        .order_by('-date')[:10]
    )
    context = {
        "attendance_record": attendance_records,
        "history": history,
        "student": student,
        "courses": courses,
        "selected_course_id": int(selected_course_id) if selected_course_id else None,
    }
    return render(request, 'student/attendance.html', context)


def studentAnnouncement(request):
    user_instance = User.objects.get(email=request.user.email)
    student_instance = Student.objects.get(user=user_instance)
    announcements = Announcement.objects.filter(status=True).order_by('-created_at')
    current_month = datetime.now().month
    current_year = datetime.now().year

    if 1 <= current_month <= 4:
        current_semester = 'first'
    elif 5 <= current_month <= 8:
        current_semester = 'second'
    else:
        current_semester = 'third'
    data={
        "student_instance": student_instance,
        "announcements": announcements,
        "current_semester":current_semester,
        "current_year":current_year
        }
    return render(request, 'student/announcement.html', context=data)

def studentAnnouncementDetail(request, ann_id):
    user_instance = User.objects.get(email=request.user.email)
    student_instance = Student.objects.get(user=user_instance)
    announcement = get_object_or_404(Announcement, id=ann_id, status=True)
    current_month = datetime.now().month
    current_year = datetime.now().year

    if 1 <= current_month <= 4:
        current_semester = 'first'
    elif 5 <= current_month <= 8:
        current_semester = 'second'
    else:
        current_semester = 'third'

    data={
        "student_instance": student_instance,
        "announcement": announcement,
        "current_semester":current_semester,
        "current_year":current_year
    }
    return render(request, "student/announcementBody.html", context=data)


def studentFeeManagement(request):
    return render(request, 'student/feesManagement.html')

def finalResults(request):
    return render(request, 'student/finalResult.html')

def editProfile(request, student_id):
    user_instance = User.objects.get(email = request.user.email)
    student_instance = Student.objects.get(user = user_instance)
    current_month = datetime.now().month
    current_year = datetime.now().year

    if 1 <= current_month <= 4:
        current_semester = 'first'
    elif 5 <= current_month <= 8:
        current_semester = 'second'
    else:
        current_semester = 'third'

    data = {
        "student_instance": student_instance,
        "student_id": student_id,
        "current_semester":current_semester,
        "current_year":current_year
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