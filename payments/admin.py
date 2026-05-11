from django.contrib import admin
from .models import PaymentRecord, PaymentTransaction

@admin.register(PaymentRecord)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['job', 'worker', 'employer', 'total_amount', 'amount_paid', 'status', 'payment_method', 'created_at']
    list_filter = ['status', 'payment_method']

@admin.register(PaymentTransaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['payment_record', 'amount', 'method', 'paid_at']
