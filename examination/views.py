from django.shortcuts import render, redirect
from schoolManagement.models import *
from student.models import *
from django.contrib import messages

# Create your views here.
def teacherExamManagement(request):
    student_instance = Student.objects.all()
    teacher_instance = User.objects.get(username = request.user.username)
    course_instance = Courses.objects.filter(teacher =teacher_instance)
    data = {
        "student_instance":student_instance,
        "course_instance":course_instance
    }
    return render(request, 'teacher/examManagement.html', context = data)

def saveExamResults(request):
    if request.method == "POST":
        student_id = request.POST.get('student')
        course_id = request.POST.get('course')

        # Check if a course was selected
        if not course_id:
            messages.error(request, "Please select a course before saving results.")
            return redirect('/teacher-exam-management')

        student = Student.objects.get(id=student_id)
        course = Courses.objects.get(id=course_id)

        # Try to get existing record
        exam, created = ExamManagement.objects.get_or_create(
            student=student,
            course=course
        )

        # Update only fields that are submitted
        if request.POST.get('first_semester_test'):
            exam.first_semester_test_marks = request.POST['first_semester_test']

        if request.POST.get('first_semester_exam'):
            exam.first_semester_exam_marks = request.POST['first_semester_exam']

        if request.POST.get('second_semester_test'):
            exam.second_semester_test_marks = request.POST['second_semester_test']

        if request.POST.get('second_semester_exam'):
            exam.second_semester_exam_marks = request.POST['second_semester_exam']

        if request.POST.get('third_semester_test'):
            exam.third_semester_test_marks = request.POST['third_semester_test']

        if request.POST.get('third_semester_exam'):
            exam.third_semester_exam_marks = request.POST['third_semester_exam']

        exam.save()  # Save updates

        messages.success(request, "Marks saved/updated successfully!")
        return redirect('/teacher-exam-management')

def teacherFinalResults(request):
    courses = Courses.objects.all()  # Get all courses for the dropdown
    selected_course = None
    exam_instance = ExamManagement.objects.select_related('student', 'course').all()

    # Check if a course is selected in the query string
    course_id = request.GET.get('course')
    if course_id:
        selected_course = Courses.objects.get(id=course_id)
        exam_instance = exam_instance.filter(course=selected_course)

    data = {
        "exam_instance": exam_instance,
        "course_instance": courses,  # For dropdown
        "selected_course": selected_course
    }
    return render(request, 'teacher/finalResults.html', context=data)

def studentTestResults(request):
    user_instance = User.objects.get(username = request.user.username)
    student_instance = Student.objects.get(user=user_instance)

    department_courses = Courses.objects.filter(department=student_instance.department)
    exam_instance = ExamManagement.objects.filter(student=student_instance)

   

    data = {
        "student_instance": student_instance,
        "exam_instance": exam_instance,
        "department_courses": department_courses,  # for dropdown
    }
    return render(request, 'student/testResults.html', context=data)

def studentFinalResults(request):
    user_instance = User.objects.get(username=request.user.username)
    student_instance = Student.objects.get(user=user_instance)

    selected_semester = request.GET.get('semester')  # "first", "second", "third", or None

    # Fetch all exam results for that student
    exam_instance = ExamManagement.objects.filter(student=student_instance).select_related('course')

    data = {
        "student_instance": student_instance,
        "exam_instance": exam_instance,
        "selected_semester": selected_semester,
    }
    return render(request, 'student/finalResult.html', context=data)