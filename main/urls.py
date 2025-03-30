from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Root and top-level pages
    path('', views.index, name='index'),
    path('donate/', views.donate, name='donate'),
    path('get-help/', views.get_help, name='get_help'),

    # About section
    path('about-us/', views.about_us, name='about_us'),
    path('what-we-do/', views.what_we_do, name='what_we_do'),
    path('governance/', views.governance, name='governance'),
    path('governance/donors-and-supporters/', views.donors_and_supporters, name='donors_and_supporters'),
    path('governance/board-members/', views.board_members, name='board_members'),
    path('governance/board-committees/', views.board_committees, name='board_committees'),
    path('governance/ceo-and-executive-team/', views.ceo_and_executive_team, name='ceo_and_executive_team'),

    # Get Help section
    path('join-teen-club/', views.join_teen_club, name='join_teen_club'),
    path('child-clinic/', views.child_clinic, name='child_clinic'),
    path('hiv-services/', views.hiv_services, name='hiv_services'),
    path('pmtct/', views.pmtct, name='pmtct'),

    # Thembi Activities - Get Involved
    path('volunteer/', views.volunteer, name='volunteer'),
    path('youth/', views.youth, name='youth'),
    path('fundraise/', views.fundraise, name='fundraise'),
    path('corporate/', views.corporate, name='corporate'),

    # Thembi Activities - Programs
    path('health/', views.health, name='health'),
    path('livelihood/', views.livelihood, name='livelihood'),
    path('community-empowerment/', views.community_empowerment, name='community_empowerment'),
    path('youth-empowerment/', views.youth_empowerment, name='youth_empowerment'),
    path('education/', views.education, name='education'),

    # Thembi Activities - Ways to Donate
    path('specific-program/', views.specific_program, name='specific_program'),
    path('general-program/', views.general_program, name='general_program'),
    path('donate-child/', views.donate_child, name='donate_child'),
    path('in-kind/', views.in_kind, name='in_kind'),

    # HIV/AIDS section
    path('about-hiv-aids/', views.about_hiv, name='about_hiv_aids'),
    path('malawi-statistics/', views.malawi_statistics, name='malawi_statistics'),
    path('basic_facts/', views.basic_facts, name='basic_facts'),
    path('world-hiv-statistics/', views.world_hiv_statistics, name='world_hiv_statistics'),

    # Authentication and dashboard
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('health-data-entry/', views.health_data_entry, name='health_data_entry'),

    # Teen Club Records Management
    path('teen-club/create/', views.TeenClubCreateView.as_view(), name='create_teen_club'),  # Added create view
    path('teen-club/<int:pk>/', views.TeenClubDetailView.as_view(), name='teen_club_detail'),
    path('teen-club/<int:pk>/edit/', views.TeenClubUpdateView.as_view(), name='teen_club_edit'),
    path('teen-club/<int:pk>/delete/', views.TeenClubDeleteView.as_view(), name='teen_club_delete'),
    path('teen-club/search/', views.search_teen_clubs, name='search_teen_clubs'),
    path('teen-clubs/', views.list_teen_clubs, name='list_teen_clubs'),
]