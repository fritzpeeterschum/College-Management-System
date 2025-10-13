from django.urls import path
from schoolManagement import views



urlpatterns = [
    path('teacher-profile', views.teacherProfile),
    path('teacher-courses', views.teacherCourse),
    # Dashboard view (list all courses)
    path('teacher-attendance/', views.teacherAttendanceDashboard),
    path('attendance-history/', views.attendanceHistory),
        # Edit specific attendance record
    path("teacher-attendance/edit/<int:record_id>/", views.editAttendanceRecord), 
    # path('update-attendance-record', views.updateAttendanceRecord),
    path("teacher-attendance/delete/<int:record_id>/", views.deleteAttendanceRecord),
    # Course-specific attendance marking page
    path('teacher-attendance/<int:course_id>/', views.teacherAttendance),
    path('teacher-announcement', views.teacherAnnouncement),
    path('teacher-announcement/<int:ann_id>/', views.teacherAnnouncementDetail),
    path('teacher-announcement/edit/<int:ann_id>/', views.editTeacherAnnouncement),
    path('teacher-announcement/delete/<int:ann_id>/', views.deleteTeacherAnnouncement),
    path('edit-teacher-profile/<int:teacher_id>', views.teacherEditProfile),
    path('update-teacher-profile/<int:teacher_id>', views.teacherUpdateProfile),
    path('admin-departments', views.adminDepartments),
    path('admin-departments-add', views.adminAddDepartments),
    path('admin-departments-edit/<int:id>/', views.adminEditDepartments),
    path('admin-departments-delete/<int:id>/', views.adminDeleteDepartments),
    path('admin-add-course', views.adminAddCourse),
    path('edit-admin-course/<int:courseId>', views.adminEditCourse), 
    path('admin-courses-delete/<int:courseId>', views.adminDeleteCourse),
    path('update-admin-course/<int:courseId>', views.adminUpdateCourse),
    path('admin-courses', views.adminCourse),
    path('admin-profile', views.adminProfile),
    path('admin-user-management', views.adminUserManagement),
    path('edit-admin-profile/<int:admin_id>', views.adminEditProfile),
    path('update-admin-profile/<int:admin_id>', views.adminUpdateProfile),
    path('admin-delete-user/<int:delete_id>', views.adminDeleteUser),
    path('admin-delete-confirmation-page/<int:delete_id>', views.adminDeleteConfirmationPage),
    path('admin-deleted-users', views.adminDeletedUsers),
    path('admin-activate-confirmation-page/<int:activate_id>', views.adminActivateConfirmationPage),
    path('admin-activate-users/<int:activate_id>', views.adminActivateUsers),
    path('admin-suspended-users', views.adminSuspendedUsers),
    path('admin-suspend-users/<int:suspend_id>', views.adminSuspendUsers),
    path('admin-suspend-confirmation-page/<int:suspend_id>', views.adminSuspendConfirmationPage),

]


    