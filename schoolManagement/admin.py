from django.contrib import admin
from .models import Management,Announcement,Attendance,ExamManagement
# Register your models here.
admin.site.register(Management)
admin.site.register(Announcement)
admin.site.register(Attendance)
admin.site.register(ExamManagement)