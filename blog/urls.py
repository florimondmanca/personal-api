"""Blog URL configuration."""

from django.urls import path
from . import views


urlpatterns = [
    path('', views.PostListView.as_view(), name='post-list'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('new/', views.PostCreateView.as_view(), name='post-create'),
]
