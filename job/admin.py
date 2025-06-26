from django.contrib import admin
from .models import Job
# Register your models here.
admin.site.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display =('title','employer','job_type','location','posted_at')
    search_fields = ('title','location','employer_full_name')
    list_filter = ('job_type','posted_at')