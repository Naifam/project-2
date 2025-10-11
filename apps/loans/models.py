from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
import math
from datetime import date, timedelta


class Borrower(models.Model):
    """Model to store borrower information"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ['-created_at']


class Loan(models.Model):
    """Model to store loan information"""
    LOAN_STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('defaulted', 'Defaulted'),
        ('cancelled', 'Cancelled'),
    ]

    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE, related_name='loans')
    principal_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    duration_months = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(360)])
    profit_margin_type = models.CharField(max_length=10, choices=[('percent', 'Percentage'), ('fixed', 'Fixed Amount')], default='percent')
    profit_margin = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    start_date = models.DateField()
    status = models.CharField(max_length=20, choices=LOAN_STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Loan #{self.id} - {self.borrower} - ${self.principal_amount}"

    @property
    def profit_amount(self):
        """Calculate profit amount based on margin type"""
        if self.profit_margin_type == 'percent':
            return self.principal_amount * (self.profit_margin / 100)
        else:  # fixed amount
            return self.profit_margin

    @property
    def total_amount(self):
        """Calculate total amount to be paid (principal + profit)"""
        return self.principal_amount + self.profit_amount

    @property
    def monthly_payment(self):
        """Calculate monthly payment (total amount divided by duration)"""
        return self.total_amount / self.duration_months

    @property
    def total_interest(self):
        """Calculate total profit to be paid"""
        return self.profit_amount

    @property
    def end_date(self):
        """Calculate loan end date"""
        return self.start_date + timedelta(days=30 * self.duration_months)

    def get_remaining_balance(self):
        """Calculate remaining balance"""
        paid_installments = self.installments.filter(status='paid').count()
        return self.principal_amount - (self.monthly_payment * paid_installments)

    class Meta:
        ordering = ['-created_at']


class Installment(models.Model):
    """Model to store installment information"""
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('partial', 'Partial'),
    ]

    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='installments')
    installment_number = models.PositiveIntegerField()
    due_date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    paid_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Installment #{self.installment_number} - {self.loan.borrower} - ${self.amount}"

    @property
    def days_until_due(self):
        """Calculate days until due date"""
        return (self.due_date - date.today()).days

    @property
    def status_color(self):
        """Return color class based on payment status and due date"""
        if self.status == 'paid':
            return 'success'  # Green
        elif self.status == 'overdue':
            return 'danger'   # Red
        elif self.days_until_due <= 10:
            return 'danger'   # Red
        elif self.days_until_due <= 30:
            return 'warning'  # Yellow
        else:
            return 'success'  # Green

    @property
    def is_overdue(self):
        """Check if installment is overdue"""
        return self.due_date < date.today() and self.status != 'paid'

    @property
    def remaining_balance(self):
        """Calculate remaining balance for this installment"""
        return self.amount - self.paid_amount

    @property
    def payment_progress(self):
        """Calculate payment progress percentage"""
        if self.amount == 0:
            return 0
        return (self.paid_amount / self.amount) * 100

    class Meta:
        ordering = ['due_date']
        unique_together = ['loan', 'installment_number']


class Payment(models.Model):
    """Model to store payment information"""
    installment = models.ForeignKey(Installment, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=50, default='cash')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment - {self.installment.loan.borrower} - ${self.amount}"

    class Meta:
        ordering = ['-payment_date']
