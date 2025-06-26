from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import JobSeekerProfile, EmployerProfile
from accounts.models import RoleEnum

User = get_user_model()

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    role = serializers.ChoiceField(choices=RoleEnum.choices)

    class Meta:
        model = User
        fields = ['email', 'full_name', 'password', 'password2', 'role']
        extra_kwargs = {
            'email': {'required': True},
            'full_name': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        role = validated_data.pop('role')  
        user = User.objects.create_user(**validated_data)
        user.role = role                   
        return user
      
class JobSeekerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSeekerProfile
        fields = ['resume', 'skills', 'experience']  # exclude 'user'

    def create(self, validated_data):
        user = self.context['request'].user  # get user from request
        return JobSeekerProfile.objects.create(user=user, **validated_data)  # adjust fields as per your model

class EmployerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployerProfile
        fields = ['company_name', 'company_website', 'job_openings']

    def create(self, validated_data):
        user = self.context['request'].user
        return EmployerProfile.objects.create(user=user, **validated_data)