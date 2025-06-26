from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import JobListCreateAPIView,JobListView,JobDetailAPIView,JobApplicationView

urlpatterns = [
    path('jobs/', JobListCreateAPIView.as_view(), name='job-list-create'),
    path('jobs/list/', JobListView.as_view(), name='job-list'),
    path('jobs/<int:pk>/', JobDetailAPIView.as_view(), name='job-detail'),
    path('jobs/<int:job_id>/apply/', JobApplicationView.as_view(), name='job-apply'),
]
