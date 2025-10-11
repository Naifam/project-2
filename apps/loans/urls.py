from django.urls import path
from . import views

app_name = 'loans'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Borrower URLs
    path('borrowers/', views.borrower_list, name='borrower_list'),
    path('borrowers/create/', views.borrower_create, name='borrower_create'),
    path('borrowers/<int:pk>/', views.borrower_detail, name='borrower_detail'),
    path('borrowers/<int:pk>/edit/', views.borrower_edit, name='borrower_edit'),
    
    # Loan URLs
    path('loans/', views.loan_list, name='loan_list'),
    path('loans/create/', views.loan_create, name='loan_create'),
    path('loans/<int:pk>/', views.loan_detail, name='loan_detail'),
    path('loans/<int:pk>/edit/', views.loan_edit, name='loan_edit'),
    
    # Installment URLs
    path('installments/', views.installment_list, name='installment_list'),
    
    # Payment URLs
    path('payments/<int:installment_pk>/create/', views.payment_create, name='payment_create'),
]
