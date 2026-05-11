from django.contrib import admin
from .models import Job, JobApplication, JobReview

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'posted_by', 'work_type', 'status', 'village', 'district', 'daily_wage', 'workers_needed', 'workers_filled', 'created_at']
    list_filter = ['work_type', 'status', 'district']
    search_fields = ['title', 'village', 'district', 'posted_by__username']

@admin.register(JobApplication)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['job', 'applicant', 'status', 'applied_at']
    list_filter = ['status']

@admin.register(JobReview)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['job', 'reviewer', 'reviewed_user', 'rating', 'created_at']
