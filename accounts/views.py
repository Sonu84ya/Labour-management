from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg
from .models import User, WorkerSkill, WorkerStats, SKILL_CHOICES, DISTRICT_CHOICES, ROLE_CHOICES
from .forms import RegisterForm, LoginForm, ProfileForm

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            WorkerStats.objects.create(user=user)
            login(request, user)
            messages.success(request, f'Welcome to GaonKaam, {user.first_name}! 🙏')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile_view(request, user_id=None):
    if user_id:
        profile_user = get_object_or_404(User, id=user_id)
    else:
        profile_user = request.user
    stats, _ = WorkerStats.objects.get_or_create(user=profile_user)
    skills = profile_user.skills.all()
    reviews = profile_user.received_reviews.select_related('reviewer', 'job').order_by('-created_at')[:10]
    posted_jobs = profile_user.posted_jobs.all()[:5]
    return render(request, 'accounts/profile.html', {
        'profile_user': profile_user,
        'stats': stats,
        'skills': skills,
        'reviews': reviews,
        'posted_jobs': posted_jobs,
        'is_own_profile': profile_user == request.user,
    })

@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            # Handle skills
            request.user.skills.all().delete()
            selected_skills = request.POST.getlist('skills')
            for skill in selected_skills:
                WorkerSkill.objects.create(user=request.user, skill=skill)
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    user_skills = list(request.user.skills.values_list('skill', flat=True))
    return render(request, 'accounts/edit_profile.html', {
        'form': form,
        'all_skills': SKILL_CHOICES,
        'user_skills': user_skills,
    })
