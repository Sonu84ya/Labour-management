from django import forms
from .models import PaymentRecord, PaymentTransaction

class PaymentRecordForm(forms.ModelForm):
    class Meta:
        model = PaymentRecord
        fields = ['job', 'worker', 'days_worked', 'daily_rate', 'payment_method', 'notes']

class PaymentTransactionForm(forms.ModelForm):
    class Meta:
        model = PaymentTransaction
        fields = ['amount', 'method', 'transaction_ref', 'note']
