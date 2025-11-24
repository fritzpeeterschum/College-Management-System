"""
URL configuration for sms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from student import urls
from schoolManagement import urls
from parent import urls
from examination import urls
from payment import urls
from smsAuth import urls
from django.views.generic import RedirectView
from student import views

urlpatterns = [
               
    path('', include('student.urls')),
    path('', include('schoolManagement.urls')),
    path('', include('parent.urls')),
    path('', include('examination.urls')),
    path('', include('payment.urls')),
    path('', include('smsAuth.urls')),
    path('admin/', admin.site.urls),
    path('blog/', RedirectView.as_view(url='/blogs/', permanent=False)),
    path('blogs/', include('blog.urls')),
    path('api/v1/', include('students.urls')),
    path('admin/', admin.site.urls),
    path('api/v1/', include('student.urls')),
    path('api/v1/', include('students.urls')),

]