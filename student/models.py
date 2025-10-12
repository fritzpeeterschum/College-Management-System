from django.db import models
from smsAuth.models import *

# Create your models here.
class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_student")
    department = models.ForeignKey('SchoolDepartment', on_delete=models.CASCADE, related_name="student_department", null=True, blank=True)
    address = models.CharField(max_length=100,null=False,blank=True)
    student_number = models.CharField(max_length=100,null=False,blank=True)
    DOB = models.CharField(max_length=30,null=False,blank=True)
    status = models.CharField(max_length=30,null=False,blank=True,default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
            return f"{self.user.first_name} {self.user.last_name}"

class SchoolDepartment(models.Model):
    name = models.CharField(max_length=100,null=False,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Courses(models.Model):
    department = models.ForeignKey(SchoolDepartment, on_delete=models.CASCADE,related_name="course_department")
    teacher = models.ForeignKey(User, on_delete=models.CASCADE,related_name="course_management")
    name = models.CharField(max_length=100,null=False,blank=True)
    course_value = models.CharField(max_length=100,null=False,blank=True)
    course_code = models.CharField(max_length=100,null=False,blank=True)
    semester =  models.CharField(max_length=100,null=False,blank=True)
    year =  models.CharField(max_length=100,null=False,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)