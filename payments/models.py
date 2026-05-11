from django.db import models
from django.conf import settings

PAYMENT_STATUS = [
    ('pending', 'Pending'),
    ('partial', 'Partial'),
    ('paid', 'Paid'),
    ('disputed', 'Disputed'),
    ('cancelled', 'Cancelled'),
]

PAYMENT_METHOD = [
    ('cash', 'Cash'),
    ('esewa', 'eSewa'),
    ('khalti', 'Khalti'),
    ('bank', 'Bank Transfer'),
    ('imepay', 'IME Pay'),
]

class PaymentRecord(models.Model):
    job = models.ForeignKey('jobs.Job', on_delete=models.CASCADE, related_name='payments')
    worker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_payments')
    employer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='made_payments')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    days_worked = models.IntegerField(default=0)
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD, default='cash')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment: {self.worker.username} ← {self.job.title} Rs.{self.total_amount}"

    def amount_pending(self):
        return self.total_amount - self.amount_paid

    def fill_percentage(self):
        if self.total_amount == 0:
            return 0
        return int((self.amount_paid / self.total_amount) * 100)

class PaymentTransaction(models.Model):
    payment_record = models.ForeignKey(PaymentRecord, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    method = models.CharField(max_length=20, choices=PAYMENT_METHOD, default='cash')
    transaction_ref = models.CharField(max_length=100, blank=True)
    paid_at = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Txn Rs.{self.amount} via {self.method}"
