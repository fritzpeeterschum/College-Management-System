from django.urls import path
from student import views
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet


urlpatterns = [
    path('student-profile', views.studentProfile),
    path('student-courses', views.studentCourse),
    path('student-attendance', views.studentAttendance),
    path('student-announcement', views.studentAnnouncement),
    path('student-announcement/<int:ann_id>/', views.studentAnnouncementDetail),
    path('student-feesManagement', views.studentFeeManagement),
    path('final-results', views.finalResults),
    path('edit-student-profile/<int:student_id>', views.editProfile),
    path('update-student-profile/<int:student_id>', views.updateProfile),
    
    
]

router = DefaultRouter()
router.register(r'students', StudentViewSet, basename='student')

urlpatterns = router.urls