from django import forms
from django.core.exceptions import ValidationError
from .models import (
    TeenClub, PMTCT, ItemDistribution, PatientHealthRecord, 
    JobOpening, IECMaterialDistribution, EducationRecord, YouthRecord
)

# Existing forms with enhancements

class TeenClubForm(forms.ModelForm):
    class Meta:
        model = TeenClub
        fields = [
            'date', 'booked', 'attendance_male', 'attendance_female', 'missed',
            'samples_high_viral', 'samples_ldl', 'malnutrition_moderate',
            'malnutrition_severe', 'referrals_psychosocial', 'referrals_clinic',
            'referrals_other', 'newly_enrolled', 'graduated'
        ]
        exclude = ['staff', 'created_at']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        """Custom validation for TeenClub form."""
        cleaned_data = super().clean()

        # Extract relevant fields
        booked = cleaned_data.get('booked')
        attendance_male = cleaned_data.get('attendance_male', 0)  # Default to 0 if None
        attendance_female = cleaned_data.get('attendance_female', 0)  # Default to 0 if None
        missed = cleaned_data.get('missed', 0)
        samples_high_viral = cleaned_data.get('samples_high_viral')
        samples_ldl = cleaned_data.get('samples_ldl')
        malnutrition_moderate = cleaned_data.get('malnutrition_moderate', 0)
        malnutrition_severe = cleaned_data.get('malnutrition_severe', 0)
        referrals_psychosocial = cleaned_data.get('referrals_psychosocial', 0)
        referrals_clinic = cleaned_data.get('referrals_clinic', 0)
        referrals_other = cleaned_data.get('referrals_other', 0)
        newly_enrolled = cleaned_data.get('newly_enrolled', 0)
        graduated = cleaned_data.get('graduated', 0)

        # Validation 1: Total attendance must not exceed booked
        if booked is not None:
            total_attendance = attendance_male + attendance_female
            if total_attendance > booked:
                raise ValidationError(
                    f"Total attendance ({total_attendance}) cannot exceed booked teens ({booked})."
                )

        # Validation 2: Ensure non-negative values for numeric fields
        numeric_fields = {
            'booked': booked,
            'attendance_male': attendance_male,
            'attendance_female': attendance_female,
            'missed': missed,
            'malnutrition_moderate': malnutrition_moderate,
            'malnutrition_severe': malnutrition_severe,
            'referrals_psychosocial': referrals_psychosocial,
            'referrals_clinic': referrals_clinic,
            'referrals_other': referrals_other,
            'newly_enrolled': newly_enrolled,
            'graduated': graduated,
        }
        for field_name, value in numeric_fields.items():
            if value is not None and value < 0:
                raise ValidationError(f"{field_name.replace('_', ' ').title()} cannot be negative.")

        # Validation 3: Samples validation (assuming samples_high_viral and samples_ldl are counts)
        total_samples = 0
        if samples_high_viral is not None:
            total_samples += samples_high_viral
            if samples_high_viral < 0:
                raise ValidationError("Samples with high viral load cannot be negative.")
        if samples_ldl is not None:
            total_samples += samples_ldl
            if samples_ldl < 0:
                raise ValidationError("Samples with LDL cannot be negative.")

        # Validation 4: Check consistency with booked and attendance
        if booked is not None and total_attendance + missed > booked:
            raise ValidationError(
                f"Total attendance ({total_attendance}) plus missed ({missed}) cannot exceed booked ({booked})."
            )

        return cleaned_data

class PMTCTForm(forms.ModelForm):
    class Meta:
        model = PMTCT
        fields = [
            'date', 'booked', 'attendance_breastfeeding', 'attendance_antenatal',
            'due_dbs', 'missed', 'hiv_positive', 'hiv_negative', 'newly_enrolled'
        ]
        exclude = ['staff', 'created_at']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        """Custom validation for PMTCT form."""
        cleaned_data = super().clean()

        # Extract fields
        booked = cleaned_data.get('booked')
        attendance_breastfeeding = cleaned_data.get('attendance_breastfeeding', 0)
        attendance_antenatal = cleaned_data.get('attendance_antenatal', 0)
        missed = cleaned_data.get('missed', 0)

        # Validation 1: Total attendance must not exceed booked
        if booked is not None:
            total_attendance = attendance_breastfeeding + attendance_antenatal
            if total_attendance > booked:
                raise ValidationError(
                    f"Total attendance ({total_attendance}) cannot exceed booked ({booked})."
                )

        # Validation 2: Non-negative values
        numeric_fields = {
            'booked': booked,
            'attendance_breastfeeding': attendance_breastfeeding,
            'attendance_antenatal': attendance_antenatal,
            'missed': missed,
            'due_dbs': cleaned_data.get('due_dbs', 0),
            'hiv_positive': cleaned_data.get('hiv_positive', 0),
            'hiv_negative': cleaned_data.get('hiv_negative', 0),
            'newly_enrolled': cleaned_data.get('newly_enrolled', 0),
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

# Newly added forms with basic validation

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