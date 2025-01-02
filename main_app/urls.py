from django.urls import path, include
from . import views
from accounts.views import login_view, logout_view  # Import only specific views if needed

urlpatterns = [
    # Homepage
    path('', views.home, name='home'),  # Set 'home' as the main homepage
    
    # Teacher-related views
    path('teacher/<int:teacher_id>/', views.teacher_profile, name='teacher_profile'),
    path('connect/<int:teacher_id>/', views.send_connection_request, name='send_connection_request'),
    path('teacher/connection-requests/', views.teacher_connection_requests, name='teacher_connection_requests'),
    
    # Connection-related views
    path('connection_requests/', views.view_connection_requests, name='view_connection_requests'),
    path('accept-connection/<int:request_id>/', views.accept_connection, name='accept_connection'),
    path('reject-connection/<int:request_id>/', views.reject_connection, name='reject_connection'),
    path('connected-users/', views.connected_users_list, name='connected_users_list'),
    path('chat/<int:user_id>/', views.chat_view, name='chat_view'),
    path('send-message/<int:user_id>/', views.send_message, name='send_message'),

    # Search
    path('search_teachers/', views.search_teachers, name='search_teachers'),

    # Accounts-related views
    path('accounts/', include('accounts.urls')),  # Include accounts app URLs
]
