from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Job, JobApplication, JobReview, WORK_TYPE_CHOICES, JOB_STATUS_CHOICES
from .forms import JobForm, ApplicationForm, ReviewForm
from accounts.models import WorkerStats

def job_list_view(request):
    jobs = Job.objects.select_related('posted_by').all()
    work_type = request.GET.get('work_type', '')
    district = request.GET.get('district', '')
    status = request.GET.get('status', '')
    search = request.GET.get('q', '')
    min_wage = request.GET.get('min_wage', '')
    max_wage = request.GET.get('max_wage', '')

    if work_type:
        jobs = jobs.filter(work_type=work_type)
    if district:
        jobs = jobs.filter(district__icontains=district)
    if status:
        jobs = jobs.filter(status=status)
    if search:
        jobs = jobs.filter(Q(title__icontains=search) | Q(description__icontains=search) | Q(village__icontains=search))
    if min_wage:
        jobs = jobs.filter(daily_wage__gte=min_wage)
    if max_wage:
        jobs = jobs.filter(daily_wage__lte=max_wage)

    urgent_jobs = jobs.filter(status='urgent')[:4]
    open_jobs = jobs.filter(status='open')

    context = {
        'jobs': jobs,
        'urgent_jobs': urgent_jobs,
        'open_jobs': open_jobs,
        'work_types': WORK_TYPE_CHOICES,
        'status_choices': JOB_STATUS_CHOICES,
        'filters': {'work_type': work_type, 'district': district, 'status': status, 'q': search},
        'total_count': jobs.count(),
    }
    return render(request, 'jobs/job_list.html', context)

def job_detail_view(request, job_id):
    job = get_object_or_404(Job.objects.select_related('posted_by'), id=job_id)
    applications = job.applications.select_related('applicant').all()
    user_application = None
    if request.user.is_authenticated:
        user_application = applications.filter(applicant=request.user).first()
    reviews = job.reviews.select_related('reviewer', 'reviewed_user').all()
    return render(request, 'jobs/job_detail.html', {
        'job': job,
        'applications': applications,
        'user_application': user_application,
        'reviews': reviews,
        'can_apply': request.user.is_authenticated and not user_application and job.posted_by != request.user and not job.is_full(),
    })

@login_required
def post_job_view(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            stats, _ = WorkerStats.objects.get_or_create(user=request.user)
            stats.jobs_posted += 1
            stats.save()
            messages.success(request, f'Job "{job.title}" posted successfully! Workers can now see it. ✅')
            return redirect('job_detail', job_id=job.id)
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = JobForm()
    return render(request, 'jobs/post_job.html', {'form': form})

@login_required
def edit_job_view(request, job_id):
    job = get_object_or_404(Job, id=job_id, posted_by=request.user)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated!')
            return redirect('job_detail', job_id=job.id)
    else:
        form = JobForm(instance=job)
    return render(request, 'jobs/post_job.html', {'form': form, 'editing': True, 'job': job})

@login_required
def apply_job_view(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if job.posted_by == request.user:
        messages.error(request, "You cannot apply to your own job.")
        return redirect('job_detail', job_id=job_id)
    if JobApplication.objects.filter(job=job, applicant=request.user).exists():
        messages.warning(request, "You have already applied to this job.")
        return redirect('job_detail', job_id=job_id)
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.job = job
            app.applicant = request.user
            app.save()
            messages.success(request, f'Applied to "{job.title}" successfully! The employer will contact you. 🙏')
            return redirect('job_detail', job_id=job_id)
    else:
        form = ApplicationForm()
    return render(request, 'jobs/apply_job.html', {'form': form, 'job': job})

@login_required
def my_jobs_view(request):
    posted = request.user.posted_jobs.all()
    applied = request.user.applications.select_related('job', 'job__posted_by').all()
    return render(request, 'jobs/my_jobs.html', {'posted_jobs': posted, 'applied_jobs': applied})

@login_required
def update_application_view(request, app_id, action):
    app = get_object_or_404(JobApplication, id=app_id, job__posted_by=request.user)
    if action == 'accept':
        app.status = 'accepted'
        app.job.workers_filled += 1
        if app.job.workers_filled >= app.job.workers_needed:
            app.job.status = 'filled'
        app.job.save()
        messages.success(request, f'Accepted {app.applicant.get_full_name()}!')
    elif action == 'reject':
        app.status = 'rejected'
        messages.info(request, f'Rejected application from {app.applicant.get_full_name()}.')
    app.save()
    return redirect('job_detail', job_id=app.job.id)


from django.http import JsonResponse
from django.views.decorators.http import require_POST

@login_required
@require_POST
def submit_review_view(request):
    """AJAX endpoint to submit a job review."""
    from django.db.models import Avg
    job_id          = request.POST.get('job')
    reviewed_user_id= request.POST.get('reviewed_user')
    rating_val      = request.POST.get('rating')
    comment         = request.POST.get('comment', '')

    try:
        job           = Job.objects.get(id=job_id)
        from accounts.models import User as AuthUser
        reviewed_user = AuthUser.objects.get(id=reviewed_user_id)
        rating        = int(rating_val)
        if not (1 <= rating <= 5):
            raise ValueError('Invalid rating')
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

    if JobReview.objects.filter(job=job, reviewer=request.user, reviewed_user=reviewed_user).exists():
        return JsonResponse({'success': False, 'error': 'You have already reviewed this user for this job.'})

    JobReview.objects.create(
        job=job, reviewer=request.user,
        reviewed_user=reviewed_user,
        rating=rating, comment=comment
    )

    # Update average rating on the reviewed user
    avg = reviewed_user.received_reviews.aggregate(avg=Avg('rating'))['avg'] or 0
    reviewed_user.rating       = round(avg, 1)
    reviewed_user.total_reviews = reviewed_user.received_reviews.count()
    reviewed_user.save()

    return JsonResponse({'success': True, 'new_rating': float(reviewed_user.rating)})
