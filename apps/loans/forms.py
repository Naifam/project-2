from django import forms
from .models import Borrower, Loan, Payment


class BorrowerForm(forms.ModelForm):
    class Meta:
        model = Borrower
        fields = ['first_name', 'last_name', 'email', 'phone', 'address']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['borrower', 'principal_amount', 'duration_months', 'profit_margin_type', 'profit_margin', 'start_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        
        # Add help text
        self.fields['principal_amount'].help_text = 'Enter the loan amount'
        self.fields['duration_months'].help_text = 'Loan duration in months'
        self.fields['profit_margin_type'].help_text = 'Choose between percentage or fixed amount'
        self.fields['profit_margin'].help_text = 'Enter profit margin (percentage or fixed amount)'
        self.fields['start_date'].help_text = 'Loan start date'

    def clean_principal_amount(self):
        principal = self.cleaned_data.get('principal_amount')
        if principal and principal <= 0:
            raise forms.ValidationError('Principal amount must be greater than 0')
        return principal

    def clean_duration_months(self):
        duration = self.cleaned_data.get('duration_months')
        if duration and duration <= 0:
            raise forms.ValidationError('Duration must be greater than 0')
        return duration

    def clean_profit_margin(self):
        margin = self.cleaned_data.get('profit_margin')
        margin_type = self.cleaned_data.get('profit_margin_type')
        
        if margin and margin < 0:
            raise forms.ValidationError('Profit margin must be greater than or equal to 0')
        
        if margin_type == 'percent' and margin > 100:
            raise forms.ValidationError('Percentage profit margin cannot exceed 100%')
        
        return margin


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'payment_date', 'payment_method', 'notes']
        widgets = {
            'payment_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        
        # Set default payment date to today
        if not self.instance.pk:
            self.fields['payment_date'].initial = forms.DateField().widget.attrs.get('value', '')
        
        # Add help text
        self.fields['amount'].help_text = 'Enter the payment amount'
        self.fields['payment_date'].help_text = 'Date when payment was received'
        self.fields['payment_method'].help_text = 'Method of payment (cash, bank transfer, etc.)'

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount and amount <= 0:
            raise forms.ValidationError('Payment amount must be greater than 0')
        return amount
