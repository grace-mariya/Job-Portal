from django.db import models
from django.conf import settings
from django.utils import timezone
from accounts.models import User

class Job(models.Model):
    JOB_TYPE_CHOICES = [
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
        ('Internship', 'Internship'),
        ('Contract', 'Contract'),
    ]

    # employer field cannot have a blank string default
    # You can either make it nullable during development or assign a default user ID (not ideal in production)
    employer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,  # Only for development/testing
        blank=True,
        limit_choices_to={'role': 'employer'}
    )
    
    title = models.CharField(max_length=255, default='Untitled Job')
    description = models.TextField(default='No description provided.')
    location = models.CharField(max_length=255, default='Remote')
    job_type = models.CharField(max_length=50, choices=JOB_TYPE_CHOICES, default='Full-time')
    posted_at = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default = False)

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()
    def __str__(self):
        return f"{self.title} - {self.employer.full_name if self.employer else 'Unknown'}"

class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cover_letter = models.TextField(blank=True)
    resume = models.FileField(upload_to='resumes/')  # optional
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('job', 'applicant')  # prevent duplicate applications

    def __str__(self):
        return f"{self.applicant.email} applied to {self.job.title}"