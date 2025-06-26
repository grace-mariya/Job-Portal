from rest_framework import serializers
from .models import Job
from .models import JobApplication


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ['employer', 'posted_at']

class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ['id', 'job', 'cover_letter', 'resume', 'applied_at']
        read_only_fields = ['id', 'applied_at']

    def create(self, validated_data):
        validated_data['applicant'] = self.context['request'].user
        return super().create(validated_data)
