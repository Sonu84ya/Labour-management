from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import PaymentRecord, PaymentTransaction
from jobs.models import Job, JobApplication
from accounts.models import WorkerStats
from .forms import PaymentRecordForm, PaymentTransactionForm
from django.db.models import Sum

@login_required
def payments_view(request):
    received = PaymentRecord.objects.filter(worker=request.user).select_related('job', 'employer').order_by('-created_at')
    paid_out = PaymentRecord.objects.filter(employer=request.user).select_related('job', 'worker').order_by('-created_at')
    total_earned = received.aggregate(total=Sum('amount_paid'))['total'] or 0
    total_pending_received = sum(p.amount_pending() for p in received if p.status in ('pending', 'partial'))
    total_paid_out_amount = paid_out.aggregate(total=Sum('amount_paid'))['total'] or 0
    return render(request, 'payments/payments.html', {
        'received_payments': received,
        'paid_out_payments': paid_out,
        'total_earned': total_earned,
        'total_pending': total_pending_received,
        'total_paid_out': total_paid_out_amount,
    })

@login_required
def create_payment_view(request):
    my_jobs = request.user.posted_jobs.filter(status__in=['filled', 'completed'])
    if request.method == 'POST':
        job_id = request.POST.get('job')
        worker_id = request.POST.get('worker')
        job = get_object_or_404(Job, id=job_id, posted_by=request.user)
        from accounts.models import User
        worker = get_object_or_404(User, id=worker_id)
        days = int(request.POST.get('days_worked', 1))
        method = request.POST.get('payment_method', 'cash')
        total = job.daily_wage * days
        record = PaymentRecord.objects.create(
            job=job, worker=worker, employer=request.user,
            total_amount=total, days_worked=days, daily_rate=job.daily_wage,
            payment_method=method,
        )
        messages.success(request, f'Payment record created for {worker.get_full_name()}.')
        return redirect('payment_detail', payment_id=record.id)
    accepted_apps = JobApplication.objects.filter(job__posted_by=request.user, status='accepted').select_related('job', 'applicant')
    return render(request, 'payments/create_payment.html', {'accepted_apps': accepted_apps, 'my_jobs': my_jobs})

@login_required
def payment_detail_view(request, payment_id):
    payment = get_object_or_404(PaymentRecord, id=payment_id)
    if request.user not in [payment.worker, payment.employer]:
        messages.error(request, 'Access denied.')
        return redirect('payments')
    transactions = payment.transactions.all()
    return render(request, 'payments/payment_detail.html', {'payment': payment, 'transactions': transactions})

@login_required
def add_transaction_view(request, payment_id):
    payment = get_object_or_404(PaymentRecord, id=payment_id, employer=request.user)
    if request.method == 'POST':
        amount = float(request.POST.get('amount', 0))
        method = request.POST.get('method', 'cash')
        ref = request.POST.get('reference', '')
        note = request.POST.get('note', '')
        PaymentTransaction.objects.create(payment_record=payment, amount=amount, method=method, transaction_ref=ref, note=note)
        payment.amount_paid = float(payment.amount_paid) + amount
        if payment.amount_paid >= float(payment.total_amount):
            payment.status = 'paid'
            stats, _ = WorkerStats.objects.get_or_create(user=payment.worker)
            stats.total_earned += payment.total_amount
            stats.save()
        elif payment.amount_paid > 0:
            payment.status = 'partial'
        payment.save()
        messages.success(request, f'Payment of Rs.{amount} recorded!')
        return redirect('payment_detail', payment_id=payment_id)
    return redirect('payment_detail', payment_id=payment_id)
