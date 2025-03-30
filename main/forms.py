from django import forms
from django.core.exceptions import ValidationError
from .models import (
    TeenClub, PMTCT, ItemDistribution, PatientHealthRecord, 
    JobOpening, IECMaterialDistribution, EducationRecord, YouthRecord
)

class TeenClubForm(forms.ModelForm):
    class Meta:
        model = TeenClub
        fields = [
            'date', 'age_group', 'booked_teens', 'attendance_male', 'attendance_female',
            'viral_load_samples', 'suppressed_viral_loads', 'samples_collected',
            'disclosures_made', 'psychosocial_conducted', 'referrals_made',
            'next_date_current_age_group', 'next_date_other_age_groups'
        ]
        exclude = ['staff', 'created_at']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'next_date_current_age_group': forms.DateInput(attrs={'type': 'date'}),
            'next_date_other_age_groups': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        """Custom validation for TeenClub form."""
        cleaned_data = super().clean()

        # Extract relevant fields
        booked_teens = cleaned_data.get('booked_teens')
        attendance_male = cleaned_data.get('attendance_male', 0)
        attendance_female = cleaned_data.get('attendance_female', 0)
        viral_load_samples = cleaned_data.get('viral_load_samples')
        samples_collected = cleaned_data.get('samples_collected')
        suppressed_viral_loads = cleaned_data.get('suppressed_viral_loads')
        disclosures_made = cleaned_data.get('disclosures_made', 0)
        psychosocial_conducted = cleaned_data.get('psychosocial_conducted', 0)
        referrals_made = cleaned_data.get('referrals_made', 0)

        # Validation 1: Total attendance must not exceed booked_teens
        if booked_teens is not None:
            total_attendance = attendance_male + attendance_female
            if total_attendance > booked_teens:
                raise ValidationError(
                    f"Total attendance ({total_attendance}) cannot exceed booked teens ({booked_teens})."
                )

        # Validation 2: Ensure non-negative values for numeric fields
        numeric_fields = {
            'booked_teens': booked_teens,
            'attendance_male': attendance_male,
            'attendance_female': attendance_female,
            'viral_load_samples': viral_load_samples,
            'suppressed_viral_loads': suppressed_viral_loads,
            'samples_collected': samples_collected,
            'disclosures_made': disclosures_made,
            'psychosocial_conducted': psychosocial_conducted,
            'referrals_made': referrals_made,
        }
        for field_name, value in numeric_fields.items():
            if value is not None and value < 0:
                raise ValidationError(f"{field_name.replace('_', ' ').title()} cannot be negative.")

        # Validation 3: Samples collected must not exceed viral load samples
        if viral_load_samples is not None and samples_collected is not None:
            if samples_collected > viral_load_samples:
                raise ValidationError(
                    f"Samples collected ({samples_collected}) cannot exceed viral load samples ({viral_load_samples})."
                )

        # Validation 4: Suppressed viral loads must not exceed viral load samples
        if viral_load_samples is not None and suppressed_viral_loads is not None:
            if suppressed_viral_loads > viral_load_samples:
                raise ValidationError(
                    f"Suppressed viral loads ({suppressed_viral_loads}) cannot exceed viral load samples ({viral_load_samples})."
                )

        return cleaned_data

