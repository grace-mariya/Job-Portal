from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import JobSeekerProfile, EmployerProfile


User = get_user_model()

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only = True, required=True)

    class Meta:
        model = User
        fields = ['email','full_name' , 'password' , 'password2']
        extra_kwargs = {
            'email':{'required':True},
            'full_name':{'required':True},
        }
    
    def validate(self,attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password":"Passwords do not match"})
        return attrs
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user  
      
class JobSeekerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSeekerProfilefields = ['id','user','resume','skills','experience']
        read_only_fields = ['user']

class EmployerprofileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployerProfile
        fields = ['id','user','company_name','company_website','job_openings']
        read_only_field = ['user']
