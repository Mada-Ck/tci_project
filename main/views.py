from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
import requests
import json
import uuid
from .forms import DonationForm, ContactForm
from .models import Donation, ContactMessage
from django.core.mail import send_mail
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import hmac
import hashlib

# Static Pages - Home
def index(request):
    return render(request, 'main/index.html')

# Static Pages - About Section
def about_us(request):
    return render(request, 'about/about-us.html')

def what_we_do(request):
    return render(request, 'about/what-we-do.html')

def governance(request):
    return render(request, 'about/governance.html')

def board_members(request):
    return render(request, 'about/board_members.html')

def board_committees(request):
    return render(request, 'about/board_committees.html')

def ceo_and_executive_team(request):
    return render(request, 'about/ceo_and_executive_team.html')

def donors_and_supporters(request):
    return render(request, 'about/donors_and_supporters.html')

# Static Pages - Get Help Section
def get_help(request):
    return render(request, 'get_help.html')

def join_teen_club(request):
    return render(request, 'get-help/join-teen-club.html')

def child_clinic(request):
    return render(request, 'get-help/child-clinic.html')

def hiv_services(request):
    return render(request, 'get-help/hiv-services.html')

def pmtct(request):
    return render(request, 'get-help/pmtct.html')

# Static Pages - Thembi Activities Section
# Get Involved
def volunteer(request):
    return render(request, 'thembi-activities/get-involved/volunteer.html')

def youth(request):
    return render(request, 'thembi-activities/get-involved/youth.html')

def fundraise(request):
    return render(request, 'thembi-activities/get-involved/fundraise.html')

def corporate(request):
    return render(request, 'thembi-activities/get-involved/corporate.html')

# Programs
def health(request):
    return render(request, 'thembi-activities/programs/health.html')

def livelihood(request):
    return render(request, 'thembi-activities/programs/livelihood.html')

def community_empowerment(request):
    return render(request, 'thembi-activities/programs/community-empowerment.html')

def youth_empowerment(request):
    return render(request, 'thembi-activities/programs/youth-empowerment.html')

def education(request):
    return render(request, 'thembi-activities/programs/education.html')

# Ways to Donate
def specific_program(request):
    return render(request, 'thembi-activities/ways-to-donate/specific-program.html')

def general_program(request):
    return render(request, 'thembi-activities/ways-to-donate/general-program.html')

def donate_child(request):
    return render(request, 'thembi-activities/ways-to-donate/donate-child.html')

def in_kind(request):
    return render(request, 'thembi-activities/ways-to-donate/in-kind.html')

# Static Pages - HIV/AIDS Section
def about_hiv(request):
    return render(request, 'hiv-aids/about_hiv.html')

def malawi_statistics(request):
    return render(request, 'hiv-aids/malawi_hiv_statistics.html')

def basic_facts(request):
    return render(request, 'hiv-aids/basic_facts_about_hiv.html')

def world_hiv_statistics(request):
    return render(request, 'hiv-aids/world_hiv_statistics.html')

# Static Pages - Legal Pages
def privacy_policy(request):
    return render(request, 'main/privacy_policy.html')

def terms_of_use(request):
    return render(request, 'main/terms_of_use.html')

# Donation Handling
def donate(request):
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.transaction_id = str(uuid.uuid4())

            # Enforce MWK for mobile payments
            if donation.payment_method in ('airtel_money', 'tnm_mpamba'):
                donation.currency = 'MWK'

            donation.save()

            if donation.payment_method == 'bank_transfer':
                messages.success(request, f'Thank you! Please complete the bank transfer to the {donation.currency} account.')
                return redirect('main:donate_success')

            # PayChangu Integration
            try:
                headers = {
                    'Authorization': f'Bearer {settings.PAYCHANGU_API_KEY}',
                    'Content-Type': 'application/json',
                }
                payload = {
                    'amount': float(donation.amount),
                    'currency': donation.currency,
                    'transaction_id': donation.transaction_id,
                    'description': f"Donation: {donation.get_donation_purpose_display()}{' - ' + donation.specific_program if donation.specific_program else ''}",
                    'payer': {
                        'name': donation.donor_name or 'Anonymous',
                        'phone': donation.phone_number if donation.payment_method in ('airtel_money', 'tnm_mpamba') else '',
                        'email': 'donor@example.com',
                    },
                    'return_url': request.build_absolute_uri('/donate/success/'),
                    'cancel_url': request.build_absolute_uri('/donate/'),
                    'payment_method': 'mobile_money' if donation.payment_method in ('airtel_money', 'tnm_mpamba') else 'card',
                    'account_number': settings.BANK_ACCOUNTS[donation.currency]['account_number'],
                }
                response = requests.post(
                    f"{settings.PAYCHANGU_BASE_URL}/checkout",
                    headers=headers,
                    data=json.dumps(payload)
                )
                response_data = response.json()
                if response.status_code == 200 and response_data.get('status') == 'success':
                    return redirect(response_data['data']['checkout_url'])
                else:
                    donation.status = 'failed'
                    donation.save()
                    messages.error(request, f'Payment initiation failed: {response_data.get("message", "Unknown error")}')
            except Exception as e:
                donation.status = 'failed'
                donation.save()
                messages.error(request, f'Payment error: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = DonationForm()
    return render(request, 'donate.html', {'form': form})

def donate_success(request):
    return render(request, 'main/donate_success.html')

# Contact Form Handling
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            subject = f"New Contact Message: {contact_message.subject}"
            message = f"""
            Name: {contact_message.name}
            Email: {contact_message.email}
            Subject: {contact_message.subject}
            Message: {contact_message.message}
            Date: {contact_message.created_at}
            """
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    settings.CONTACT_EMAILS,
                    fail_silently=False,
                )
                messages.success(request, 'Your message has been sent successfully!')
                return redirect('main:contact_success')
            except Exception as e:
                messages.error(request, f'Error sending email: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm()
    return render(request, 'main/contact.html', {'form': form})

def contact_success(request):
    return render(request, 'main/contact_success.html')

# Newsletter Subscription Handling
def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            # Placeholder: In a real app, save email to database or external service
            messages.success(request, 'Thank you for subscribing to our newsletter!')
            return redirect('main:index')
        else:
            messages.error(request, 'Please provide a valid email address.')
    return redirect('main:index')

# PayChangu Webhook
@csrf_exempt
def paychangu_webhook(request):
    if request.method == 'POST':
        signature = request.headers.get('Signature')
        payload = request.body
        computed_signature = hmac.new(
            settings.PAYCHANGU_SECRET.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()

        if signature == computed_signature:
            data = json.loads(payload)
            event_type = data.get('event_type')
            if event_type == 'api.charge.payment':
                transaction_id = data.get('reference')
                status = data.get('status')
                try:
                    donation = Donation.objects.get(transaction_id=transaction_id)
                    donation.status = 'completed' if status == 'success' else 'failed'
                    donation.save()
                except Donation.DoesNotExist:
                    pass
            return HttpResponse(status=200)
        return HttpResponse(status=403)
    return HttpResponse(status=400)