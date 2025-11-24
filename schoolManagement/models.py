from django.db import models
from smsAuth.models import *
from students.models import *
from django.utils import timezone



# Create your models here.
class Management(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_management")
    address = models.CharField(max_length=100,null=False,blank=True)
    employee_number = models.CharField(max_length=100,null=False,blank=True)
    marital_status = models.CharField(max_length=100,null=False,blank=True)
    DOB = models.DateField(max_length=30,null=False,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Announcement(models.Model):
    user = models.ForeignKey(Management, on_delete=models.CASCADE, related_name="user_announcement")
    title = models.CharField(max_length=200, null=False, blank=True)
    announcement = models.CharField(max_length=500, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

class ExamManagement(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="user_examManagement")
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name="user_courses")
    first_semester_test_marks = models.CharField(max_length=20, null=False, blank=True)
    first_semester_exam_marks = models.CharField(max_length=20, null=False, blank=True)
    second_semester_test_marks = models.CharField(max_length=20, null=False, blank=True)
    second_semester_exam_marks = models.CharField(max_length=20, null=False, blank=True)
    third_semester_test_marks = models.CharField(max_length=20, null=False, blank=True)
    third_semester_exam_marks = models.CharField(max_length=20, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    class Meta:
        unique_together = ('student', 'course')  # one row per student per course

    def __str__(self):
        return f"{self.student.name} - {self.course.name}"

class Attendance(models.Model):
    STATUS_CHOICES = [
        ("Present", "Present"),
        ("Absent", "Absent"),
        ("Late", "Late"),
    ]
    marked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='marked_attendances')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_attendances', null=True, blank=True)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name='course_attendances', null=True, blank=True)
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Absent")
    note = models.CharField(max_length=255, null=True, blank=True)  # optional free-text field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.course.name} ({self.status})"
