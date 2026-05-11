from django import forms
from .models import Job, JobApplication, JobReview

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'work_type', 'status', 'village', 'district',
                  'daily_wage', 'workers_needed', 'duration', 'start_date',
                  'meals_provided', 'transport_provided', 'tools_required']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Wheat Harvest Help Needed'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 4, 'placeholder': 'Describe the work...'}),
            'work_type': forms.Select(attrs={'class': 'form-input'}),
            'status': forms.Select(attrs={'class': 'form-input'}),
            'village': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Bhumidanda'}),
            'district': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Sindhupalchok'}),
            'daily_wage': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'e.g. 800'}),
            'workers_needed': forms.NumberInput(attrs={'class': 'form-input', 'min': 1}),
            'duration': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. 3 days, 2 weeks'}),
            'start_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
        }

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-input', 'rows': 4,
                'placeholder': 'Introduce yourself, your experience, and why you want this job...'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = JobReview
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-input'}),
            'comment': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
        }
