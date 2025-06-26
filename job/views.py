from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.exceptions import PermissionDenied
from .models import JobApplication
from .serializers import JobApplicationSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Job
from .serializers import JobSerializer

# Custom permission for employers
class IsEmployer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'employer'


class JobListCreateAPIView(APIView):
    permission_classes = [permissions.AllowAny]  # Public access for GET

    def get(self, request):
        jobs = Job.objects.filter(is_deleted=False)
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not IsEmployer().has_permission(request, self):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(employer=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobListView(ListAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        title = self.request.query_params.get('title')
        location = self.request.query_params.get('location')
        job_type = self.request.query_params.get('job_type')

        if title:
            queryset = queryset.filter(title__icontains=title)
        if location:
            queryset = queryset.filter(location__icontains=location)
        if job_type:
            queryset = queryset.filter(job_type=job_type)

        return queryset


class JobDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk, user):
        job = get_object_or_404(Job, pk=pk, is_deleted=False)
        if job.employer != user and user.role == 'employer':
            raise PermissionDenied("You can only manage your own jobs.")
        return job

    def get(self, request, pk):
        job = get_object_or_404(Job, pk=pk, is_deleted=False)
        serializer = JobSerializer(job)
        return Response(serializer.data)

    def put(self, request, pk):
        job = self.get_object(pk, request.user)
        serializer = JobSerializer(job, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        job = self.get_object(pk, request.user)
        serializer = JobSerializer(job, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        job = self.get_object(pk, request.user)
        job.is_deleted = True
        job.save()
        return Response({'detail': 'Job soft-deleted.'}, status=status.HTTP_204_NO_CONTENT)

class JobApplicationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, job_id):
        data = request.data.copy()
        data['job'] = job_id
        serializer = JobApplicationSerializer(data=data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        
        return Response(serializer.errors, status=400)

