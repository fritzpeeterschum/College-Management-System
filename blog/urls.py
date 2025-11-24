from django.urls import path, include
from . import views
from .views import BlogListCreateView, BlogDetailView

urlpatterns = [
    path('blog/', views.BlogListCreateView.as_view(), name='blog-list-create'),
    path('blog/<int:pk>/', views.BlogDetailView.as_view(), name='blog-detail'),

    
]
