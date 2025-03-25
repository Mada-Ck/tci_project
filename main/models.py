from django.db import models
from django.contrib.auth.models import User


# Updated TeenClub Model
class TeenClub(models.Model):
    AGE_GROUPS = [
        ('10-14', '10-14 years'),
        ('15-19', '15-19 years'),
        ('20-24', '20-24 years'),
    ]

    date = models.DateField()
    age_group = models.CharField(max_length=10, choices=AGE_GROUPS)

    # Booking and Attendance
    booked_teens = models.IntegerField(default=0)
    attendance_male = models.IntegerField(default=0)
    attendance_female = models.IntegerField(default=0)

    # Viral Load and Suppression
    viral_load_samples = models.IntegerField(default=0)
    suppressed_viral_loads = models.IntegerField(default=0)

    # Samples and Disclosures
    samples_collected = models.IntegerField(default=0)
    disclosures_made = models.IntegerField(default=0)

    # Psychosocial and Referrals
    psychosocial_conducted = models.IntegerField(default=0)
    referrals_made = models.IntegerField(default=0)

    # Next Follow-up Dates
    next_date_current_age_group = models.DateField(null=True, blank=True)
    next_date_other_age_groups = models.DateField(null=True, blank=True)

    # Additional Tracking
    staff = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_attendance(self):
        return self.attendance_male + self.attendance_female

    def viral_load_suppression_rate(self):
        if self.viral_load_samples > 0:
            return (self.suppressed_viral_loads / self.viral_load_samples) * 100
        return 0

    def __str__(self):
        return f"Teen Club - {self.age_group} - {self.date}"


# Updated PMTCT Model
class PMTCT(models.Model):
    date = models.DateField()

    # Antenatal Care (ANC) Services
    total_pregnant_women_anc = models.IntegerField(default=0)
    women_counseled_hiv_testing = models.IntegerField(default=0)
    women_tested_for_hiv = models.IntegerField(default=0)
    women_with_known_hiv_status = models.IntegerField(default=0)

    # Syphilis Screening
    women_tested_for_syphilis = models.IntegerField(default=0)
    women_positive_syphilis = models.IntegerField(default=0)

    # Antiretroviral Therapy (ART) Provision
    hiv_positive_pregnant_women_initiated_art = models.IntegerField(default=0)
    hiv_positive_pregnant_women_current_art = models.IntegerField(default=0)
    hiv_exposed_infants_art_prophylaxis = models.IntegerField(default=0)

    # Labor and Delivery Services
    hiv_positive_women_safe_delivery = models.IntegerField(default=0)
    hiv_positive_women_delivery_complications = models.IntegerField(default=0)

    # Postnatal Care and Infant Follow-Up
    hiv_exposed_infants_tested = models.IntegerField(default=0)
    hiv_exposed_infants_positive = models.IntegerField(default=0)
    infants_exclusive_breastfeeding = models.IntegerField(default=0)
    infants_exclusive_formula_feeding = models.IntegerField(default=0)
    infants_mixed_feeding = models.IntegerField(default=0)

    # Community Engagement and Support
    male_partners_counseled_tested = models.IntegerField(default=0)
    support_group_participants = models.IntegerField(default=0)

    # Additional Tracking
    staff = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def hiv_testing_rate(self):
        if self.total_pregnant_women_anc > 0:
            return (self.women_tested_for_hiv / self.total_pregnant_women_anc) * 100
        return 0

    def art_coverage_rate(self):
        if self.hiv_positive_pregnant_women_initiated_art > 0:
            return (self.hiv_positive_pregnant_women_current_art / self.hiv_positive_pregnant_women_initiated_art) * 100
        return 0

    def infant_hiv_exposure_rate(self):
        if self.hiv_exposed_infants_tested > 0:
            return (self.hiv_exposed_infants_positive / self.hiv_exposed_infants_tested) * 100
        return 0

    def __str__(self):
        return f"PMTCT Activity - {self.date}"


# Unchanged Models
class ItemDistribution(models.Model):
    DISTRIBUTION_TYPES = [
        ('FOOD', 'Food'),
        ('LIKUNI_PHALA', 'Likuni Phala'),
        ('CLOTHES', 'Clothes'),
        ('SCHOOL_ITEMS', 'School Items'),
        ('SCHOOL_FEES', 'School Fees'),
        ('LIVESTOCK', 'Livestock'),
        ('FARM_INPUTS', 'Farm Inputs'),
        ('OTHER', 'Other'),
    ]
    date = models.DateField()
    distribution_type = models.CharField(max_length=20, choices=DISTRIBUTION_TYPES)
    quantity = models.IntegerField(default=0)
    recipient_count = models.IntegerField(default=0)
    details = models.TextField(blank=True)
    staff = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.distribution_type} - {self.date}"


