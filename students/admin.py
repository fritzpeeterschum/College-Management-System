from django.contrib import admin
from .models import Student, SchoolDepartment,Courses

# Register your models here.
admin.site.register(Student)
admin.site.register(SchoolDepartment)
admin.site.register(Courses)
