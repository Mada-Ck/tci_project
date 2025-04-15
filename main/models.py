from django.db import models

class Donation(models.Model):
    DONATION_PURPOSES = [
        ('child', 'Donate for a Child'),
        ('specific_program', 'Donate for a Specific Program'),
        ('general_program', 'Donate for a Program'),
        ('general', 'General Donation'),
    ]

    PAYMENT_METHODS = [
        ('bank_transfer', 'Bank Transfer'),
        ('airtel_money', 'Airtel Money'),
        ('tnm_mpamba', 'TNM Mpamba'),
        ('card', 'Credit/Debit Card'),
    ]

    donor_name = models.CharField(max_length=100, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=[('MWK', 'Malawi Kwacha'), ('USD', 'US Dollar')], default='MWK')
    donation_purpose = models.CharField(max_length=50, choices=DONATION_PURPOSES)
    specific_program = models.CharField(max_length=50, blank=True)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS)
    phone_number = models.CharField(max_length=12, blank=True)
    transaction_id = models.CharField(max_length=100, blank=True, unique=True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending', choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ])

    def __str__(self):
        return f"{self.donor_name or 'Anonymous'} - {self.amount} {self.currency}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"