class PMTCTForm(forms.ModelForm):
    class Meta:
        model = PMTCT
        fields = [
            'date', 'total_pregnant_women_anc', 'women_counseled_hiv_testing',
            'women_tested_for_hiv', 'women_with_known_hiv_status',
            'women_tested_for_syphilis', 'women_positive_syphilis',
            'hiv_positive_pregnant_women_initiated_art', 'hiv_positive_pregnant_women_current_art',
            'hiv_exposed_infants_art_prophylaxis', 'hiv_positive_women_safe_delivery',
            'hiv_positive_women_delivery_complications', 'hiv_exposed_infants_tested',
            'hiv_exposed_infants_positive', 'infants_exclusive_breastfeeding',
            'infants_exclusive_formula_feeding', 'infants_mixed_feeding',
            'male_partners_counseled_tested', 'support_group_participants'
        ]
        exclude = ['staff', 'created_at']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        """Custom validation for PMTCT form."""
        cleaned_data = super().clean()

        # Extract relevant fields
        total_pregnant_women_anc = cleaned_data.get('total_pregnant_women_anc')
        women_tested_for_hiv = cleaned_data.get('women_tested_for_hiv', 0)
        hiv_positive_pregnant_women_initiated_art = cleaned_data.get('hiv_positive_pregnant_women_initiated_art', 0)
        hiv_positive_pregnant_women_current_art = cleaned_data.get('hiv_positive_pregnant_women_current_art', 0)
        hiv_exposed_infants_tested = cleaned_data.get('hiv_exposed_infants_tested', 0)
        hiv_exposed_infants_positive = cleaned_data.get('hiv_exposed_infants_positive', 0)
        infants_exclusive_breastfeeding = cleaned_data.get('infants_exclusive_breastfeeding', 0)
        infants_exclusive_formula_feeding = cleaned_data.get('infants_exclusive_formula_feeding', 0)
        infants_mixed_feeding = cleaned_data.get('infants_mixed_feeding', 0)

        # Validation 1: Women tested for HIV should not exceed total pregnant women at ANC
        if total_pregnant_women_anc is not None and women_tested_for_hiv > total_pregnant_women_anc:
            raise ValidationError(
                f"Women tested for HIV ({women_tested_for_hiv}) cannot exceed total pregnant women at ANC ({total_pregnant_women_anc})."
            )

        # Validation 2: Current ART should not exceed initiated ART
        if hiv_positive_pregnant_women_initiated_art is not None and hiv_positive_pregnant_women_current_art > hiv_positive_pregnant_women_initiated_art:
            raise ValidationError(
                f"Women currently on ART ({hiv_positive_pregnant_women_current_art}) cannot exceed those initiated on ART ({hiv_positive_pregnant_women_initiated_art})."
            )

        # Validation 3: Positive infants should not exceed tested infants
        if hiv_exposed_infants_tested is not None and hiv_exposed_infants_positive > hiv_exposed_infants_tested:
            raise ValidationError(
                f"HIV-positive infants ({hiv_exposed_infants_positive}) cannot exceed tested infants ({hiv_exposed_infants_tested})."
            )

        # Validation 4: Non-negative values for all numeric fields
        numeric_fields = {
            'total_pregnant_women_anc': total_pregnant_women_anc,
            'women_counseled_hiv_testing': cleaned_data.get('women_counseled_hiv_testing', 0),
            'women_tested_for_hiv': women_tested_for_hiv,
            'women_with_known_hiv_status': cleaned_data.get('women_with_known_hiv_status', 0),
            'women_tested_for_syphilis': cleaned_data.get('women_tested_for_syphilis', 0),
            'women_positive_syphilis': cleaned_data.get('women_positive_syphilis', 0),
            'hiv_positive_pregnant_women_initiated_art': hiv_positive_pregnant_women_initiated_art,
            'hiv_positive_pregnant_women_current_art': hiv_positive_pregnant_women_current_art,
            'hiv_exposed_infants_art_prophylaxis': cleaned_data.get('hiv_exposed_infants_art_prophylaxis', 0),
            'hiv_positive_women_safe_delivery': cleaned_data.get('hiv_positive_women_safe_delivery', 0),
            'hiv_positive_women_delivery_complications': cleaned_data.get('hiv_positive_women_delivery_complications', 0),
            'hiv_exposed_infants_tested': hiv_exposed_infants_tested,
            'hiv_exposed_infants_positive': hiv_exposed_infants_positive,
            'infants_exclusive_breastfeeding': infants_exclusive_breastfeeding,
            'infants_exclusive_formula_feeding': infants_exclusive_formula_feeding,
            'infants_mixed_feeding': infants_mixed_feeding,
            'male_partners_counseled_tested': cleaned_data.get('male_partners_counseled_tested', 0),
            'support_group_participants': cleaned_data.get('support_group_participants', 0),
        }
        for field_name, value in numeric_fields.items():
            if value is not None and value < 0:
                raise ValidationError(f"{field_name.replace('_', ' ').title()} cannot be negative.")

        return cleaned_data

