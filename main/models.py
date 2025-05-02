from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import Truncator
from django.utils import timezone

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

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    excerpt = models.CharField(max_length=300, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Testimonial(models.Model):
    quote = models.TextField(help_text="The main quote or testimonial text (the story).")
    author_name = models.CharField(max_length=100, help_text="Name of the person giving the testimonial.")
    author_relation = models.CharField(max_length=150, blank=True, help_text="Relation to Thembi (e.g., 'Bursary Recipient').")
    author_image = models.ImageField(upload_to='testimonials/', blank=True, null=True, help_text="Optional: Upload a picture of the author.")
    feature_on_homepage = models.BooleanField(default=False, db_index=True, help_text="Check to feature this testimonial on the homepage.")
    related_program_info = models.CharField(max_length=100, blank=True, help_text="Optional: Mention the specific program.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'"{Truncator(self.quote).words(8)}..." - {self.author_name}'

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Testimonial / Success Story"
        verbose_name_plural = "Testimonials / Success Stories"

class Beneficiary(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    registration_date = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        unique_together = ('first_name', 'last_name', 'date_of_birth')

class PMTCTCase(models.Model):
    mother = models.ForeignKey(Beneficiary, on_delete=models.PROTECT, related_name='pmtct_cases')
    start_date = models.DateField()
    status = models.CharField(max_length=50, choices=[
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('discontinued', 'Discontinued'),
    ], default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"PMTCT for {self.mother} - {self.start_date}"

class EducationSupportLog(models.Model):
    beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='education_support')
    beneficiary_name = models.CharField(max_length=100)  # For distinct count in home_view
    support_type = models.CharField(max_length=50, choices=[
        ('school_fees', 'School Fees'),
        ('supplies', 'School Supplies'),
        ('uniforms', 'Uniforms'),
        ('other', 'Other'),
    ])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    support_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.beneficiary_name} - {self.support_type} on {self.support_date}"

class HIVTestRecord(models.Model):
    person = models.ForeignKey(Beneficiary, on_delete=models.SET_NULL, null=True, blank=True, related_name='hiv_tests')
    test_date = models.DateField()
    result = models.CharField(max_length=50, choices=[
        ('positive', 'Positive'),
        ('negative', 'Negative'),
        ('inconclusive', 'Inconclusive'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"HIV Test for {self.person} - {self.test_date}"

class TeenClubMember(models.Model):
    beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='teen_club_memberships')
    join_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Teen Club Member: {self.beneficiary}"

    class Meta:
        verbose_name = "Teen Club Member"
        verbose_name_plural = "Teen Club Members"

class YouthTrainingLog(models.Model):
    training_name = models.CharField(max_length=200)
    num_attendees = models.PositiveIntegerField()
    training_date = models.DateField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.training_name} - {self.training_date}"