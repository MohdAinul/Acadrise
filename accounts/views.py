from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate  # Added authenticate import
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse  # Add HttpResponse here
from .forms import StudentProfileForm, TeacherProfileForm,UsersignupForm
from .models import Profile, Student, Teacher
from django.contrib import messages
from .otp_utils import generate_otp, send_otp_email  # Import the OTP functions
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from random import randint
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from .models import Teacher
import sys

def home(request):
    return HttpResponse("Debug: Home view is working")

def signup(request):
    if request.method == 'POST':
        form = UsersignupForm(request.POST)
        if form.is_valid():
            # Save user
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Get the user type from the form
            user_type = form.cleaned_data['user_type']
            print(f"Signup initiated with user_type: {user_type}")
            if not hasattr(user, 'profile'): 
                profile = Profile.objects.create(user=user, user_type=user_type)
            else:  # If the user already has a profile
                profile = user.profile
                profile.user_type = user_type
                profile.save()

            # Generate OTP using the Profile model's method
            otp = profile.generate_verification_code()
            # Send OTP email
            send_otp_email(user, otp)


            return redirect('verify_otp', user_id=user.id)
    else:
        form = UsersignupForm()

    return render(request, 'accounts/signup.html', {'form': form})

def verify_otp(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if not hasattr(user, 'profile'):
        messages.error(request, 'User profile does not exist.')
        return redirect('signup') 

    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        
        if user.profile.verification_code == entered_otp:
            user.profile.email_verified = True
            user.profile.verification_code = None
            user.profile.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            if user.profile.user_type == 'student':
                return redirect('profile_setup_student')
            elif user.profile.user_type == 'teacher':
                return redirect('profile_setup_teacher')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')

    return render(request, "accounts/verify_otp.html")

@login_required
def profile_setup_student(request):
    user = request.user
    try:
        student = user.student_profile
    except Student.DoesNotExist:
        student = Student.objects.create(user=user, name=user.username)

    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('index')  # Redirect to homepage
    else:
        form = StudentProfileForm(instance=student)

    return render(request, 'accounts/profile_setup.html', {'form': form, 'is_student': True})
@login_required
def profile_setup_teacher(request):
    user = request.user

    # Ensure the user has a teacher profile
    try:
        teacher = user.teacher_profile
    except Teacher.DoesNotExist:
        teacher = Teacher.objects.create(user=user, name=user.username)

    # Redirect non-teachers to the student profile setup
    if user.profile.user_type != 'teacher':
        return redirect('profile_setup_student')

    # Handle form submission
    if request.method == 'POST':
        form = TeacherProfileForm(request.POST, request.FILES, instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('index')  # Redirect to homepage
    else:
        form = TeacherProfileForm(instance=teacher)

    return render(request, 'accounts/profile_setup.html', {
        'form': form,
        'is_teacher': True
    })



def login_view(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username_or_email, password=password)

        if user is not None:
            login(request, user)
            return redirect('index') 
        else:
            messages.error(request, "Invalid credentials. Please try again.")
    teachers = Teacher.objects.order_by('?')[:4]

    return render(request, 'accounts/login.html')

# Logout view
def logout_view(request):
    logout(request)
    return redirect("index")

@login_required
def profile(request):
    user = request.user
    profile = None
    form = None
    user_type = None

    try:
        # Check for the user type and associated profile
        if hasattr(user, 'student_profile'):
            profile = user.student_profile
            form = StudentProfileForm(request.POST or None, request.FILES or None, instance=profile)
            user_type = 'student'
        elif hasattr(user, 'teacher_profile'):
            profile = user.teacher_profile
            form = TeacherProfileForm(request.POST or None, request.FILES or None, instance=profile)
            user_type = 'teacher'

        # Handle POST requests
        if request.method == 'POST':
            # Handle profile picture upload form submission
            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']
                profile.save()
                messages.success(request, "Profile picture updated successfully!")
                return redirect('profile')

            # Handle full profile update form submission
            if form.is_valid():
                form.save()
                messages.success(request, "Profile updated successfully!")
                return redirect('profile')
    except Exception as e:
        messages.error(request, f"An error occurred: {e}")

    # Render the template with context
    return render(request, 'accounts/profile.html', {
        'user': user,
        'profile': profile,
        'form': form,
        'user_type': user_type,
    })
