from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSignupSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .models import JobSeekerProfile,EmployerProfile
from .serializers import JobSeekerProfileSerializer,EmployerProfileSerializer
from rest_framework import viewsets, permissions
from accounts.models import RoleEnum
from rest_framework.permissions import AllowAny
# Create your views here.
class UserSignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_class = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token =RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=205)
        except Exception as e:
            return Response(status = 400)

class ProfileDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role == RoleEnum.JOBSEEKER:
            profile = JobSeekerProfile.objects.filter(user=user).first()
            serializer = JobSeekerProfileSerializer(profile)
        elif user.role == RoleEnum.EMPLOYER:
            profile = EmployerProfile.objects.filter(user=user).first()
            serializer = EmployerProfileSerializer(profile)
        else:
            return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)

class ProfileCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        if user.role == RoleEnum.JOBSEEKER:
            if hasattr(user, 'jobseekerprofile'):
                return Response({"detail": "Job seeker profile already exists."}, status=status.HTTP_400_BAD_REQUEST)
            serializer = JobSeekerProfileSerializer(data=request.data, context={'request': request})

        elif user.role == RoleEnum.EMPLOYER:
            if hasattr(user, 'employerprofile'):
                return Response({"detail": "Employer profile already exists."}, status=status.HTTP_400_BAD_REQUEST)
            serializer = EmployerProfileSerializer(data=request.data, context={'request': request})

        else:
            return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def post(self, request):
        user = request.user

        if user.role == RoleEnum.JOBSEEKER:
            if hasattr(user, 'jobseekerprofile'):
                return Response({"detail": "Job seeker profile already exists."}, status=status.HTTP_400_BAD_REQUEST)
            serializer = JobSeekerProfileSerializer(data=request.data, context={'request': request})

        elif user.role == RoleEnum.EMPLOYER:
            if hasattr(user, 'employerprofile'):
                return Response({"detail": "Employer profile already exists."}, status=status.HTTP_400_BAD_REQUEST)
            serializer = EmployerProfileSerializer(data=request.data, context={'request': request})

        else:
            return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        user = request.user

        if user.role == RoleEnum.JOBSEEKER:
            profile = JobSeekerProfile.objects.filter(user=user).first()
            serializer = JobSeekerProfileSerializer(profile, data=request.data, context={'request': request})
        elif user.role == RoleEnum.EMPLOYER:
            profile = EmployerProfile.objects.filter(user=user).first()
            serializer = EmployerProfileSerializer(profile, data=request.data, context={'request': request})
        else:
            return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)

        if not profile:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        user = request.user

        if user.role == RoleEnum.JOBSEEKER:
            profile = JobSeekerProfile.objects.filter(user=user).first()
            serializer = JobSeekerProfileSerializer(profile, data=request.data, partial=True, context={'request': request})
        elif user.role == RoleEnum.EMPLOYER:
            profile = EmployerProfile.objects.filter(user=user).first()
            serializer = EmployerProfileSerializer(profile, data=request.data, partial=True, context={'request': request})
        else:
            return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)

        if not profile:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user

        if user.role == RoleEnum.JOBSEEKER:
            profile = JobSeekerProfile.objects.filter(user=user).first()
        elif user.role == RoleEnum.EMPLOYER:
            profile = EmployerProfile.objects.filter(user=user).first()
        else:
            return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)

        if not profile:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        profile.delete()
        return Response({"message": "Profile deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
