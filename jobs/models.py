from django.db import models
from django.conf import settings

WORK_TYPE_CHOICES = [
    ('farming', '🌾 Farming'),
    ('construction', '🏗️ Construction'),
    ('domestic', '🏠 Domestic Help'),
    ('loading', '🚛 Loading/Unloading'),
    ('craft', '🎨 Craft & Weaving'),
    ('carpentry', '🪚 Carpentry'),
    ('irrigation', '🌱 Irrigation'),
    ('driving', '🚗 Driving'),
    ('cooking', '🍳 Cooking'),
    ('other', '🔧 Other'),
]

JOB_STATUS_CHOICES = [
    ('open', 'Open'),
    ('urgent', 'Urgent'),
    ('filled', 'Filled'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
]

class Job(models.Model):
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posted_jobs')
    title = models.CharField(max_length=200)
    description = models.TextField()
    work_type = models.CharField(max_length=50, choices=WORK_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=JOB_STATUS_CHOICES, default='open')
    village = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    daily_wage = models.DecimalField(max_digits=10, decimal_places=2)
    workers_needed = models.IntegerField(default=1)
    workers_filled = models.IntegerField(default=0)
    duration = models.CharField(max_length=100, help_text="e.g. 3 days, 2 weeks")
    start_date = models.DateField(null=True, blank=True)
    meals_provided = models.BooleanField(default=False)
    transport_provided = models.BooleanField(default=False)
    tools_required = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} – {self.village}"

    def spots_remaining(self):
        return self.workers_needed - self.workers_filled

    def is_full(self):
        return self.workers_filled >= self.workers_needed

    def fill_percentage(self):
        needed = self.workers_needed or 0
        filled = self.workers_filled or 0
        if needed == 0:
            return 0
        return int((filled / needed) * 100)

    def fill_percentage_css(self):
        return f"{self.fill_percentage()}%"

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    message = models.TextField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('job', 'applicant')
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.applicant.username} → {self.job.title}"

class JobReview(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='given_reviews')
    reviewed_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('job', 'reviewer', 'reviewed_user')

    def __str__(self):
        return f"Review by {self.reviewer.username} for {self.reviewed_user.username}"
