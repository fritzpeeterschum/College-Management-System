from django.shortcuts import render, redirect
from schoolManagement.models import *
from student.models import *
from datetime import datetime
from django.contrib import messages

# Create your views here.
def teacherExamManagement(request):
        current_month = datetime.now().month
        current_year = datetime.now().year
        if 1 <= current_month <= 4:
            current_semester = 'first'
        elif 5 <= current_month <= 8:
            current_semester = 'second'
        else:
            current_semester = 'third'

        data = {
            "current_semester":current_semester,
            "current_year":current_year,
        }
        return render(request, 'teacher/examManagement.html', context = data)

def fetchCourseSemesters(request):
    student_instance = []
    current_month = datetime.now().month
    current_year = datetime.now().year
    if 1 <= current_month <= 4:
        current_semester = 'first'
    elif 5 <= current_month <= 8:
        current_semester = 'second'
    else:
        current_semester = 'third'

    if request.method == "POST":
        semester = request.POST.get('semester')
        year = request.POST.get('year')
        teacher_instance = User.objects.get(username=request.user.username)

        if semester == "First Semester" and year == "First Year":
            student_instance = Student.objects.all()
            first_semester_course_instance = Courses.objects.filter(
                teacher=teacher_instance,
                semester="First",
                year="First"
            )

    data = {
        "student_instance": student_instance,
        "course_instance": first_semester_course_instance,
        "current_semester":current_semester,
        "current_year":current_year,
    }

    return render(request, 'teacher/examManagement.html', context=data)

def saveExamResults(request):
    if request.method == "POST":
        student_id = request.POST.get('student')
        course_id = request.POST.get('course')
        first_semester_test = request.POST.get('first_semester_test')
        first_semester_exam = request.POST.get('first_semester_exam')


        student = Student.objects.get(id = student_id)
        course = Courses.objects.get(id=course_id)

        exam_instance = ExamManagement.objects.create(student = student, course = course, first_semester_test_marks = first_semester_test, first_semester_exam_marks = first_semester_exam)
        if exam_instance:
            messages.success(request, "Marks saved/updated successfully!")
            return redirect('/teacher-exam-management')
        else:
            messages.success(request, "Something went wrong!")
            return redirect('/teacher-exam-management')

def teacherFinalResults(request):
    courses = Courses.objects.all()  # Get all courses for the dropdown
    selected_course = None
    exam_instance = ExamManagement.objects.select_related('student', 'course').all()
    teacher_instance = User.objects.get(username = request.user.username)
    current_month = datetime.now().month
    current_year = datetime.now().year

    if 1 <= current_month <= 4:
        current_semester = 'first'
    elif 5 <= current_month <= 8:
        current_semester = 'second'
    else:
        current_semester = 'third'

    # Check if a course is selected in the query string
    course_id = request.GET.get('course')
    if course_id:
        selected_course = Courses.objects.get(id=course_id)
        exam_instance = exam_instance.filter(course=selected_course)

    data = {
        "exam_instance": exam_instance,
        "course_instance": courses,  # For dropdown
        "selected_course": selected_course,
        "teacher_instance":teacher_instance,
        "current_semester":current_semester,
        "current_year":current_year
    }
    return render(request, 'teacher/finalResults.html', context=data)

def studentTestResults(request):
    user_instance = User.objects.get(username = request.user.username)
    student_instance = Student.objects.get(user=user_instance)

    department_courses = Courses.objects.filter(department=student_instance.department)
    exam_instance = ExamManagement.objects.filter(student=student_instance)

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
        "exam_instance": exam_instance,
        "department_courses": department_courses,  # for dropdown
        "current_semester":current_semester,
        "current_year":current_year
    }
    return render(request, 'student/testResults.html', context=data)

def studentFinalResults(request):
    user_instance = User.objects.get(username=request.user.username)
    student_instance = Student.objects.get(user=user_instance)

    selected_semester = request.GET.get('semester')  # "first", "second", "third", or None

    # Fetch all exam results for that student
    exam_instance = ExamManagement.objects.filter(student=student_instance).select_related('course')

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
        "exam_instance": exam_instance,
        "selected_semester": selected_semester,
        "current_semester":current_semester,
        "current_year":current_year
    }
    return render(request, 'student/finalResult.html', context=data)