class ClinicHealthRecord(models.Model):
    date = models.DateField()
    clinic_visits = models.IntegerField(default=0)
    vaccinations = models.IntegerField(default=0)
    other_interventions = models.TextField(blank=True)
    staff = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Clinic Health Record - {self.date}"


class JobOpening(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    posted_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class PatientHealthRecord(models.Model):
    patient_name = models.CharField(max_length=100)
    visit_date = models.DateField()
    diagnosis = models.TextField()
    recorded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient_name} - {self.visit_date}"


class IECMaterialDistribution(models.Model):
    organisation_unit = models.CharField(max_length=100, default="TA Mwaulambya")
    data_set = models.CharField(max_length=100, default="LAHARS 1.1 IEC Material Distribution (Print)")
    period = models.CharField(max_length=50, default="January 2025")
    implementing_partner = models.CharField(max_length=100, default="Light House Trust")
    distributes_iec = models.BooleanField(default=True)
    staff = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    # IC1: Posters
    posters_facilities_prevention = models.IntegerField(default=0)
    posters_facilities_care = models.IntegerField(default=0)
    posters_facilities_impact = models.IntegerField(default=0)
    posters_facilities_rssh = models.IntegerField(default=0)
    posters_communities_prevention = models.IntegerField(default=0)
    posters_communities_care = models.IntegerField(default=0)
    posters_communities_impact = models.IntegerField(default=0)
    posters_communities_rssh = models.IntegerField(default=0)
    posters_hotspots_prevention = models.IntegerField(default=0)
    posters_hotspots_care = models.IntegerField(default=0)
    posters_hotspots_impact = models.IntegerField(default=0)
    posters_hotspots_rssh = models.IntegerField(default=0)

    # IC2: Pamphlets
    pamphlets_facilities_prevention = models.IntegerField(default=0)
    pamphlets_facilities_care = models.IntegerField(default=0)
    pamphlets_facilities_impact = models.IntegerField(default=0)
    pamphlets_facilities_rssh = models.IntegerField(default=0)
    pamphlets_communities_prevention = models.IntegerField(default=0)
    pamphlets_communities_care = models.IntegerField(default=0)
    pamphlets_communities_impact = models.IntegerField(default=0)
    pamphlets_communities_rssh = models.IntegerField(default=0)
    pamphlets_hotspots_prevention = models.IntegerField(default=0)
    pamphlets_hotspots_care = models.IntegerField(default=0)
    pamphlets_hotspots_impact = models.IntegerField(default=0)
    pamphlets_hotspots_rssh = models.IntegerField(default=0)

    # IC3: Brochures
    brochures_facilities_prevention = models.IntegerField(default=0)
    brochures_facilities_care = models.IntegerField(default=0)
    brochures_facilities_impact = models.IntegerField(default=0)
    brochures_facilities_rssh = models.IntegerField(default=0)
    brochures_communities_prevention = models.IntegerField(default=0)
    brochures_communities_care = models.IntegerField(default=0)
    brochures_communities_impact = models.IntegerField(default=0)
    brochures_communities_rssh = models.IntegerField(default=0)
    brochures_hotspots_prevention = models.IntegerField(default=0)
    brochures_hotspots_care = models.IntegerField(default=0)
    brochures_hotspots_impact = models.IntegerField(default=0)
    brochures_hotspots_rssh = models.IntegerField(default=0)

    # IC4: Newsletters
    newsletters_facilities_prevention = models.IntegerField(default=0)
    newsletters_facilities_care = models.IntegerField(default=0)
    newsletters_facilities_impact = models.IntegerField(default=0)
    newsletters_facilities_rssh = models.IntegerField(default=0)
    newsletters_communities_prevention = models.IntegerField(default=0)
    newsletters_communities_care = models.IntegerField(default=0)
    newsletters_communities_impact = models.IntegerField(default=0)
    newsletters_communities_rssh = models.IntegerField(default=0)
    newsletters_hotspots_prevention = models.IntegerField(default=0)
    newsletters_hotspots_care = models.IntegerField(default=0)
    newsletters_hotspots_impact = models.IntegerField(default=0)
    newsletters_hotspots_rssh = models.IntegerField(default=0)

    # IC5: Magazines
    magazines_facilities_prevention = models.IntegerField(default=0)
    magazines_facilities_care = models.IntegerField(default=0)
    magazines_facilities_impact = models.IntegerField(default=0)
    magazines_facilities_rssh = models.IntegerField(default=0)
    magazines_communities_prevention = models.IntegerField(default=0)
    magazines_communities_care = models.IntegerField(default=0)
    magazines_communities_impact = models.IntegerField(default=0)
    magazines_communities_rssh = models.IntegerField(default=0)
    magazines_hotspots_prevention = models.IntegerField(default=0)
    magazines_hotspots_care = models.IntegerField(default=0)
    magazines_hotspots_impact = models.IntegerField(default=0)
    magazines_hotspots_rssh = models.IntegerField(default=0)

    # IC6: T-shirts
    tshirts_facilities_prevention = models.IntegerField(default=0)
    tshirts_facilities_care = models.IntegerField(default=0)
    tshirts_facilities_impact = models.IntegerField(default=0)
    tshirts_facilities_rssh = models.IntegerField(default=0)
    tshirts_communities_prevention = models.IntegerField(default=0)
    tshirts_communities_care = models.IntegerField(default=0)
    tshirts_communities_impact = models.IntegerField(default=0)
    tshirts_communities_rssh = models.IntegerField(default=0)
    tshirts_hotspots_prevention = models.IntegerField(default=0)
    tshirts_hotspots_care = models.IntegerField(default=0)
    tshirts_hotspots_impact = models.IntegerField(default=0)
    tshirts_hotspots_rssh = models.IntegerField(default=0)

    # IC7: Caps
    caps_facilities_prevention = models.IntegerField(default=0)
    caps_facilities_care = models.IntegerField(default=0)
    caps_facilities_impact = models.IntegerField(default=0)
    caps_facilities_rssh = models.IntegerField(default=0)
    caps_communities_prevention = models.IntegerField(default=0)
    caps_communities_care = models.IntegerField(default=0)
    caps_communities_impact = models.IntegerField(default=0)
    caps_communities_rssh = models.IntegerField(default=0)
    caps_hotspots_prevention = models.IntegerField(default=0)
    caps_hotspots_care = models.IntegerField(default=0)
    caps_hotspots_impact = models.IntegerField(default=0)
    caps_hotspots_rssh = models.IntegerField(default=0)

    # IC8: Calendars
    calendars_facilities_prevention = models.IntegerField(default=0)
    calendars_facilities_care = models.IntegerField(default=0)
    calendars_facilities_impact = models.IntegerField(default=0)
    calendars_facilities_rssh = models.IntegerField(default=0)
    calendars_communities_prevention = models.IntegerField(default=0)
    calendars_communities_care = models.IntegerField(default=0)
    calendars_communities_impact = models.IntegerField(default=0)
    calendars_communities_rssh = models.IntegerField(default=0)
    calendars_hotspots_prevention = models.IntegerField(default=0)
    calendars_hotspots_care = models.IntegerField(default=0)
    calendars_hotspots_impact = models.IntegerField(default=0)
    calendars_hotspots_rssh = models.IntegerField(default=0)

    # IC9: Other (Specify)
    other_facilities_prevention = models.IntegerField(default=0)
    other_facilities_care = models.IntegerField(default=0)
    other_facilities_impact = models.IntegerField(default=0)
    other_facilities_rssh = models.IntegerField(default=0)
    other_communities_prevention = models.IntegerField(default=0)
    other_communities_care = models.IntegerField(default=0)
    other_communities_impact = models.IntegerField(default=0)
    other_communities_rssh = models.IntegerField(default=0)
    other_hotspots_prevention = models.IntegerField(default=0)
    other_hotspots_care = models.IntegerField(default=0)
    other_hotspots_impact = models.IntegerField(default=0)
    other_hotspots_rssh = models.IntegerField(default=0)
    other_specify = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.data_set} - {self.period}"


class EducationRecord(models.Model):
    student_name = models.CharField(max_length=100)
    school_name = models.CharField(max_length=100)
    grade = models.CharField(max_length=20)
    attendance = models.IntegerField(default=0)
    performance_notes = models.TextField(blank=True)
    recorded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_name} - {self.school_name}"


class YouthRecord(models.Model):
    youth_name = models.CharField(max_length=100)
    activity_date = models.DateField()
    activity_type = models.CharField(max_length=50)
    participation_notes = models.TextField(blank=True)
    recorded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.youth_name} - {self.activity_date}"