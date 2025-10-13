from django.urls import path
from smsAuth import views


urlpatterns = [
    path('create-management-account', views.createManageAccount),
    path('create-student-account', views.createStudentAccount),
    path('create-parent-account', views.createParentAccount),
    path('create-student-account-auth', views.createStudentAccountAuth),
    path('create-management-account-auth', views.createManagementAccountAuth),
    path('create-parent-account-auth', views.createParentAccountAuth),
    path('school-user-auth', views.schoolUserAuthentication),
    path('management-user-auth', views.managementUserAuthentication),
    path('', views.studentUserLogin),
    path('management-login', views.managementUserLogin),
    path('student-logout', views.studentUserLogout),
    path('management-logout', views.managementUserLogout),
    path('reset-password', views.resetPassword),
    path('reset-password-auth', views.resetPasswordAuth),

]