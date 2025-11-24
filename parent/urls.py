from django.urls import path, include
from parent import admin, views
from blog import *
from . import views


urlpatterns = [
    path('parent-profile', views.parentProfile, name='parent-profile'),
    path('parent-attendance', views.parentAttendance),
    path('parent-results', views.parentResults),
    path('edit-parent-profile/<int:parent_id>', views.editParentProfile),
    path('update-parent-profile/<int:parent_id>', views.updateParentProfile),
    path('', include('blog.urls')),
    path('api-auth/', include('rest_framework.urls')),
   

]