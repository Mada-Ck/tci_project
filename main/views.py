from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import TeenClub, PMTCT
from .forms import TeenClubForm, PMTCTForm

# Static page views
def index(request):
    return render(request, 'index.html')

def donate(request):
    return render(request, 'donate.html')

def get_help(request):
    return render(request, 'get_help.html')

def about_us(request):
    return render(request, 'about/about-us.html')

def what_we_do(request):
    return render(request, 'about/what-we-do.html')

def governance(request):
    return render(request, 'about/governance.html')

def donors_and_supporters(request):
    return render(request, 'about/donors_and_supporters.html')

def board_members(request):
    return render(request, 'about/board_members.html')

def board_committees(request):
    return render(request, 'about/board_committees.html')

def ceo_and_executive_team(request):
    return render(request, 'about/ceo_and_executive_team.html')

def join_teen_club(request):
    return render(request, 'get-help/join-teen-club.html')

def child_clinic(request):
    return render(request, 'get-help/child-clinic.html')

def hiv_services(request):
    return render(request, 'get-help/hiv-services.html')

def pmtct(request):
    return render(request, 'get-help/pmtct.html')

def volunteer(request):
    return render(request, 'thembi-activities/get-involved/volunteer.html')

def youth(request):
    return render(request, 'thembi-activities/get-involved/youth.html')

def fundraise(request):
    return render(request, 'thembi-activities/get-involved/fundraise.html')

def corporate(request):
    return render(request, 'thembi-activities/get-involved/corporate.html')

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

def specific_program(request):
    return render(request, 'thembi-activities/ways-to-donate/specific-program.html')

def general_program(request):
    return render(request, 'thembi-activities/ways-to-donate/general-program.html')

def donate_child(request):
    return render(request, 'thembi-activities/ways-to-donate/donate-child.html')

def in_kind(request):
    return render(request, 'thembi-activities/ways-to-donate/in-kind.html')

def about_hiv(request):
    return render(request, 'hiv-aids/about_hiv.html')

def malawi_statistics(request):
    return render(request, 'hiv-aids/malawi_hiv_statistics.html')

def basic_facts(request):
    return render(request, 'hiv-aids/basic_facts_about_hiv.html')

def world_hiv_statistics(request):
    return render(request, 'hiv-aids/world_hiv_statistics.html')

# Authentication views
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in successfully!')
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('login')

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')

@login_required
def dashboard(request):
    return render(request, 'main/dashboard.html')

@login_required
def health_data_entry(request):
    return render(request, 'data-entry/health_data_entry.html')

# Teen Club views
class TeenClubCreateView(LoginRequiredMixin, CreateView):
    model = TeenClub
    form_class = TeenClubForm
    template_name = 'create_record.html'
    success_url = reverse_lazy('list_teen_clubs')

    def form_valid(self, form):
        form.instance.staff = self.request.user
        messages.success(self.request, 'Teen Club record created successfully!')
        return super().form_valid(form)

@login_required
def list_teen_clubs(request):
    teen_clubs = TeenClub.objects.all()
    return render(request, 'list_records.html', {'records': teen_clubs, 'title': 'Teen Club Records'})

# PMTCT views
class PMTCTCreateView(LoginRequiredMixin, CreateView):
    model = PMTCT
    form_class = PMTCTForm
    template_name = 'main/pmtct_create.html'
    success_url = reverse_lazy('list_pmct')

    def form_valid(self, form):
        form.instance.staff = self.request.user
        messages.success(self.request, 'PMTCT record created successfully!')
        return super().form_valid(form)

@login_required
def list_pmtct(request):
    pmtct_records = PMTCT.objects.all()
    return render(request, 'main/pmtct_list.html', {'records': pmtct_records, 'title': 'PMTCT Records'})