class ItemDistributionForm(forms.ModelForm):
    class Meta:
        model = ItemDistribution
        fields = ['date', 'distribution_type', 'quantity', 'recipient_count', 'details']
        exclude = ['staff', 'created_at']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'details': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        """Custom validation for ItemDistribution form."""
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        recipient_count = cleaned_data.get('recipient_count')

        if quantity is not None and quantity < 0:
            raise ValidationError("Quantity cannot be negative.")
        if recipient_count is not None and recipient_count < 0:
            raise ValidationError("Recipient count cannot be negative.")

        return cleaned_data

class HealthRecordForm(forms.ModelForm):
    class Meta:
        model = PatientHealthRecord
        fields = ['patient_name', 'visit_date', 'diagnosis']
        exclude = ['recorded_by', 'created_at']
        widgets = {
            'visit_date': forms.DateInput(attrs={'type': 'date'}),
            'diagnosis': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        """Custom validation for HealthRecord form."""
        cleaned_data = super().clean()
        patient_name = cleaned_data.get('patient_name')
        if patient_name and not patient_name.strip():
            raise ValidationError("Patient name cannot be empty.")
        return cleaned_data

class JobOpeningForm(forms.ModelForm):
    class Meta:
        model = JobOpening
        fields = ['title', 'description']

    def clean(self):
        """Custom validation for JobOpening form."""
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        if title and not title.strip():
            raise ValidationError("Title cannot be empty.")
        return cleaned_data

class IECMaterialForm(forms.ModelForm):
    class Meta:
        model = IECMaterialDistribution
        fields = [
            'organisation_unit', 'data_set', 'period', 'implementing_partner',
            'distributes_iec', 'posters_facilities_prevention', 'pamphlets_communities_care',
            'brochures_hotspots_impact', 'other_specify'
        ]
        exclude = ['staff', 'created_at']
        widgets = {
            'distributes_iec': forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')]),
            'other_specify': forms.Textarea(attrs={'rows': 2}),
        }

    def clean(self):
        """Custom validation for IECMaterialDistribution form."""
        cleaned_data = super().clean()
        distributes_iec = cleaned_data.get('distributes_iec')
        posters = cleaned_data.get('posters_facilities_prevention', 0)
        pamphlets = cleaned_data.get('pamphlets_communities_care', 0)
        brochures = cleaned_data.get('brochures_hotspots_impact', 0)

        # Ensure non-negative values
        if posters < 0:
            raise ValidationError("Posters cannot be negative.")
        if pamphlets < 0:
            raise ValidationError("Pamphlets cannot be negative.")
        if brochures < 0:
            raise ValidationError("Brochures cannot be negative.")

        # If distributing IEC materials, ensure at least one type is specified
        if distributes_iec and posters + pamphlets + brochures == 0:
            raise ValidationError("If distributing IEC materials, at least one type must have a positive count.")

        return cleaned_data

class EducationRecordForm(forms.ModelForm):
    class Meta:
        model = EducationRecord
        fields = ['student_name', 'school_name', 'grade', 'attendance', 'performance_notes']
        exclude = ['recorded_by', 'created_at']
        widgets = {
            'performance_notes': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        """Custom validation for EducationRecord form."""
        cleaned_data = super().clean()
        student_name = cleaned_data.get('student_name')
        attendance = cleaned_data.get('attendance')

        if student_name and not student_name.strip():
            raise ValidationError("Student name cannot be empty.")
        if attendance is not None and attendance < 0:
            raise ValidationError("Attendance cannot be negative.")

        return cleaned_data

class YouthRecordForm(forms.ModelForm):
    class Meta:
        model = YouthRecord
        fields = ['youth_name', 'activity_date', 'activity_type', 'participation_notes']
        exclude = ['recorded_by', 'created_at']
        widgets = {
            'activity_date': forms.DateInput(attrs={'type': 'date'}),
            'participation_notes': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        """Custom validation for YouthRecord form."""
        cleaned_data = super().clean()
        youth_name = cleaned_data.get('youth_name')
        if youth_name and not youth_name.strip():
            raise ValidationError("Youth name cannot be empty.")
        return cleaned_data