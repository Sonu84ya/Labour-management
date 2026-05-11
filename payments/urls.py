from django.urls import path
from . import views

urlpatterns = [
    path('', views.payments_view, name='payments'),
    path('create/', views.create_payment_view, name='create_payment'),
    path('<int:payment_id>/', views.payment_detail_view, name='payment_detail'),
    path('<int:payment_id>/add/', views.add_transaction_view, name='add_transaction'),
]
