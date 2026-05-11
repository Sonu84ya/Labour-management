from django.contrib.auth.models import AbstractUser
from django.db import models

DISTRICT_CHOICES = [
    ('sindhupalchok', 'Sindhupalchok'),
    ('nuwakot', 'Nuwakot'),
    ('kavrepalanchok', 'Kavrepalanchok'),
    ('makwanpur', 'Makwanpur'),
    ('dhading', 'Dhading'),
    ('rasuwa', 'Rasuwa'),
    ('lalitpur', 'Lalitpur'),
    ('bhaktapur', 'Bhaktapur'),
    ('kathmandu', 'Kathmandu'),
    ('other', 'Other'),
]

ROLE_CHOICES = [
    ('worker', 'Worker'),
    ('employer', 'Employer / Job Poster'),
    ('both', 'Both'),
]

class User(AbstractUser):
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='worker')
    phone = models.CharField(max_length=15, blank=True)
    district = models.CharField(max_length=50, choices=DISTRICT_CHOICES, default='sindhupalchok')
    village = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    total_reviews = models.IntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.role})"

    def get_initials(self):
        name = self.get_full_name()
        if name:
            parts = name.split()
            return (parts[0][0] + parts[-1][0]).upper() if len(parts) > 1 else parts[0][:2].upper()
        return self.username[:2].upper()

SKILL_CHOICES = [
    ('farming', '🌾 Farming'),
    ('construction', '🏗️ Construction'),
    ('domestic', '🏠 Domestic Help'),
    ('loading', '🚛 Loading/Unloading'),
    ('craft', '🎨 Craft & Weaving'),
    ('carpentry', '🪚 Carpentry'),
    ('irrigation', '🌱 Irrigation'),
    ('driving', '🚗 Driving'),
    ('cooking', '🍳 Cooking'),
    ('plumbing', '🔧 Plumbing'),
]

class WorkerSkill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')
    skill = models.CharField(max_length=50, choices=SKILL_CHOICES)
    experience_years = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user', 'skill')

    def __str__(self):
        return f"{self.user.username} - {self.skill}"

class WorkerStats(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='stats')
    jobs_completed = models.IntegerField(default=0)
    jobs_posted = models.IntegerField(default=0)
    total_earned = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_paid_out = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"Stats for {self.user.username}"
