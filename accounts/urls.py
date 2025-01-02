from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

from django.urls import path, include
from main_app import views as main_views 
from main_app.views import home
from django.contrib.auth import views as auth_views



urlpatterns = [
    path("", main_views.index, name="index"),
    path('signup/', views.signup, name='signup'),
    path('verify_otp/<int:user_id>/', views.verify_otp, name='verify_otp'),
    path('profile/setup/student/', views.profile_setup_student, name='profile_setup_student'),
    path('profile/setup/teacher/', views.profile_setup_teacher, name='profile_setup_teacher'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),  # Home page
    path('password_reset/', 
        auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), 
        name='password_reset'),
    path('password_reset_done/', 
        auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), 
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), 
        name='password_reset_confirm'),
    path('reset/done/', 
        auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), 
        name='password_reset_complete'),
]