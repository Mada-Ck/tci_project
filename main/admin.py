# main/admin.py
from django.contrib import admin
from .models import Donation, ContactMessage, BlogPost, Testimonial, Beneficiary

# Register your models here
admin.site.register(Donation)
admin.site.register(ContactMessage)
admin.site.register(BlogPost)

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'author_relation', 'feature_on_homepage', 'created_at')
    list_filter = ('feature_on_homepage', 'author_relation')
    search_fields = ('quote', 'author_name', 'author_relation')
    list_editable = ('feature_on_homepage',)
    fieldsets = (
        (None, {'fields': ('quote', 'author_name', 'author_relation', 'related_program_info')}),
        ('Media', {'fields': ('author_image',)}),
        ('Homepage Feature', {
            'description': "Select ONE testimonial to feature on the homepage.",
            'fields': ('feature_on_homepage',)
        }),
    )

@admin.register(Beneficiary)
class BeneficiaryAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth', 'is_active')
    search_fields = ('first_name', 'last_name')