from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal
from .models import Borrower, Loan, Installment, Payment
from .forms import BorrowerForm, LoanForm, PaymentForm


def dashboard(request):
    """Main dashboard with loan overview and statistics"""
    # Get current date for calculations
    today = date.today()
    
    # Basic statistics
    total_loans = Loan.objects.count()
    active_loans = Loan.objects.filter(status='active').count()
    total_borrowers = Borrower.objects.count()
    
    # Financial statistics
    total_principal = Loan.objects.aggregate(total=Sum('principal_amount'))['total'] or 0
    total_outstanding = Loan.objects.filter(status='active').aggregate(total=Sum('principal_amount'))['total'] or 0
    
    # Payment statistics
    overdue_installments = Installment.objects.filter(
        due_date__lt=today,
        status__in=['pending', 'partial']
    ).count()
    
    due_soon_installments = Installment.objects.filter(
        due_date__lte=today + timedelta(days=10),
        due_date__gte=today,
        status__in=['pending', 'partial']
    ).count()
    
    # Recent loans
    recent_loans = Loan.objects.select_related('borrower').order_by('-created_at')[:5]
    
    # Overdue installments
    overdue_installments_list = Installment.objects.filter(
        due_date__lt=today,
        status__in=['pending', 'partial']
    ).select_related('loan__borrower').order_by('due_date')[:10]
    
    # Due soon installments
    due_soon_installments_list = Installment.objects.filter(
        due_date__lte=today + timedelta(days=10),
        due_date__gte=today,
        status__in=['pending', 'partial']
    ).select_related('loan__borrower').order_by('due_date')[:10]
    
    context = {
        'total_loans': total_loans,
        'active_loans': active_loans,
        'total_borrowers': total_borrowers,
        'total_principal': total_principal,
        'total_outstanding': total_outstanding,
        'overdue_installments': overdue_installments,
        'due_soon_installments': due_soon_installments,
        'recent_loans': recent_loans,
        'overdue_installments_list': overdue_installments_list,
        'due_soon_installments_list': due_soon_installments_list,
    }
    
    return render(request, 'loans/dashboard.html', context)


def borrower_list(request):
    """List all borrowers"""
    borrowers = Borrower.objects.all().order_by('-created_at')
    return render(request, 'loans/borrower_list.html', {'borrowers': borrowers})


def borrower_detail(request, pk):
    """View borrower details and their loans"""
    borrower = get_object_or_404(Borrower, pk=pk)
    loans = borrower.loans.all().order_by('-created_at')
    
    context = {
        'borrower': borrower,
        'loans': loans,
    }
    return render(request, 'loans/borrower_detail.html', context)


def borrower_create(request):
    """Create new borrower"""
    if request.method == 'POST':
        form = BorrowerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Borrower created successfully!')
            return redirect('loans:borrower_list')
    else:
        form = BorrowerForm()
    
    return render(request, 'loans/borrower_form.html', {'form': form, 'title': 'Add New Borrower'})


def borrower_edit(request, pk):
    """Edit borrower"""
    borrower = get_object_or_404(Borrower, pk=pk)
    if request.method == 'POST':
        form = BorrowerForm(request.POST, instance=borrower)
        if form.is_valid():
            form.save()
            messages.success(request, 'Borrower updated successfully!')
            return redirect('loans:borrower_detail', pk=borrower.pk)
    else:
        form = BorrowerForm(instance=borrower)
    
    return render(request, 'loans/borrower_form.html', {'form': form, 'title': 'Edit Borrower'})


def loan_list(request):
    """List all loans"""
    loans = Loan.objects.select_related('borrower').all().order_by('-created_at')
    return render(request, 'loans/loan_list.html', {'loans': loans})


