from django.urls import path
from examination import views


urlpatterns = [
    path('teacher-exam-management', views.teacherExamManagement),
    path('save-results', views.saveExamResults),
    path('teacher-final-results', views.teacherFinalResults),
    path('school-test-results', views.studentTestResults),
    path('student-final-results', views.studentFinalResults),
    path('fetch-course-semesters', views.fetchCourseSemesters),
]