from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from jobs.models import Job
from accounts.models import User, WorkerStats

@login_required
def home_view(request):
    urgent_jobs = Job.objects.filter(status='urgent').select_related('posted_by').order_by('-created_at')[:6]
    recent_jobs = Job.objects.filter(status='open').select_related('posted_by').order_by('-created_at')[:6]
    total_jobs = Job.objects.filter(status__in=['open', 'urgent']).count()
    total_workers = User.objects.filter(role__in=['worker', 'both']).count()
    stats = None
    if request.user.is_authenticated:
        stats, _ = WorkerStats.objects.get_or_create(user=request.user)
    return render(request, 'core/home.html', {
        'urgent_jobs': urgent_jobs,
        'recent_jobs': recent_jobs,
        'total_jobs': total_jobs,
        'total_workers': total_workers,
        'stats': stats,
    })

def about_view(request):
    return render(request, 'core/about.html')


@login_required
def workers_view(request):
    from accounts.models import User, WorkerSkill, SKILL_CHOICES, DISTRICT_CHOICES
    workers = User.objects.filter(role__in=['worker', 'both']).prefetch_related('skills')

    skill    = request.GET.get('skill', '')
    district = request.GET.get('district', '')
    search   = request.GET.get('q', '')

    if skill:
        workers = workers.filter(skills__skill=skill)
    if district:
        workers = workers.filter(district=district)
    if search:
        from django.db.models import Q
        workers = workers.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(village__icontains=search)
        )

    return render(request, 'core/workers.html', {
        'workers': workers.distinct(),
        'skill_choices': SKILL_CHOICES,
        'district_choices': DISTRICT_CHOICES,
        'filters': {'skill': skill, 'district': district, 'q': search},
        'total': workers.distinct().count(),
    })
