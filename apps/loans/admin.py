from django.contrib import admin
from .models import Borrower, Loan, Installment, Payment


@admin.register(Borrower)
class BorrowerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone', 'created_at']
    list_filter = ['created_at']
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    ordering = ['-created_at']


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ['id', 'borrower', 'principal_amount', 'profit_margin_type', 'profit_margin', 'duration_months', 'status', 'start_date']
    list_filter = ['status', 'start_date', 'created_at', 'profit_margin_type']
    search_fields = ['borrower__first_name', 'borrower__last_name', 'borrower__email']
    ordering = ['-created_at']
    readonly_fields = ['total_amount', 'total_interest', 'monthly_payment', 'profit_amount']


@admin.register(Installment)
class InstallmentAdmin(admin.ModelAdmin):
    list_display = ['loan', 'installment_number', 'due_date', 'amount', 'status', 'days_until_due']
    list_filter = ['status', 'due_date']
    search_fields = ['loan__borrower__first_name', 'loan__borrower__last_name']
    ordering = ['due_date']
    readonly_fields = ['days_until_due', 'status_color', 'is_overdue']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['installment', 'amount', 'payment_date', 'payment_method']
    list_filter = ['payment_date', 'payment_method']
    search_fields = ['installment__loan__borrower__first_name', 'installment__loan__borrower__last_name']
    ordering = ['-payment_date']