def loan_detail(request, pk):
    """View loan details and installments"""
    loan = get_object_or_404(Loan, pk=pk)
    installments = loan.installments.all().order_by('due_date')
    
    # Calculate loan statistics
    paid_installments = installments.filter(status='paid').count()
    pending_installments = installments.filter(status='pending').count()
    overdue_installments = installments.filter(status='overdue').count()
    
    total_paid = installments.filter(status='paid').aggregate(total=Sum('amount'))['total'] or 0
    remaining_balance = loan.principal_amount - total_paid
    
    context = {
        'loan': loan,
        'installments': installments,
        'paid_installments': paid_installments,
        'pending_installments': pending_installments,
        'overdue_installments': overdue_installments,
        'total_paid': total_paid,
        'remaining_balance': remaining_balance,
    }
    return render(request, 'loans/loan_detail.html', context)


def loan_create(request):
    """Create new loan"""
    if request.method == 'POST':
        form = LoanForm(request.POST)
        if form.is_valid():
            loan = form.save()
            # Generate installments
            generate_installments(loan)
            messages.success(request, 'Loan created successfully!')
            return redirect('loans:loan_detail', pk=loan.pk)
    else:
        form = LoanForm()
    
    return render(request, 'loans/loan_form.html', {'form': form, 'title': 'Create New Loan'})


def loan_edit(request, pk):
    """Edit loan"""
    loan = get_object_or_404(Loan, pk=pk)
    if request.method == 'POST':
        form = LoanForm(request.POST, instance=loan)
        if form.is_valid():
            form.save()
            messages.success(request, 'Loan updated successfully!')
            return redirect('loans:loan_detail', pk=loan.pk)
    else:
        form = LoanForm(instance=loan)
    
    return render(request, 'loans/loan_form.html', {'form': form, 'title': 'Edit Loan'})


def installment_list(request):
    """List all installments with status filtering"""
    status_filter = request.GET.get('status', 'all')
    due_filter = request.GET.get('due', 'all')
    
    installments = Installment.objects.select_related('loan__borrower').all()
    
    # Apply filters
    if status_filter != 'all':
        installments = installments.filter(status=status_filter)
    
    if due_filter == 'overdue':
        installments = installments.filter(due_date__lt=date.today(), status__in=['pending', 'partial'])
    elif due_filter == 'due_soon':
        installments = installments.filter(
            due_date__lte=date.today() + timedelta(days=10),
            due_date__gte=date.today(),
            status__in=['pending', 'partial']
        )
    
    installments = installments.order_by('due_date')
    
    context = {
        'installments': installments,
        'status_filter': status_filter,
        'due_filter': due_filter,
    }
    return render(request, 'loans/installment_list.html', context)


def payment_create(request, installment_pk):
    """Record payment for an installment"""
    installment = get_object_or_404(Installment, pk=installment_pk)
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.installment = installment
            payment.save()
            
            # Update installment status
            update_installment_status(installment)
            
            messages.success(request, 'Payment recorded successfully!')
            return redirect('loans:loan_detail', pk=installment.loan.pk)
    else:
        form = PaymentForm()
    
    context = {
        'form': form,
        'installment': installment,
        'title': f'Record Payment - {installment.loan.borrower}',
    }
    return render(request, 'loans/payment_form.html', context)


def generate_installments(loan):
    """Generate installments for a loan"""
    monthly_payment = loan.monthly_payment
    current_date = loan.start_date
    
    for i in range(1, loan.duration_months + 1):
        # Calculate due date (30 days from previous installment)
        due_date = current_date + timedelta(days=30)
        
        Installment.objects.create(
            loan=loan,
            installment_number=i,
            due_date=due_date,
            amount=monthly_payment
        )
        
        current_date = due_date


def update_installment_status(installment):
    """Update installment status based on payments"""
    total_paid = installment.payments.aggregate(total=Sum('amount'))['total'] or 0
    
    if total_paid >= installment.amount:
        installment.status = 'paid'
        installment.paid_amount = installment.amount
        if not installment.paid_date:
            installment.paid_date = date.today()
    elif total_paid > 0:
        installment.status = 'partial'
        installment.paid_amount = total_paid
    else:
        installment.status = 'pending'
        installment.paid_amount = 0
    
    # Check if overdue
    if installment.due_date < date.today() and installment.status != 'paid':
        installment.status = 'overdue'
    
    installment.save()
