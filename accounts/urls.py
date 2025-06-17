from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)
from .views import UserSignupView, JobSeekerProfileViewSet, EmployerProfileViewSet

# Setup the router
router = DefaultRouter()
router.register(r'jobseekers', JobSeekerProfileViewSet, basename='jobseeker')
router.register(r'employers', EmployerProfileViewSet, basename='employer')

# Combine all urls in a single urlpatterns list
urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('', include(router.urls)),
]
