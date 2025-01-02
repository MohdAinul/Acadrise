import random
from django.core.mail import send_mail
from django.conf import settings
# otp_utils.py
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string


def generate_otp():
    return random.randint(100000, 999999)  # Generate a 6-digit OTP




def send_otp_email(user, otp):
    subject = 'Your OTP Code'
    message = f'Your OTP code is {otp}.'

    # Using the User object for more personalized email, such as the username
    recipient_email = user.email
    
    send_mail(
        subject,
        message,
        'contact@acadrise.com',
        [recipient_email],
        fail_silently=False,
    )

    return otp
