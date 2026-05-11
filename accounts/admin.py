from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, WorkerSkill, WorkerStats

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'get_full_name', 'phone', 'role', 'district', 'is_verified', 'rating']
    list_filter = ['role', 'district', 'is_verified']
    fieldsets = UserAdmin.fieldsets + (
        ('GaonKaam Profile', {'fields': ('role', 'phone', 'district', 'village', 'bio', 'profile_photo', 'rating', 'is_verified')}),
    )

admin.register(WorkerSkill)(type('WorkerSkillAdmin', (admin.ModelAdmin,), {'list_display': ['user', 'skill', 'experience_years']}))
admin.register(WorkerStats)(type('WorkerStatsAdmin', (admin.ModelAdmin,), {'list_display': ['user', 'jobs_completed', 'total_earned']}))
