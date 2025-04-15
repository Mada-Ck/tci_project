from django import forms
from .models import Donation, ContactMessage

class DonationForm(forms.ModelForm):
    specific_program = forms.ChoiceField(
        choices=[
            ('', 'Choose a program'),
            ('hiv_services', 'HIV Services'),
            ('youth_empowerment', 'Youth Empowerment'),
            ('community_empowerment', 'Community Empowerment'),
            ('education', 'Education'),
        ],
        required=False
    )
    phone_number = forms.CharField(max_length=12, required=False)
    currency = forms.ChoiceField(
        choices=[('MWK', 'Malawi Kwacha'), ('USD', 'US Dollar')],
        widget=forms.RadioSelect,
        initial='MWK'
    )

    class Meta:
        model = Donation
        fields = ['donation_purpose', 'specific_program', 'donor_name', 'amount', 'currency', 'payment_method', 'phone_number']
        widgets = {
            'donation_purpose': forms.Select,
            'payment_method': forms.RadioSelect,
            'amount': forms.NumberInput(attrs={'min': '1000', 'step': '100'}),
            'donor_name': forms.TextInput(attrs={'placeholder': 'Enter your name'}),
            'phone_number': forms.TextInput(attrs={'placeholder': '+265xxxxxxxxx'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        donation_purpose = cleaned_data.get('donation_purpose')
        specific_program = cleaned_data.get('specific_program')
        payment_method = cleaned_data.get('payment_method')
        phone_number = cleaned_data.get('phone_number')
        currency = cleaned_data.get('currency')
        amount = cleaned_data.get('amount')

        # Validate specific program
        if donation_purpose == 'specific_program' and not specific_program:
            self.add_error('specific_program', 'Please select a specific program.')

        # Validate mobile payments
        if payment_method in ('airtel_money', 'tnm_mpamba'):
            if currency != 'MWK':
                self.add_error('currency', 'Mobile payments are only available in Malawi Kwacha.')
            if not phone_number:
                self.add_error('phone_number', 'Phone number is required for mobile payments.')
            elif not phone_number.startswith('+265') or len(phone_number) != 12:
                self.add_error('phone_number', 'Phone number must be in the format +265xxxxxxxxx.')

        # Validate amount
        if amount and amount < 1000:
            self.add_error('amount', f'Amount must be at least 1000 {currency}.')

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your Email'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'placeholder': 'Your Message'}),
        }