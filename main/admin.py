from django.contrib import admin
from .models import TeenClub, PMTCT, ItemDistribution, PatientHealthRecord, ClinicHealthRecord, JobOpening, IECMaterialDistribution

# Register your models here.
admin.site.register(TeenClub)
admin.site.register(PMTCT)
admin.site.register(ItemDistribution)
admin.site.register(PatientHealthRecord)
admin.site.register(ClinicHealthRecord)
admin.site.register(JobOpening)
admin.site.register(IECMaterialDistribution)